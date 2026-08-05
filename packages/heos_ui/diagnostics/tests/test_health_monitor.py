import pytest
from heos_ui.diagnostics import (
    DiagnosticResult,
    DiagnosticsEngine,
    HealthMonitor,
)
from heos_ui.events.bus import EventBus
from heos_ui.runtime.scheduler_core import Scheduler
from heos_ui.telemetry import TelemetryService


def create_monitor() -> HealthMonitor:
    return HealthMonitor(
        diagnostics=DiagnosticsEngine(),
        telemetry=TelemetryService(),
        event_bus=EventBus(),
    )


def test_starts_without_checks() -> None:
    monitor = create_monitor()

    assert monitor.check_count == 0


def test_healthy_run() -> None:
    monitor = create_monitor()

    monitor.register(
        lambda: DiagnosticResult(
            component="event_bus",
            healthy=True,
        )
    )

    snapshot = monitor.run()

    assert snapshot.healthy
    assert snapshot.check_count == 1
    assert snapshot.failed_count == 0


def test_failed_run() -> None:
    monitor = create_monitor()

    monitor.register(
        lambda: DiagnosticResult(
            component="fronius",
            healthy=False,
            message="Unavailable",
        )
    )

    snapshot = monitor.run()

    assert not snapshot.healthy
    assert snapshot.failed_count == 1


def test_run_records_telemetry() -> None:
    monitor = create_monitor()

    monitor.register(
        lambda: DiagnosticResult(
            component="runtime",
            healthy=True,
        )
    )

    monitor.run()

    assert monitor.telemetry.get(
        "health.healthy"
    ) == 1.0
    assert monitor.telemetry.get(
        "health.check_count"
    ) == 1.0
    assert monitor.telemetry.get(
        "health.failed_count"
    ) == 0.0


def test_run_publishes_event() -> None:
    monitor = create_monitor()
    received = []

    monitor.event_bus.subscribe(
        "health.completed",
        received.append,
    )

    snapshot = monitor.run()

    assert received == [snapshot]


def test_scheduler_runs_monitor() -> None:
    monitor = create_monitor()
    scheduler = Scheduler()

    monitor.register(
        lambda: DiagnosticResult(
            component="scheduler",
            healthy=True,
        )
    )
    monitor.schedule(
        scheduler,
        interval=5.0,
    )

    scheduler.tick(4.0)

    assert monitor.diagnostics.count == 0

    scheduler.tick(1.0)

    assert monitor.diagnostics.count == 1


def test_invalid_interval_is_rejected() -> None:
    monitor = create_monitor()

    with pytest.raises(
        ValueError,
        match="must be positive",
    ):
        monitor.schedule(
            Scheduler(),
            interval=0.0,
        )