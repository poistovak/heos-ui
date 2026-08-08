from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot

from .brain_runtime_orchestrator import BrainRuntimeCycleResult
from .heos_brain_runtime import HEOSBrainRuntime


class HEOSApplicationState(str, Enum):
    CREATED = "created"
    RUNNING = "running"
    STOPPED = "stopped"


@dataclass(slots=True)
class HEOSApplicationRuntime:
    brain: HEOSBrainRuntime
    _state: HEOSApplicationState = HEOSApplicationState.CREATED
    _ticks: int = 0

    @classmethod
    def create(cls) -> HEOSApplicationRuntime:
        return cls(
            brain=HEOSBrainRuntime.create(),
        )

    @property
    def state(self) -> HEOSApplicationState:
        return self._state

    @property
    def running(self) -> bool:
        return self._state is HEOSApplicationState.RUNNING

    @property
    def stopped(self) -> bool:
        return self._state is HEOSApplicationState.STOPPED

    @property
    def ticks(self) -> int:
        return self._ticks

    @property
    def last_result(self) -> BrainRuntimeCycleResult | None:
        return self.brain.last_result

    def start(self) -> None:
        if self._state is not HEOSApplicationState.CREATED:
            raise RuntimeError(
                f"Cannot start application from state {self._state.value}."
            )

        self.brain.start()
        self._state = HEOSApplicationState.RUNNING

    def tick(
        self,
        snapshot: BrainRuntimeSnapshot,
    ) -> BrainRuntimeCycleResult:
        if not self.running:
            raise RuntimeError(
                f"Cannot tick application in state {self._state.value}."
            )

        result = self.brain.process(snapshot)
        self._ticks += 1

        if self.brain.stopped:
            self._state = HEOSApplicationState.STOPPED

        return result

    def stop(self) -> None:
        if not self.running:
            raise RuntimeError(
                f"Cannot stop application from state {self._state.value}."
            )

        self.brain.stop()
        self._state = HEOSApplicationState.STOPPED
