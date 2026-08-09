from heos_ui.widgets.heos_application_run_operations_dashboard_health_renderer import (
    HEOSApplicationRunOperationsDashboardHealthRenderer,
    HEOSApplicationRunOperationsDashboardRenderField,
    HEOSApplicationRunOperationsDashboardRenderScene,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_health_widget import (
    HEOSApplicationRunOperationsDashboardHealthView,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardSeverity,
)


def view(
    *,
    title: str = "HEOS Operations Dashboard",
    status: str = "HEALTHY",
    detail: str = "Healthy 4, idle 1.",
    refreshes: str = "Refreshes 5",
    frames: str = "Frames 5",
    sequence: str = "Sequence 5",
    severity: HEOSApplicationRunOperationsDashboardSeverity = (
        HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    ),
) -> HEOSApplicationRunOperationsDashboardHealthView:
    return HEOSApplicationRunOperationsDashboardHealthView(
        title=title,
        status=status,
        detail=detail,
        refreshes=refreshes,
        frames=frames,
        sequence=sequence,
        severity=severity,
    )


def test_renderer_returns_render_scene() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view()
    )

    assert isinstance(
        scene,
        HEOSApplicationRunOperationsDashboardRenderScene,
    )


def test_renderer_preserves_title() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(title="HEOS Operations Control")
    )

    assert scene.title == "HEOS Operations Control"


def test_renderer_preserves_status() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(status="HEALTHY")
    )

    assert scene.status == "HEALTHY"


def test_renderer_preserves_success_severity() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
            )
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    )


def test_renderer_preserves_warning_severity() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(
            status="DEGRADED",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.WARNING
            ),
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunOperationsDashboardSeverity.WARNING
    )


def test_renderer_preserves_neutral_severity() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(
            status="IDLE",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
            ),
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
    )


def test_renderer_creates_detail_field() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(detail="Healthy 221, idle 1.")
    )

    field = scene.fields[0]

    assert isinstance(
        field,
        HEOSApplicationRunOperationsDashboardRenderField,
    )
    assert field.label == "Detail"
    assert field.value == "Healthy 221, idle 1."


def test_renderer_creates_refreshes_field() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(refreshes="Refreshes 222")
    )

    field = scene.fields[1]

    assert field.label == "Refreshes"
    assert field.value == "Refreshes 222"


def test_renderer_creates_frames_field() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(frames="Frames 222")
    )

    field = scene.fields[2]

    assert field.label == "Frames"
    assert field.value == "Frames 222"


def test_renderer_creates_sequence_field() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(sequence="Sequence 222")
    )

    field = scene.fields[3]

    assert field.label == "Sequence"
    assert field.value == "Sequence 222"


def test_renderer_creates_four_fields() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view()
    )

    assert scene.field_count == 4
    assert len(scene.fields) == 4


def test_renderer_preserves_field_order() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view()
    )

    assert tuple(
        field.label
        for field in scene.fields
    ) == (
        "Detail",
        "Refreshes",
        "Frames",
        "Sequence",
    )


def test_degraded_view_renders_warning_scene() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(
            status="DEGRADED",
            detail="Degraded 2, healthy 5.",
            refreshes="Refreshes 7",
            frames="Frames 7",
            sequence="Sequence 7",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.WARNING
            ),
        )
    )

    assert scene.status == "DEGRADED"
    assert scene.fields[0].value == "Degraded 2, healthy 5."
    assert (
        scene.severity
        is HEOSApplicationRunOperationsDashboardSeverity.WARNING
    )


def test_idle_view_renders_neutral_scene() -> None:
    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        view(
            status="IDLE",
            detail="No dashboard refreshes recorded.",
            refreshes="Refreshes —",
            frames="Frames —",
            sequence="Sequence —",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
            ),
        )
    )

    assert scene.status == "IDLE"
    assert scene.fields[1].value == "Refreshes —"
    assert scene.fields[2].value == "Frames —"
    assert scene.fields[3].value == "Sequence —"
    assert (
        scene.severity
        is HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
    )


def test_render_scene_is_snapshot() -> None:
    source = view(
        title="HEOS Operations Dashboard",
        refreshes="Refreshes 222",
        frames="Frames 222",
        sequence="Sequence 222",
    )

    scene = HEOSApplicationRunOperationsDashboardHealthRenderer().render(
        source
    )

    assert scene.title == "HEOS Operations Dashboard"
    assert scene.fields[1].value == "Refreshes 222"
    assert scene.fields[2].value == "Frames 222"
    assert scene.fields[3].value == "Sequence 222"
    assert scene.field_count == 4
