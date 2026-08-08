from __future__ import annotations

from dataclasses import dataclass

from .brain_runtime_health import (
    BrainRuntimeHealthAssessor,
    BrainRuntimeHealthLevel,
)
from .brain_runtime_history import BrainRuntimeHistory
from .brain_runtime_metrics import BrainRuntimeMetrics
from .brain_runtime_recovery import (
    BrainRuntimeRecoveryAction,
    BrainRuntimeRecoveryPolicy,
)


@dataclass(frozen=True, slots=True)
class BrainRuntimeDiagnosticReport:
    total_states: int
    latest_cycle: int | None
    attention_states: int
    attention_ratio: float
    health: BrainRuntimeHealthLevel
    recommended_action: BrainRuntimeRecoveryAction
    summary: str

    @property
    def healthy(self) -> bool:
        return self.health is BrainRuntimeHealthLevel.HEALTHY

    @property
    def requires_attention(self) -> bool:
        return self.health in {
            BrainRuntimeHealthLevel.DEGRADED,
            BrainRuntimeHealthLevel.CRITICAL,
        }


@dataclass(frozen=True, slots=True)
class BrainRuntimeDiagnostics:
    metrics: BrainRuntimeMetrics = BrainRuntimeMetrics()
    health: BrainRuntimeHealthAssessor = BrainRuntimeHealthAssessor()
    recovery: BrainRuntimeRecoveryPolicy = BrainRuntimeRecoveryPolicy()

    def inspect(
        self,
        history: BrainRuntimeHistory,
    ) -> BrainRuntimeDiagnosticReport:
        metrics = self.metrics.analyze(history)
        health = self.health.assess(metrics)
        recovery = self.recovery.decide(health)

        summary = self._summary(
            health.level,
            metrics.total,
            metrics.latest_cycle,
        )

        return BrainRuntimeDiagnosticReport(
            total_states=metrics.total,
            latest_cycle=metrics.latest_cycle,
            attention_states=metrics.attention,
            attention_ratio=metrics.attention_ratio,
            health=health.level,
            recommended_action=recovery.action,
            summary=summary,
        )

    @staticmethod
    def _summary(
        health: BrainRuntimeHealthLevel,
        total_states: int,
        latest_cycle: int | None,
    ) -> str:
        if health is BrainRuntimeHealthLevel.UNKNOWN:
            return "Runtime has no diagnostic history."

        cycle = (
            str(latest_cycle)
            if latest_cycle is not None
            else "unknown"
        )

        return (
            f"Runtime health is {health.value}; "
            f"{total_states} states observed; "
            f"latest cycle {cycle}."
        )
