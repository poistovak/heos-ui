from __future__ import annotations

from dataclasses import dataclass

from heos_ui.decision import (
    DecisionAction,
    DecisionAuditTrail,
    DecisionOutcome,
)
from heos_ui.energy import EnergySnapshot

from .safety_gate import ExecutionSafetyGate


@dataclass(frozen=True, slots=True)
class PipelineResult:
    target: str
    executed: bool
    success: bool
    message: str


@dataclass(slots=True)
class SafeExecutionPipeline:
    gate: ExecutionSafetyGate
    audit: DecisionAuditTrail

    def execute(
        self,
        snapshot: EnergySnapshot,
        candidate: DecisionAction,
        *,
        success: bool = True,
        message: str = "",
    ) -> PipelineResult:
        target = candidate.action.target
        gate_decision = self.gate.evaluate(target)

        if not gate_decision.allowed:
            return PipelineResult(
                target=target,
                executed=False,
                success=False,
                message=gate_decision.reason,
            )

        outcome = DecisionOutcome(
            success=success,
            message=message,
        )

        self.audit.record(
            snapshot,
            candidate,
            outcome,
        )

        return PipelineResult(
            target=target,
            executed=True,
            success=success,
            message=message,
        )