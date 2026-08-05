from heos_ui.widgets.heatpump import (
    HeatPumpState,
    HeatPumpWidget,
)


def test_default_state() -> None:
    widget = HeatPumpWidget()

    assert widget.mode == "offline"
    assert widget.outdoor_temperature == 0.0
    assert widget.water_temperature == 0.0
    assert widget.compressor_power == 0.0
    assert not widget.compressor_running
    assert not widget.online


def test_update() -> None:
    widget = HeatPumpWidget()

    widget.update(
        HeatPumpState(
            mode="heating",
            outdoor_temperature=4.5,
            water_temperature=34.0,
            compressor_power=2.35,
            compressor_running=True,
        )
    )

    assert widget.mode == "heating"
    assert widget.outdoor_temperature == 4.5
    assert widget.water_temperature == 34.0
    assert widget.compressor_power == 2.35
    assert widget.compressor_running
    assert widget.online


def test_replace_state() -> None:
    widget = HeatPumpWidget()

    widget.update(
        HeatPumpState(
            "heating",
            2.0,
            35.0,
            2.1,
            True,
        )
    )

    widget.update(
        HeatPumpState(
            "dhw",
            6.0,
            50.0,
            2.8,
            True,
        )
    )

    assert widget.mode == "dhw"
    assert widget.water_temperature == 50.0


def test_offline() -> None:
    widget = HeatPumpWidget()

    widget.update(
        HeatPumpState(
            mode="offline",
            outdoor_temperature=0.0,
            water_temperature=0.0,
            compressor_power=0.0,
            compressor_running=False,
            online=False,
        )
    )

    assert not widget.online


def test_state_property() -> None:
    widget = HeatPumpWidget()

    state = HeatPumpState(
        "cooling",
        28.0,
        18.0,
        1.9,
        True,
    )

    widget.update(state)

    assert widget.state is state