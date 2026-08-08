from __future__ import annotations

from dataclasses import dataclass

from .audit import DecisionAuditRecord, DecisionAuditTrail


@dataclass(frozen=True, slots=True)
class FeedbackSummary:
    target: str
    total: int
    successful: int
    failed: int
    consecutive_failures: int

    @property
    def success_rate(self) -> float:
        if self.total == 0:
            return 0.0

        return self.successful / self.total

    @property
    def healthy(self) -> bool:
        return self.consecutive_failures == 0


class FeedbackEngine:
    """Derive operational feedback from decision outcomes."""

    def __init__(
        self,
        audit: DecisionAuditTrail,
    ) -> None:
        self._audit = audit

    def summarize(
        self,
        target: str,
    ) -> FeedbackSummary:
        records = self._audit.for_target(target)

        successful = sum(
            1
            for record in records
            if record.outcome.success
        )

        failed = len(records) - successful

        return FeedbackSummary(
            target=target,
            total=len(records),
            successful=successful,
            failed=failed,
            consecutive_failures=self._failure_streak(records),
        )

    def should_back_off(
        self,
        target: str,
        *,
        failure_threshold: int = 3,
    ) -> bool:
        if failure_threshold <= 0:
            raise ValueError(
                "failure_threshold must be greater than zero."
            )

        summary = self.summarize(target)

        return (
            summary.consecutive_failures
            >= failure_threshold
        )

    @staticmethod
    def _failure_streak(
        records: tuple[DecisionAuditRecord, ...],
    ) -> int:
        failures = 0

        for record in reversed(records):
            if record.outcome.success:
                break

            failures += 1

        return failures