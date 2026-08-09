from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_health_renderer as history_renderer,
)
from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_health_widget as history_widget,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_presenter import (
    HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity,
)

HealthRenderer = (
    history_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthRenderer
)
RenderField = (
    history_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderField
)
RenderScene = (
    history_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryRenderScene
)
HealthView = (
    history_widget.HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView
)


def view(
    *,
    title: str = "HEOS Operations Dashboard Runtime History",
    status: str = "HEALTHY",
    detail: str = "Healthy 5, idle 1.",
    cycles: str = "Cycles 6",
    frames: str = "Frames 6",
    latest: str = "Latest cycle 6",
    severity: HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity = (
        HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.SUCCESS
    ),
) -> HealthView:
    return HealthView(
        title=title,
        status=status,
        detail=detail,
        cycles=cycles,
        frames=frames,
        latest=latest,
        severity=severity,
    )


def test_renderer_returns_render_scene() -> None:
    scene = HealthRenderer().render(view())

    assert isinstance(scene, RenderScene)


def test_renderer_preserves_title() -> None:
    scene = HealthRenderer().render(
        view(title="HEOS Runtime Observatory")
    )

    assert scene.title == "HEOS Runtime Observatory"


def test_renderer_preserves_status() -> None:
    scene = HealthRenderer().render(
        view(status="HEALTHY")
    )

    assert scene.status == "HEALTHY"


def test_renderer_preserves_success_severity() -> None:
    scene = HealthRenderer().render(
        view(
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.SUCCESS
            )
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.SUCCESS
    )


def test_renderer_preserves_warning_severity() -> None:
    scene = HealthRenderer().render(
        view(
            status="DEGRADED",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
            ),
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
    )


def test_renderer_preserves_neutral_severity() -> None:
    scene = HealthRenderer().render(
        view(
            status="EMPTY",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.NEUTRAL
            ),
        )
    )

    assert (
        scene.severity
        is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.NEUTRAL
    )


def test_renderer_creates_detail_field() -> None:
    scene = HealthRenderer().render(
        view(detail="Healthy 231, idle 2.")
    )

    field = scene.fields[0]

    assert isinstance(field, RenderField)
    assert field.label == "Detail"
    assert field.value == "Healthy 231, idle 2."


def test_renderer_creates_cycles_field() -> None:
    scene = HealthRenderer().render(
        view(cycles="Cycles 233")
    )

    field = scene.fields[1]

    assert field.label == "Cycles"
    assert field.value == "Cycles 233"


def test_renderer_creates_frames_field() -> None:
    scene = HealthRenderer().render(
        view(frames="Frames 233")
    )

    field = scene.fields[2]

    assert field.label == "Frames"
    assert field.value == "Frames 233"


def test_renderer_creates_latest_field() -> None:
    scene = HealthRenderer().render(
        view(latest="Latest cycle 233")
    )

    field = scene.fields[3]

    assert field.label == "Latest"
    assert field.value == "Latest cycle 233"


def test_renderer_creates_four_fields() -> None:
    scene = HealthRenderer().render(view())

    assert scene.field_count == 4
    assert len(scene.fields) == 4


def test_renderer_preserves_field_order() -> None:
    scene = HealthRenderer().render(view())

    assert tuple(field.label for field in scene.fields) == (
        "Detail",
        "Cycles",
        "Frames",
        "Latest",
    )


def test_degraded_view_renders_warning_scene() -> None:
    scene = HealthRenderer().render(
        view(
            status="DEGRADED",
            detail="Degraded 2, healthy 8, idle 1.",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
            ),
        )
    )

    assert scene.status == "DEGRADED"
    assert scene.fields[0].value == "Degraded 2, healthy 8, idle 1."
    assert (
        scene.severity
        is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
    )


def test_empty_view_renders_neutral_scene() -> None:
    scene = HealthRenderer().render(
        view(
            status="EMPTY",
            detail="No runtime history recorded.",
            cycles="Cycles 0",
            frames="Frames 0",
            latest="Latest cycle —",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.NEUTRAL
            ),
        )
    )

    assert scene.status == "EMPTY"
    assert scene.fields[1].value == "Cycles 0"
    assert scene.fields[2].value == "Frames 0"
    assert scene.fields[3].value == "Latest cycle —"
    assert (
        scene.severity
        is HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.NEUTRAL
    )


def test_render_scene_is_snapshot() -> None:
    source = view(
        cycles="Cycles 233",
        frames="Frames 233",
        latest="Latest cycle 233",
    )

    scene = HealthRenderer().render(source)

    assert scene.fields[1].value == "Cycles 233"
    assert scene.fields[2].value == "Frames 233"
    assert scene.fields[3].value == "Latest cycle 233"
    assert scene.field_count == 4
