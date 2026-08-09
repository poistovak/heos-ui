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
from heos_ui.widgets.heos_application_run_live_session_statistics import (
    HEOSApplicationRunLiveSessionStatistics,
)
from heos_ui.widgets.heos_application_run_presenter import (
    HEOSApplicationRunPresenter,
)
from heos_ui.widgets.heos_application_run_session_health import (
    HEOSApplicationRunSessionHealth,
    HEOSApplicationRunSessionHealthSummary,
)
from heos_ui.widgets.heos_application_run_session_health_pipeline import (
    HEOSApplicationRunSessionHealthPipeline,
    HEOSApplicationRunSessionHealthPipelineResult,
)
from heos_ui.widgets.heos_application_run_session_presenter import (
    HEOSApplicationRunSessionHealthPresenter,
    HEOSApplicationRunSessionSeverity,
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


def publish(
    live: HEOSApplicationRunLiveSession,
    snapshots: tuple[BrainRuntimeSnapshot, ...],
) -> None:
    application = HEOSApplicationRuntime.create()

    result = HEOSApplicationRuntimeLoop(
        application=application,
    ).run(snapshots)

    live.publish(
        application,
        result,
        requested=len(snapshots),
    )


def test_create_builds_default_presenter() -> None:
    pipeline = HEOSApplicationRunSessionHealthPipeline.create()

    assert isinstance(
        pipeline.presenter,
        HEOSApplicationRunSessionHealthPresenter,
    )


def test_evaluate_returns_pipeline_result() -> None:
    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        session()
    )

    assert isinstance(
        result,
        HEOSApplicationRunSessionHealthPipelineResult,
    )


def test_empty_session_produces_empty_statistics() -> None:
    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        session()
    )

    assert isinstance(
        result.statistics,
        HEOSApplicationRunLiveSessionStatistics,
    )
    assert result.statistics.total_runs == 0


def test_empty_session_produces_empty_health() -> None:
    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        session()
    )

    assert isinstance(
        result.summary,
        HEOSApplicationRunSessionHealthSummary,
    )
    assert result.summary.health is HEOSApplicationRunSessionHealth.EMPTY


def test_empty_session_produces_idle_presentation() -> None:
    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        session()
    )

    assert result.presentation.status == "IDLE"
    assert (
        result.presentation.severity
        is HEOSApplicationRunSessionSeverity.NEUTRAL
    )


def test_completed_run_produces_healthy_summary() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=200),
        ),
    )

    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        live
    )

    assert result.summary.health is HEOSApplicationRunSessionHealth.HEALTHY
    assert result.summary.healthy


def test_completed_run_produces_success_presentation() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=200),
        ),
    )

    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        live
    )

    assert result.presentation.status == "HEALTHY"
    assert (
        result.presentation.severity
        is HEOSApplicationRunSessionSeverity.SUCCESS
    )


def test_pipeline_preserves_completed_counts() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
            snapshot(cycle=200),
        ),
    )

    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        live
    )

    assert result.statistics.total_runs == 1
    assert result.statistics.completed_runs == 1
    assert result.statistics.processed == 2
    assert result.statistics.rendered == 2


def test_idle_run_remains_healthy_session() -> None:
    live = session()

    publish(live, ())
    publish(
        live,
        (
            snapshot(cycle=200),
        ),
    )

    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        live
    )

    assert result.statistics.idle_runs == 1
    assert result.summary.healthy
    assert result.presentation.status == "HEALTHY"


def test_interrupted_run_produces_degraded_summary() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(
                cycle=200,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=201),
            snapshot(cycle=202),
        ),
    )

    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        live
    )

    assert result.statistics.interrupted_runs == 1
    assert result.statistics.skipped == 2
    assert result.summary.degraded


def test_interrupted_run_produces_warning_presentation() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(
                cycle=200,
                health=SystemHealth.DEGRADED,
                successful=False,
            ),
            snapshot(cycle=201),
        ),
    )

    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        live
    )

    assert result.presentation.status == "DEGRADED"
    assert (
        result.presentation.severity
        is HEOSApplicationRunSessionSeverity.WARNING
    )


def test_multiple_runs_flow_through_entire_pipeline() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
            snapshot(cycle=2),
        ),
    )
    publish(live, ())
    publish(
        live,
        (
            snapshot(cycle=200),
        ),
    )

    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        live
    )

    assert result.statistics.total_runs == 3
    assert result.statistics.completed_runs == 2
    assert result.statistics.idle_runs == 1
    assert result.summary.healthy
    assert result.presentation.runs == "Runs 3"


def test_latest_sequence_flows_through_pipeline() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
        ),
    )
    publish(
        live,
        (
            snapshot(cycle=200),
        ),
    )

    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        live
    )

    assert result.statistics.latest_sequence == 2
    assert result.summary.latest_sequence == 2


def test_pipeline_result_is_snapshot() -> None:
    live = session()

    publish(
        live,
        (
            snapshot(cycle=1),
        ),
    )

    result = HEOSApplicationRunSessionHealthPipeline.create().evaluate(
        live
    )

    publish(
        live,
        (
            snapshot(cycle=200),
        ),
    )

    assert result.statistics.total_runs == 1
    assert result.summary.total_runs == 1
    assert result.presentation.runs == "Runs 1"


def test_custom_presenter_flows_through_pipeline() -> None:
    pipeline = HEOSApplicationRunSessionHealthPipeline(
        presenter=HEOSApplicationRunSessionHealthPresenter(
            title="HEOS M200 Session",
        )
    )

    result = pipeline.evaluate(session())

    assert result.presentation.title == "HEOS M200 Session"
