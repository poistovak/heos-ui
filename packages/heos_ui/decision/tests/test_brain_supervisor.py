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
from heos_ui.decision.brain import HEOSBrainSupervisor
from heos_ui.decision.recovery import RecoveryPolicy
from heos_ui.decision.runtime import DecisionRuntime
from heos_ui.decision.runtime_cycle import RuntimeCycle
from heos_ui.decision.runtime_history import RuntimeCycleHistory
from heos_ui.diagnostics import HealthRegistry, SystemHealth
from heos_ui.energy import EnergySnapshot
from heos_ui.execution import ExecutionEngine


def candidate(
    target: str = "wattpilot",
) -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=100,
            target=target,
            action="set_current",
            reason="Brain supervisor test.",
        ),
        action=Action(
            priority=100,
            target=target,
            command="set_current",
            parameters={"amps": 16},
        ),
    )


def create_brain() -> tuple[
    HEOSBrainSupervisor,
    HealthRegistry,
    DecisionAuditTrail,
    ExecutionEngine,
]:
    audit = DecisionAuditTrail()
    feedback = FeedbackEngine(audit)

    backoff = BackoffPolicy(
        feedback=feedback,
        failure_threshold=2,
    )

    recovery = RecoveryPolicy(backoff)
    health = HealthRegistry(recovery)

    guard = HealthAwareDecisionGuard(health)
    actions = ActionQueue()
    execution = ExecutionEngine()

    guarded = GuardedDecisionPipeline(
        resolver=ConflictResolver(),
        guard=guard,
        actions=actions,
    )

    runtime = DecisionRuntime(
        pipeline=guarded,
        actions=actions,
        execution=execution,
    )

    cycle = RuntimeCycle(runtime=runtime)

    brain = HEOSBrainSupervisor(
        cycle=cycle,
        history=RuntimeCycleHistory(),
        health=health,
    )

    return brain, health, audit, execution


def fail(
    audit: DecisionAuditTrail,
    target: str,
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(target),
        DecisionOutcome(success=False),
    )


def test_brain_starts_empty() -> None:
    brain, _, _, _ = create_brain()

    assert brain.cycle_count == 0
    assert brain.last_report is None


def test_run_records_cycle_history() -> None:
    brain, _, _, _ = create_brain()

    report = brain.run([])

    assert report.sequence == 1
    assert brain.cycle_count == 1
    assert brain.last_report == report


def test_healthy_system_is_reported() -> None:
    brain, health, _, _ = create_brain()

    health.register("wattpilot")
    health.register("daikin")

    report = brain.run([])

    assert report.system_health is SystemHealth.HEALTHY
    assert report.healthy_targets == 2
    assert report.unhealthy_targets == 0


def test_degraded_system_is_reported() -> None:
    brain, health, audit, _ = create_brain()

    health.register("wattpilot")
    health.register("daikin")

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    report = brain.run([])

    assert report.system_health is SystemHealth.DEGRADED
    assert report.healthy_targets == 1
    assert report.unhealthy_targets == 1


def test_successful_execution_is_reported() -> None:
    brain, health, _, execution = create_brain()

    health.register("wattpilot")

    execution.register(
        "wattpilot",
        lambda action: None,
    )

    report = brain.run(
        [candidate()]
    )

    assert report.cycle.report.accepted == 1
    assert report.cycle.report.executed == 1
    assert report.successful


def test_blocked_decision_makes_cycle_unsuccessful() -> None:
    brain, _, _, _ = create_brain()

    report = brain.run(
        [candidate()]
    )

    assert report.cycle.report.blocked == 1
    assert not report.successful


def test_degraded_health_makes_brain_report_unsuccessful() -> None:
    brain, health, audit, _ = create_brain()

    health.register("wattpilot")

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    report = brain.run([])

    assert report.cycle.successful
    assert not report.successful


def test_sequence_increments_across_cycles() -> None:
    brain, _, _, _ = create_brain()

    first = brain.run([])
    second = brain.run([])
    third = brain.run([])

    assert first.sequence == 1
    assert second.sequence == 2
    assert third.sequence == 3
    assert brain.cycle_count == 3