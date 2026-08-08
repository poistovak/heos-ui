from __future__ import annotations

from dataclasses import dataclass

from .runtime import DecisionRuntimeResult


@dataclass(frozen=True, slots=True)
class RuntimeExecutionReport:
    accepted: int
    blocked: int
    executed: int

    @property
    def total(self) -> int:
        return self.accepted + self.blocked

    @property
    def fully_executed(self) -> bool:
        return (
            self.blocked == 0
            and self.executed == self.accepted
        )

    @property
    def has_blocked(self) -> bool:
        return self.blocked > 0

    @classmethod
    def from_result(
        cls,
        result: DecisionRuntimeResult,
    ) -> RuntimeExecutionReport:
        return cls(
            accepted=len(result.guarded.accepted),
            blocked=len(result.guarded.blocked),
            executed=result.executed,
        )