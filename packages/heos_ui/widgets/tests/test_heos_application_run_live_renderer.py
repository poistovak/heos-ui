from heos_ui.widgets.heos_application_run_live_renderer import (
    HEOSApplicationRunLiveRenderer,
)
from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunSeverity,
)
from heos_ui.widgets.heos_application_run_status import (
    HEOSApplicationRunStatusView,
)


def view(
    *,
    title: str = "HEOS Application",
    status: str = "COMPLETED",
    detail: str = "Processed 3, rendered 3.",
    cycles: str = "Cycles 1–193",
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


def test_live_renderer_starts_empty() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    assert renderer.latest is None
    assert renderer.latest_frame is None
    assert renderer.render_count == 0
    assert not renderer.has_frame


def test_render_returns_canvas_frame() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    frame = renderer.render(view())

    assert frame.command_count == 4


def test_render_stores_latest_result() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    frame = renderer.render(view())

    assert renderer.latest is not None
    assert renderer.latest.frame is frame
    assert renderer.latest_frame is frame
    assert renderer.has_frame


def test_render_increments_count() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    renderer.render(view())

    assert renderer.render_count == 1


def test_multiple_renders_increment_count() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    renderer.render(view(status="IDLE"))
    renderer.render(view(status="COMPLETED"))
    renderer.render(view(status="INTERRUPTED"))

    assert renderer.render_count == 3


def test_second_render_replaces_latest_frame() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    first = renderer.render(
        view(
            status="IDLE",
            severity=HEOSApplicationRunSeverity.NEUTRAL,
        )
    )

    second = renderer.render(
        view(
            status="COMPLETED",
            severity=HEOSApplicationRunSeverity.SUCCESS,
        )
    )

    assert renderer.latest_frame is second
    assert renderer.latest_frame is not first


def test_previous_frame_remains_snapshot() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    first = renderer.render(
        view(
            status="IDLE",
            detail="No cycles processed.",
            cycles="Cycles —",
            severity=HEOSApplicationRunSeverity.NEUTRAL,
        )
    )

    renderer.render(view())

    assert first.commands[1].text == "IDLE"
    assert first.commands[2].text == "Detail: No cycles processed."
    assert first.commands[3].text == "Cycles: Cycles —"


def test_completed_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    frame = renderer.render(
        view(
            status="COMPLETED",
            cycles="Cycles 1–193",
        )
    )

    assert frame.commands[1].text == "COMPLETED"
    assert frame.commands[3].text == "Cycles: Cycles 1–193"
    assert frame.severity is HEOSApplicationRunSeverity.SUCCESS


def test_warning_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    frame = renderer.render(
        view(
            status="INTERRUPTED",
            detail="Processed 1, skipped 2.",
            cycles="Cycle 193",
            severity=HEOSApplicationRunSeverity.WARNING,
        )
    )

    assert frame.commands[1].text == "INTERRUPTED"
    assert frame.commands[2].text == "Detail: Processed 1, skipped 2."
    assert frame.severity is HEOSApplicationRunSeverity.WARNING


def test_neutral_view_flows_to_frame() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    frame = renderer.render(
        view(
            status="IDLE",
            detail="No cycles processed.",
            cycles="Cycles —",
            severity=HEOSApplicationRunSeverity.NEUTRAL,
        )
    )

    assert frame.commands[1].text == "IDLE"
    assert frame.severity is HEOSApplicationRunSeverity.NEUTRAL


def test_latest_result_preserves_scene() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    renderer.render(
        view(
            title="HEOS Runtime",
            status="COMPLETED",
        )
    )

    assert renderer.latest is not None
    assert renderer.latest.scene.title == "HEOS Runtime"
    assert renderer.latest.scene.status == "COMPLETED"


def test_clear_removes_latest_frame() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    renderer.render(view())
    renderer.clear()

    assert renderer.latest is None
    assert renderer.latest_frame is None
    assert not renderer.has_frame


def test_clear_preserves_render_count() -> None:
    renderer = HEOSApplicationRunLiveRenderer.create()

    renderer.render(view())
    renderer.render(view())
    renderer.clear()

    assert renderer.render_count == 2
