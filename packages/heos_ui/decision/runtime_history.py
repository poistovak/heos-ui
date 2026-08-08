from __future__ import annotations

from dataclasses import dataclass, field

from .runtime_cycle import RuntimeCycleResult


@dataclass(frozen=True, slots=True)
class RuntimeCycleRecord:
    sequence: int
    result: RuntimeCycleResult


@dataclass(slots=True)
class RuntimeCycleHistory:
    _records: list[RuntimeCycleRecord] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def record(
        self,
        result: RuntimeCycleResult,
    ) -> RuntimeCycleRecord:
        entry = RuntimeCycleRecord(
            sequence=len(self._records) + 1,
            result=result,
        )

        self._records.append(entry)
        return entry

    @property
    def count(self) -> int:
        return len(self._records)

    def records(self) -> tuple[RuntimeCycleRecord, ...]:
        return tuple(self._records)

    def latest(self) -> RuntimeCycleRecord | None:
        if not self._records:
            return None

        return self._records[-1]

    def successful(self) -> tuple[RuntimeCycleRecord, ...]:
        return tuple(
            record
            for record in self._records
            if record.result.successful
        )

    def failed(self) -> tuple[RuntimeCycleRecord, ...]:
        return tuple(
            record
            for record in self._records
            if not record.result.successful
        )

    def clear(self) -> None:
        self._records.clear()