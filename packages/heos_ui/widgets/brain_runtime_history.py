from __future__ import annotations

from dataclasses import dataclass, field

from .brain_runtime_lifecycle import BrainRuntimeLifecycle
from .brain_runtime_state import BrainRuntimeState


@dataclass(slots=True)
class BrainRuntimeHistory:
    _states: list[BrainRuntimeState] = field(
        default_factory=list,
        init=False,
    )

    @property
    def count(self) -> int:
        return len(self._states)

    @property
    def empty(self) -> bool:
        return not self._states

    @property
    def states(self) -> tuple[BrainRuntimeState, ...]:
        return tuple(self._states)

    @property
    def latest(self) -> BrainRuntimeState | None:
        if not self._states:
            return None

        return self._states[-1]

    def record(
        self,
        runtime: BrainRuntimeLifecycle,
    ) -> BrainRuntimeState:
        state = BrainRuntimeState.capture(runtime)
        self._states.append(state)

        return state

    def clear(self) -> None:
        self._states.clear()
