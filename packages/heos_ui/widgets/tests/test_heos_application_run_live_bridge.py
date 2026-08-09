from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.heos_application_run_live_bridge import (
    HEOSApplicationRunLiveBridge,
    HEOSApplicationRunLiveBridgeResult,
)
from heos_ui.widgets.heos_application_run_live_controller import (
    HEOSApplicationRunLiveController,
)
from heos_ui.widgets.heos_application_run_live_renderer import (
    HEOSApplicationRunLiveRenderer,
)
from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunPresenter,
)
from heos_ui.widgets.heos_application_run_status import (
    HEOSApplicationRunStatusWidget,
)
from heos_ui.widgets.heos_application_run_status_binding import (
    HEOSApplicationRunStatusBinding,
)
from heos_ui.widgets.heos_application_run_status_controller import (
    HEOSApplicationRunStatusController,
)
from heos_ui.widgets.heos_application_runtime import HEOSApplicationRuntime
from heos_ui.widgets.heos_application_runtime_loop import (
    HEOSApplicationRuntimeLoop,
)


def snapshot(
    *,
    cycle: int,
    health: SystemHealth = SystemHealth.HEALTHY,
    successful: bool = True,
) -> BrainRuntimeSnapshot:
    return BrainRuntimeSnapshot(
        cycle_sequence=cycle,
        system_health=health,
        accepted=4,
        blocked=0,
        executed=4,
        healthy_targets=5,
        unhealthy_targets=0,
        successful=successful,
    )


def bridge() -> HEOSApplicationRunLiveBridge:
    return HEOSApplicationRunLiveBridge(
        controller=HEOSApplicationRunLiveController(
            controller=HEOSApplicationRunStatusController(
                binding=HEOSApplicationRunStatusBinding(
                    presenter=HEOSApplicationRunPresenter(),
                    widget=HEOSApplicationRunStatusWidget(),
                )
            ),
            renderer=HEOSApplicationRunLiveRenderer.create(),
        )
    )


def run(
    snapshots: tuple[BrainRuntimeSnapshot, ...],
) -> tuple[
    HEOSApplicationRuntime,
    object,
]:
    application = HEOSApplicationRuntime.create()

    result = HEOSApplicationRuntimeLoop(
        application=application,
    ).run(snapshots)

    return application, result


def test_bridge_starts_empty() -> None:
    live_bridge = bridge()

    assert live_bridge.latest is None
    assert not live_bridge.has_data


def test_publish_returns_bridge_result() -> None:
    application, result = run(
        (
            snapshot(cycle=195),
        )
    )

    published = bridge().publish(
        application,
        result,
        requested=1,
    )

    assert isinstance(
        published,
        HEOSApplicationRunLiveBridgeResult,
    )


def test_publish_captures_report() -> None:
    application, result = run(
        (
            snapshot(cycle=195),
        )
    )

    published = bridge().publish(
        application,
        result,
        requested=1,
    )

    assert published.report.requested == 1
    assert published.report.processed == 1
    assert published.report.rendered == 1


def test_publish_creates_completed_view() -> None:
    application, result = run(
        (
            snapshot(cycle=195),
        )
    )

    published = bridge().publish(
        application,
        result,
        requested=1,
    )

    assert published.update.view.status == "COMPLETED"
    assert published.update.view.successful


def test_publish_creates_canvas_frame() -> None:
    application, result = run(
        (
            snapshot(cycle=195),
        )
    )

    published = bridge().publish(
        application,
        result,
        requested=1,
    )

    assert published.update.frame.command_count == 4
    assert published.update.frame.commands[1].text == "COMPLETED"


def test_publish_preserves_cycle_range() -> None:
    application, result = run(
        (
            snapshot(cycle=10),
            snapshot(cycle=195),
        )
    )

    published = bridge().publish(
        application,
        result,
        requested=2,
    )

    assert published.report.first_cycle == 10
    assert published.report.last_cycle == 195
    assert published.update.view.cycles == "Cycles 10–195"


def test_empty_run_flows_to_idle_frame() -> None:
    application, result = run(())

    published = bridge().publish(
        application,
        result,
        requested=0,
    )

    assert published.report.completed
    assert published.update.view.status == "IDLE"
    assert published.update.frame.commands[1].text == "IDLE"


def test_interrupted_run_flows_to_warning_frame() -> None:
    application, result = run(
        (
            snapshot(
                cycle=195,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=196),
            snapshot(cycle=197),
        )
    )

    published = bridge().publish(
        application,
        result,
        requested=3,
    )

    assert published.report.stopped
    assert published.report.processed == 1
    assert published.report.skipped == 2
    assert published.update.view.status == "INTERRUPTED"
    assert published.update.view.warning
    assert published.update.frame.commands[1].text == "INTERRUPTED"


def test_first_publish_has_sequence_one() -> None:
    application, result = run(
        (
            snapshot(cycle=195),
        )
    )
    live_bridge = bridge()

    published = live_bridge.publish(
        application,
        result,
        requested=1,
    )

    assert published.sequence == 1


def test_second_publish_increments_sequence() -> None:
    live_bridge = bridge()

    application1, result1 = run(
        (
            snapshot(cycle=1),
        )
    )
    first = live_bridge.publish(
        application1,
        result1,
        requested=1,
    )

    application2, result2 = run(
        (
            snapshot(cycle=1),
            snapshot(cycle=195),
        )
    )
    second = live_bridge.publish(
        application2,
        result2,
        requested=2,
    )

    assert first.sequence == 1
    assert second.sequence == 2


def test_latest_tracks_last_publish() -> None:
    live_bridge = bridge()

    application, result = run(
        (
            snapshot(cycle=195),
        )
    )

    published = live_bridge.publish(
        application,
        result,
        requested=1,
    )

    assert live_bridge.latest is published
    assert live_bridge.has_data


def test_previous_publish_remains_snapshot() -> None:
    live_bridge = bridge()

    application1, result1 = run(
        (
            snapshot(cycle=1),
        )
    )
    first = live_bridge.publish(
        application1,
        result1,
        requested=1,
    )

    application2, result2 = run(
        (
            snapshot(cycle=1),
            snapshot(cycle=195),
        )
    )
    live_bridge.publish(
        application2,
        result2,
        requested=2,
    )

    assert first.report.processed == 1
    assert first.update.view.cycles == "Cycle 1"
    assert first.sequence == 1


def test_clear_removes_bridge_and_live_state() -> None:
    live_bridge = bridge()

    application, result = run(
        (
            snapshot(cycle=195),
        )
    )

    live_bridge.publish(
        application,
        result,
        requested=1,
    )
    live_bridge.clear()

    assert live_bridge.latest is None
    assert not live_bridge.has_data
    assert live_bridge.controller.latest is None
    assert live_bridge.controller.latest_frame is None


def test_clear_preserves_live_sequence_counter() -> None:
    live_bridge = bridge()

    application, result = run(
        (
            snapshot(cycle=195),
        )
    )

    live_bridge.publish(
        application,
        result,
        requested=1,
    )
    live_bridge.clear()

    published = live_bridge.publish(
        application,
        result,
        requested=1,
    )

    assert published.sequence == 2
