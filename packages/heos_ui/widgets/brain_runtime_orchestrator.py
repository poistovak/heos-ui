from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision.brain_snapshot import BrainRuntimeSnapshot
from heos_ui.scene.paint import PaintCommand

from .brain_runtime_diagnostics import (
    BrainRuntimeDiagnosticReport,
    BrainRuntimeDiagnostics,
)
from .brain_runtime_events import BrainRuntimeEvents
from .brain_runtime_health import (
    BrainRuntimeHealthAssessor,
    BrainRuntimeHealthSnapshot,
)
from .brain_runtime_history import BrainRuntimeHistory
from .brain_runtime_metrics import BrainRuntimeMetrics
from .brain_runtime_recovery import (
    BrainRuntimeRecovery,
    BrainRuntimeRecoveryAction,
    BrainRuntimeRecoveryDecision,
)


@dataclass(frozen=True, slots=True)
class BrainRuntimeCycleResult:
    cycle: int | None
    diagnostic: BrainRuntimeDiagnosticReport
    recovery: BrainRuntimeRecoveryDecision
    frame: tuple[PaintCommand, ...] | None

    @property
    def rendered(self) -> bool:
        return self.frame is not None

    @property
    def stopped(self) -> bool:
        return self.recovery.should_stop


@dataclass(slots=True)
class BrainRuntimeOrchestrator:
    events: BrainRuntimeEvents
    history: BrainRuntimeHistory
    diagnostics: BrainRuntimeDiagnostics
    recovery: BrainRuntimeRecovery
    metrics: BrainRuntimeMetrics
    health_assessor: BrainRuntimeHealthAssessor

    def start(self) -> None:
        self.events.start()
        self.history.record(self.events.runtime)

    def run(
        self,
        snapshot: BrainRuntimeSnapshot,
    ) -> BrainRuntimeCycleResult:
        self.events.publish(snapshot)
        self.history.record(self.events.runtime)

        metrics = self.metrics.analyze(self.history)
        health = self.health_assessor.assess(metrics)
        diagnostic = self.diagnostics.inspect(self.history)
        recovery = self.recovery.apply(health)

        frame: tuple[PaintCommand, ...] | None = None

        if recovery.action in {
            BrainRuntimeRecoveryAction.CONTINUE,
            BrainRuntimeRecoveryAction.CONTINUE_WITH_CAUTION,
        }:
            frame, _ = self.events.render()

        return BrainRuntimeCycleResult(
            cycle=self.events.runtime.session.cycle,
            diagnostic=diagnostic,
            recovery=recovery,
            frame=frame,
        )

    def health(self) -> BrainRuntimeHealthSnapshot:
        metrics = self.metrics.analyze(self.history)
        return self.health_assessor.assess(metrics)
