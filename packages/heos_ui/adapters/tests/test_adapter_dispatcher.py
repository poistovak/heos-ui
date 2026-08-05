import pytest
from heos_ui.adapters import AdapterDispatcher
from heos_ui.decision import Action


def action(target: str = "wattpilot") -> Action:
    return Action(
        priority=100,
        target=target,
        command="set_current",
        parameters={"amps": 16},
    )


def test_starts_empty() -> None:
    dispatcher = AdapterDispatcher()

    assert dispatcher.adapter_count == 0


def test_register_adapter() -> None:
    dispatcher = AdapterDispatcher()

    dispatcher.register(
        "wattpilot",
        lambda item: item.command,
    )

    assert dispatcher.has_adapter("wattpilot")
    assert dispatcher.adapter_count == 1


def test_dispatch_action() -> None:
    dispatcher = AdapterDispatcher()
    received = []

    dispatcher.register(
        "wattpilot",
        received.append,
    )

    item = action()
    dispatcher.dispatch(item)

    assert received == [item]


def test_dispatch_returns_value() -> None:
    dispatcher = AdapterDispatcher()

    dispatcher.register(
        "wattpilot",
        lambda item: item.parameters["amps"],
    )

    assert dispatcher.dispatch(action()) == 16


def test_unknown_adapter_raises_key_error() -> None:
    dispatcher = AdapterDispatcher()

    with pytest.raises(
        KeyError,
        match="missing",
    ):
        dispatcher.dispatch(
            action("missing")
        )


def test_clear() -> None:
    dispatcher = AdapterDispatcher()

    dispatcher.register(
        "wattpilot",
        lambda item: None,
    )
    dispatcher.clear()

    assert dispatcher.adapter_count == 0
    assert not dispatcher.has_adapter("wattpilot")