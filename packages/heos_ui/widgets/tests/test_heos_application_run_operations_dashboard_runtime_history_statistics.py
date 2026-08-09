from heos_ui.widgets.heos_application_run_operations_dashboard_runtime import (
    HEOSApplicationRunOperationsDashboardRuntime,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history import (
    HEOSApplicationRunOperationsDashboardRuntimeHistory,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_statistics import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics,
)
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)


def operations_session() -> HEOSApplicationRunOperationsSession:
    return HEOSApplicationRunOperationsSession.create()


def history_with_cycles(
    count: int,
) -> HEOSApplicationRunOperationsDashboardRuntimeHistory:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    for _ in range(count):
        history.append(
            runtime.run(operations)
        )

    return history


def test_empty_history_has_zero_statistics() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics.capture(
            HEOSApplicationRunOperationsDashboardRuntimeHistory()
        )
    )

    assert statistics.total_cycles == 0
    assert statistics.idle_cycles == 0
    assert statistics.healthy_cycles == 0
    assert statistics.degraded_cycles == 0


def test_empty_history_has_no_frames() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics.capture(
            HEOSApplicationRunOperationsDashboardRuntimeHistory()
        )
    )

    assert statistics.rendered_frames == 0
    assert statistics.latest_cycle is None
    assert statistics.empty
    assert not statistics.healthy


def test_single_runtime_cycle_is_counted() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics.capture(
            history_with_cycles(1)
        )
    )

    assert statistics.total_cycles == 1
    assert statistics.latest_cycle == 1


def test_runtime_cycles_accumulate() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics.capture(
            history_with_cycles(3)
        )
    )

    assert statistics.total_cycles == 3
    assert statistics.latest_cycle == 3


def test_every_runtime_cycle_has_rendered_frame() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics.capture(
            history_with_cycles(4)
        )
    )

    assert statistics.rendered_frames == 4


def test_healthy_runtime_cycles_are_counted() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics.capture(
            history_with_cycles(3)
        )
    )

    assert statistics.healthy_cycles == 3
    assert statistics.degraded_cycles == 0


def test_idle_cycles_are_excluded_from_active_cycles() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics(
            total_cycles=5,
            idle_cycles=2,
            healthy_cycles=2,
            degraded_cycles=1,
            rendered_frames=5,
            latest_cycle=5,
        )
    )

    assert statistics.active_cycles == 3


def test_degraded_cycle_makes_statistics_unhealthy() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics(
            total_cycles=4,
            idle_cycles=0,
            healthy_cycles=3,
            degraded_cycles=1,
            rendered_frames=4,
            latest_cycle=4,
        )
    )

    assert not statistics.healthy


def test_history_without_degradation_is_healthy() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics(
            total_cycles=4,
            idle_cycles=1,
            healthy_cycles=3,
            degraded_cycles=0,
            rendered_frames=4,
            latest_cycle=4,
        )
    )

    assert statistics.healthy


def test_statistics_preserve_counts() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics(
            total_cycles=8,
            idle_cycles=2,
            healthy_cycles=4,
            degraded_cycles=2,
            rendered_frames=8,
            latest_cycle=8,
        )
    )

    assert statistics.total_cycles == 8
    assert statistics.idle_cycles == 2
    assert statistics.healthy_cycles == 4
    assert statistics.degraded_cycles == 2
    assert statistics.rendered_frames == 8


def test_latest_cycle_tracks_last_runtime_cycle() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics.capture(
            history_with_cycles(6)
        )
    )

    assert statistics.latest_cycle == 6


def test_statistics_are_snapshot() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    history.append(
        runtime.run(operations)
    )

    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics.capture(
            history
        )
    )

    history.append(
        runtime.run(operations)
    )

    assert statistics.total_cycles == 1
    assert statistics.rendered_frames == 1
    assert statistics.latest_cycle == 1


def test_clear_produces_empty_statistics() -> None:
    history = history_with_cycles(2)

    history.clear()

    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics.capture(
            history
        )
    )

    assert statistics.empty
    assert statistics.total_cycles == 0
    assert statistics.latest_cycle is None


def test_active_cycles_include_healthy_and_degraded() -> None:
    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics(
            total_cycles=7,
            idle_cycles=2,
            healthy_cycles=3,
            degraded_cycles=2,
            rendered_frames=7,
            latest_cycle=7,
        )
    )

    assert statistics.active_cycles == 5


def test_latest_cycle_can_continue_after_history_reset() -> None:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    history.append(
        runtime.run(operations)
    )
    history.clear()
    history.append(
        runtime.run(operations)
    )

    statistics = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryStatistics.capture(
            history
        )
    )

    assert statistics.total_cycles == 1
    assert statistics.latest_cycle == 2
