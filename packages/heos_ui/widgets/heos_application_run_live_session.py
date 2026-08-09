from __future__ import annotations

from dataclasses import dataclass, field

from .heos_application_run_live_bridge import (
    HEOSApplicationRunLiveBridge,
    HEOSApplicationRunLiveBridgeResult,
)
from .heos_application_runtime import HEOSApplicationRuntime
from .heos_application_runtime_loop import HEOSApplicationLoopResult


@dataclass(slots=True)
class HEOSApplicationRunLiveSession:
    bridge: HEOSApplicationRunLiveBridge
    _history: list[HEOSApplicationRunLiveBridgeResult] = field(
        default_factory=list,
        init=False,
    )

    @property
    def history(self) -> tuple[HEOSApplicationRunLiveBridgeResult, ...]:
        return tuple(self._history)

    @property
    def latest(self) -> HEOSApplicationRunLiveBridgeResult | None:
        if not self._history:
            return None

        return self._history[-1]

    @property
    def run_count(self) -> int:
        return len(self._history)

    @property
    def has_runs(self) -> bool:
        return bool(self._history)

    def publish(
        self,
        application: HEOSApplicationRuntime,
        result: HEOSApplicationLoopResult,
        *,
        requested: int,
    ) -> HEOSApplicationRunLiveBridgeResult:
        published = self.bridge.publish(
            application,
            result,
            requested=requested,
        )
        self._history.append(published)

        return published

    def clear(self) -> None:
        self._history.clear()
        self.bridge.clear()
