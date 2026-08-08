from heos_ui.decision import (
    Action,
    BackoffPolicy,
    Decision,
    DecisionAction,
    DecisionAuditTrail,
    DecisionOutcome,
    FeedbackEngine,
)
from heos_ui.decision.recovery import (
    RecoveryPolicy,
    RecoveryState,
)
from heos_ui.energy import EnergySnapshot
from heos_ui.execution import ExecutionEngine
from heos_ui.execution.safety_gate import ExecutionSafetyGate


def candidate(
    target: str = "wattpilot",
) -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=100,
            target=target,
            action="set_current",
            reason="PV surplus available.",
        ),
        action=Action(
            priority=100,
            target=target,
            command="set_current",
            parameters={"amps": 16},
        ),
    )


def record_failure(
    audit: DecisionAuditTrail,
    target: str = "wattpilot",
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(target),
        DecisionOutcome(success=False),
    )


def create_gate(
    threshold: int = 3,
) -> tuple[
    ExecutionSafetyGate,
    RecoveryPolicy,
    DecisionAuditTrail,
]:
    audit = DecisionAuditTrail()
    feedback = FeedbackEngine(audit)
    backoff = BackoffPolicy(
        feedback=feedback,
        failure_threshold=threshold,
    )
    recovery = RecoveryPolicy(backoff)

    gate = ExecutionSafetyGate(
        engine=ExecutionEngine(),
        recovery=recovery,
    )

    return gate, recovery, audit


def test_healthy_target_is_allowed() -> None:
    gate, _, _ = create_gate()

    result = gate.evaluate("wattpilot")

    assert result.allowed
    assert result.state is RecoveryState.HEALTHY
    assert result.reason == "Target is healthy."


def test_allows_healthy_target() -> None:
    gate, _, _ = create_gate()

    assert gate.allows("wattpilot")


def test_backoff_target_is_blocked() -> None:
    gate, _, audit = create_gate(
        threshold=2,
    )

    record_failure(audit)
    record_failure(audit)

    result = gate.evaluate("wattpilot")

    assert not result.allowed
    assert result.state is RecoveryState.BACKOFF
    assert result.reason == "Target is in backoff."


def test_allows_returns_false_during_backoff() -> None:
    gate, _, audit = create_gate(
        threshold=2,
    )

    record_failure(audit)
    record_failure(audit)

    assert not gate.allows("wattpilot")


def test_probe_is_allowed() -> None:
    gate, recovery, audit = create_gate(
        threshold=2,
    )

    record_failure(audit)
    record_failure(audit)

    recovery.begin_probe("wattpilot")

    result = gate.evaluate("wattpilot")

    assert result.allowed
    assert result.state is RecoveryState.PROBE
    assert result.reason == "Recovery probe is allowed."


def test_targets_are_independent() -> None:
    gate, _, audit = create_gate(
        threshold=2,
    )

    record_failure(audit, "wattpilot")
    record_failure(audit, "wattpilot")

    assert not gate.allows("wattpilot")
    assert gate.allows("daikin")