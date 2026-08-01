from heos_ui.runtime import FrameClock


def test_clock_starts_at_zero() -> None:
    clock = FrameClock()

    assert clock.frame == 0


def test_tick_increments_frame() -> None:
    clock = FrameClock()

    assert clock.tick() == 1
    assert clock.tick() == 2
    assert clock.tick() == 3


def test_reset() -> None:
    clock = FrameClock()

    clock.tick()
    clock.tick()

    clock.reset()

    assert clock.frame == 0


def test_tick_after_reset() -> None:
    clock = FrameClock()

    clock.tick()
    clock.reset()

    assert clock.tick() == 1


def test_many_ticks() -> None:
    clock = FrameClock()

    for _ in range(100):
        clock.tick()

    assert clock.frame == 100