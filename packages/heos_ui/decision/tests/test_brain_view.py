from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.decision.brain_view import BrainViewModel
from heos_ui.diagnostics import SystemHealth


def snapshot(
    *,
    cycle: int = 154,
    health: SystemHealth = SystemHealth.HEALTHY,
    accepted: int = 4,
    blocked: int = 0,
    executed: int = 4,
    healthy_targets: int = 5,
    unhealthy_targets: int = 0,
    successful: bool = True,
) -> BrainRuntimeSnapshot:
    return BrainRuntimeSnapshot(
        cycle_sequence=cycle,
        system_health=health,
        accepted=accepted,
        blocked=blocked,
        executed=executed,
        healthy_targets=healthy_targets,
        unhealthy_targets=unhealthy_targets,
        successful=successful,
    )


def test_builds_view_model() -> None:
    view = BrainViewModel.from_snapshot(
        snapshot()
    )

    assert view.cycle == 154
    assert view.health == "HEALTHY"
    assert view.successful


def test_runtime_counts_are_exposed() -> None:
    view = BrainViewModel.from_snapshot(
        snapshot(
            accepted=3,
            blocked=2,
            executed=2,
        )
    )

    assert view.accepted == 3
    assert view.blocked == 2
    assert view.executed == 2
    assert view.total_decisions == 5


def test_execution_percent() -> None:
    view = BrainViewModel.from_snapshot(
        snapshot(
            accepted=4,
            executed=3,
        )
    )

    assert view.execution_percent == 75


def test_zero_execution_percent_without_decisions() -> None:
    view = BrainViewModel.from_snapshot(
        snapshot(
            accepted=0,
            executed=0,
        )
    )

    assert view.execution_percent == 0


def test_target_counts() -> None:
    view = BrainViewModel.from_snapshot(
        snapshot(
            healthy_targets=4,
            unhealthy_targets=2,
        )
    )

    assert view.total_targets == 6
    assert view.target_summary == "4/6 healthy"


def test_successful_status_is_running() -> None:
    view = BrainViewModel.from_snapshot(
        snapshot(successful=True)
    )

    assert view.status == "RUNNING"


def test_unsuccessful_status_requires_attention() -> None:
    view = BrainViewModel.from_snapshot(
        snapshot(
            health=SystemHealth.DEGRADED,
            successful=False,
        )
    )

    assert view.health == "DEGRADED"
    assert view.status == "ATTENTION"


def test_snapshot_is_decoupled_from_view() -> None:
    source = snapshot()

    view = BrainViewModel.from_snapshot(source)

    assert view.cycle == source.cycle_sequence
    assert view.total_decisions == source.total_decisions
    assert view.execution_percent == 100