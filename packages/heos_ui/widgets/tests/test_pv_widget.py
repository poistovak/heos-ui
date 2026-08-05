from heos_ui.widgets.pv import (
    PVState,
    PVWidget,
)


def test_default_state() -> None:
    widget = PVWidget()

    assert widget.power == 0.0
    assert widget.today_energy == 0.0
    assert not widget.online


def test_update() -> None:
    widget = PVWidget()

    widget.update(
        PVState(
            power=7342.5,
            today_energy=41.8,
            online=True,
        )
    )

    assert widget.power == 7342.5
    assert widget.today_energy == 41.8
    assert widget.online


def test_replace_state() -> None:
    widget = PVWidget()

    widget.update(PVState(1000.0, 5.0))
    widget.update(PVState(2500.0, 12.3))

    assert widget.power == 2500.0
    assert widget.today_energy == 12.3


def test_offline() -> None:
    widget = PVWidget()

    widget.update(
        PVState(
            power=0.0,
            today_energy=0.0,
            online=False,
        )
    )

    assert not widget.online


def test_state_property() -> None:
    widget = PVWidget()

    state = PVState(
        5000.0,
        25.0,
    )

    widget.update(state)

    assert widget.state is state