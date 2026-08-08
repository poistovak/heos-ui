from __future__ import annotations

from dataclasses import dataclass

from heos_ui.execution import ExecutionEngine

from .action_queue import ActionQueue
from .conflict import DecisionAction
from .guarded_pipeline import (
    GuardedDecisionPipeline,
    GuardedDecisionResult,
)


@dataclass(frozen=True, slots=True)
class DecisionRuntimeResult:
    guarded: GuardedDecisionResult
    executed: int


@dataclass(slots=True)
class DecisionRuntime:
    pipeline: GuardedDecisionPipeline
    actions: ActionQueue
    execution: ExecutionEngine

    def run(
        self,
        candidates: list[DecisionAction],
    ) -> DecisionRuntimeResult:
        guarded = self.pipeline.process(candidates)

        executed = 0

        while self.actions.count:
            action = self.actions.dequeue()

            if action is None:
                break

            self.execution.execute(action)
            executed += 1

        return DecisionRuntimeResult(
            guarded=guarded,
            executed=executed,
        )