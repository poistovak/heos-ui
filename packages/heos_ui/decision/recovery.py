from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from .backoff import BackoffPolicy


class RecoveryState(str, Enum):
    HEALTHY = "healthy"
    BACKOFF = "backoff"
    PROBE = "probe"


@dataclass(slots=True)
class RecoveryPolicy:
    backoff: BackoffPolicy
    _states: dict[str, RecoveryState] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    def state(
        self,
        target: str,
    ) -> RecoveryState:
        current = self._states.get(
            target,
            RecoveryState.HEALTHY,
        )

        if (
            current is RecoveryState.HEALTHY
            and not self.backoff.allows(target)
        ):
            current = RecoveryState.BACKOFF
            self._states[target] = current

        return current

    def begin_probe(
        self,
        target: str,
    ) -> RecoveryState:
        if self.state(target) is not RecoveryState.BACKOFF:
            raise RuntimeError(
                f"Target '{target}' is not in backoff."
            )

        self._states[target] = RecoveryState.PROBE
        return RecoveryState.PROBE

    def probe_succeeded(
        self,
        target: str,
    ) -> RecoveryState:
        self._require_probe(target)

        self._states[target] = RecoveryState.HEALTHY
        return RecoveryState.HEALTHY

    def probe_failed(
        self,
        target: str,
    ) -> RecoveryState:
        self._require_probe(target)

        self._states[target] = RecoveryState.BACKOFF
        return RecoveryState.BACKOFF

    def can_execute(
        self,
        target: str,
    ) -> bool:
        return self.state(target) is not RecoveryState.BACKOFF

    def reset(
        self,
        target: str,
    ) -> None:
        self._states.pop(target, None)

    def clear(self) -> None:
        self._states.clear()

    def _require_probe(
        self,
        target: str,
    ) -> None:
        if self.state(target) is not RecoveryState.PROBE:
            raise RuntimeError(
                f"Target '{target}' is not probing."
            )