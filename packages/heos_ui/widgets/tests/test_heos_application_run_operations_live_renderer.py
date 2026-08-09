from heos_ui.widgets.heos_application_run_operations_health_widget import (
    HEOSApplicationRunOperationsHealthView,
)
from heos_ui.widgets.heos_application_run_operations_live_renderer import (
    HEOSApplicationRunOperationsLiveRenderer,
)
from heos_ui.widgets.heos_application_run_operations_presenter import (
    HEOSApplicationRunOperationsSeverity,
)


def view(
    *,
    title: str = "HEOS Operations",
    status: str = "HEALTHY",
    detail: str = "Healthy 214, idle 1.",
    updates: str = "Updates 215",
    frames: str = "Frames 215",
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


def test_live_renderer_starts_empty() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    assert renderer.latest is None
    assert renderer.latest_frame is None
    assert renderer.render_count == 0
    assert not renderer.has_frame


def test_render_returns_canvas_frame() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    frame = renderer.render(view())

    assert frame.command_count == 5


def test_render_stores_latest_result() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    frame = renderer.render(view())

    assert renderer.latest is not None
    assert renderer.latest.frame is frame
    assert renderer.latest_frame is frame
    assert renderer.has_frame


def test_first_render_increments_count() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    renderer.render(view())

    assert renderer.render_count == 1


def test_multiple_renders_increment_count() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    renderer.render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )
    renderer.render(view())
    renderer.render(
        view(
            status="DEGRADED",
            severity=HEOSApplicationRunOperationsSeverity.WARNING,
        )
    )

    assert renderer.render_count == 3


def test_second_render_replaces_latest_frame() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    first = renderer.render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )
    second = renderer.render(view())

    assert renderer.latest_frame is second
    assert renderer.latest_frame is not first


def test_previous_frame_remains_snapshot() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    first = renderer.render(
        view(
            status="IDLE",
            detail="No operations updates recorded.",
            updates="Updates —",
            frames="Frames —",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )

    renderer.render(view())

    assert first.commands[1].text == "IDLE"
    assert (
        first.commands[2].text
        == "Detail: No operations updates recorded."
    )
    assert first.commands[3].text == "Updates: Updates —"
    assert first.commands[4].text == "Frames: Frames —"


def test_healthy_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    frame = renderer.render(
        view(
            status="HEALTHY",
            updates="Updates 215",
        )
    )

    assert frame.commands[1].text == "HEALTHY"
    assert frame.commands[3].text == "Updates: Updates 215"
    assert (
        frame.severity
        is HEOSApplicationRunOperationsSeverity.SUCCESS
    )


def test_degraded_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    frame = renderer.render(
        view(
            status="DEGRADED",
            detail="Degraded 2, healthy 5.",
            severity=HEOSApplicationRunOperationsSeverity.WARNING,
        )
    )

    assert frame.commands[1].text == "DEGRADED"
    assert (
        frame.commands[2].text
        == "Detail: Degraded 2, healthy 5."
    )
    assert (
        frame.severity
        is HEOSApplicationRunOperationsSeverity.WARNING
    )


def test_idle_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    frame = renderer.render(
        view(
            status="IDLE",
            detail="No operations updates recorded.",
            updates="Updates —",
            frames="Frames —",
            severity=HEOSApplicationRunOperationsSeverity.NEUTRAL,
        )
    )

    assert frame.commands[1].text == "IDLE"
    assert (
        frame.severity
        is HEOSApplicationRunOperationsSeverity.NEUTRAL
    )


def test_latest_result_preserves_scene() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    renderer.render(
        view(
            title="HEOS Operations Health",
            status="HEALTHY",
        )
    )

    assert renderer.latest is not None
    assert renderer.latest.scene.title == "HEOS Operations Health"
    assert renderer.latest.scene.status == "HEALTHY"


def test_clear_removes_latest_frame() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    assert renderer.latest is None
    assert renderer.latest_frame is None
    assert not renderer.has_frame


def test_clear_preserves_render_count() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    renderer.render(view())
    renderer.render(view())
    renderer.clear()

    assert renderer.render_count == 2


def test_render_after_clear_continues_count() -> None:
    renderer = HEOSApplicationRunOperationsLiveRenderer.create()

    renderer.render(view())
    renderer.clear()
    frame = renderer.render(view())

    assert renderer.render_count == 2
    assert renderer.latest_frame is frame
    assert renderer.has_frame
