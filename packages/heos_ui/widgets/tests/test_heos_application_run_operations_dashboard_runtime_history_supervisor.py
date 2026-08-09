import pytest
from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_supervisor as history_supervisor,
)
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)

Supervisor = (
    history_supervisor.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySupervisor
)
SupervisorState = (
    history_supervisor.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySupervisorState
)


def operations_session() -> HEOSApplicationRunOperationsSession:
    return HEOSApplicationRunOperationsSession.create()


def running_supervisor() -> Supervisor:
    supervisor = Supervisor.create()
    supervisor.start()
    return supervisor


def test_supervisor_starts_stopped() -> None:
    supervisor = Supervisor.create()

    assert supervisor.state is SupervisorState.STOPPED
    assert not supervisor.running
    assert supervisor.run_count == 0
    assert supervisor.latest is None
    assert not supervisor.has_updates


def test_create_builds_controller() -> None:
    supervisor = Supervisor.create()

    assert supervisor.controller is not None


def test_start_marks_supervisor_running() -> None:
    supervisor = Supervisor.create()

    supervisor.start()

    assert supervisor.running
    assert supervisor.state is SupervisorState.RUNNING


def test_start_is_idempotent() -> None:
    supervisor = Supervisor.create()

    supervisor.start()
    supervisor.start()

    assert supervisor.running
    assert supervisor.run_count == 0


def test_run_requires_running_supervisor() -> None:
    supervisor = Supervisor.create()

    with pytest.raises(
        RuntimeError,
        match="Runtime history supervisor is not running.",
    ):
        supervisor.run(
            operations_session()
        )


def test_run_returns_history_update() -> None:
    supervisor = running_supervisor()

    update = supervisor.run(
        operations_session()
    )

    assert update is supervisor.latest


def test_first_run_increments_count() -> None:
    supervisor = running_supervisor()

    supervisor.run(
        operations_session()
    )

    assert supervisor.run_count == 1


def test_first_run_updates_controller_tick_count() -> None:
    supervisor = running_supervisor()

    supervisor.run(
        operations_session()
    )

    assert supervisor.controller.tick_count == 1


def test_run_exposes_latest_update() -> None:
    supervisor = running_supervisor()

    update = supervisor.run(
        operations_session()
    )

    assert supervisor.latest is update
    assert supervisor.has_updates


def test_multiple_runs_increment_count() -> None:
    supervisor = running_supervisor()
    operations = operations_session()

    supervisor.run(operations)
    supervisor.run(operations)
    supervisor.run(operations)

    assert supervisor.run_count == 3
    assert supervisor.controller.tick_count == 3


def test_multiple_runs_accumulate_history() -> None:
    supervisor = running_supervisor()
    operations = operations_session()

    supervisor.run(operations)
    supervisor.run(operations)
    third = supervisor.run(operations)

    assert third.sequence == 3
    assert third.statistics.total_cycles == 3


def test_stop_marks_supervisor_stopped() -> None:
    supervisor = running_supervisor()

    supervisor.stop()

    assert not supervisor.running
    assert supervisor.state is SupervisorState.STOPPED


def test_stop_preserves_history() -> None:
    supervisor = running_supervisor()

    update = supervisor.run(
        operations_session()
    )
    supervisor.stop()

    assert supervisor.latest is update
    assert supervisor.run_count == 1
    assert supervisor.has_updates


def test_run_after_stop_is_rejected() -> None:
    supervisor = running_supervisor()

    supervisor.stop()

    with pytest.raises(
        RuntimeError,
        match="Runtime history supervisor is not running.",
    ):
        supervisor.run(
            operations_session()
        )


def test_supervisor_can_restart() -> None:
    supervisor = running_supervisor()
    operations = operations_session()

    first = supervisor.run(operations)
    supervisor.stop()
    supervisor.start()
    second = supervisor.run(operations)

    assert first.sequence == 1
    assert second.sequence == 2
    assert supervisor.run_count == 2
    assert supervisor.running


def test_reset_stops_supervisor() -> None:
    supervisor = running_supervisor()

    supervisor.run(
        operations_session()
    )
    supervisor.reset()

    assert not supervisor.running
    assert supervisor.state is SupervisorState.STOPPED


def test_reset_clears_run_count() -> None:
    supervisor = running_supervisor()

    supervisor.run(
        operations_session()
    )
    supervisor.run(
        operations_session()
    )
    supervisor.reset()

    assert supervisor.run_count == 0


def test_reset_clears_updates() -> None:
    supervisor = running_supervisor()

    supervisor.run(
        operations_session()
    )
    supervisor.reset()

    assert supervisor.latest is None
    assert not supervisor.has_updates
    assert supervisor.controller.tick_count == 0


def test_supervisor_can_run_after_reset_and_start() -> None:
    supervisor = running_supervisor()
    operations = operations_session()

    supervisor.run(operations)
    supervisor.reset()
    supervisor.start()

    update = supervisor.run(operations)

    assert supervisor.running
    assert supervisor.run_count == 1
    assert update.sequence == 1
