from heos_ui.runtime import RenderLoop


def test_loop_starts_at_frame_zero() -> None:
    loop = RenderLoop()

    assert loop.frame == 0


def test_tick_advances_frame() -> None:
    loop = RenderLoop()

    loop.tick()

    assert loop.frame == 1


def test_multiple_ticks() -> None:
    loop = RenderLoop()

    for _ in range(5):
        loop.tick()

    assert loop.frame == 5


def test_profiler_records_frames() -> None:
    loop = RenderLoop()

    loop.tick()
    loop.tick()

    assert loop.profiler.snapshot.frame_count == 2


def test_empty_pipeline_renders_zero_widgets() -> None:
    loop = RenderLoop()

    assert loop.tick() == 0