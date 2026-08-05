from heos_ui.overlay import (
    Overlay,
    OverlayManager,
)


def test_empty_manager() -> None:
    manager = OverlayManager()

    assert manager.count == 0
    assert manager.top is None


def test_show_overlay() -> None:
    manager = OverlayManager()

    manager.show(
        Overlay("dialog")
    )

    assert manager.count == 1
    assert manager.top.id == "dialog"


def test_hide_overlay() -> None:
    manager = OverlayManager()

    manager.show(
        Overlay("dialog")
    )

    assert manager.hide("dialog")
    assert manager.count == 0


def test_hide_unknown_overlay() -> None:
    manager = OverlayManager()

    assert not manager.hide("missing")


def test_stack_order() -> None:
    manager = OverlayManager()

    manager.show(Overlay("a"))
    manager.show(Overlay("b"))

    assert manager.top.id == "b"


def test_clear() -> None:
    manager = OverlayManager()

    manager.show(Overlay("a"))
    manager.show(Overlay("b"))

    manager.clear()

    assert manager.count == 0


def test_overlays_are_tuple() -> None:
    manager = OverlayManager()

    manager.show(Overlay("dialog"))

    assert isinstance(
        manager.overlays,
        tuple,
    )