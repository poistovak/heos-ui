from __future__ import annotations

from dataclasses import dataclass

from .heos_application_runtime_loop import HEOSApplicationLoopResult


@dataclass(frozen=True, slots=True)
class HEOSApplicationLoopTelemetry:
    requested: int
    processed: int
    rendered: int
    stopped: bool
    early_stop: bool
    first_cycle: int | None
    last_cycle: int | None

    @property
    def completed(self) -> bool:
        return not self.stopped and self.processed == self.requested

    @property
    def skipped(self) -> int:
        return max(self.requested - self.processed, 0)

    @classmethod
    def capture(
        cls,
        result: HEOSApplicationLoopResult,
        *,
        requested: int,
    ) -> HEOSApplicationLoopTelemetry:
        first_cycle = (
            result.results[0].cycle
            if result.results
            else None
        )
        last_cycle = (
            result.results[-1].cycle
            if result.results
            else None
        )

        rendered = sum(
            item.rendered
            for item in result.results
        )

        return cls(
            requested=requested,
            processed=result.processed,
            rendered=rendered,
            stopped=result.stopped,
            early_stop=result.stopped and result.processed < requested,
            first_cycle=first_cycle,
            last_cycle=last_cycle,
        )
