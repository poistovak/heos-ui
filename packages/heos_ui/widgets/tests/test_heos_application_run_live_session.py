from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.heos_application_run_live_bridge import (
    HEOSApplicationRunLiveBridge,
)
from heos_ui.widgets.heos_application_run_live_controller import (
    HEOSApplicationRunLiveController,
)
from heos_ui.widgets.heos_application_run_live_renderer import (
    HEOSApplicationRunLiveRenderer,
)
from heos_ui.widgets.heos_application_run_live_session import (
    HEOSApplicationRunLiveSession,
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


def session() -> HEOSApplicationRunLiveSession:
    return HEOSApplicationRunLiveSession(
        bridge=HEOSApplicationRunLiveBridge(
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
    )


def run(
    snapshots: tuple[BrainRuntimeSnapshot, ...],
):
    application = HEOSApplicationRuntime.create()
    result = HEOSApplicationRuntimeLoop(
        application=application,
    ).run(snapshots)

    return application, result


def test_session_starts_empty() -> None:
    live = session()

    assert live.history == ()
    assert live.latest is None
    assert live.run_count == 0
    assert not live.has_runs


def test_publish_adds_first_run() -> None:
    live = session()
    application, result = run(
        (
            snapshot(cycle=196),
        )
    )

    published = live.publish(
        application,
        result,
        requested=1,
    )

    assert live.run_count == 1
    assert live.has_runs
    assert live.latest is published


def test_history_contains_published_run() -> None:
    live = session()
    application, result = run(
        (
            snapshot(cycle=196),
        )
    )

    published = live.publish(
        application,
        result,
        requested=1,
    )

    assert live.history == (published,)


def test_multiple_runs_preserve_order() -> None:
    live = session()

    application1, result1 = run(
        (
            snapshot(cycle=1),
        )
    )
    first = live.publish(
        application1,
        result1,
        requested=1,
    )

    application2, result2 = run(
        (
            snapshot(cycle=2),
            snapshot(cycle=196),
        )
    )
    second = live.publish(
        application2,
        result2,
        requested=2,
    )

    assert live.history == (first, second)
    assert live.latest is second
    assert live.run_count == 2


def test_history_is_exposed_as_tuple_snapshot() -> None:
    live = session()
    application, result = run(
        (
            snapshot(cycle=196),
        )
    )

    live.publish(
        application,
        result,
        requested=1,
    )

    history = live.history

    assert isinstance(history, tuple)
    assert len(history) == 1


def test_previous_history_snapshot_does_not_change() -> None:
    live = session()

    application1, result1 = run(
        (
            snapshot(cycle=1),
        )
    )
    live.publish(
        application1,
        result1,
        requested=1,
    )

    history = live.history

    application2, result2 = run(
        (
            snapshot(cycle=196),
        )
    )
    live.publish(
        application2,
        result2,
        requested=1,
    )

    assert len(history) == 1
    assert len(live.history) == 2


def test_completed_run_is_stored() -> None:
    live = session()
    application, result = run(
        (
            snapshot(cycle=196),
        )
    )

    published = live.publish(
        application,
        result,
        requested=1,
    )

    assert published.report.completed
    assert published.update.view.status == "COMPLETED"


def test_empty_run_is_stored() -> None:
    live = session()
    application, result = run(())

    published = live.publish(
        application,
        result,
        requested=0,
    )

    assert published.report.processed == 0
    assert published.update.view.status == "IDLE"
    assert live.run_count == 1


def test_interrupted_run_is_stored() -> None:
    live = session()
    application, result = run(
        (
            snapshot(
                cycle=196,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=197),
        )
    )

    published = live.publish(
        application,
        result,
        requested=2,
    )

    assert published.report.stopped
    assert published.report.skipped == 1
    assert published.update.view.status == "INTERRUPTED"
    assert live.latest is published


def test_bridge_sequence_continues_across_session_runs() -> None:
    live = session()

    application1, result1 = run(
        (
            snapshot(cycle=1),
        )
    )
    first = live.publish(
        application1,
        result1,
        requested=1,
    )

    application2, result2 = run(
        (
            snapshot(cycle=196),
        )
    )
    second = live.publish(
        application2,
        result2,
        requested=1,
    )

    assert first.sequence == 1
    assert second.sequence == 2


def test_clear_removes_session_history() -> None:
    live = session()
    application, result = run(
        (
            snapshot(cycle=196),
        )
    )

    live.publish(
        application,
        result,
        requested=1,
    )
    live.clear()

    assert live.history == ()
    assert live.latest is None
    assert live.run_count == 0
    assert not live.has_runs


def test_clear_removes_bridge_live_state() -> None:
    live = session()
    application, result = run(
        (
            snapshot(cycle=196),
        )
    )

    live.publish(
        application,
        result,
        requested=1,
    )
    live.clear()

    assert live.bridge.latest is None
    assert not live.bridge.has_data
    assert live.bridge.controller.latest is None


def test_publish_after_clear_starts_new_session_history() -> None:
    live = session()
    application, result = run(
        (
            snapshot(cycle=196),
        )
    )

    live.publish(
        application,
        result,
        requested=1,
    )
    live.clear()

    published = live.publish(
        application,
        result,
        requested=1,
    )

    assert live.run_count == 1
    assert live.history == (published,)


def test_publish_after_clear_preserves_live_sequence() -> None:
    live = session()
    application, result = run(
        (
            snapshot(cycle=196),
        )
    )

    first = live.publish(
        application,
        result,
        requested=1,
    )
    live.clear()
    second = live.publish(
        application,
        result,
        requested=1,
    )

    assert first.sequence == 1
    assert second.sequence == 2
