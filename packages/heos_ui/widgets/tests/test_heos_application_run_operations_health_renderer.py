from heos_ui.widgets.heos_application_run_operations_health_renderer import (
    HEOSApplicationRunOperationsHealthRenderer,
    HEOSApplicationRunOperationsRenderField,
    HEOSApplicationRunOperationsRenderScene,
)
from heos_ui.widgets.heos_application_run_operations_health_widget import (
    HEOSApplicationRunOperationsHealthView,
)
from heos_ui.widgets.heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsSeverity,
)


def view(
    *,
    title: str = "HEOS Operations",
    status: str = "HEALTHY",
    detail: str = "Healthy 5, idle 1.",
    updates: str = "Updates 6",
    frames: str = "Frames 6",
    severity: HEOSApplicationRunOperationsSeverity = (
        HEOSApplicationRunOperationsSeverity.SUCCESS
    ),
) -> HEOSApplicationRunOperationsHealthView:
    return HEOSApplicationRunOperationsHealthView(
        title=title,
        status=status,
        detail=detail,
        updates=updates,
        frames=frames,
        severity=severity,
    )


def test_renderer_returns_scene() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view()
    )

    assert isinstance(
        scene,
        HEOSApplicationRunOperationsRenderScene,
    )


def test_renderer_preserves_title() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view(title="HEOS Operations Health")
    )

    assert scene.title == "HEOS Operations Health"


def test_renderer_preserves_status() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view(status="HEALTHY")
    )

    assert scene.status == "HEALTHY"


def test_renderer_preserves_success_severity() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view(
            severity=HEOSApplicationRunOperationsSeverity.SUCCESS,
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunOperationsSeverity.SUCCESS
    )


def test_renderer_preserves_warning_severity() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view(
            status="DEGRADED",
            severity=HEOSApplicationRunOperationsSeverity.WARNING,
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunOperationsSeverity.WARNING
    )


def test_renderer_preserves_neutral_severity() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunOperationsSeverity.NEUTRAL
    )


def test_renderer_creates_detail_field() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view(
            detail="Healthy 211, idle 1.",
        )
    )

    field = scene.fields[0]

    assert isinstance(
        field,
        HEOSApplicationRunOperationsRenderField,
    )
    assert field.label == "Detail"
    assert field.value == "Healthy 211, idle 1."


def test_renderer_creates_updates_field() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view(updates="Updates 212")
    )

    field = scene.fields[1]

    assert field.label == "Updates"
    assert field.value == "Updates 212"


def test_renderer_creates_frames_field() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view(frames="Frames 212")
    )

    field = scene.fields[2]

    assert field.label == "Frames"
    assert field.value == "Frames 212"


def test_renderer_creates_three_fields() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view()
    )

    assert scene.field_count == 3
    assert len(scene.fields) == 3


def test_renderer_preserves_field_order() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view()
    )

    assert tuple(
        field.label
        for field in scene.fields
    ) == (
        "Detail",
        "Updates",
        "Frames",
    )


def test_degraded_view_renders_warning_scene() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view(
            status="DEGRADED",
            detail="Degraded 2, healthy 5.",
            updates="Updates 7",
            frames="Frames 7",
            severity=HEOSApplicationRunOperationsSeverity.WARNING,
        )
    )

    assert scene.status == "DEGRADED"
    assert scene.fields[0].value == "Degraded 2, healthy 5."
    assert (
        scene.severity
        is HEOSApplicationRunOperationsSeverity.WARNING
    )


def test_idle_view_renders_neutral_scene() -> None:
    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        view(
            status="IDLE",
            detail="No operations updates recorded.",
            updates="Updates —",
            frames="Frames —",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )

    assert scene.status == "IDLE"
    assert scene.fields[1].value == "Updates —"
    assert scene.fields[2].value == "Frames —"
    assert (
        scene.severity
        is HEOSApplicationRunOperationsSeverity.NEUTRAL
    )


def test_render_scene_is_snapshot() -> None:
    source = view(
        title="HEOS Operations",
        updates="Updates 212",
        frames="Frames 212",
    )

    scene = HEOSApplicationRunOperationsHealthRenderer().render(
        source
    )

    assert scene.title == "HEOS Operations"
    assert scene.fields[1].value == "Updates 212"
    assert scene.fields[2].value == "Frames 212"
    assert scene.field_count == 3
