from heos_ui.input import (
    InputDispatcher,
    InputEvent,
)


def test_register_handler() -> None:
    dispatcher = InputDispatcher()

    called = []

    dispatcher.register(
        "click",
        lambda event: called.append(event.target),
    )

    dispatcher.dispatch(
        InputEvent(
            "click",
            "button",
        )
    )

    assert called == ["button"]


def test_unknown_event() -> None:
    dispatcher = InputDispatcher()

    count = dispatcher.dispatch(
        InputEvent(
            "hover",
            "widget",
        )
    )

    assert count == 0


def test_multiple_handlers() -> None:
    dispatcher = InputDispatcher()

    calls = []

    dispatcher.register(
        "click",
        lambda event: calls.append(1),
    )

    dispatcher.register(
        "click",
        lambda event: calls.append(2),
    )

    count = dispatcher.dispatch(
        InputEvent(
            "click",
            "widget",
        )
    )

    assert count == 2
    assert calls == [1, 2]


def test_registered_events() -> None:
    dispatcher = InputDispatcher()

    dispatcher.register(
        "click",
        lambda event: None,
    )

    dispatcher.register(
        "drag",
        lambda event: None,
    )

    assert dispatcher.registered_events == (
        "click",
        "drag",
    )


def test_dispatch_repeatable() -> None:
    dispatcher = InputDispatcher()

    total = []

    dispatcher.register(
        "tap",
        lambda event: total.append(event.target),
    )

    dispatcher.dispatch(
        InputEvent(
            "tap",
            "a",
        )
    )

    dispatcher.dispatch(
        InputEvent(
            "tap",
            "b",
        )
    )

    assert total == [
        "a",
        "b",
    ]