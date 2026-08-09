from heos_ui.widgets.heos_application_run_session_health_widget import (
    HEOSApplicationRunSessionHealthView,
)
from heos_ui.widgets.heos_application_run_session_live_renderer import (
    HEOSApplicationRunSessionLiveRenderer,
)
from heos_ui.widgets.heos_application_run_session_presenter import (
    HEOSApplicationRunSessionSeverity,
)


def view(
    *,
    title: str = "HEOS Live Session",
    status: str = "HEALTHY",
    detail: str = "Completed 5, interrupted 0.",
    runs: str = "Runs 5",
    cycles: str = "Processed 10, rendered 10.",
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


def test_live_renderer_starts_empty() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    assert renderer.latest is None
    assert renderer.latest_frame is None
    assert renderer.render_count == 0
    assert not renderer.has_frame


def test_render_returns_canvas_frame() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    frame = renderer.render(view())

    assert frame.command_count == 5


def test_render_stores_latest_result() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    frame = renderer.render(view())

    assert renderer.latest is not None
    assert renderer.latest.frame is frame
    assert renderer.latest_frame is frame
    assert renderer.has_frame


def test_first_render_increments_count() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    renderer.render(view())

    assert renderer.render_count == 1


def test_multiple_renders_increment_count() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    renderer.render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunSessionSeverity.NEUTRAL,
        )
    )
    renderer.render(view())
    renderer.render(
        view(
            status="DEGRADED",
            severity=HEOSApplicationRunSessionSeverity.WARNING,
        )
    )

    assert renderer.render_count == 3


def test_second_render_replaces_latest_frame() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    first = renderer.render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunSessionSeverity.NEUTRAL,
        )
    )

    second = renderer.render(view())

    assert renderer.latest_frame is second
    assert renderer.latest_frame is not first


def test_previous_frame_remains_snapshot() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    first = renderer.render(
        view(
            status="IDLE",
            detail="No application runs recorded.",
            runs="Runs —",
            cycles="Cycles —",
            severity=HEOSApplicationRunSessionSeverity.NEUTRAL,
        )
    )

    renderer.render(view())

    assert first.commands[1].text == "IDLE"
    assert (
        first.commands[2].text
        == "Detail: No application runs recorded."
    )
    assert first.commands[3].text == "Runs: Runs —"
    assert first.commands[4].text == "Cycles: Cycles —"


def test_healthy_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    frame = renderer.render(
        view(
            status="HEALTHY",
            runs="Runs 205",
        )
    )

    assert frame.commands[1].text == "HEALTHY"
    assert frame.commands[3].text == "Runs: Runs 205"
    assert (
        frame.severity
        is HEOSApplicationRunSessionSeverity.SUCCESS
    )


def test_degraded_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    frame = renderer.render(
        view(
            status="DEGRADED",
            detail="Interrupted 1, skipped 2.",
            severity=HEOSApplicationRunSessionSeverity.WARNING,
        )
    )

    assert frame.commands[1].text == "DEGRADED"
    assert (
        frame.commands[2].text
        == "Detail: Interrupted 1, skipped 2."
    )
    assert (
        frame.severity
        is HEOSApplicationRunSessionSeverity.WARNING
    )


def test_idle_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    frame = renderer.render(
        view(
            status="IDLE",
            detail="No application runs recorded.",
            runs="Runs —",
            cycles="Cycles —",
            severity=HEOSApplicationRunSessionSeverity.NEUTRAL,
        )
    )

    assert frame.commands[1].text == "IDLE"
    assert (
        frame.severity
        is HEOSApplicationRunSessionSeverity.NEUTRAL
    )


def test_latest_result_preserves_scene() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    renderer.render(
        view(
            title="HEOS Operations",
            status="HEALTHY",
        )
    )

    assert renderer.latest is not None
    assert renderer.latest.scene.title == "HEOS Operations"
    assert renderer.latest.scene.status == "HEALTHY"


def test_clear_removes_latest_frame() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    assert renderer.latest is None
    assert renderer.latest_frame is None
    assert not renderer.has_frame


def test_clear_preserves_render_count() -> None:
    renderer = HEOSApplicationRunSessionLiveRenderer.create()

    renderer.render(view())
    renderer.render(view())
    renderer.clear()

    assert renderer.render_count == 2
