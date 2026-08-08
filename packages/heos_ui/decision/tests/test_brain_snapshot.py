from heos_ui.decision.brain import BrainCycleReport
from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.decision.runtime_cycle import RuntimeCycleResult
from heos_ui.decision.runtime_report import RuntimeExecutionReport
from heos_ui.diagnostics import SystemHealth


def report(
    *,
    sequence: int = 1,
    accepted: int = 1,
    blocked: int = 0,
    executed: int = 1,
    system_health: SystemHealth = SystemHealth.HEALTHY,
    healthy_targets: int = 2,
    unhealthy_targets: int = 0,
) -> BrainCycleReport:
    return BrainCycleReport(
        sequence=sequence,
        cycle=RuntimeCycleResult(
            report=RuntimeExecutionReport(
                accepted=accepted,
                blocked=blocked,
                executed=executed,
            )
        ),
        system_health=system_health,
        healthy_targets=healthy_targets,
        unhealthy_targets=unhealthy_targets,
    )


def test_snapshot_from_report() -> None:
    snapshot = BrainRuntimeSnapshot.from_report(
        report(sequence=7)
    )

    assert snapshot.cycle_sequence == 7
    assert snapshot.system_health is SystemHealth.HEALTHY


def test_snapshot_contains_runtime_counts() -> None:
    snapshot = BrainRuntimeSnapshot.from_report(
        report(
            accepted=3,
            blocked=1,
            executed=2,
        )
    )

    assert snapshot.accepted == 3
    assert snapshot.blocked == 1
    assert snapshot.executed == 2


def test_snapshot_contains_health_counts() -> None:
    snapshot = BrainRuntimeSnapshot.from_report(
        report(
            healthy_targets=4,
            unhealthy_targets=2,
        )
    )

    assert snapshot.healthy_targets == 4
    assert snapshot.unhealthy_targets == 2


def test_total_decisions() -> None:
    snapshot = BrainRuntimeSnapshot.from_report(
        report(
            accepted=3,
            blocked=2,
            executed=3,
        )
    )

    assert snapshot.total_decisions == 5


def test_execution_rate() -> None:
    snapshot = BrainRuntimeSnapshot.from_report(
        report(
            accepted=4,
            executed=3,
        )
    )

    assert snapshot.execution_rate == 0.75


def test_execution_rate_is_zero_without_accepted_decisions() -> None:
    snapshot = BrainRuntimeSnapshot.from_report(
        report(
            accepted=0,
            blocked=1,
            executed=0,
        )
    )

    assert snapshot.execution_rate == 0.0


def test_successful_state_is_preserved() -> None:
    snapshot = BrainRuntimeSnapshot.from_report(
        report()
    )

    assert snapshot.successful


def test_degraded_state_is_unsuccessful() -> None:
    snapshot = BrainRuntimeSnapshot.from_report(
        report(
            system_health=SystemHealth.DEGRADED,
            healthy_targets=1,
            unhealthy_targets=1,
        )
    )

    assert snapshot.system_health is SystemHealth.DEGRADED
    assert not snapshot.successful