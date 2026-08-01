from heos_ui.layout import Rect
from heos_ui.scene import SceneNode
from heos_ui.scene.render_queue import RenderQueue


def node(name: str) -> SceneNode:
    return SceneNode(
        id=name,
        rect=Rect(
            0.0,
            0.0,
            100.0,
            100.0,
        ),
    )


def test_queue_starts_empty() -> None:
    queue = RenderQueue()

    assert queue.empty
    assert queue.size == 0


def test_push() -> None:
    queue = RenderQueue()

    queue.push(node("solar"))

    assert queue.size == 1


def test_pop_fifo() -> None:
    queue = RenderQueue()

    queue.push(node("a"))
    queue.push(node("b"))

    assert queue.pop().id == "a"
    assert queue.pop().id == "b"


def test_extend() -> None:
    queue = RenderQueue()

    queue.extend(
        [
            node("a"),
            node("b"),
            node("c"),
        ]
    )

    assert queue.size == 3


def test_clear() -> None:
    queue = RenderQueue()

    queue.push(node("a"))
    queue.clear()

    assert queue.empty


def test_iteration() -> None:
    queue = RenderQueue()

    queue.extend(
        [
            node("x"),
            node("y"),
        ]
    )

    assert [item.id for item in queue] == [
        "x",
        "y",
    ]
