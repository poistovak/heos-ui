from heos_ui.decision import (
    Action,
    BackoffPolicy,
    Decision,
    DecisionAction,
    DecisionAuditTrail,
    FeedbackEngine,
)
from heos_ui.decision.recovery import (
    RecoveryPolicy,
    RecoveryState,
)
from heos_ui.decision.recovery_scheduler import RecoveryScheduler
from heos_ui.decision.self_healing import SelfHealingCoordinator
from heos_ui.energy import EnergySnapshot
from heos_ui.execution import (
    ExecutionEngine,
    ExecutionSafetyGate,
    SafeExecutionPipeline,
)
from heos_ui.runtime.scheduler_core import Scheduler


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


def create_coordinator(
    threshold: int = 2,
    probe_delay: float = 10.0,
) -> tuple[
    SelfHealingCoordinator,
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

    gate = ExecutionSafetyGate(
        engine=ExecutionEngine(),
        recovery=recovery,
    )

    pipeline = SafeExecutionPipeline(
        gate=gate,
        audit=audit,
    )

    coordinator = SelfHealingCoordinator(
        pipeline=pipeline,
        recovery=recovery,
        recovery_scheduler=recovery_scheduler,
    )

    return coordinator, scheduler


def test_starts_healthy() -> None:
    coordinator, _ = create_coordinator()

    assert (
        coordinator.state("wattpilot")
        is RecoveryState.HEALTHY
    )


def test_failures_enter_backoff() -> None:
    coordinator, _ = create_coordinator()

    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )
    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )

    assert (
        coordinator.state("wattpilot")
        is RecoveryState.BACKOFF
    )


def test_backoff_schedules_recovery() -> None:
    coordinator, _ = create_coordinator()

    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )
    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )

    assert coordinator.is_recovery_scheduled(
        "wattpilot"
    )


def test_scheduler_opens_probe() -> None:
    coordinator, scheduler = create_coordinator(
        probe_delay=5.0,
    )

    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )
    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )

    scheduler.tick(5.0)

    assert (
        coordinator.state("wattpilot")
        is RecoveryState.PROBE
    )


def test_successful_probe_recovers_target() -> None:
    coordinator, scheduler = create_coordinator(
        probe_delay=5.0,
    )

    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )
    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )

    scheduler.tick(5.0)

    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=True,
        message="Probe recovered.",
    )

    assert (
        coordinator.state("wattpilot")
        is RecoveryState.HEALTHY
    )


def test_failed_probe_returns_to_backoff() -> None:
    coordinator, scheduler = create_coordinator(
        probe_delay=5.0,
    )

    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )
    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
    )

    scheduler.tick(5.0)

    coordinator.execute(
        EnergySnapshot(),
        candidate(),
        success=False,
        message="Probe failed.",
    )

    assert (
        coordinator.state("wattpilot")
        is RecoveryState.BACKOFF
    )


def test_targets_are_independent() -> None:
    coordinator, _ = create_coordinator()

    coordinator.execute(
        EnergySnapshot(),
        candidate("wattpilot"),
        success=False,
    )
    coordinator.execute(
        EnergySnapshot(),
        candidate("wattpilot"),
        success=False,
    )

    assert (
        coordinator.state("wattpilot")
        is RecoveryState.BACKOFF
    )
    assert (
        coordinator.state("daikin")
        is RecoveryState.HEALTHY
    )