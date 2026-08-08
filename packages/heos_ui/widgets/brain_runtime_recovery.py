from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .brain_runtime_health import (
    BrainRuntimeHealthLevel,
    BrainRuntimeHealthSnapshot,
)
from .brain_runtime_lifecycle import BrainRuntimeLifecycle


class BrainRuntimeRecoveryAction(str, Enum):
    WAIT = "wait"
    CONTINUE = "continue"
    CONTINUE_WITH_CAUTION = "continue_with_caution"
    STOP = "stop"


@dataclass(frozen=True, slots=True)
class BrainRuntimeRecoveryDecision:
    action: BrainRuntimeRecoveryAction
    reason: str

    @property
    def should_stop(self) -> bool:
        return self.action is BrainRuntimeRecoveryAction.STOP

    @property
    def can_continue(self) -> bool:
        return self.action in {
            BrainRuntimeRecoveryAction.CONTINUE,
            BrainRuntimeRecoveryAction.CONTINUE_WITH_CAUTION,
        }


@dataclass(frozen=True, slots=True)
class BrainRuntimeRecoveryPolicy:
    def decide(
        self,
        health: BrainRuntimeHealthSnapshot,
    ) -> BrainRuntimeRecoveryDecision:
        if health.level is BrainRuntimeHealthLevel.UNKNOWN:
            return BrainRuntimeRecoveryDecision(
                action=BrainRuntimeRecoveryAction.WAIT,
                reason="Runtime health is unknown.",
            )

        if health.level is BrainRuntimeHealthLevel.HEALTHY:
            return BrainRuntimeRecoveryDecision(
                action=BrainRuntimeRecoveryAction.CONTINUE,
                reason="Runtime is healthy.",
            )

        if health.level is BrainRuntimeHealthLevel.DEGRADED:
            return BrainRuntimeRecoveryDecision(
                action=BrainRuntimeRecoveryAction.CONTINUE_WITH_CAUTION,
                reason="Runtime is degraded.",
            )

        return BrainRuntimeRecoveryDecision(
            action=BrainRuntimeRecoveryAction.STOP,
            reason="Runtime health is critical.",
        )


@dataclass(slots=True)
class BrainRuntimeRecovery:
    runtime: BrainRuntimeLifecycle
    policy: BrainRuntimeRecoveryPolicy

    def apply(
        self,
        health: BrainRuntimeHealthSnapshot,
    ) -> BrainRuntimeRecoveryDecision:
        decision = self.policy.decide(health)

        if (
            decision.should_stop
            and not self.runtime.stopped
        ):
            self.runtime.stop()

        return decision
