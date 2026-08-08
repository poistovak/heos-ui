from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .brain_runtime_metrics import BrainRuntimeMetricsSnapshot


class BrainRuntimeHealthLevel(str, Enum):
    UNKNOWN = "unknown"
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    CRITICAL = "critical"


@dataclass(frozen=True, slots=True)
class BrainRuntimeHealthSnapshot:
    level: BrainRuntimeHealthLevel
    total_states: int
    attention_states: int
    attention_ratio: float
    latest_cycle: int | None

    @property
    def healthy(self) -> bool:
        return self.level is BrainRuntimeHealthLevel.HEALTHY

    @property
    def requires_attention(self) -> bool:
        return self.level in {
            BrainRuntimeHealthLevel.DEGRADED,
            BrainRuntimeHealthLevel.CRITICAL,
        }


@dataclass(frozen=True, slots=True)
class BrainRuntimeHealthAssessor:
    critical_attention_ratio: float = 0.5

    def assess(
        self,
        metrics: BrainRuntimeMetricsSnapshot,
    ) -> BrainRuntimeHealthSnapshot:
        if metrics.total == 0:
            level = BrainRuntimeHealthLevel.UNKNOWN
        elif metrics.attention == 0:
            level = BrainRuntimeHealthLevel.HEALTHY
        elif metrics.attention_ratio >= self.critical_attention_ratio:
            level = BrainRuntimeHealthLevel.CRITICAL
        else:
            level = BrainRuntimeHealthLevel.DEGRADED

        return BrainRuntimeHealthSnapshot(
            level=level,
            total_states=metrics.total,
            attention_states=metrics.attention,
            attention_ratio=metrics.attention_ratio,
            latest_cycle=metrics.latest_cycle,
        )
