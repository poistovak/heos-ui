from heos_ui.decision import (
    Action,
    BackoffPolicy,
    Decision,
    DecisionAction,
    DecisionAuditTrail,
    DecisionOutcome,
    FeedbackEngine,
)
from heos_ui.decision.recovery import RecoveryPolicy, RecoveryState
from heos_ui.decision.recovery_scheduler import RecoveryScheduler
from heos_ui.diagnostics.health_telemetry import HealthStateTelemetry
from heos_ui.energy import EnergySnapshot
from heos_ui.runtime.scheduler_core import Scheduler
from heos_ui.telemetry import TelemetryService


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


def create_health_telemetry(
    threshold: int = 2,
    probe_delay: float = 5.0,
) -> tuple[
    HealthStateTelemetry,
    RecoveryPolicy,
    RecoveryScheduler,
    DecisionAuditTrail,
    Scheduler,
    TelemetryService,
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

    telemetry = TelemetryService()

    health = HealthStateTelemetry(
        telemetry=telemetry,
        recovery=recovery,
        recovery_scheduler=recovery_scheduler,
    )

    return (
        health,
        recovery,
        recovery_scheduler,
        audit,
        scheduler,
        telemetry,
    )


def fail(
    audit: DecisionAuditTrail,
    target: str = "wattpilot",
) -> None:
    audit.record(
        EnergySnapshot(),
        candidate(target),
        DecisionOutcome(success=False),
    )


def test_healthy_state_is_recorded() -> None:
    health, _, _, _, _, telemetry = create_health_telemetry()

    state = health.update("wattpilot")

    assert state is RecoveryState.HEALTHY
    assert telemetry.get("health.wattpilot.healthy") == 1.0
    assert telemetry.get("health.wattpilot.backoff") == 0.0
    assert telemetry.get("health.wattpilot.probe") == 0.0


def test_backoff_state_is_recorded() -> None:
    health, _, _, audit, _, telemetry = create_health_telemetry()

    fail(audit)
    fail(audit)

    state = health.update("wattpilot")

    assert state is RecoveryState.BACKOFF
    assert telemetry.get("health.wattpilot.healthy") == 0.0
    assert telemetry.get("health.wattpilot.backoff") == 1.0


def test_recovery_schedule_is_recorded() -> None:
    health, _, recovery_scheduler, audit, _, telemetry = (
        create_health_telemetry()
    )

    fail(audit)
    fail(audit)

    recovery_scheduler.schedule_probe("wattpilot")
    health.update("wattpilot")

    assert (
        telemetry.get(
            "health.wattpilot.recovery_scheduled"
        )
        == 1.0
    )


def test_probe_state_is_recorded() -> None:
    health, recovery, recovery_scheduler, audit, scheduler, telemetry = (
        create_health_telemetry()
    )

    fail(audit)
    fail(audit)

    recovery_scheduler.schedule_probe("wattpilot")
    scheduler.tick(5.0)

    state = health.update("wattpilot")

    assert state is RecoveryState.PROBE
    assert telemetry.get("health.wattpilot.probe") == 1.0
    assert telemetry.get("health.wattpilot.backoff") == 0.0
    assert (
        telemetry.get(
            "health.wattpilot.recovery_scheduled"
        )
        == 0.0
    )

    assert recovery.state("wattpilot") is RecoveryState.PROBE


def test_targets_have_independent_metrics() -> None:
    health, _, _, audit, _, telemetry = create_health_telemetry()

    fail(audit, "wattpilot")
    fail(audit, "wattpilot")

    health.update("wattpilot")
    health.update("daikin")

    assert telemetry.get("health.wattpilot.backoff") == 1.0
    assert telemetry.get("health.daikin.healthy") == 1.0


def test_update_returns_current_state() -> None:
    health, _, _, _, _, _ = create_health_telemetry()

    assert (
        health.update("wattpilot")
        is RecoveryState.HEALTHY
    )