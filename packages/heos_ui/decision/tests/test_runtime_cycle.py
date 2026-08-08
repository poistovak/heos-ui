from heos_ui.decision import (
    Action,
    ActionQueue,
    BackoffPolicy,
    ConflictResolver,
    Decision,
    DecisionAction,
    DecisionAuditTrail,
    DecisionOutcome,
    FeedbackEngine,
    GuardedDecisionPipeline,
    HealthAwareDecisionGuard,
)
from heos_ui.decision.recovery import RecoveryPolicy
from heos_ui.decision.runtime import DecisionRuntime
from heos_ui.decision.runtime_cycle import RuntimeCycle
from heos_ui.diagnostics import HealthRegistry
from heos_ui.energy import EnergySnapshot
from heos_ui.execution import ExecutionEngine


def candidate(
    target: str = "wattpilot",
    *,
    priority: int = 100,
    command: str = "set_current",
) -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=priority,
            target=target,
            action=command,
            reason="Runtime cycle test.",
        ),
        action=Action(
            priority=priority,
            target=target,
            command=command,
            parameters={"amps": 16},
        ),
    )


def create_cycle(
    threshold: int = 2,
) -> tuple[
    RuntimeCycle,
    HealthRegistry,
    DecisionAuditTrail,
    ExecutionEngine,
]:
    audit = DecisionAuditTrail()
    feedback = FeedbackEngine(audit)

    backoff = BackoffPolicy(
        feedback=feedback,
        failure_threshold=threshold,
    )

    recovery = RecoveryPolicy(backoff)
    registry = HealthRegistry(recovery)

    guard = HealthAwareDecisionGuard(registry)
    actions = ActionQueue()
    execution = ExecutionEngine()

    pipeline = GuardedDecisionPipeline(
        resolver=ConflictResolver(),
        guard=guard,
        actions=actions,
    )

    runtime = DecisionRuntime(
        pipeline=pipeline,
        actions=actions,
        execution=execution,
    )

    cycle = RuntimeCycle(runtime=runtime)

    return cycle, registry, audit, execution


def fail(
    audit: DecisionAuditTrail,
    target: str,
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(target),
        DecisionOutcome(success=False),
    )


def test_cycle_starts_at_zero() -> None:
    cycle, _, _, _ = create_cycle()

    assert cycle.cycle_count == 0


def test_empty_cycle() -> None:
    cycle, _, _, _ = create_cycle()

    result = cycle.run([])

    assert result.report.total == 0
    assert result.report.executed == 0
    assert result.successful
    assert cycle.cycle_count == 1


def test_healthy_candidate_completes_cycle() -> None:
    cycle, registry, _, execution = create_cycle()

    registry.register("wattpilot")

    received = []
    execution.register(
        "wattpilot",
        received.append,
    )

    item = candidate()
    result = cycle.run([item])

    assert result.report.accepted == 1
    assert result.report.blocked == 0
    assert result.report.executed == 1
    assert result.successful
    assert received == [item.action]


def test_blocked_candidate_fails_cycle() -> None:
    cycle, _, _, _ = create_cycle()

    result = cycle.run(
        [candidate()]
    )

    assert result.report.accepted == 0
    assert result.report.blocked == 1
    assert result.report.executed == 0
    assert not result.successful


def test_backoff_candidate_is_reported_blocked() -> None:
    cycle, registry, audit, _ = create_cycle()

    registry.register("wattpilot")

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    result = cycle.run(
        [candidate()]
    )

    assert result.report.blocked == 1
    assert result.report.executed == 0
    assert not result.successful


def test_cycle_count_increments() -> None:
    cycle, _, _, _ = create_cycle()

    cycle.run([])
    cycle.run([])
    cycle.run([])

    assert cycle.cycle_count == 3


def test_multiple_targets_complete_cycle() -> None:
    cycle, registry, _, execution = create_cycle()

    registry.register("wattpilot")
    registry.register("daikin")

    received = []

    execution.register(
        "wattpilot",
        received.append,
    )
    execution.register(
        "daikin",
        received.append,
    )

    result = cycle.run(
        [
            candidate("wattpilot"),
            candidate("daikin", priority=50),
        ]
    )

    assert result.report.accepted == 2
    assert result.report.executed == 2
    assert result.successful
    assert len(received) == 2