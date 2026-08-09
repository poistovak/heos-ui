from __future__ import annotations

from dataclasses import dataclass

from .heos_application_run_live_session import HEOSApplicationRunLiveSession
from .heos_application_run_live_session_statistics import (
    HEOSApplicationRunLiveSessionStatistics,
)
from .heos_application_run_session_health import (
    HEOSApplicationRunSessionHealthSummary,
)
from .heos_application_run_session_presenter import (
    HEOSApplicationRunSessionHealthPresenter,
    HEOSApplicationRunSessionPresentation,
)


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionHealthPipelineResult:
    statistics: HEOSApplicationRunLiveSessionStatistics
    summary: HEOSApplicationRunSessionHealthSummary
    presentation: HEOSApplicationRunSessionPresentation


@dataclass(frozen=True, slots=True)
class HEOSApplicationRunSessionHealthPipeline:
    presenter: HEOSApplicationRunSessionHealthPresenter

    @classmethod
    def create(cls) -> HEOSApplicationRunSessionHealthPipeline:
        return cls(
            presenter=HEOSApplicationRunSessionHealthPresenter(),
        )

    def evaluate(
        self,
        session: HEOSApplicationRunLiveSession,
    ) -> HEOSApplicationRunSessionHealthPipelineResult:
        statistics = HEOSApplicationRunLiveSessionStatistics.capture(
            session
        )
        summary = HEOSApplicationRunSessionHealthSummary.from_statistics(
            statistics
        )
        presentation = self.presenter.present(summary)

        return HEOSApplicationRunSessionHealthPipelineResult(
            statistics=statistics,
            summary=summary,
            presentation=presentation,
        )
