from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from heos_ui.energy import EnergySnapshot

from .conflict import DecisionAction


@dataclass(frozen=True, slots=True)
class DecisionOutcome:
    success: bool
    message: str = ""


@dataclass(frozen=True, slots=True)
class DecisionAuditRecord:
    snapshot: EnergySnapshot
    candidate: DecisionAction
    outcome: DecisionOutcome
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(slots=True)
class DecisionAuditTrail:
    _records: list[DecisionAuditRecord] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def record(
        self,
        snapshot: EnergySnapshot,
        candidate: DecisionAction,
        outcome: DecisionOutcome,
    ) -> DecisionAuditRecord:
        record = DecisionAuditRecord(
            snapshot=snapshot,
            candidate=candidate,
            outcome=outcome,
        )
        self._records.append(record)
        return record

    def records(self) -> tuple[DecisionAuditRecord, ...]:
        return tuple(self._records)

    def successful(self) -> tuple[DecisionAuditRecord, ...]:
        return tuple(
            record
            for record in self._records
            if record.outcome.success
        )

    def failed(self) -> tuple[DecisionAuditRecord, ...]:
        return tuple(
            record
            for record in self._records
            if not record.outcome.success
        )

    def for_target(
        self,
        target: str,
    ) -> tuple[DecisionAuditRecord, ...]:
        return tuple(
            record
            for record in self._records
            if record.candidate.action.target == target
        )

    @property
    def count(self) -> int:
        return len(self._records)

    def clear(self) -> None:
        self._records.clear()