import importlib

import pytest
from heos_ui.widgets.heos_application_run_operations_session import (
    HEOSApplicationRunOperationsSession,
)

history_session = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_session"
)
session_controller = importlib.import_module(
    "heos_ui.widgets."
    "heos_application_run_operations_dashboard_runtime_history_session_controller"
)

SessionController = (
    session_controller.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySessionController
)
SessionUpdate = (
    history_session.
    HEOSApplicationRunOperationsDashboardRuntimeHistorySessionUpdate
)


def operations_session() -> HEOSApplicationRunOperationsSession:
    return HEOSApplicationRunOperationsSession.create()


def running_controller() -> SessionController:
    controller = SessionController.create()
    controller.start()
    return controller


def test_controller_starts_stopped() -> None:
    controller = SessionController.create()

    assert not controller.running
    assert controller.tick_count == 0
    assert controller.latest is None
    assert not controller.has_updates


def test_create_builds_history_session() -> None:
    controller = SessionController.create()

    assert controller.session is not None


def test_start_marks_controller_running() -> None:
    controller = SessionController.create()

    controller.start()

    assert controller.running


def test_start_is_idempotent() -> None:
    controller = SessionController.create()

    controller.start()
    controller.start()

    assert controller.running
    assert controller.tick_count == 0


def test_tick_requires_running_controller() -> None:
    controller = SessionController.create()

    with pytest.raises(
        RuntimeError,
        match="Runtime history session controller is not running.",
    ):
        controller.tick(
            operations_session()
        )


def test_tick_returns_session_update() -> None:
    controller = running_controller()

    update = controller.tick(
        operations_session()
    )

    assert isinstance(
        update,
        SessionUpdate,
    )


def test_first_tick_increments_count() -> None:
    controller = running_controller()

    controller.tick(
        operations_session()
    )

    assert controller.tick_count == 1


def test_tick_exposes_latest_update() -> None:
    controller = running_controller()

    update = controller.tick(
        operations_session()
    )

    assert controller.latest is update
    assert controller.has_updates


def test_multiple_ticks_increment_count() -> None:
    controller = running_controller()
    operations = operations_session()

    controller.tick(operations)
    controller.tick(operations)
    controller.tick(operations)

    assert controller.tick_count == 3


def test_multiple_ticks_accumulate_session_history() -> None:
    controller = running_controller()
    operations = operations_session()

    controller.tick(operations)
    controller.tick(operations)
    third = controller.tick(operations)

    assert controller.session.refresh_count == 3
    assert third.statistics.total_cycles == 3


def test_stop_marks_controller_stopped() -> None:
    controller = running_controller()

    controller.stop()

    assert not controller.running


def test_stop_preserves_existing_updates() -> None:
    controller = running_controller()

    update = controller.tick(
        operations_session()
    )
    controller.stop()

    assert controller.latest is update
    assert controller.tick_count == 1
    assert controller.has_updates


def test_tick_after_stop_is_rejected() -> None:
    controller = running_controller()

    controller.stop()

    with pytest.raises(
        RuntimeError,
        match="Runtime history session controller is not running.",
    ):
        controller.tick(
            operations_session()
        )


def test_controller_can_restart_after_stop() -> None:
    controller = running_controller()
    operations = operations_session()

    first = controller.tick(operations)
    controller.stop()
    controller.start()
    second = controller.tick(operations)

    assert first.sequence == 1
    assert second.sequence == 2
    assert controller.tick_count == 2
    assert controller.running


def test_reset_stops_controller() -> None:
    controller = running_controller()

    controller.tick(
        operations_session()
    )
    controller.reset()

    assert not controller.running


def test_reset_clears_tick_count() -> None:
    controller = running_controller()

    controller.tick(
        operations_session()
    )
    controller.tick(
        operations_session()
    )
    controller.reset()

    assert controller.tick_count == 0


def test_reset_clears_session_updates() -> None:
    controller = running_controller()

    controller.tick(
        operations_session()
    )
    controller.reset()

    assert controller.latest is None
    assert not controller.has_updates
    assert controller.session.refresh_count == 0


def test_controller_can_start_after_reset() -> None:
    controller = running_controller()
    operations = operations_session()

    controller.tick(operations)
    controller.reset()
    controller.start()

    update = controller.tick(operations)

    assert controller.running
    assert controller.tick_count == 1
    assert update.sequence == 1


def test_runtime_cycle_continues_after_reset() -> None:
    controller = running_controller()
    operations = operations_session()

    first = controller.tick(operations)
    controller.reset()
    controller.start()
    second = controller.tick(operations)

    assert first.statistics.latest_cycle == 1
    assert second.statistics.latest_cycle == 2
