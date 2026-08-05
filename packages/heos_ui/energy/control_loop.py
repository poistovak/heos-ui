from __future__ import annotations

from dataclasses import dataclass

from heos_ui.adapters import AdapterDispatcher
from heos_ui.decision import Action, ActionQueue, Decision, DecisionPlanner
from heos_ui.execution import ExecutionEngine


@dataclass(frozen=True, slots=True)
class ControlResult:
    decision: Decision | None
    action: Action | None
    executed: bool
    result: object | None = None


@dataclass(slots=True)
class EnergyControlLoop:
    planner: DecisionPlanner
    actions: ActionQueue
    execution: ExecutionEngine
    dispatcher: AdapterDispatcher

    def submit(
        self,
        decision: Decision,
        action: Action,
    ) -> None:
        self.planner.add(decision)
        self.actions.enqueue(action)

    def run_once(self) -> ControlResult:
        decision = self.planner.next()
        action = self.actions.dequeue()

        if decision is None or action is None:
            return ControlResult(
                decision=decision,
                action=action,
                executed=False,
            )

        if decision.target != action.target:
            raise ValueError(
                "Decision target and action target must match."
            )

        if not self.execution.has_handler(action.target):
            self.execution.register(
                action.target,
                self.dispatcher.dispatch,
            )

        result = self.execution.execute(action)

        return ControlResult(
            decision=decision,
            action=action,
            executed=True,
            result=result,
        )

    @property
    def pending(self) -> int:
        return max(
            self.planner.count,
            self.actions.count,
        )

    def clear(self) -> None:
        self.planner.clear()
        self.actions.clear()