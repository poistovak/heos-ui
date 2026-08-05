from __future__ import annotations

from enum import Enum, auto


class RuntimeState(Enum):
    CREATED = auto()
    RUNNING = auto()
    PAUSED = auto()
    STOPPED = auto()


class RuntimeStateMachine:
    def __init__(self) -> None:
        self._state = RuntimeState.CREATED

    @property
    def state(self) -> RuntimeState:
        return self._state

    def start(self) -> None:
        if self._state is RuntimeState.CREATED:
            self._state = RuntimeState.RUNNING

    def pause(self) -> None:
        if self._state is RuntimeState.RUNNING:
            self._state = RuntimeState.PAUSED

    def resume(self) -> None:
        if self._state is RuntimeState.PAUSED:
            self._state = RuntimeState.RUNNING

    def stop(self) -> None:
        if self._state in (
            RuntimeState.RUNNING,
            RuntimeState.PAUSED,
        ):
            self._state = RuntimeState.STOPPED