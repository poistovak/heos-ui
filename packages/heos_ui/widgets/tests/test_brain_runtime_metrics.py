from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_history import BrainRuntimeHistory
from heos_ui.widgets.brain_runtime_lifecycle import BrainRuntimeLifecycle
from heos_ui.widgets.brain_runtime_metrics import BrainRuntimeMetrics
from heos_ui.widgets.brain_runtime_session import BrainRuntimeSession


def snapshot(
    *,
    cycle: int = 171,
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


def lifecycle() -> BrainRuntimeLifecycle:
    return BrainRuntimeLifecycle(
        session=BrainRuntimeSession(
            runtime=BrainRuntimeFactory.create(),
        )
    )


def test_empty_history_has_zero_metrics() -> None:
    metrics = BrainRuntimeMetrics().analyze(
        BrainRuntimeHistory()
    )

    assert metrics.total == 0
    assert metrics.created == 0
    assert metrics.started == 0
    assert metrics.running == 0
    assert metrics.stopped == 0


def test_empty_history_has_no_cycle_metrics() -> None:
    metrics = BrainRuntimeMetrics().analyze(
        BrainRuntimeHistory()
    )

    assert metrics.latest_cycle is None
    assert metrics.max_cycle is None


def test_created_state_is_counted() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    history.record(runtime)

    metrics = BrainRuntimeMetrics().analyze(history)

    assert metrics.total == 1
    assert metrics.created == 1


def test_lifecycle_states_are_counted() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    history.record(runtime)

    runtime.start()
    history.record(runtime)

    runtime.publish(snapshot())
    history.record(runtime)

    runtime.stop()
    history.record(runtime)

    metrics = BrainRuntimeMetrics().analyze(history)

    assert metrics.total == 4
    assert metrics.created == 1
    assert metrics.started == 1
    assert metrics.running == 1
    assert metrics.stopped == 1


def test_active_counts_started_and_running_states() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()
    history.record(runtime)

    runtime.publish(snapshot())
    history.record(runtime)

    metrics = BrainRuntimeMetrics().analyze(history)

    assert metrics.active == 2


def test_healthy_running_state_is_counted() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()
    runtime.publish(snapshot())
    history.record(runtime)

    metrics = BrainRuntimeMetrics().analyze(history)

    assert metrics.healthy == 1
    assert metrics.attention == 0


def test_attention_state_is_counted() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()
    runtime.publish(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )
    history.record(runtime)

    metrics = BrainRuntimeMetrics().analyze(history)

    assert metrics.attention == 1
    assert metrics.healthy == 0


def test_attention_ratio_is_calculated() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()

    runtime.publish(snapshot(cycle=1))
    history.record(runtime)

    runtime.publish(
        snapshot(
            cycle=2,
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )
    history.record(runtime)

    metrics = BrainRuntimeMetrics().analyze(history)

    assert metrics.attention_ratio == 0.5


def test_empty_attention_ratio_is_zero() -> None:
    metrics = BrainRuntimeMetrics().analyze(
        BrainRuntimeHistory()
    )

    assert metrics.attention_ratio == 0.0


def test_latest_cycle_comes_from_latest_state() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()

    runtime.publish(snapshot(cycle=10))
    history.record(runtime)

    runtime.publish(snapshot(cycle=171))
    history.record(runtime)

    metrics = BrainRuntimeMetrics().analyze(history)

    assert metrics.latest_cycle == 171


def test_max_cycle_tracks_highest_cycle() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()

    runtime.publish(snapshot(cycle=171))
    history.record(runtime)

    runtime.publish(snapshot(cycle=20))
    history.record(runtime)

    runtime.publish(snapshot(cycle=90))
    history.record(runtime)

    metrics = BrainRuntimeMetrics().analyze(history)

    assert metrics.latest_cycle == 90
    assert metrics.max_cycle == 171


def test_metrics_snapshot_does_not_change_with_history() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()
    runtime.publish(snapshot(cycle=1))
    history.record(runtime)

    metrics = BrainRuntimeMetrics().analyze(history)

    runtime.publish(snapshot(cycle=2))
    history.record(runtime)

    assert metrics.total == 1
    assert metrics.latest_cycle == 1
