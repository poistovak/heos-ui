from __future__ import annotations

from dataclasses import dataclass

from .conflict import DecisionAction
from .runtime import DecisionRuntime
from .runtime_report import RuntimeExecutionReport


@dataclass(frozen=True, slots=True)
class RuntimeCycleResult:
    report: RuntimeExecutionReport

    @property
    def successful(self) -> bool:
        return self.report.fully_executed


@dataclass(slots=True)
class RuntimeCycle:
    runtime: DecisionRuntime
    cycle_count: int = 0

    def run(
        self,
        candidates: list[DecisionAction],
    ) -> RuntimeCycleResult:
        result = self.runtime.run(candidates)

        report = RuntimeExecutionReport.from_result(result)

        self.cycle_count += 1

        return RuntimeCycleResult(
            report=report,
        )