from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunSeverity,
)
from heos_ui.widgets.heos_application_run_status import (
    HEOSApplicationRunStatusView,
)
from heos_ui.widgets.heos_application_run_status_renderer import (
    HEOSApplicationRunRenderField,
    HEOSApplicationRunRenderScene,
    HEOSApplicationRunStatusRenderer,
)


def view(
    *,
    title: str = "HEOS Application",
    status: str = "COMPLETED",
    detail: str = "Processed 3, rendered 3.",
    cycles: str = "Cycles 1–190",
    severity: HEOSApplicationRunSeverity = (
        HEOSApplicationRunSeverity.SUCCESS
    ),
) -> HEOSApplicationRunStatusView:
    return HEOSApplicationRunStatusView(
        title=title,
        status=status,
        detail=detail,
        cycles=cycles,
        severity=severity,
    )


def test_renderer_returns_scene() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view()
    )

    assert isinstance(scene, HEOSApplicationRunRenderScene)


def test_renderer_preserves_title() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view(title="HEOS Runtime")
    )

    assert scene.title == "HEOS Runtime"


def test_renderer_preserves_status() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view(status="COMPLETED")
    )

    assert scene.status == "COMPLETED"


def test_renderer_preserves_success_severity() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view(
            severity=HEOSApplicationRunSeverity.SUCCESS,
        )
    )

    assert scene.severity is HEOSApplicationRunSeverity.SUCCESS


def test_renderer_preserves_warning_severity() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view(
            status="INTERRUPTED",
            severity=HEOSApplicationRunSeverity.WARNING,
        )
    )

    assert scene.severity is HEOSApplicationRunSeverity.WARNING


def test_renderer_preserves_neutral_severity() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunSeverity.NEUTRAL,
        )
    )

    assert scene.severity is HEOSApplicationRunSeverity.NEUTRAL


def test_renderer_creates_detail_field() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view(
            detail="Processed 5, rendered 5.",
        )
    )

    field = scene.fields[0]

    assert isinstance(field, HEOSApplicationRunRenderField)
    assert field.label == "Detail"
    assert field.value == "Processed 5, rendered 5."


def test_renderer_creates_cycles_field() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view(
            cycles="Cycles 10–190",
        )
    )

    field = scene.fields[1]

    assert field.label == "Cycles"
    assert field.value == "Cycles 10–190"


def test_renderer_creates_two_fields() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view()
    )

    assert scene.field_count == 2
    assert len(scene.fields) == 2


def test_renderer_preserves_field_order() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view()
    )

    assert tuple(
        field.label
        for field in scene.fields
    ) == (
        "Detail",
        "Cycles",
    )


def test_interrupted_view_renders_warning_scene() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view(
            status="INTERRUPTED",
            detail="Processed 1, skipped 2.",
            cycles="Cycle 190",
            severity=HEOSApplicationRunSeverity.WARNING,
        )
    )

    assert scene.status == "INTERRUPTED"
    assert scene.fields[0].value == "Processed 1, skipped 2."
    assert scene.fields[1].value == "Cycle 190"
    assert scene.severity is HEOSApplicationRunSeverity.WARNING


def test_idle_view_renders_neutral_scene() -> None:
    scene = HEOSApplicationRunStatusRenderer().render(
        view(
            status="IDLE",
            detail="No cycles processed.",
            cycles="Cycles —",
            severity=HEOSApplicationRunSeverity.NEUTRAL,
        )
    )

    assert scene.status == "IDLE"
    assert scene.fields[0].value == "No cycles processed."
    assert scene.fields[1].value == "Cycles —"
    assert scene.severity is HEOSApplicationRunSeverity.NEUTRAL
