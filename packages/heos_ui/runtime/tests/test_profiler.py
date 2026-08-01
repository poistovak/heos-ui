from time import sleep

from heos_ui.runtime.profiler import (
    RenderProfiler,
    RenderProfilerSnapshot,
)


def test_profiler_starts_empty() -> None:
    profiler = RenderProfiler()

    assert profiler.snapshot == RenderProfilerSnapshot(
        frame_count=0,
        total_frame_time=0.0,
        average_frame_time=0.0,
        last_frame_time=0.0,
    )


def test_single_frame() -> None:
    profiler = RenderProfiler()

    profiler.begin_frame()
    sleep(0.001)
    elapsed = profiler.end_frame()

    assert elapsed > 0.0
    assert profiler.snapshot.frame_count == 1


def test_average_frame_time() -> None:
    profiler = RenderProfiler()

    for _ in range(3):
        profiler.begin_frame()
        sleep(0.001)
        profiler.end_frame()

    assert profiler.snapshot.frame_count == 3
    assert profiler.snapshot.average_frame_time > 0.0


def test_reset() -> None:
    profiler = RenderProfiler()

    profiler.begin_frame()
    sleep(0.001)
    profiler.end_frame()

    profiler.reset()

    assert profiler.snapshot == RenderProfilerSnapshot(
        frame_count=0,
        total_frame_time=0.0,
        average_frame_time=0.0,
        last_frame_time=0.0,
    )
