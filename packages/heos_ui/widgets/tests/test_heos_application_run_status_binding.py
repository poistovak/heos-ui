from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunPresenter,
    HEOSApplicationRunSeverity,
)
from heos_ui.widgets.heos_application_run_status import (
    HEOSApplicationRunStatusWidget,
)
from heos_ui.widgets.heos_application_run_status_binding import (
    HEOSApplicationRunStatusBinding,
)
from heos_ui.widgets.heos_application_run_summary import (
    HEOSApplicationRunStatus,
    HEOSApplicationRunSummary,
)


def summary(
    *,
    status: HEOSApplicationRunStatus,
    processed: int = 0,
    rendered: int = 0,
    skipped: int = 0,
    first_cycle: int | None = None,
    last_cycle: int | None = None,
) -> HEOSApplicationRunSummary:
    return HEOSApplicationRunSummary(
        status=status,
        headline="test",
        processed=processed,
        rendered=rendered,
        skipped=skipped,
        first_cycle=first_cycle,
        last_cycle=last_cycle,
    )


def binding() -> HEOSApplicationRunStatusBinding:
    return HEOSApplicationRunStatusBinding(
        presenter=HEOSApplicationRunPresenter(),
        widget=HEOSApplicationRunStatusWidget(),
    )


def test_binding_starts_empty() -> None:
    run_binding = binding()

    assert not run_binding.has_data
    assert run_binding.view is None


def test_empty_summary_updates_widget() -> None:
    run_binding = binding()

    view = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.EMPTY,
        )
    )

    assert run_binding.has_data
    assert view.status == "IDLE"


def test_completed_summary_updates_widget() -> None:
    run_binding = binding()

    view = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=3,
            rendered=3,
            first_cycle=1,
            last_cycle=3,
        )
    )

    assert view.status == "COMPLETED"
    assert view.successful


def test_completed_summary_preserves_detail() -> None:
    run_binding = binding()

    view = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=3,
            rendered=3,
            first_cycle=1,
            last_cycle=3,
        )
    )

    assert view.detail == "Processed 3, rendered 3."


def test_interrupted_summary_updates_warning_view() -> None:
    run_binding = binding()

    view = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.INTERRUPTED,
            processed=1,
            skipped=2,
            first_cycle=10,
            last_cycle=10,
        )
    )

    assert view.status == "INTERRUPTED"
    assert view.warning


def test_interrupted_summary_preserves_counts() -> None:
    run_binding = binding()

    view = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.INTERRUPTED,
            processed=1,
            skipped=2,
            first_cycle=10,
            last_cycle=10,
        )
    )

    assert view.detail == "Processed 1, skipped 2."


def test_cycle_range_flows_through_binding() -> None:
    run_binding = binding()

    view = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=3,
            rendered=3,
            first_cycle=10,
            last_cycle=188,
        )
    )

    assert view.cycles == "Cycles 10–188"


def test_single_cycle_flows_through_binding() -> None:
    run_binding = binding()

    view = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=1,
            rendered=1,
            first_cycle=188,
            last_cycle=188,
        )
    )

    assert view.cycles == "Cycle 188"


def test_binding_exposes_latest_view() -> None:
    run_binding = binding()

    view = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=1,
            rendered=1,
            first_cycle=188,
            last_cycle=188,
        )
    )

    assert run_binding.view is view


def test_second_update_replaces_latest_view() -> None:
    run_binding = binding()

    first = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.EMPTY,
        )
    )

    second = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=1,
            rendered=1,
            first_cycle=188,
            last_cycle=188,
        )
    )

    assert run_binding.view is second
    assert run_binding.view is not first
    assert second.status == "COMPLETED"


def test_binding_uses_presenter_severity() -> None:
    run_binding = binding()

    view = run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.INTERRUPTED,
            processed=1,
            skipped=1,
            first_cycle=188,
            last_cycle=188,
        )
    )

    assert view.severity is HEOSApplicationRunSeverity.WARNING


def test_clear_removes_widget_view() -> None:
    run_binding = binding()

    run_binding.update(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=1,
            rendered=1,
            first_cycle=188,
            last_cycle=188,
        )
    )

    run_binding.clear()

    assert not run_binding.has_data
    assert run_binding.view is None
