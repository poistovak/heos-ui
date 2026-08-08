from __future__ import annotations

from dataclasses import dataclass

from heos_ui.diagnostics import SystemHealth

from .brain import BrainCycleReport


@dataclass(frozen=True, slots=True)
class BrainRuntimeSnapshot:
    cycle_sequence: int
    system_health: SystemHealth
    accepted: int
    blocked: int
    executed: int
    healthy_targets: int
    unhealthy_targets: int
    successful: bool

    @property
    def total_decisions(self) -> int:
        return self.accepted + self.blocked

    @property
    def execution_rate(self) -> float:
        if self.accepted == 0:
            return 0.0

        return self.executed / self.accepted

    @classmethod
    def from_report(
        cls,
        report: BrainCycleReport,
    ) -> BrainRuntimeSnapshot:
        runtime = report.cycle.report

        return cls(
            cycle_sequence=report.sequence,
            system_health=report.system_health,
            accepted=runtime.accepted,
            blocked=runtime.blocked,
            executed=runtime.executed,
            healthy_targets=report.healthy_targets,
            unhealthy_targets=report.unhealthy_targets,
            successful=report.successful,
        )