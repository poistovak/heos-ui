from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot

from .brain_runtime_orchestrator import BrainRuntimeCycleResult
from .heos_application_runtime import HEOSApplicationRuntime


@dataclass(frozen=True, slots=True)
class HEOSApplicationLoopResult:
    processed: int
    stopped: bool
    results: tuple[BrainRuntimeCycleResult, ...]

    @property
    def completed(self) -> bool:
        return not self.stopped

    @property
    def last_result(self) -> BrainRuntimeCycleResult | None:
        if not self.results:
            return None

        return self.results[-1]


@dataclass(slots=True)
class HEOSApplicationRuntimeLoop:
    application: HEOSApplicationRuntime

    def run(
        self,
        snapshots: tuple[BrainRuntimeSnapshot, ...],
    ) -> HEOSApplicationLoopResult:
        if not self.application.running:
            self.application.start()

        results: list[BrainRuntimeCycleResult] = []

        for snapshot in snapshots:
            result = self.application.tick(snapshot)
            results.append(result)

            if self.application.stopped:
                break

        return HEOSApplicationLoopResult(
            processed=len(results),
            stopped=self.application.stopped,
            results=tuple(results),
        )
