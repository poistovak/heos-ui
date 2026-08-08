from __future__ import annotations

from dataclasses import dataclass

from heos_ui.events.bus import EventBus

from .brain_runtime_diagnostics import BrainRuntimeDiagnostics
from .brain_runtime_events import BrainRuntimeEvents
from .brain_runtime_factory import BrainRuntimeFactory
from .brain_runtime_health import BrainRuntimeHealthAssessor
from .brain_runtime_history import BrainRuntimeHistory
from .brain_runtime_integration import BrainRuntimeIntegration
from .brain_runtime_lifecycle import BrainRuntimeLifecycle
from .brain_runtime_metrics import BrainRuntimeMetrics
from .brain_runtime_orchestrator import BrainRuntimeOrchestrator
from .brain_runtime_recovery import (
    BrainRuntimeRecovery,
    BrainRuntimeRecoveryPolicy,
)
from .brain_runtime_service import BrainRuntimeService
from .brain_runtime_session import BrainRuntimeSession


@dataclass(frozen=True, slots=True)
class BrainRuntimeBootstrap:
    @staticmethod
    def create() -> BrainRuntimeService:
        runtime = BrainRuntimeLifecycle(
            session=BrainRuntimeSession(
                runtime=BrainRuntimeFactory.create(),
            )
        )

        orchestrator = BrainRuntimeOrchestrator(
            events=BrainRuntimeEvents(
                runtime=runtime,
                event_bus=EventBus(),
            ),
            history=BrainRuntimeHistory(),
            diagnostics=BrainRuntimeDiagnostics(),
            recovery=BrainRuntimeRecovery(
                runtime=runtime,
                policy=BrainRuntimeRecoveryPolicy(),
            ),
            metrics=BrainRuntimeMetrics(),
            health_assessor=BrainRuntimeHealthAssessor(),
        )

        integration = BrainRuntimeIntegration(
            orchestrator=orchestrator,
        )

        return BrainRuntimeService(
            integration=integration,
        )
