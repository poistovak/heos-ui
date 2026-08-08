from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone

from .conflict import DecisionAction


@dataclass(frozen=True, slots=True)
class DecisionTraceEntry:
    candidate: DecisionAction
    accepted: bool
    reason: str
    timestamp: datetime = field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


@dataclass(slots=True)
class DecisionTrace:
    _entries: list[DecisionTraceEntry] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def record(
        self,
        candidate: DecisionAction,
        *,
        accepted: bool,
        reason: str,
    ) -> DecisionTraceEntry:
        entry = DecisionTraceEntry(
            candidate=candidate,
            accepted=accepted,
            reason=reason,
        )
        self._entries.append(entry)
        return entry

    def entries(self) -> tuple[DecisionTraceEntry, ...]:
        return tuple(self._entries)

    def accepted(self) -> tuple[DecisionTraceEntry, ...]:
        return tuple(
            entry for entry in self._entries if entry.accepted
        )

    def rejected(self) -> tuple[DecisionTraceEntry, ...]:
        return tuple(
            entry for entry in self._entries if not entry.accepted
        )

    @property
    def count(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        self._entries.clear()