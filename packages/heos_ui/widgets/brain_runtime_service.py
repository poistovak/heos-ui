from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot

from .brain_runtime_diagnostics import BrainRuntimeDiagnosticReport
from .brain_runtime_integration import BrainRuntimeIntegration
from .brain_runtime_orchestrator import BrainRuntimeCycleResult
from .brain_runtime_state import BrainRuntimeState


class BrainRuntimeServiceState(str, Enum):
    CREATED = "created"
    ACTIVE = "active"
    STOPPED = "stopped"


@dataclass(slots=True)
class BrainRuntimeService:
    integration: BrainRuntimeIntegration
    _state: BrainRuntimeServiceState = BrainRuntimeServiceState.CREATED
    _processed_cycles: int = 0

    @property
    def state(self) -> BrainRuntimeServiceState:
        return self._state

    @property
    def active(self) -> bool:
        return self._state is BrainRuntimeServiceState.ACTIVE

    @property
    def stopped(self) -> bool:
        return self._state is BrainRuntimeServiceState.STOPPED

    @property
    def processed_cycles(self) -> int:
        return self._processed_cycles

    @property
    def runtime_state(self) -> BrainRuntimeState:
        return self.integration.state

    @property
    def diagnostics(self) -> BrainRuntimeDiagnosticReport:
        return self.integration.diagnostics

    @property
    def last_result(self) -> BrainRuntimeCycleResult | None:
        return self.integration.last_result

    def start(self) -> None:
        if self._state is not BrainRuntimeServiceState.CREATED:
            raise RuntimeError(
                f"Cannot start runtime service from state {self._state.value}."
            )

        self.integration.start()
        self._state = BrainRuntimeServiceState.ACTIVE

    def process(
        self,
        snapshot: BrainRuntimeSnapshot,
    ) -> BrainRuntimeCycleResult:
        if not self.active:
            raise RuntimeError(
                f"Cannot process snapshot in service state {self._state.value}."
            )

        result = self.integration.update(snapshot)
        self._processed_cycles += 1

        if self.integration.stopped:
            self._state = BrainRuntimeServiceState.STOPPED

        return result

    def stop(self) -> None:
        if not self.active:
            raise RuntimeError(
                f"Cannot stop runtime service from state {self._state.value}."
            )

        self.integration.stop()
        self._state = BrainRuntimeServiceState.STOPPED
