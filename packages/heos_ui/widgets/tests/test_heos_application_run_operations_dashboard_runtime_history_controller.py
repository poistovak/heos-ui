from heos_ui.widgets.heos_application_run_operations_dashboard_runtime import (
    HEOSApplicationRunOperationsDashboardRuntimeCycle,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_controller import (
    HEOSApplicationRunOperationsDashboardRuntimeHistoryController,
)
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)


def operations_session() -> HEOSApplicationRunOperationsSession:
    return HEOSApplicationRunOperationsSession.create()


def test_controller_starts_empty() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )

    assert controller.latest is None
    assert controller.cycle_count == 0
    assert not controller.has_cycles


def test_run_returns_runtime_cycle() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )

    cycle = controller.run(
        operations_session()
    )

    assert isinstance(
        cycle,
        HEOSApplicationRunOperationsDashboardRuntimeCycle,
    )


def test_first_run_has_cycle_one() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )

    cycle = controller.run(
        operations_session()
    )

    assert cycle.cycle == 1


def test_first_run_is_added_to_history() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )

    cycle = controller.run(
        operations_session()
    )

    assert controller.history.cycles == (cycle,)
    assert controller.cycle_count == 1
    assert controller.has_cycles


def test_latest_tracks_runtime_cycle() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )

    cycle = controller.run(
        operations_session()
    )

    assert controller.latest is cycle


def test_multiple_runs_are_recorded() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )
    operations = operations_session()

    first = controller.run(operations)
    second = controller.run(operations)
    third = controller.run(operations)

    assert controller.history.cycles == (
        first,
        second,
        third,
    )
    assert controller.cycle_count == 3


def test_multiple_runs_preserve_cycle_numbers() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )
    operations = operations_session()

    first = controller.run(operations)
    second = controller.run(operations)
    third = controller.run(operations)

    assert first.cycle == 1
    assert second.cycle == 2
    assert third.cycle == 3


def test_latest_tracks_last_cycle() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )
    operations = operations_session()

    controller.run(operations)
    second = controller.run(operations)

    assert controller.latest is second


def test_get_returns_recorded_cycle() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )
    operations = operations_session()

    controller.run(operations)
    second = controller.run(operations)
    controller.run(operations)

    assert controller.get(2) is second


def test_get_returns_none_for_unknown_cycle() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )

    controller.run(
        operations_session()
    )

    assert controller.get(999) is None


def test_runtime_and_history_share_same_cycle() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )

    cycle = controller.run(
        operations_session()
    )

    assert controller.runtime.latest is cycle
    assert controller.history.latest is cycle
    assert controller.latest is cycle


def test_history_tracks_runtime_statistics() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )
    operations = operations_session()

    controller.run(operations)
    second = controller.run(operations)

    assert second.statistics.total_refreshes == 2
    assert second.statistics.latest_sequence == 2
    assert controller.latest is second


def test_clear_removes_history() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )

    controller.run(
        operations_session()
    )
    controller.clear()

    assert controller.history.cycles == ()
    assert controller.cycle_count == 0
    assert controller.latest is None
    assert not controller.has_cycles


def test_clear_removes_runtime_state() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )

    controller.run(
        operations_session()
    )
    controller.clear()

    assert controller.runtime.latest is None
    assert not controller.runtime.has_cycle


def test_run_after_clear_continues_runtime_cycle_number() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )
    operations = operations_session()

    first = controller.run(operations)
    controller.clear()
    second = controller.run(operations)

    assert first.cycle == 1
    assert second.cycle == 2
    assert controller.cycle_count == 1
    assert controller.latest is second


def test_run_after_clear_starts_new_history() -> None:
    controller = (
        HEOSApplicationRunOperationsDashboardRuntimeHistoryController.create()
    )
    operations = operations_session()

    controller.run(operations)
    controller.run(operations)
    controller.clear()

    cycle = controller.run(operations)

    assert controller.history.cycles == (cycle,)
    assert controller.history.first is cycle
    assert controller.history.latest is cycle
    assert controller.cycle_count == 1
