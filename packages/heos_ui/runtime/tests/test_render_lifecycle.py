import pytest
from heos_ui.runtime import RenderLifecycle


def test_lifecycle_starts_idle() -> None:
    lifecycle = RenderLifecycle()

    assert lifecycle.frame == 0
    assert lifecycle.active is False


def test_begin_activates_frame() -> None:
    lifecycle = RenderLifecycle()

    assert lifecycle.begin() == 1
    assert lifecycle.active is True


def test_end_deactivates_frame() -> None:
    lifecycle = RenderLifecycle()

    lifecycle.begin()
    lifecycle.end()

    assert lifecycle.active is False


def test_nested_begin_is_rejected() -> None:
    lifecycle = RenderLifecycle()

    lifecycle.begin()

    with pytest.raises(
        RuntimeError,
        match="Render frame already active.",
    ):
        lifecycle.begin()


def test_end_without_begin_is_rejected() -> None:
    lifecycle = RenderLifecycle()

    with pytest.raises(
        RuntimeError,
        match="No active render frame.",
    ):
        lifecycle.end()


def test_reset() -> None:
    lifecycle = RenderLifecycle()

    lifecycle.begin()
    lifecycle.end()
    lifecycle.reset()

    assert lifecycle.frame == 0
    assert lifecycle.active is False