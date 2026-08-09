from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunPresenter,
    HEOSApplicationRunSeverity,
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


def test_empty_summary_is_idle() -> None:
    presentation = HEOSApplicationRunPresenter().present(
        summary(
            status=HEOSApplicationRunStatus.EMPTY,
        )
    )

    assert presentation.status == "IDLE"
    assert presentation.severity is HEOSApplicationRunSeverity.NEUTRAL


def test_empty_summary_has_no_cycle_range() -> None:
    presentation = HEOSApplicationRunPresenter().present(
        summary(
            status=HEOSApplicationRunStatus.EMPTY,
        )
    )

    assert presentation.cycles == "Cycles —"


def test_completed_summary_is_success() -> None:
    presentation = HEOSApplicationRunPresenter().present(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=3,
            rendered=3,
            first_cycle=1,
            last_cycle=3,
        )
    )

    assert presentation.status == "COMPLETED"
    assert presentation.severity is HEOSApplicationRunSeverity.SUCCESS


def test_completed_detail_contains_counts() -> None:
    presentation = HEOSApplicationRunPresenter().present(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=3,
            rendered=3,
            first_cycle=1,
            last_cycle=3,
        )
    )

    assert presentation.detail == "Processed 3, rendered 3."


def test_interrupted_summary_is_warning() -> None:
    presentation = HEOSApplicationRunPresenter().present(
        summary(
            status=HEOSApplicationRunStatus.INTERRUPTED,
            processed=1,
            skipped=2,
            first_cycle=10,
            last_cycle=10,
        )
    )

    assert presentation.status == "INTERRUPTED"
    assert presentation.severity is HEOSApplicationRunSeverity.WARNING


def test_interrupted_detail_contains_skipped_count() -> None:
    presentation = HEOSApplicationRunPresenter().present(
        summary(
            status=HEOSApplicationRunStatus.INTERRUPTED,
            processed=1,
            skipped=2,
            first_cycle=10,
            last_cycle=10,
        )
    )

    assert presentation.detail == "Processed 1, skipped 2."


def test_single_cycle_uses_singular_label() -> None:
    presentation = HEOSApplicationRunPresenter().present(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=1,
            rendered=1,
            first_cycle=186,
            last_cycle=186,
        )
    )

    assert presentation.cycles == "Cycle 186"


def test_cycle_range_uses_range_label() -> None:
    presentation = HEOSApplicationRunPresenter().present(
        summary(
            status=HEOSApplicationRunStatus.COMPLETED,
            processed=3,
            rendered=3,
            first_cycle=10,
            last_cycle=186,
        )
    )

    assert presentation.cycles == "Cycles 10–186"


def test_custom_title_is_preserved() -> None:
    presenter = HEOSApplicationRunPresenter(
        title="HEOS Runtime",
    )

    presentation = presenter.present(
        summary(
            status=HEOSApplicationRunStatus.EMPTY,
        )
    )

    assert presentation.title == "HEOS Runtime"


def test_default_title_is_stable() -> None:
    presentation = HEOSApplicationRunPresenter().present(
        summary(
            status=HEOSApplicationRunStatus.EMPTY,
        )
    )

    assert presentation.title == "HEOS Application"


def test_presentation_is_immutable_snapshot() -> None:
    source = summary(
        status=HEOSApplicationRunStatus.COMPLETED,
        processed=2,
        rendered=2,
        first_cycle=1,
        last_cycle=2,
    )

    presentation = HEOSApplicationRunPresenter().present(source)

    assert presentation.status == "COMPLETED"
    assert presentation.cycles == "Cycles 1–2"
