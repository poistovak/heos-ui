from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_live_session import HEOSApplicationRunLiveSession


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunLiveSessionStatistics:
    total_runs: int
    completed_runs: int
    interrupted_runs: int
    idle_runs: int
    processed: int
    rendered: int
    skipped: int
    latest_sequence: int | None

    @property
    def active_runs(self) -> int:
        return self.completed_runs + self.interrupted_runs

    @property
    def successful(self) -> bool:
        return (
            self.total_runs > 0
            and self.interrupted_runs == 0
        )

    @property
    def empty(self) -> bool:
        return self.total_runs == 0

    @classmethod
    def capture(
        cls,
        session: HEOSApplicationRunLiveSession,
    ) -> HEOSApplicationRunLiveSessionStatistics:
        history = session.history

        completed_runs = 0
        interrupted_runs = 0
        idle_runs = 0
        processed = 0
        rendered = 0
        skipped = 0

        for item in history:
            report = item.report

            processed += report.processed
            rendered += report.rendered
            skipped += report.skipped

            if report.processed == 0:
                idle_runs += 1
            elif report.completed:
                completed_runs += 1
            else:
                interrupted_runs += 1

        latest_sequence = (
            history[-1].sequence
            if history
            else None
        )

        return cls(
            total_runs=len(history),
            completed_runs=completed_runs,
            interrupted_runs=interrupted_runs,
            idle_runs=idle_runs,
            processed=processed,
            rendered=rendered,
            skipped=skipped,
            latest_sequence=latest_sequence,
        )
