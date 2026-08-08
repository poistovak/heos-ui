from __future__ import annotations

from dataclasses import dataclass, field

from heos_ui.diagnostics import HealthRegistry, SystemHealth

from .conflict import DecisionAction
from .runtime_cycle import RuntimeCycle, RuntimeCycleResult
from .runtime_history import RuntimeCycleHistory


@dataclass(frozen=True, slots=True)
class BrainCycleReport:
    sequence: int
    cycle: RuntimeCycleResult
    system_health: SystemHealth
    healthy_targets: int
    unhealthy_targets: int

    @property
    def successful(self) -> bool:
        return (
            self.cycle.successful
            and self.system_health is SystemHealth.HEALTHY
        )


@dataclass(slots=True)
class HEOSBrainSupervisor:
    cycle: RuntimeCycle
    history: RuntimeCycleHistory
    health: HealthRegistry
    _last_report: BrainCycleReport | None = field(
        default=None,
        init=False,
        repr=False,
    )

    def run(
        self,
        candidates: list[DecisionAction],
    ) -> BrainCycleReport:
        cycle_result = self.cycle.run(candidates)
        history_record = self.history.record(cycle_result)

        health_snapshot = self.health.snapshot()
        unhealthy = self.health.unhealthy()

        report = BrainCycleReport(
            sequence=history_record.sequence,
            cycle=cycle_result,
            system_health=self.health.system_health,
            healthy_targets=(
                len(health_snapshot) - len(unhealthy)
            ),
            unhealthy_targets=len(unhealthy),
        )

        self._last_report = report
        return report

    @property
    def cycle_count(self) -> int:
        return self.history.count

    @property
    def last_report(self) -> BrainCycleReport | None:
        return self._last_report