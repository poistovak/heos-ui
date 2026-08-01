import pytest

from heos_ui.widgets import (
    BatteryState,
    BatteryWidget,
    GridWidget,
    PowerDirection,
    PowerWidget,
    SolarWidget,
)


def test_power_widget_renders_watts() -> None:
    widget = PowerWidget(
        id="house-power",
        title="House",
        power_w=850,
    )

    assert widget.power_kw == 0.85
    assert widget.render() == "House: 850 W"


def test_power_widget_renders_kilowatts() -> None:
    widget = PowerWidget(
        id="house-power",
        title="House",
        power_w=8400,
    )

    assert widget.power_kw == 8.4
    assert widget.render() == "House: 8.4 kW"


def test_solar_widget_rejects_negative_power() -> None:
    with pytest.raises(
        ValueError,
        match="Solar power cannot be negative.",
    ):
        SolarWidget(
            id="solar-power",
            title="Solar",
            power_w=-1,
        )


@pytest.mark.parametrize(
    ("power_w", "direction"),
    [
        (2500, PowerDirection.IMPORT),
        (-2500, PowerDirection.EXPORT),
        (0, PowerDirection.IDLE),
    ],
)
def test_grid_widget_detects_direction(
    power_w: float,
    direction: PowerDirection,
) -> None:
    widget = GridWidget(
        id="grid-power",
        title="Grid",
        power_w=power_w,
    )

    assert widget.direction is direction


def test_grid_widget_renders_export_without_negative_value() -> None:
    widget = GridWidget(
        id="grid-power",
        title="Grid",
        power_w=-2100,
    )

    assert widget.render() == "Grid: 2.1 kW (export)"


@pytest.mark.parametrize(
    ("power_w", "state"),
    [
        (1800, BatteryState.CHARGING),
        (-1800, BatteryState.DISCHARGING),
        (0, BatteryState.IDLE),
    ],
)
def test_battery_widget_detects_state(
    power_w: float,
    state: BatteryState,
) -> None:
    widget = BatteryWidget(
        id="battery",
        title="Battery",
        power_w=power_w,
        state_of_charge=82,
    )

    assert widget.state is state


def test_battery_widget_renders_state() -> None:
    widget = BatteryWidget(
        id="battery",
        title="Battery",
        power_w=1800,
        state_of_charge=82,
    )

    assert widget.render() == "Battery: 82% · 1.8 kW (charging)"


@pytest.mark.parametrize("state_of_charge", [-1, 101])
def test_battery_widget_rejects_invalid_state_of_charge(
    state_of_charge: float,
) -> None:
    with pytest.raises(
        ValueError,
        match="Battery state of charge must be between 0 and 100.",
    ):
        BatteryWidget(
            id="battery",
            title="Battery",
            power_w=0,
            state_of_charge=state_of_charge,
        )