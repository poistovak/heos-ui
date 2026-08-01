from heos_ui.runtime import (
    RenderDiagnostics,
    RenderLifecycle,
    RenderMetrics,
    RenderProfilerSnapshot,
    RenderStatistics,
    RuntimeSnapshot,
)


def create_snapshot() -> RuntimeSnapshot:
    return RuntimeSnapshot(
        diagnostics=RenderDiagnostics(
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
        ),
        lifecycle=RenderLifecycle(
            frame=4,
            active=False,
        ),
    )


def test_snapshot_frame() -> None:
    assert create_snapshot().frame == 4


def test_snapshot_active() -> None:
    assert create_snapshot().active is False


def test_snapshot_rendered_frames() -> None:
    assert create_snapshot().rendered_frames == 4


def test_snapshot_total_widgets() -> None:
    assert create_snapshot().total_widgets == 12


def test_snapshot_statistics_reference() -> None:
    snapshot = create_snapshot()

    assert snapshot.diagnostics.statistics.rendered == 9


def test_snapshot_profiler_reference() -> None:
    snapshot = create_snapshot()

    assert snapshot.diagnostics.profiler.frame_count == 4