from heos_ui.dashboard.layout import DashboardLayout
from heos_ui.dashboard.runtime import DashboardRuntime
from heos_ui.layout import Rect
from heos_ui.scene import SceneGraph, SceneNode


def create_runtime() -> DashboardRuntime:
    scene = SceneGraph(
        SceneNode(
            id="root",
            rect=Rect(
                0,
                0,
                1920,
                1080,
            ),
        )
    )

    return DashboardRuntime.create(
        DashboardLayout(),
        scene,
    )


def test_runtime_created() -> None:
    runtime = create_runtime()

    assert runtime.layout is not None


def test_runtime_running() -> None:
    runtime = create_runtime()

    runtime.start()

    assert runtime.running


def test_runtime_stop() -> None:
    runtime = create_runtime()

    runtime.start()
    runtime.stop()

    assert not runtime.running


def test_runtime_has_window() -> None:
    runtime = create_runtime()

    assert runtime.window.root.id == "root"


def test_overlay_manager_exists() -> None:
    runtime = create_runtime()

    assert runtime.window.overlay_count == 0