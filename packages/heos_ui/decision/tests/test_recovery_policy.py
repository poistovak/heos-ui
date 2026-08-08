import pytest
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


def create_recovery(
    threshold: int = 3,
) -> tuple[
    RecoveryPolicy,
    DecisionAuditTrail,
]:
    audit = DecisionAuditTrail()
    feedback = FeedbackEngine(audit)
    backoff = BackoffPolicy(
        feedback=feedback,
        failure_threshold=threshold,
    )

    return RecoveryPolicy(backoff), audit


def test_target_starts_healthy() -> None:
    recovery, _ = create_recovery()

    assert (
        recovery.state("wattpilot")
        is RecoveryState.HEALTHY
    )
    assert recovery.can_execute("wattpilot")


def test_failures_enter_backoff() -> None:
    recovery, audit = create_recovery(
        threshold=2,
    )

    record_failure(audit)
    record_failure(audit)

    assert (
        recovery.state("wattpilot")
        is RecoveryState.BACKOFF
    )
    assert not recovery.can_execute("wattpilot")


def test_begin_probe() -> None:
    recovery, audit = create_recovery(
        threshold=2,
    )

    record_failure(audit)
    record_failure(audit)

    assert (
        recovery.begin_probe("wattpilot")
        is RecoveryState.PROBE
    )
    assert recovery.can_execute("wattpilot")


def test_probe_success_returns_healthy() -> None:
    recovery, audit = create_recovery(
        threshold=2,
    )

    record_failure(audit)
    record_failure(audit)

    recovery.begin_probe("wattpilot")

    assert (
        recovery.probe_succeeded("wattpilot")
        is RecoveryState.HEALTHY
    )


def test_probe_failure_returns_backoff() -> None:
    recovery, audit = create_recovery(
        threshold=2,
    )

    record_failure(audit)
    record_failure(audit)

    recovery.begin_probe("wattpilot")

    assert (
        recovery.probe_failed("wattpilot")
        is RecoveryState.BACKOFF
    )
    assert not recovery.can_execute("wattpilot")


def test_probe_requires_backoff() -> None:
    recovery, _ = create_recovery()

    with pytest.raises(
        RuntimeError,
        match="not in backoff",
    ):
        recovery.begin_probe("wattpilot")


def test_probe_result_requires_probe_state() -> None:
    recovery, _ = create_recovery()

    with pytest.raises(
        RuntimeError,
        match="not probing",
    ):
        recovery.probe_succeeded("wattpilot")


def test_targets_are_independent() -> None:
    recovery, audit = create_recovery(
        threshold=2,
    )

    record_failure(audit, "wattpilot")
    record_failure(audit, "wattpilot")

    assert (
        recovery.state("wattpilot")
        is RecoveryState.BACKOFF
    )
    assert (
        recovery.state("daikin")
        is RecoveryState.HEALTHY
    )


def test_reset_target() -> None:
    recovery, audit = create_recovery(
        threshold=2,
    )

    record_failure(audit)
    record_failure(audit)

    recovery.state("wattpilot")
    recovery.reset("wattpilot")

    assert (
        recovery.state("wattpilot")
        is RecoveryState.BACKOFF
    )


def test_clear_recovery_state() -> None:
    recovery, audit = create_recovery(
        threshold=2,
    )

    record_failure(audit)
    record_failure(audit)

    recovery.state("wattpilot")
    recovery.clear()

    assert (
        recovery.state("wattpilot")
        is RecoveryState.BACKOFF
    )