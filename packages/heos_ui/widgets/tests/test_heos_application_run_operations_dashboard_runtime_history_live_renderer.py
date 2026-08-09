from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_health_widget as health_widget,
)
from heos_ui.widgets import (
    heos_application_run_operations_dashboard_runtime_history_live_renderer as live_renderer,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_runtime_history_presenter import (
    HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity,
)

LiveRenderer = (
    live_renderer.HEOSApplicationRunOperationsDashboardRuntimeHistoryLiveRenderer
)
HealthView = (
    health_widget.HEOSApplicationRunOperationsDashboardRuntimeHistoryHealthView
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


def test_live_renderer_starts_empty() -> None:
    renderer = LiveRenderer.create()

    assert renderer.latest_result is None
    assert renderer.latest_frame is None
    assert renderer.render_count == 0
    assert not renderer.has_frame


def test_create_builds_pipeline() -> None:
    renderer = LiveRenderer.create()

    assert renderer.pipeline is not None


def test_render_returns_frame_result() -> None:
    renderer = LiveRenderer.create()

    result = renderer.render(view())

    assert result.frame.command_count == 6
    assert result.scene.field_count == 4


def test_render_stores_latest_result() -> None:
    renderer = LiveRenderer.create()

    result = renderer.render(view())

    assert renderer.latest_result is result


def test_render_stores_latest_frame() -> None:
    renderer = LiveRenderer.create()

    result = renderer.render(view())

    assert renderer.latest_frame is result.frame
    assert renderer.has_frame


def test_first_render_increments_count() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())

    assert renderer.render_count == 1


def test_multiple_renders_increment_count() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())
    renderer.render(view())
    renderer.render(view())

    assert renderer.render_count == 3


def test_latest_result_tracks_last_render() -> None:
    renderer = LiveRenderer.create()

    renderer.render(
        view(
            cycles="Cycles 1",
            latest="Latest cycle 1",
        )
    )
    second = renderer.render(
        view(
            cycles="Cycles 236",
            latest="Latest cycle 236",
        )
    )

    assert renderer.latest_result is second
    assert renderer.latest_frame is second.frame


def test_latest_frame_contains_latest_status() -> None:
    renderer = LiveRenderer.create()

    renderer.render(
        view(status="HEALTHY")
    )
    renderer.render(
        view(
            status="DEGRADED",
            severity=(
                HEOSApplicationRunOperationsDashboardRuntimeHistorySeverity.WARNING
            ),
        )
    )

    assert renderer.latest_frame is not None
    assert renderer.latest_frame.commands[1].text == "DEGRADED"


def test_previous_result_remains_snapshot() -> None:
    renderer = LiveRenderer.create()

    first = renderer.render(
        view(
            cycles="Cycles 1",
            frames="Frames 1",
            latest="Latest cycle 1",
        )
    )

    renderer.render(
        view(
            cycles="Cycles 236",
            frames="Frames 236",
            latest="Latest cycle 236",
        )
    )

    assert first.frame.commands[3].text == "Cycles: Cycles 1"
    assert first.frame.commands[4].text == "Frames: Frames 1"
    assert first.frame.commands[5].text == "Latest: Latest cycle 1"


def test_clear_removes_latest_result() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    assert renderer.latest_result is None


def test_clear_removes_latest_frame() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    assert renderer.latest_frame is None
    assert not renderer.has_frame


def test_clear_preserves_render_count() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())
    renderer.render(view())
    renderer.clear()

    assert renderer.render_count == 2


def test_renderer_can_render_after_clear() -> None:
    renderer = LiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    result = renderer.render(
        view(
            cycles="Cycles 236",
            latest="Latest cycle 236",
        )
    )

    assert renderer.latest_result is result
    assert renderer.latest_frame is result.frame
    assert renderer.render_count == 2
    assert renderer.has_frame


def test_empty_view_can_be_rendered() -> None:
    renderer = LiveRenderer.create()

    result = renderer.render(
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

    assert result.scene.status == "EMPTY"
    assert result.frame.commands[1].text == "EMPTY"
    assert result.frame.commands[5].text == "Latest: Latest cycle —"
