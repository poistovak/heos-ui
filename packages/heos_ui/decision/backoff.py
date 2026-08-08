from __future__ import annotations

from dataclasses import dataclass

from .feedback import FeedbackEngine


@dataclass(frozen=True, slots=True)
class BackoffDecision:
    target: str
    blocked: bool
    failure_streak: int
    threshold: int


@dataclass(slots=True)
class BackoffPolicy:
    feedback: FeedbackEngine
    failure_threshold: int = 3

    def __post_init__(self) -> None:
        if self.failure_threshold <= 0:
            raise ValueError(
                "failure_threshold must be greater than zero."
            )

    def evaluate(
        self,
        target: str,
    ) -> BackoffDecision:
        summary = self.feedback.summarize(target)

        return BackoffDecision(
            target=target,
            blocked=(
                summary.consecutive_failures
                >= self.failure_threshold
            ),
            failure_streak=summary.consecutive_failures,
            threshold=self.failure_threshold,
        )

    def allows(
        self,
        target: str,
    ) -> bool:
        return not self.evaluate(target).blocked