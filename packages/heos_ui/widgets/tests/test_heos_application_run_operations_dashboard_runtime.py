from heos_ui.widgets.heos_application_run_operations_dashboard_health import (
    HEOSApplicationRunOperationsDashboardHealth,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardSeverity,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime import (
    HEOSApplicationRunOperationsDashboardRuntime,
    HEOSApplicationRunOperationsDashboardRuntimeCycle,
)
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)


def operations_session() -> HEOSApplicationRunOperationsSession:
    return HEOSApplicationRunOperationsSession.create()


def test_runtime_starts_empty() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    assert runtime.latest is None
    assert runtime.cycle == 0
    assert not runtime.has_cycle


def test_run_returns_runtime_cycle() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    cycle = runtime.run(
        operations_session()
    )

    assert isinstance(
        cycle,
        HEOSApplicationRunOperationsDashboardRuntimeCycle,
    )


def test_first_run_has_cycle_one() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    cycle = runtime.run(
        operations_session()
    )

    assert cycle.cycle == 1
    assert runtime.cycle == 1


def test_run_stores_latest_cycle() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    cycle = runtime.run(
        operations_session()
    )

    assert runtime.latest is cycle
    assert runtime.has_cycle


def test_empty_operations_produce_idle_dashboard_update() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    cycle = runtime.run(
        operations_session()
    )

    assert cycle.update.view.status == "IDLE"
    assert cycle.update.frame.commands[1].text == "IDLE"


def test_first_runtime_statistics_capture_one_refresh() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    cycle = runtime.run(
        operations_session()
    )

    assert cycle.statistics.total_refreshes == 1
    assert cycle.statistics.idle_refreshes == 1
    assert cycle.statistics.rendered_frames == 1
    assert cycle.statistics.latest_sequence == 1


def test_first_runtime_health_is_healthy() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    cycle = runtime.run(
        operations_session()
    )

    assert (
        cycle.health.health
        is HEOSApplicationRunOperationsDashboardHealth.HEALTHY
    )
    assert cycle.health.healthy


def test_runtime_presentation_is_healthy() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    cycle = runtime.run(
        operations_session()
    )

    assert cycle.presentation.status == "HEALTHY"
    assert (
        cycle.presentation.severity
        is HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    )


def test_runtime_view_tracks_presentation() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    cycle = runtime.run(
        operations_session()
    )

    assert cycle.view.status == cycle.presentation.status
    assert cycle.view.detail == cycle.presentation.detail
    assert cycle.view.refreshes == cycle.presentation.refreshes
    assert cycle.view.frames == cycle.presentation.frames
    assert cycle.view.sequence == cycle.presentation.sequence


def test_runtime_frame_tracks_view() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    cycle = runtime.run(
        operations_session()
    )

    assert cycle.frame.commands[0].text == cycle.view.title
    assert cycle.frame.commands[1].text == cycle.view.status
    assert cycle.frame.command_count == 6


def test_multiple_runs_increment_cycle() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()

    first = runtime.run(operations)
    second = runtime.run(operations)
    third = runtime.run(operations)

    assert first.cycle == 1
    assert second.cycle == 2
    assert third.cycle == 3
    assert runtime.cycle == 3


def test_multiple_runs_accumulate_dashboard_statistics() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()

    runtime.run(operations)
    runtime.run(operations)
    third = runtime.run(operations)

    assert third.statistics.total_refreshes == 3
    assert third.statistics.idle_refreshes == 3
    assert third.statistics.rendered_frames == 3
    assert third.statistics.latest_sequence == 3


def test_renderer_count_tracks_runtime_cycles() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()

    runtime.run(operations)
    runtime.run(operations)

    assert runtime.renderer.render_count == 2


def test_previous_runtime_cycle_remains_snapshot() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()

    first = runtime.run(operations)
    runtime.run(operations)

    assert first.cycle == 1
    assert first.statistics.total_refreshes == 1
    assert first.statistics.latest_sequence == 1
    assert first.presentation.refreshes == "Refreshes 1"
    assert first.presentation.sequence == "Sequence 1"


def test_clear_removes_runtime_state() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()

    runtime.run(
        operations_session()
    )
    runtime.clear()

    assert runtime.latest is None
    assert not runtime.has_cycle
    assert runtime.dashboard.history == ()
    assert runtime.widget.view is None
    assert runtime.renderer.latest_frame is None


def test_clear_preserves_runtime_cycle_counter() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()

    runtime.run(operations)
    runtime.clear()

    cycle = runtime.run(operations)

    assert cycle.cycle == 2
    assert runtime.cycle == 2


def test_clear_preserves_renderer_count() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()

    runtime.run(operations)
    runtime.clear()
    runtime.run(operations)

    assert runtime.renderer.render_count == 2


def test_dashboard_sequence_continues_after_clear() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()

    first = runtime.run(operations)
    runtime.clear()
    second = runtime.run(operations)

    assert first.update.sequence == 1
    assert second.update.sequence == 2
    assert second.statistics.latest_sequence == 2
