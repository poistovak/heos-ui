from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from heos_ui.decision.recovery import RecoveryPolicy, RecoveryState


class SystemHealth(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"


@dataclass(frozen=True, slots=True)
class TargetHealth:
    target: str
    state: RecoveryState


@dataclass(slots=True)
class HealthRegistry:
    recovery: RecoveryPolicy
    _targets: set[str] = field(
        default_factory=set,
        init=False,
        repr=False,
    )

    def register(
        self,
        target: str,
    ) -> None:
        if not target:
            raise ValueError("target must not be empty.")

        self._targets.add(target)

    def unregister(
        self,
        target: str,
    ) -> None:
        self._targets.discard(target)

    def contains(
        self,
        target: str,
    ) -> bool:
        return target in self._targets

    @property
    def count(self) -> int:
        return len(self._targets)

    def health(
        self,
        target: str,
    ) -> TargetHealth:
        if target not in self._targets:
            raise KeyError(target)

        return TargetHealth(
            target=target,
            state=self.recovery.state(target),
        )

    def snapshot(self) -> tuple[TargetHealth, ...]:
        return tuple(
            self.health(target)
            for target in sorted(self._targets)
        )

    @property
    def system_health(self) -> SystemHealth:
        if all(
            item.state is RecoveryState.HEALTHY
            for item in self.snapshot()
        ):
            return SystemHealth.HEALTHY

        return SystemHealth.DEGRADED

    def unhealthy(self) -> tuple[TargetHealth, ...]:
        return tuple(
            item
            for item in self.snapshot()
            if item.state is not RecoveryState.HEALTHY
        )