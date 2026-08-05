from heos_ui.widgets.battery import (
    BatteryState,
    BatteryWidget,
)


def test_default_state() -> None:
    widget = BatteryWidget()

    assert widget.soc == 0.0
    assert widget.power == 0.0
    assert widget.capacity == 0.0
    assert not widget.charging
    assert not widget.online


def test_update() -> None:
    widget = BatteryWidget()

    widget.update(
        BatteryState(
            soc=82.5,
            power=4.2,
            capacity=12.8,
            charging=True,
            online=True,
        )
    )

    assert widget.soc == 82.5
    assert widget.power == 4.2
    assert widget.capacity == 12.8
    assert widget.charging
    assert widget.online


def test_replace_state() -> None:
    widget = BatteryWidget()

    widget.update(BatteryState(50.0, 2.0, 10.0, True))
    widget.update(BatteryState(75.0, -3.5, 10.0, False))

    assert widget.soc == 75.0
    assert widget.power == -3.5
    assert not widget.charging


def test_offline() -> None:
    widget = BatteryWidget()

    widget.update(
        BatteryState(
            soc=0.0,
            power=0.0,
            capacity=0.0,
            charging=False,
            online=False,
        )
    )

    assert not widget.online


def test_state_property() -> None:
    widget = BatteryWidget()

    state = BatteryState(
        soc=90.0,
        power=1.5,
        capacity=15.0,
        charging=True,
    )

    widget.update(state)

    assert widget.state is state