from heos_ui.widgets.heos_application_run_operations_dashboard_runtime import (
    HEOSApplicationRunOperationsDashboardRuntime,
    HEOSApplicationRunOperationsDashboardRuntimeCycle,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history import (
    HEOSApplicationRunOperationsDashboardRuntimeHistory,
)
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)


def operations_session() -> HEOSApplicationRunOperationsSession:
    return HEOSApplicationRunOperationsSession.create()


def runtime_cycle(
    cycle_number: int,
) -> HEOSApplicationRunOperationsDashboardRuntimeCycle:
    runtime = HEOSApplicationRunOperationsDashboardRuntime.create()
    operations = operations_session()

    cycle = runtime.run(operations)

    for _ in range(1, cycle_number):
        cycle = runtime.run(operations)

    return cycle


def test_history_starts_empty() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    assert history.cycles == ()
    assert history.count == 0
    assert history.empty


def test_empty_history_has_no_first_cycle() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    assert history.first is None


def test_empty_history_has_no_latest_cycle() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    assert history.latest is None


def test_append_adds_cycle() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()
    cycle = runtime_cycle(1)

    history.append(cycle)

    assert history.count == 1
    assert not history.empty


def test_append_preserves_cycle_identity() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()
    cycle = runtime_cycle(1)

    history.append(cycle)

    assert history.cycles[0] is cycle


def test_first_returns_first_cycle() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()
    first = runtime_cycle(1)
    second = runtime_cycle(2)

    history.append(first)
    history.append(second)

    assert history.first is first


def test_latest_returns_latest_cycle() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()
    first = runtime_cycle(1)
    second = runtime_cycle(2)

    history.append(first)
    history.append(second)

    assert history.latest is second


def test_multiple_cycles_preserve_order() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()
    first = runtime_cycle(1)
    second = runtime_cycle(2)
    third = runtime_cycle(3)

    history.append(first)
    history.append(second)
    history.append(third)

    assert history.cycles == (
        first,
        second,
        third,
    )


def test_count_tracks_appended_cycles() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    history.append(runtime_cycle(1))
    history.append(runtime_cycle(2))
    history.append(runtime_cycle(3))

    assert history.count == 3


def test_get_returns_matching_cycle() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()
    first = runtime_cycle(1)
    second = runtime_cycle(2)
    third = runtime_cycle(3)

    history.append(first)
    history.append(second)
    history.append(third)

    assert history.get(2) is second


def test_get_returns_none_for_unknown_cycle() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    history.append(runtime_cycle(1))

    assert history.get(999) is None


def test_cycles_property_is_snapshot_tuple() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()
    first = runtime_cycle(1)

    history.append(first)
    snapshot = history.cycles

    history.append(runtime_cycle(2))

    assert snapshot == (first,)
    assert history.count == 2


def test_clear_removes_all_cycles() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    history.append(runtime_cycle(1))
    history.append(runtime_cycle(2))
    history.clear()

    assert history.cycles == ()
    assert history.count == 0
    assert history.empty


def test_clear_removes_first_and_latest() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    history.append(runtime_cycle(1))
    history.clear()

    assert history.first is None
    assert history.latest is None


def test_history_can_be_reused_after_clear() -> None:
    history = HEOSApplicationRunOperationsDashboardRuntimeHistory()

    history.append(runtime_cycle(1))
    history.clear()

    cycle = runtime_cycle(2)
    history.append(cycle)

    assert history.count == 1
    assert history.first is cycle
    assert history.latest is cycle
    assert not history.empty
