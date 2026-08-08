from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot

from .brain_runtime_diagnostics import BrainRuntimeDiagnosticReport
from .brain_runtime_lifecycle import BrainRuntimeLifecycleState
from .brain_runtime_orchestrator import (
    BrainRuntimeCycleResult,
    BrainRuntimeOrchestrator,
)
from .brain_runtime_state import BrainRuntimeState


@dataclass(slots=True)
class BrainRuntimeIntegration:
    orchestrator: BrainRuntimeOrchestrator
    _last_result: BrainRuntimeCycleResult | None = None

    @property
    def started(self) -> bool:
        return self.orchestrator.events.runtime.started

    @property
    def running(self) -> bool:
        return self.orchestrator.events.runtime.running

    @property
    def stopped(self) -> bool:
        return self.orchestrator.events.runtime.stopped

    @property
    def lifecycle(self) -> BrainRuntimeLifecycleState:
        return self.orchestrator.events.runtime.state

    @property
    def state(self) -> BrainRuntimeState:
        return BrainRuntimeState.capture(
            self.orchestrator.events.runtime
        )

    @property
    def last_result(self) -> BrainRuntimeCycleResult | None:
        return self._last_result

    @property
    def diagnostics(self) -> BrainRuntimeDiagnosticReport:
        return self.orchestrator.diagnostics.inspect(
            self.orchestrator.history
        )

    def start(self) -> None:
        self.orchestrator.start()

    def update(
        self,
        snapshot: BrainRuntimeSnapshot,
    ) -> BrainRuntimeCycleResult:
        result = self.orchestrator.run(snapshot)
        self._last_result = result
        return result

    def stop(self) -> None:
        if not self.stopped:
            self.orchestrator.events.stop()
            self.orchestrator.history.record(
                self.orchestrator.events.runtime
            )
