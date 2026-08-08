from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .brain_status import BrainStatusWidget


class BrainStatusSeverity(str, Enum):
    UNKNOWN = "unknown"
    NORMAL = "normal"
    WARNING = "warning"


@dataclass(frozen=True, slots=True)
class BrainStatusPresentation:
    title: str
    status: str
    health: str
    cycle: str
    execution: str
    targets: str
    severity: BrainStatusSeverity


@dataclass(frozen=True, slots=True)
class BrainStatusPresenter:
    def present(
        self,
        widget: BrainStatusWidget,
    ) -> BrainStatusPresentation:
        if not widget.has_data:
            return BrainStatusPresentation(
                title=widget.title,
                status="UNKNOWN",
                health="UNKNOWN",
                cycle="Cycle —",
                execution="Execution —",
                targets="Targets —",
                severity=BrainStatusSeverity.UNKNOWN,
            )

        severity = (
            BrainStatusSeverity.NORMAL
            if widget.status == "RUNNING"
            else BrainStatusSeverity.WARNING
        )

        return BrainStatusPresentation(
            title=widget.title,
            status=widget.status,
            health=widget.health,
            cycle=f"Cycle {widget.cycle}",
            execution=f"Execution {widget.execution_percent}%",
            targets=f"Targets {widget.target_summary}",
            severity=severity,
        )