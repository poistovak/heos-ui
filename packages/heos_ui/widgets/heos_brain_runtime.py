from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot

from .brain_runtime_bootstrap import BrainRuntimeBootstrap
from .brain_runtime_diagnostics import BrainRuntimeDiagnosticReport
from .brain_runtime_orchestrator import BrainRuntimeCycleResult
from .brain_runtime_service import (
    BrainRuntimeService,
    BrainRuntimeServiceState,
)
from .brain_runtime_state import BrainRuntimeState


@dataclass(slots=True)
class HEOSBrainRuntime:
    service: BrainRuntimeService

    @classmethod
    def create(cls) -> HEOSBrainRuntime:
        return cls(
            service=BrainRuntimeBootstrap.create(),
        )

    @property
    def state(self) -> BrainRuntimeServiceState:
        return self.service.state

    @property
    def active(self) -> bool:
        return self.service.active

    @property
    def stopped(self) -> bool:
        return self.service.stopped

    @property
    def processed_cycles(self) -> int:
        return self.service.processed_cycles

    @property
    def runtime_state(self) -> BrainRuntimeState:
        return self.service.runtime_state

    @property
    def diagnostics(self) -> BrainRuntimeDiagnosticReport:
        return self.service.diagnostics

    @property
    def last_result(self) -> BrainRuntimeCycleResult | None:
        return self.service.last_result

    def start(self) -> None:
        self.service.start()

    def process(
        self,
        snapshot: BrainRuntimeSnapshot,
    ) -> BrainRuntimeCycleResult:
        return self.service.process(snapshot)

    def stop(self) -> None:
        self.service.stop()
