from heos_ui.decision.brain import BrainCycleReport
from heos_ui.decision.brain_telemetry import BrainCycleTelemetry
from heos_ui.decision.runtime_cycle import RuntimeCycleResult
from heos_ui.decision.runtime_report import RuntimeExecutionReport
from heos_ui.diagnostics import SystemHealth
from heos_ui.telemetry import TelemetryService


def report(
    *,
    sequence: int = 1,
    accepted: int = 1,
    blocked: int = 0,
    executed: int = 1,
    system_health: SystemHealth = SystemHealth.HEALTHY,
    healthy_targets: int = 2,
    unhealthy_targets: int = 0,
) -> BrainCycleReport:
    return BrainCycleReport(
        sequence=sequence,
        cycle=RuntimeCycleResult(
            report=RuntimeExecutionReport(
                accepted=accepted,
                blocked=blocked,
                executed=executed,
            )
        ),
        system_health=system_health,
        healthy_targets=healthy_targets,
        unhealthy_targets=unhealthy_targets,
    )


def test_records_sequence() -> None:
    telemetry = TelemetryService()
    recorder = BrainCycleTelemetry(telemetry)

    recorder.record(
        report(sequence=7)
    )

    assert telemetry.get("brain.cycle.sequence") == 7.0


def test_records_runtime_counts() -> None:
    telemetry = TelemetryService()
    recorder = BrainCycleTelemetry(telemetry)

    recorder.record(
        report(
            accepted=3,
            blocked=1,
            executed=3,
        )
    )

    assert telemetry.get("brain.cycle.accepted") == 3.0
    assert telemetry.get("brain.cycle.blocked") == 1.0
    assert telemetry.get("brain.cycle.executed") == 3.0


def test_records_health_counts() -> None:
    telemetry = TelemetryService()
    recorder = BrainCycleTelemetry(telemetry)

    recorder.record(
        report(
            healthy_targets=3,
            unhealthy_targets=1,
        )
    )

    assert (
        telemetry.get("brain.health.healthy_targets")
        == 3.0
    )
    assert (
        telemetry.get("brain.health.unhealthy_targets")
        == 1.0
    )


def test_successful_cycle_records_one() -> None:
    telemetry = TelemetryService()
    recorder = BrainCycleTelemetry(telemetry)

    recorder.record(report())

    assert telemetry.get("brain.cycle.successful") == 1.0


def test_blocked_cycle_records_zero() -> None:
    telemetry = TelemetryService()
    recorder = BrainCycleTelemetry(telemetry)

    recorder.record(
        report(
            accepted=0,
            blocked=1,
            executed=0,
        )
    )

    assert telemetry.get("brain.cycle.successful") == 0.0


def test_degraded_system_records_unsuccessful_cycle() -> None:
    telemetry = TelemetryService()
    recorder = BrainCycleTelemetry(telemetry)

    recorder.record(
        report(
            system_health=SystemHealth.DEGRADED,
            healthy_targets=1,
            unhealthy_targets=1,
        )
    )

    assert telemetry.get("brain.cycle.successful") == 0.0


def test_new_cycle_overwrites_current_metrics() -> None:
    telemetry = TelemetryService()
    recorder = BrainCycleTelemetry(telemetry)

    recorder.record(
        report(
            sequence=1,
            accepted=1,
            executed=1,
        )
    )

    recorder.record(
        report(
            sequence=2,
            accepted=2,
            executed=2,
        )
    )

    assert telemetry.get("brain.cycle.sequence") == 2.0
    assert telemetry.get("brain.cycle.accepted") == 2.0
    assert telemetry.get("brain.cycle.executed") == 2.0