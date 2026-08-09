from heos_ui.widgets.heos_application_run_operations_dashboard_health_widget import (
    HEOSApplicationRunOperationsDashboardHealthView,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_live_renderer import (
    HEOSApplicationRunOperationsDashboardLiveRenderer,
)
from heos_ui.widgets.heos_application_run_operations_dashboard_presenter import (
    HEOSApplicationRunOperationsDashboardSeverity,
)


def view(
    *,
    title: str = "HEOS Operations Dashboard",
    status: str = "HEALTHY",
    detail: str = "Healthy 224, idle 1.",
    refreshes: str = "Refreshes 225",
    frames: str = "Frames 225",
    sequence: str = "Sequence 225",
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


def test_live_renderer_starts_empty() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    assert renderer.latest is None
    assert renderer.latest_frame is None
    assert renderer.render_count == 0
    assert not renderer.has_frame


def test_render_returns_canvas_frame() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    frame = renderer.render(view())

    assert frame.command_count == 6


def test_render_stores_latest_result() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    frame = renderer.render(view())

    assert renderer.latest is not None
    assert renderer.latest.frame is frame
    assert renderer.latest_frame is frame
    assert renderer.has_frame


def test_first_render_increments_count() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    renderer.render(view())

    assert renderer.render_count == 1


def test_multiple_renders_increment_count() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    renderer.render(
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
    renderer.render(view())
    renderer.render(
        view(
            status="DEGRADED",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.WARNING
            ),
        )
    )

    assert renderer.render_count == 3


def test_second_render_replaces_latest_frame() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    first = renderer.render(
        view(
            status="IDLE",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
            ),
        )
    )
    second = renderer.render(view())

    assert renderer.latest_frame is second
    assert renderer.latest_frame is not first


def test_previous_frame_remains_snapshot() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    first = renderer.render(
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

    renderer.render(view())

    assert first.commands[1].text == "IDLE"
    assert (
        first.commands[2].text
        == "Detail: No dashboard refreshes recorded."
    )
    assert first.commands[3].text == "Refreshes: Refreshes —"
    assert first.commands[4].text == "Frames: Frames —"
    assert first.commands[5].text == "Sequence: Sequence —"


def test_healthy_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    frame = renderer.render(
        view(
            status="HEALTHY",
            refreshes="Refreshes 225",
            sequence="Sequence 225",
        )
    )

    assert frame.commands[1].text == "HEALTHY"
    assert frame.commands[3].text == "Refreshes: Refreshes 225"
    assert frame.commands[5].text == "Sequence: Sequence 225"
    assert (
        frame.severity
        is HEOSApplicationRunOperationsDashboardSeverity.SUCCESS
    )


def test_degraded_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    frame = renderer.render(
        view(
            status="DEGRADED",
            detail="Degraded 2, healthy 5.",
            severity=(
                HEOSApplicationRunOperationsDashboardSeverity.WARNING
            ),
        )
    )

    assert frame.commands[1].text == "DEGRADED"
    assert (
        frame.commands[2].text
        == "Detail: Degraded 2, healthy 5."
    )
    assert (
        frame.severity
        is HEOSApplicationRunOperationsDashboardSeverity.WARNING
    )


def test_idle_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    frame = renderer.render(
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

    assert frame.commands[1].text == "IDLE"
    assert (
        frame.severity
        is HEOSApplicationRunOperationsDashboardSeverity.NEUTRAL
    )


def test_latest_result_preserves_scene() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    renderer.render(
        view(
            title="HEOS Operations Control",
            status="HEALTHY",
            sequence="Sequence 225",
        )
    )

    assert renderer.latest is not None
    assert renderer.latest.scene.title == "HEOS Operations Control"
    assert renderer.latest.scene.status == "HEALTHY"
    assert (
        renderer.latest.scene.fields[3].value
        == "Sequence 225"
    )


def test_latest_frame_contains_six_commands() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    renderer.render(view())

    assert renderer.latest_frame is not None
    assert renderer.latest_frame.command_count == 6


def test_clear_removes_latest_frame() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    assert renderer.latest is None
    assert renderer.latest_frame is None
    assert not renderer.has_frame


def test_clear_preserves_render_count() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    renderer.render(view())
    renderer.render(view())
    renderer.clear()

    assert renderer.render_count == 2


def test_render_after_clear_continues_count() -> None:
    renderer = HEOSApplicationRunOperationsDashboardLiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    frame = renderer.render(view())

    assert renderer.render_count == 2
    assert renderer.latest_frame is frame
    assert renderer.has_frame
