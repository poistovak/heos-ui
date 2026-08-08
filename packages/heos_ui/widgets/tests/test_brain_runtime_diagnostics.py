from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.diagnostics import SystemHealth
from heos_ui.widgets.brain_runtime_diagnostics import BrainRuntimeDiagnostics
from heos_ui.widgets.brain_runtime_factory import BrainRuntimeFactory
from heos_ui.widgets.brain_runtime_health import BrainRuntimeHealthLevel
from heos_ui.widgets.brain_runtime_history import BrainRuntimeHistory
from heos_ui.widgets.brain_runtime_lifecycle import BrainRuntimeLifecycle
from heos_ui.widgets.brain_runtime_recovery import BrainRuntimeRecoveryAction
from heos_ui.widgets.brain_runtime_session import BrainRuntimeSession


def snapshot(
    *,
    cycle: int = 175,
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


def test_empty_history_reports_unknown() -> None:
    report = BrainRuntimeDiagnostics().inspect(
        BrainRuntimeHistory()
    )

    assert report.health is BrainRuntimeHealthLevel.UNKNOWN
    assert report.recommended_action is BrainRuntimeRecoveryAction.WAIT


def test_empty_history_has_zero_states() -> None:
    report = BrainRuntimeDiagnostics().inspect(
        BrainRuntimeHistory()
    )

    assert report.total_states == 0
    assert report.latest_cycle is None
    assert report.summary == "Runtime has no diagnostic history."


def test_healthy_history_reports_healthy() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()
    runtime.publish(snapshot())
    history.record(runtime)

    report = BrainRuntimeDiagnostics().inspect(history)

    assert report.health is BrainRuntimeHealthLevel.HEALTHY
    assert report.healthy
    assert not report.requires_attention


def test_healthy_history_recommends_continue() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()
    runtime.publish(snapshot())
    history.record(runtime)

    report = BrainRuntimeDiagnostics().inspect(history)

    assert report.recommended_action is BrainRuntimeRecoveryAction.CONTINUE


def test_degraded_history_requires_attention() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()

    runtime.publish(snapshot(cycle=1))
    history.record(runtime)

    runtime.publish(snapshot(cycle=2))
    history.record(runtime)

    runtime.publish(snapshot(cycle=3))
    history.record(runtime)

    runtime.publish(
        snapshot(
            cycle=4,
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )
    history.record(runtime)

    report = BrainRuntimeDiagnostics().inspect(history)

    assert report.health is BrainRuntimeHealthLevel.DEGRADED
    assert report.requires_attention
    assert report.attention_ratio == 0.25


def test_degraded_history_recommends_caution() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()

    runtime.publish(snapshot(cycle=1))
    history.record(runtime)

    runtime.publish(snapshot(cycle=2))
    history.record(runtime)

    runtime.publish(
        snapshot(
            cycle=3,
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )
    history.record(runtime)

    report = BrainRuntimeDiagnostics().inspect(history)

    assert (
        report.recommended_action
        is BrainRuntimeRecoveryAction.CONTINUE_WITH_CAUTION
    )


def test_critical_history_recommends_stop() -> None:
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

    report = BrainRuntimeDiagnostics().inspect(history)

    assert report.health is BrainRuntimeHealthLevel.CRITICAL
    assert report.recommended_action is BrainRuntimeRecoveryAction.STOP


def test_report_contains_attention_count() -> None:
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

    report = BrainRuntimeDiagnostics().inspect(history)

    assert report.attention_states == 1


def test_report_tracks_latest_cycle() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()

    runtime.publish(snapshot(cycle=10))
    history.record(runtime)

    runtime.publish(snapshot(cycle=175))
    history.record(runtime)

    report = BrainRuntimeDiagnostics().inspect(history)

    assert report.latest_cycle == 175


def test_summary_contains_health_and_cycle() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()
    runtime.publish(snapshot(cycle=175))
    history.record(runtime)

    report = BrainRuntimeDiagnostics().inspect(history)

    assert "healthy" in report.summary
    assert "175" in report.summary


def test_diagnostic_report_is_snapshot() -> None:
    runtime = lifecycle()
    history = BrainRuntimeHistory()

    runtime.start()
    runtime.publish(snapshot(cycle=1))
    history.record(runtime)

    first = BrainRuntimeDiagnostics().inspect(history)

    runtime.publish(
        snapshot(
            cycle=2,
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )
    history.record(runtime)

    assert first.total_states == 1
    assert first.latest_cycle == 1
    assert first.health is BrainRuntimeHealthLevel.HEALTHY
