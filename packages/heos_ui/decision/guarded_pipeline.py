from __future__ import annotations

from dataclasses import dataclass

from .action_queue import ActionQueue
from .conflict import ConflictResolver, DecisionAction
from .health_guard import HealthAwareDecisionGuard


@dataclass(frozen=True, slots=True)
class BlockedDecision:
    candidate: DecisionAction
    reason: str


@dataclass(frozen=True, slots=True)
class GuardedDecisionResult:
    accepted: tuple[DecisionAction, ...]
    blocked: tuple[BlockedDecision, ...]


@dataclass(slots=True)
class GuardedDecisionPipeline:
    resolver: ConflictResolver
    guard: HealthAwareDecisionGuard
    actions: ActionQueue

    def process(
        self,
        candidates: list[DecisionAction],
    ) -> GuardedDecisionResult:
        resolved = self.resolver.resolve(candidates)

        accepted: list[DecisionAction] = []
        blocked: list[BlockedDecision] = []

        for candidate in resolved:
            guard_result = self.guard.evaluate(candidate)

            if not guard_result.allowed:
                blocked.append(
                    BlockedDecision(
                        candidate=candidate,
                        reason=guard_result.reason,
                    )
                )
                continue

            self.actions.enqueue(candidate.action)
            accepted.append(candidate)

        return GuardedDecisionResult(
            accepted=tuple(accepted),
            blocked=tuple(blocked),
        )