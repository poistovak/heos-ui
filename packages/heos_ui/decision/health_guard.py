from __future__ import annotations

from dataclasses import dataclass

from heos_ui.diagnostics.health_registry import HealthRegistry

from .conflict import DecisionAction
from .recovery import RecoveryState


@dataclass(frozen=True, slots=True)
class HealthGuardResult:
    target: str
    allowed: bool
    state: RecoveryState | None
    reason: str


@dataclass(slots=True)
class HealthAwareDecisionGuard:
    registry: HealthRegistry

    def evaluate(
        self,
        candidate: DecisionAction,
    ) -> HealthGuardResult:
        target = candidate.action.target

        if not self.registry.contains(target):
            return HealthGuardResult(
                target=target,
                allowed=False,
                state=None,
                reason="Target is not registered.",
            )

        health = self.registry.health(target)

        if health.state is RecoveryState.HEALTHY:
            return HealthGuardResult(
                target=target,
                allowed=True,
                state=health.state,
                reason="Target is healthy.",
            )

        if health.state is RecoveryState.BACKOFF:
            return HealthGuardResult(
                target=target,
                allowed=False,
                state=health.state,
                reason="Target is in backoff.",
            )

        return HealthGuardResult(
            target=target,
            allowed=False,
            state=health.state,
            reason="Target is in recovery probe.",
        )

    def allows(
        self,
        candidate: DecisionAction,
    ) -> bool:
        return self.evaluate(candidate).allowed