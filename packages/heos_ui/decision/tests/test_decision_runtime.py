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
            reason="Policy matched.",
        ),
        action=Action(
            priority=priority,
            target=target,
            command=command,
            parameters={"amps": 16},
        ),
    )


def create_runtime(
    threshold: int = 2,
) -> tuple[
    DecisionRuntime,
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

    return runtime, registry, audit, execution


def fail(
    audit: DecisionAuditTrail,
    target: str,
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(target),
        DecisionOutcome(success=False),
    )


def test_empty_runtime() -> None:
    runtime, _, _, _ = create_runtime()

    result = runtime.run([])

    assert result.executed == 0
    assert result.guarded.accepted == ()
    assert result.guarded.blocked == ()


def test_executes_healthy_candidate() -> None:
    runtime, registry, _, execution = create_runtime()

    registry.register("wattpilot")

    received = []

    execution.register(
        "wattpilot",
        received.append,
    )

    item = candidate()

    result = runtime.run([item])

    assert result.executed == 1
    assert received == [item.action]


def test_unknown_target_is_not_executed() -> None:
    runtime, _, _, execution = create_runtime()

    execution.register(
        "wattpilot",
        lambda action: None,
    )

    result = runtime.run(
        [candidate()]
    )

    assert result.executed == 0
    assert len(result.guarded.blocked) == 1


def test_backoff_target_is_not_executed() -> None:
    runtime, registry, audit, execution = create_runtime()

    registry.register("wattpilot")

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    execution.register(
        "wattpilot",
        lambda action: None,
    )

    result = runtime.run(
        [candidate()]
    )

    assert result.executed == 0
    assert len(result.guarded.blocked) == 1


def test_conflict_executes_only_winner() -> None:
    runtime, registry, _, execution = create_runtime()

    registry.register("wattpilot")

    received = []

    execution.register(
        "wattpilot",
        received.append,
    )

    low = candidate(
        priority=10,
        command="set_current",
    )
    high = candidate(
        priority=100,
        command="stop",
    )

    result = runtime.run(
        [
            low,
            high,
        ]
    )

    assert result.executed == 1
    assert received == [high.action]


def test_multiple_targets_are_executed() -> None:
    runtime, registry, _, execution = create_runtime()

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

    result = runtime.run(
        [
            candidate("wattpilot", priority=100),
            candidate("daikin", priority=50),
        ]
    )

    assert result.executed == 2
    assert len(received) == 2


def test_action_queue_is_drained() -> None:
    runtime, registry, _, execution = create_runtime()

    registry.register("wattpilot")

    execution.register(
        "wattpilot",
        lambda action: None,
    )

    runtime.run(
        [candidate()]
    )

    assert runtime.actions.count == 0