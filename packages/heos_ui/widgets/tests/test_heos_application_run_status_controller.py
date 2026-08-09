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
    last_cycle: int | None = 189,
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


def controller() -> HEOSApplicationRunStatusController:
    return HEOSApplicationRunStatusController(
        binding=HEOSApplicationRunStatusBinding(
            presenter=HEOSApplicationRunPresenter(),
            widget=HEOSApplicationRunStatusWidget(),
        )
    )


def test_controller_starts_empty() -> None:
    run_controller = controller()

    assert not run_controller.has_data
    assert run_controller.view is None
    assert run_controller.last_summary is None


def test_completed_report_updates_widget() -> None:
    run_controller = controller()

    view = run_controller.update(
        report()
    )

    assert run_controller.has_data
    assert view.status == "COMPLETED"
    assert view.successful


def test_completed_report_preserves_counts() -> None:
    run_controller = controller()

    view = run_controller.update(
        report(
            processed=3,
            rendered=3,
        )
    )

    assert view.detail == "Processed 3, rendered 3."


def test_completed_report_preserves_cycle_range() -> None:
    run_controller = controller()

    view = run_controller.update(
        report(
            first_cycle=10,
            last_cycle=189,
        )
    )

    assert view.cycles == "Cycles 10–189"


def test_empty_report_updates_idle_view() -> None:
    run_controller = controller()

    view = run_controller.update(
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

    assert view.status == "IDLE"
    assert view.neutral


def test_interrupted_report_updates_warning_view() -> None:
    run_controller = controller()

    view = run_controller.update(
        report(
            state=HEOSApplicationState.STOPPED,
            requested=3,
            processed=1,
            rendered=0,
            skipped=2,
            first_cycle=1,
            last_cycle=1,
            completed=False,
            stopped=True,
        )
    )

    assert view.status == "INTERRUPTED"
    assert view.warning


def test_interrupted_report_preserves_skipped_count() -> None:
    run_controller = controller()

    view = run_controller.update(
        report(
            state=HEOSApplicationState.STOPPED,
            requested=3,
            processed=1,
            rendered=0,
            skipped=2,
            first_cycle=1,
            last_cycle=1,
            completed=False,
            stopped=True,
        )
    )

    assert view.detail == "Processed 1, skipped 2."


def test_controller_exposes_last_summary() -> None:
    run_controller = controller()

    run_controller.update(
        report()
    )

    assert run_controller.last_summary is not None
    assert run_controller.last_summary.processed == 3
    assert run_controller.last_summary.last_cycle == 189


def test_second_update_replaces_summary_and_view() -> None:
    run_controller = controller()

    first_view = run_controller.update(
        report(
            first_cycle=1,
            last_cycle=1,
        )
    )

    first_summary = run_controller.last_summary

    second_view = run_controller.update(
        report(
            first_cycle=2,
            last_cycle=189,
        )
    )

    assert run_controller.view is second_view
    assert second_view is not first_view
    assert run_controller.last_summary is not first_summary
    assert run_controller.last_summary is not None
    assert run_controller.last_summary.last_cycle == 189


def test_single_cycle_uses_singular_label() -> None:
    run_controller = controller()

    view = run_controller.update(
        report(
            processed=1,
            rendered=1,
            first_cycle=189,
            last_cycle=189,
        )
    )

    assert view.cycles == "Cycle 189"


def test_clear_removes_summary_and_view() -> None:
    run_controller = controller()

    run_controller.update(
        report()
    )

    run_controller.clear()

    assert not run_controller.has_data
    assert run_controller.view is None
    assert run_controller.last_summary is None


def test_previous_summary_remains_snapshot() -> None:
    run_controller = controller()

    run_controller.update(
        report(
            first_cycle=1,
            last_cycle=1,
        )
    )

    first_summary = run_controller.last_summary

    run_controller.update(
        report(
            first_cycle=2,
            last_cycle=189,
        )
    )

    assert first_summary is not None
    assert first_summary.cycle_range == (1, 1)
