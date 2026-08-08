from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision.recovery import RecoveryPolicy, RecoveryState

from .engine import ExecutionEngine


@dataclass(frozen=True, slots=True)
class GateDecision:
    target: str
    allowed: bool
    state: RecoveryState
    reason: str


@dataclass(slots=True)
class ExecutionSafetyGate:
    engine: ExecutionEngine
    recovery: RecoveryPolicy

    def evaluate(
        self,
        target: str,
    ) -> GateDecision:
        state = self.recovery.state(target)

        if state is RecoveryState.BACKOFF:
            return GateDecision(
                target=target,
                allowed=False,
                state=state,
                reason="Target is in backoff.",
            )

        if state is RecoveryState.PROBE:
            return GateDecision(
                target=target,
                allowed=True,
                state=state,
                reason="Recovery probe is allowed.",
            )

        return GateDecision(
            target=target,
            allowed=True,
            state=state,
            reason="Target is healthy.",
        )

    def allows(
        self,
        target: str,
    ) -> bool:
        return self.evaluate(target).allowed