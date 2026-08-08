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
from heos_ui.decision.recovery_scheduler import RecoveryScheduler
from heos_ui.energy import EnergySnapshot
from heos_ui.runtime.scheduler_core import Scheduler


def candidate() -> DecisionAction:
    return DecisionAction(
        decision=Decision(
            priority=100,
            target="wattpilot",
            action="set_current",
            reason="PV surplus available.",
        ),
        action=Action(
            priority=100,
            target="wattpilot",
            command="set_current",
            parameters={"amps": 16},
        ),
    )


def create_recovery_scheduler(
    *,
    threshold: int = 2,
    probe_delay: float = 30.0,
) -> tuple[
    RecoveryScheduler,
    RecoveryPolicy,
    DecisionAuditTrail,
    Scheduler,
]:
    audit = DecisionAuditTrail()
    feedback = FeedbackEngine(audit)

    backoff = BackoffPolicy(
        feedback=feedback,
        failure_threshold=threshold,
    )

    recovery = RecoveryPolicy(backoff)
    scheduler = Scheduler()

    recovery_scheduler = RecoveryScheduler(
        recovery=recovery,
        scheduler=scheduler,
        probe_delay=probe_delay,
    )

    return (
        recovery_scheduler,
        recovery,
        audit,
        scheduler,
    )


def fail(
    audit: DecisionAuditTrail,
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(),
        DecisionOutcome(success=False),
    )


def test_invalid_probe_delay() -> None:
    audit = DecisionAuditTrail()
    feedback = FeedbackEngine(audit)
    backoff = BackoffPolicy(feedback=feedback)
    recovery = RecoveryPolicy(backoff)

    with pytest.raises(
        ValueError,
        match="greater than zero",
    ):
        RecoveryScheduler(
            recovery=recovery,
            scheduler=Scheduler(),
            probe_delay=0.0,
        )


def test_healthy_target_is_not_scheduled() -> None:
    recovery_scheduler, _, _, _ = (
        create_recovery_scheduler()
    )

    assert not recovery_scheduler.schedule_probe(
        "wattpilot"
    )
    assert recovery_scheduler.scheduled_count == 0


def test_backoff_target_is_scheduled() -> None:
    recovery_scheduler, recovery, audit, _ = (
        create_recovery_scheduler()
    )

    fail(audit)
    fail(audit)

    assert (
        recovery.state("wattpilot")
        is RecoveryState.BACKOFF
    )

    assert recovery_scheduler.schedule_probe(
        "wattpilot"
    )

    assert recovery_scheduler.is_scheduled(
        "wattpilot"
    )


def test_duplicate_schedule_is_rejected() -> None:
    recovery_scheduler, _, audit, _ = (
        create_recovery_scheduler()
    )

    fail(audit)
    fail(audit)

    assert recovery_scheduler.schedule_probe(
        "wattpilot"
    )

    assert not recovery_scheduler.schedule_probe(
        "wattpilot"
    )


def test_probe_waits_for_delay() -> None:
    recovery_scheduler, recovery, audit, scheduler = (
        create_recovery_scheduler(
            probe_delay=10.0,
        )
    )

    fail(audit)
    fail(audit)

    recovery_scheduler.schedule_probe(
        "wattpilot"
    )

    scheduler.tick(9.0)

    assert (
        recovery.state("wattpilot")
        is RecoveryState.BACKOFF
    )


def test_probe_starts_after_delay() -> None:
    recovery_scheduler, recovery, audit, scheduler = (
        create_recovery_scheduler(
            probe_delay=10.0,
        )
    )

    fail(audit)
    fail(audit)

    recovery_scheduler.schedule_probe(
        "wattpilot"
    )

    scheduler.tick(10.0)

    assert (
        recovery.state("wattpilot")
        is RecoveryState.PROBE
    )

    assert not recovery_scheduler.is_scheduled(
        "wattpilot"
    )


def test_targets_are_independent() -> None:
    recovery_scheduler, recovery, audit, scheduler = (
        create_recovery_scheduler(
            probe_delay=5.0,
        )
    )

    fail(audit)
    fail(audit)

    recovery_scheduler.schedule_probe(
        "wattpilot"
    )

    scheduler.tick(5.0)

    assert (
        recovery.state("wattpilot")
        is RecoveryState.PROBE
    )

    assert (
        recovery.state("daikin")
        is RecoveryState.HEALTHY
    )