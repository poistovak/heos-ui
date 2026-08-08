from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.scene.paint import PaintCommand

from .brain_runtime_session import BrainRuntimeSession


class BrainRuntimeLifecycleState(str, Enum):
    CREATED = "created"
    STARTED = "started"
    RUNNING = "running"
    STOPPED = "stopped"


@dataclass(slots=True)
class BrainRuntimeLifecycle:
    session: BrainRuntimeSession
    _state: BrainRuntimeLifecycleState = BrainRuntimeLifecycleState.CREATED

    @property
    def state(self) -> BrainRuntimeLifecycleState:
        return self._state

    @property
    def started(self) -> bool:
        return self._state in {
            BrainRuntimeLifecycleState.STARTED,
            BrainRuntimeLifecycleState.RUNNING,
        }

    @property
    def running(self) -> bool:
        return self._state is BrainRuntimeLifecycleState.RUNNING

    @property
    def stopped(self) -> bool:
        return self._state is BrainRuntimeLifecycleState.STOPPED

    def start(self) -> None:
        if self._state is not BrainRuntimeLifecycleState.CREATED:
            raise RuntimeError(
                f"Cannot start runtime from state {self._state.value}."
            )

        self._state = BrainRuntimeLifecycleState.STARTED

    def publish(
        self,
        snapshot: BrainRuntimeSnapshot,
    ) -> None:
        if self._state not in {
            BrainRuntimeLifecycleState.STARTED,
            BrainRuntimeLifecycleState.RUNNING,
        }:
            raise RuntimeError(
                f"Cannot publish runtime snapshot in state {self._state.value}."
            )

        self.session.publish(snapshot)
        self._state = BrainRuntimeLifecycleState.RUNNING

    def render(self) -> tuple[PaintCommand, ...]:
        if self._state is not BrainRuntimeLifecycleState.RUNNING:
            raise RuntimeError(
                f"Cannot render runtime in state {self._state.value}."
            )

        return self.session.render()

    def stop(self) -> None:
        if self._state not in {
            BrainRuntimeLifecycleState.STARTED,
            BrainRuntimeLifecycleState.RUNNING,
        }:
            raise RuntimeError(
                f"Cannot stop runtime from state {self._state.value}."
            )

        self._state = BrainRuntimeLifecycleState.STOPPED
