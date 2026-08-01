from heos_ui.runtime import (
    RenderDiagnostics,
    RenderMetrics,
    RenderProfilerSnapshot,
    RenderStatistics,
)


def test_diagnostics_snapshot() -> None:
    diagnostics = RenderDiagnostics(
        statistics=RenderStatistics(
            attempted=12,
            rendered=9,
            skipped=3,
            batches=4,
        ),
        metrics=RenderMetrics(
            frames=4,
            rendered_widgets=9,
            skipped_widgets=3,
        ),
        profiler=RenderProfilerSnapshot(
            frame_count=4,
            total_frame_time=6.4,
            average_frame_time=1.6,
            last_frame_time=1.4,
        ),
    )

    assert diagnostics.rendered_frames == 4
    assert diagnostics.total_widgets == 12


def test_metrics_reference() -> None:
    metrics = RenderMetrics(
        frames=2,
        rendered_widgets=5,
        skipped_widgets=1,
    )

    diagnostics = RenderDiagnostics(
        statistics=RenderStatistics(
            attempted=6,
            rendered=5,
            skipped=1,
            batches=2,
        ),
        metrics=metrics,
        profiler=RenderProfilerSnapshot(
            frame_count=2,
            total_frame_time=3.2,
            average_frame_time=1.6,
            last_frame_time=1.5,
        ),
    )

    assert diagnostics.metrics is metrics


def test_statistics_reference() -> None:
    statistics = RenderStatistics(
        attempted=1,
        rendered=1,
        skipped=0,
        batches=1,
    )

    diagnostics = RenderDiagnostics(
        statistics=statistics,
        metrics=RenderMetrics(
            frames=1,
            rendered_widgets=1,
            skipped_widgets=0,
        ),
        profiler=RenderProfilerSnapshot(
            frame_count=1,
            total_frame_time=1.0,
            average_frame_time=1.0,
            last_frame_time=1.0,
        ),
    )

    assert diagnostics.statistics is statistics


def test_profiler_reference() -> None:
    profiler = RenderProfilerSnapshot(
        frame_count=3,
        total_frame_time=5.0,
        average_frame_time=1.67,
        last_frame_time=1.5,
    )

    diagnostics = RenderDiagnostics(
        statistics=RenderStatistics(
            attempted=8,
            rendered=6,
            skipped=2,
            batches=3,
        ),
        metrics=RenderMetrics(
            frames=3,
            rendered_widgets=6,
            skipped_widgets=2,
        ),
        profiler=profiler,
    )

    assert diagnostics.profiler is profiler