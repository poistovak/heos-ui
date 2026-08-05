from heos_ui.widgets.house import (
    HouseState,
    HouseWidget,
)


def test_default_state() -> None:
    widget = HouseWidget()

    assert widget.power == 0.0
    assert widget.today_energy == 0.0
    assert not widget.online


def test_update() -> None:
    widget = HouseWidget()

    widget.update(
        HouseState(
            power=2350.0,
            today_energy=14.8,
            online=True,
        )
    )

    assert widget.power == 2350.0
    assert widget.today_energy == 14.8
    assert widget.online


def test_replace_state() -> None:
    widget = HouseWidget()

    widget.update(
        HouseState(
            power=1200.0,
            today_energy=6.0,
        )
    )
    widget.update(
        HouseState(
            power=3100.0,
            today_energy=18.5,
        )
    )

    assert widget.power == 3100.0
    assert widget.today_energy == 18.5


def test_offline() -> None:
    widget = HouseWidget()

    widget.update(
        HouseState(
            power=0.0,
            today_energy=0.0,
            online=False,
        )
    )

    assert not widget.online


def test_state_property() -> None:
    widget = HouseWidget()

    state = HouseState(
        power=1800.0,
        today_energy=9.5,
    )

    widget.update(state)

    assert widget.state is state