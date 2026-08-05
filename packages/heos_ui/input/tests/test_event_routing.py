from heos_ui.input import InputEvent
from heos_ui.input.routing import EventRouter


def test_register_route() -> None:
    router = EventRouter()

    called = []

    router.register(
        "battery",
        lambda event: called.append(event.target),
    )

    assert router.route(
        InputEvent(
            "click",
            "battery",
        )
    )

    assert called == ["battery"]


def test_unknown_target() -> None:
    router = EventRouter()

    assert not router.route(
        InputEvent(
            "click",
            "missing",
        )
    )


def test_unregister() -> None:
    router = EventRouter()

    router.register(
        "battery",
        lambda event: None,
    )

    router.unregister("battery")

    assert not router.route(
        InputEvent(
            "click",
            "battery",
        )
    )


def test_registered_widgets() -> None:
    router = EventRouter()

    router.register("battery", lambda event: None)
    router.register("solar", lambda event: None)

    assert router.registered_widgets == (
        "battery",
        "solar",
    )


def test_replace_handler() -> None:
    router = EventRouter()

    result = []

    router.register(
        "battery",
        lambda event: result.append(1),
    )

    router.register(
        "battery",
        lambda event: result.append(2),
    )

    router.route(
        InputEvent(
            "click",
            "battery",
        )
    )

    assert result == [2]