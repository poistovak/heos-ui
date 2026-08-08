from __future__ import annotations

from dataclasses import dataclass

from .brain_snapshot import BrainRuntimeSnapshot


@dataclass(frozen=True, slots=True)
class BrainViewModel:
    cycle: int
    health: str
    accepted: int
    blocked: int
    executed: int
    total_decisions: int
    execution_percent: int
    healthy_targets: int
    unhealthy_targets: int
    total_targets: int
    successful: bool

    @property
    def status(self) -> str:
        return "RUNNING" if self.successful else "ATTENTION"

    @property
    def target_summary(self) -> str:
        return (
            f"{self.healthy_targets}/{self.total_targets} healthy"
        )

    @classmethod
    def from_snapshot(
        cls,
        snapshot: BrainRuntimeSnapshot,
    ) -> BrainViewModel:
        total_targets = (
            snapshot.healthy_targets
            + snapshot.unhealthy_targets
        )

        execution_percent = round(
            snapshot.execution_rate * 100
        )

        return cls(
            cycle=snapshot.cycle_sequence,
            health=snapshot.system_health.value.upper(),
            accepted=snapshot.accepted,
            blocked=snapshot.blocked,
            executed=snapshot.executed,
            total_decisions=snapshot.total_decisions,
            execution_percent=execution_percent,
            healthy_targets=snapshot.healthy_targets,
            unhealthy_targets=snapshot.unhealthy_targets,
            total_targets=total_targets,
            successful=snapshot.successful,
        )