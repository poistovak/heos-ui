from heos_ui.widgets.heos_application_run_live_controller import (
    HEOSApplicationRunLiveController,
    HEOSApplicationRunLiveUpdate,
)
from heos_ui.widgets.heos_application_run_live_renderer import (
    HEOSApplicationRunLiveRenderer,
)
from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunPresenter,
)
from heos_ui.widgets.heos_application_run_report import HEOSApplicationRunReport
from heos_ui.widgets.heos_application_run_status import (
    HEOSApplicationRunStatusWidget,
)
from heos_ui.widgets.heos_application_run_status_binding import (
    HEOSApplicationRunStatusBinding,
)
from heos_ui.widgets.heos_application_run_status_controller import (
    HEOSApplicationRunStatusController,
)
from heos_ui.widgets.heos_application_runtime import HEOSApplicationState


def report(
    *,
    state: HEOSApplicationState = HEOSApplicationState.RUNNING,
    requested: int = 3,
    processed: int = 3,
    rendered: int = 3,
    skipped: int = 0,
    first_cycle: int | None = 1,
    last_cycle: int | None = 194,
    completed: bool = True,
    stopped: bool = False,
) -> HEOSApplicationRunReport:
    return HEOSApplicationRunReport(
        state=state,
        requested=requested,
        processed=processed,
        rendered=rendered,
        skipped=skipped,
        first_cycle=first_cycle,
        last_cycle=last_cycle,
        completed=completed,
        stopped=stopped,
    )


def live_controller() -> HEOSApplicationRunLiveController:
    return HEOSApplicationRunLiveController(
        controller=HEOSApplicationRunStatusController(
            binding=HEOSApplicationRunStatusBinding(
                presenter=HEOSApplicationRunPresenter(),
                widget=HEOSApplicationRunStatusWidget(),
            )
        ),
        renderer=HEOSApplicationRunLiveRenderer.create(),
    )


def test_live_controller_starts_empty() -> None:
    live = live_controller()

    assert live.latest is None
    assert live.latest_frame is None
    assert live.update_count == 0
    assert not live.has_data


def test_update_returns_live_update() -> None:
    live = live_controller()

    result = live.update(report())

    assert isinstance(result, HEOSApplicationRunLiveUpdate)


def test_first_update_has_sequence_one() -> None:
    live = live_controller()

    result = live.update(report())

    assert result.sequence == 1
    assert live.update_count == 1


def test_update_creates_completed_view() -> None:
    live = live_controller()

    result = live.update(report())

    assert result.view.status == "COMPLETED"
    assert result.view.successful


def test_update_creates_canvas_frame() -> None:
    live = live_controller()

    result = live.update(report())

    assert result.frame.command_count == 4
    assert result.frame.commands[1].text == "COMPLETED"


def test_live_controller_exposes_latest_frame() -> None:
    live = live_controller()

    result = live.update(report())

    assert live.latest_frame is result.frame
    assert live.has_data


def test_multiple_updates_increment_sequence() -> None:
    live = live_controller()

    first = live.update(
        report(
            first_cycle=1,
            last_cycle=1,
        )
    )
    second = live.update(
        report(
            first_cycle=1,
            last_cycle=194,
        )
    )

    assert first.sequence == 1
    assert second.sequence == 2
    assert live.update_count == 2


def test_second_update_replaces_latest() -> None:
    live = live_controller()

    first = live.update(
        report(
            first_cycle=1,
            last_cycle=1,
        )
    )
    second = live.update(
        report(
            first_cycle=1,
            last_cycle=194,
        )
    )

    assert live.latest is second
    assert live.latest is not first
    assert live.latest_frame is second.frame


def test_previous_update_remains_snapshot() -> None:
    live = live_controller()

    first = live.update(
        report(
            first_cycle=1,
            last_cycle=1,
        )
    )

    live.update(
        report(
            first_cycle=1,
            last_cycle=194,
        )
    )

    assert first.sequence == 1
    assert first.view.cycles == "Cycle 1"
    assert first.frame.commands[3].text == "Cycles: Cycle 1"


def test_interrupted_report_flows_to_live_frame() -> None:
    live = live_controller()

    result = live.update(
        report(
            state=HEOSApplicationState.STOPPED,
            requested=3,
            processed=1,
            rendered=0,
            skipped=2,
            first_cycle=194,
            last_cycle=194,
            completed=False,
            stopped=True,
        )
    )

    assert result.view.status == "INTERRUPTED"
    assert result.view.warning
    assert result.frame.commands[1].text == "INTERRUPTED"


def test_empty_report_flows_to_live_frame() -> None:
    live = live_controller()

    result = live.update(
        report(
            requested=0,
            processed=0,
            rendered=0,
            skipped=0,
            first_cycle=None,
            last_cycle=None,
            completed=True,
            stopped=False,
        )
    )

    assert result.view.status == "IDLE"
    assert result.view.neutral
    assert result.frame.commands[1].text == "IDLE"


def test_renderer_count_matches_live_updates() -> None:
    live = live_controller()

    live.update(report())
    live.update(report())

    assert live.update_count == 2
    assert live.renderer.render_count == 2


def test_clear_removes_live_state() -> None:
    live = live_controller()

    live.update(report())
    live.clear()

    assert live.latest is None
    assert live.latest_frame is None
    assert not live.has_data
    assert live.controller.view is None
    assert live.renderer.latest_frame is None


def test_clear_preserves_update_counter() -> None:
    live = live_controller()

    live.update(report())
    live.update(report())
    live.clear()

    assert live.update_count == 2
    assert live.renderer.render_count == 2
