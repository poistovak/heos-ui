from heos_ui.layout import Rect
from heos_ui.overlay import OverlayManager
from heos_ui.scene import SceneGraph, SceneNode
from heos_ui.window import WindowManager


def create_manager() -> WindowManager:
    root = SceneNode(
        id="root",
        rect=Rect(
            0.0,
            0.0,
            100.0,
            100.0,
        ),
    )

    return WindowManager(
        scene=SceneGraph(root),
        overlays=OverlayManager(),
    )


def test_initial_state() -> None:
    manager = create_manager()

    assert not manager.running


def test_start() -> None:
    manager = create_manager()

    manager.start()

    assert manager.running


def test_stop() -> None:
    manager = create_manager()

    manager.start()
    manager.stop()

    assert not manager.running


def test_root_exists() -> None:
    manager = create_manager()

    assert manager.root.id == "root"


def test_overlay_count() -> None:
    manager = create_manager()

    assert manager.overlay_count == 0


def test_start_stop_repeatable() -> None:
    manager = create_manager()

    manager.start()
    manager.stop()
    manager.start()

    assert manager.running