from heos_ui.widgets.heos_application_run_session_health_renderer import (
    HEOSApplicationRunSessionHealthRenderer,
    HEOSApplicationRunSessionRenderField,
    HEOSApplicationRunSessionRenderScene,
)
from heos_ui.widgets.heos_application_run_session_health_widget import (
    HEOSApplicationRunSessionHealthView,
)
from heos_ui.widgets.heos_application_run_session_presenter import (
    HEOSApplicationRunSessionSeverity,
)


def view(
    *,
    title: str = "HEOS Live Session",
    status: str = "HEALTHY",
    detail: str = "Completed 3, interrupted 0.",
    runs: str = "Runs 3",
    cycles: str = "Processed 6, rendered 6.",
    severity: HEOSApplicationRunSessionSeverity = (
        HEOSApplicationRunSessionSeverity.SUCCESS
    ),
) -> HEOSApplicationRunSessionHealthView:
    return HEOSApplicationRunSessionHealthView(
        title=title,
        status=status,
        detail=detail,
        runs=runs,
        cycles=cycles,
        severity=severity,
    )


def test_renderer_returns_scene() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view()
    )

    assert isinstance(scene, HEOSApplicationRunSessionRenderScene)


def test_renderer_preserves_title() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view(title="HEOS Operations")
    )

    assert scene.title == "HEOS Operations"


def test_renderer_preserves_status() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view(status="HEALTHY")
    )

    assert scene.status == "HEALTHY"


def test_renderer_preserves_success_severity() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view(
            severity=HEOSApplicationRunSessionSeverity.SUCCESS,
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunSessionSeverity.SUCCESS
    )


def test_renderer_preserves_warning_severity() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view(
            status="DEGRADED",
            severity=HEOSApplicationRunSessionSeverity.WARNING,
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunSessionSeverity.WARNING
    )


def test_renderer_preserves_neutral_severity() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunSessionSeverity.NEUTRAL,
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunSessionSeverity.NEUTRAL
    )


def test_renderer_creates_detail_field() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view(detail="Completed 5, interrupted 0.")
    )

    field = scene.fields[0]

    assert isinstance(
        field,
        HEOSApplicationRunSessionRenderField,
    )
    assert field.label == "Detail"
    assert field.value == "Completed 5, interrupted 0."


def test_renderer_creates_runs_field() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view(runs="Runs 202")
    )

    field = scene.fields[1]

    assert field.label == "Runs"
    assert field.value == "Runs 202"


def test_renderer_creates_cycles_field() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view(
            cycles="Processed 202, rendered 202.",
        )
    )

    field = scene.fields[2]

    assert field.label == "Cycles"
    assert field.value == "Processed 202, rendered 202."


def test_renderer_creates_three_fields() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view()
    )

    assert scene.field_count == 3
    assert len(scene.fields) == 3


def test_renderer_preserves_field_order() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view()
    )

    assert tuple(
        field.label
        for field in scene.fields
    ) == (
        "Detail",
        "Runs",
        "Cycles",
    )


def test_degraded_view_renders_warning_scene() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view(
            status="DEGRADED",
            detail="Interrupted 1, skipped 2.",
            runs="Runs 3",
            cycles="Processed 5, rendered 4.",
            severity=HEOSApplicationRunSessionSeverity.WARNING,
        )
    )

    assert scene.status == "DEGRADED"
    assert scene.fields[0].value == "Interrupted 1, skipped 2."
    assert (
        scene.severity
        is HEOSApplicationRunSessionSeverity.WARNING
    )


def test_idle_view_renders_neutral_scene() -> None:
    scene = HEOSApplicationRunSessionHealthRenderer().render(
        view(
            status="IDLE",
            detail="No application runs recorded.",
            runs="Runs —",
            cycles="Cycles —",
            severity=HEOSApplicationRunSessionSeverity.NEUTRAL,
        )
    )

    assert scene.status == "IDLE"
    assert scene.fields[1].value == "Runs —"
    assert scene.fields[2].value == "Cycles —"
    assert (
        scene.severity
        is HEOSApplicationRunSessionSeverity.NEUTRAL
    )


def test_render_scene_is_snapshot() -> None:
    source = view(
        title="HEOS Live Session",
        runs="Runs 202",
    )

    scene = HEOSApplicationRunSessionHealthRenderer().render(
        source
    )

    assert scene.title == "HEOS Live Session"
    assert scene.fields[1].value == "Runs 202"
    assert scene.field_count == 3
