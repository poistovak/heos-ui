from __future__ import annotations

from dataclasses import dataclass

from .brain_runtime_lifecycle import (
    BrainRuntimeLifecycle,
    BrainRuntimeLifecycleState,
)


@dataclass(frozen=True, slots=True)
class BrainRuntimeState:
    lifecycle: BrainRuntimeLifecycleState
    has_data: bool
    status: str
    cycle: int | None
    started: bool
    running: bool
    stopped: bool

    @classmethod
    def capture(
        cls,
        runtime: BrainRuntimeLifecycle,
    ) -> BrainRuntimeState:
        return cls(
            lifecycle=runtime.state,
            has_data=runtime.session.has_data,
            status=runtime.session.status,
            cycle=runtime.session.cycle,
            started=runtime.started,
            running=runtime.running,
            stopped=runtime.stopped,
        )
