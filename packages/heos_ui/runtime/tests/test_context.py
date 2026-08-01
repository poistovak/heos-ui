from heos_ui.runtime import (
    FrameClock,
    RenderContext,
    RenderDiagnostics,
    RenderLifecycle,
    RenderMetrics,
    RenderProfilerSnapshot,
    RenderStatistics,
)


def create_context() -> RenderContext:
    return RenderContext(
        clock=FrameClock(frame=8),
        lifecycle=RenderLifecycle(
            frame=8,
            active=True,
        ),
        diagnostics=RenderDiagnostics(
            statistics=RenderStatistics(
                attempted=12,
                rendered=10,
                skipped=2,
                batches=4,
            ),
            metrics=RenderMetrics(
                frames=8,
                rendered_widgets=10,
                skipped_widgets=2,
            ),
            profiler=RenderProfilerSnapshot(
                frame_count=8,
                total_frame_time=10.4,
                average_frame_time=1.3,
                last_frame_time=1.2,
            ),
        ),
    )


def test_frame() -> None:
    assert create_context().frame == 8


def test_active() -> None:
    assert create_context().active is True


def test_clock_reference() -> None:
    assert create_context().clock.frame == 8


def test_lifecycle_reference() -> None:
    assert create_context().lifecycle.active is True


def test_diagnostics_reference() -> None:
    assert create_context().diagnostics.metrics.frames == 8


def test_statistics_reference() -> None:
    assert create_context().diagnostics.statistics.rendered == 10