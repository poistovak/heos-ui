import pytest

from heos_ui.widgets import (
    BatteryState,
    FlowWidget,
    PowerDirection,
)


def test_flow_widget_detects_balanced_export_flow() -> None:
    widget = FlowWidget(
        id="energy-flow",
        title="Energy flow",
        solar_power_w=8200,
        house_power_w=2400,
        battery_power_w=3100,
        grid_power_w=-2700,
    )

    assert widget.balance_w == 0
    assert widget.is_balanced is True
    assert widget.battery_state is BatteryState.CHARGING
    assert widget.grid_direction is PowerDirection.EXPORT


def test_flow_widget_detects_balanced_import_flow() -> None:
    widget = FlowWidget(
        id="energy-flow",
        title="Energy flow",
        solar_power_w=500,
        house_power_w=2500,
        battery_power_w=0,
        grid_power_w=2000,
    )

    assert widget.balance_w == 0
    assert widget.is_balanced is True
    assert widget.battery_state is BatteryState.IDLE
    assert widget.grid_direction is PowerDirection.IMPORT


def test_flow_widget_detects_battery_discharge() -> None:
    widget = FlowWidget(
        id="energy-flow",
        title="Energy flow",
        solar_power_w=1000,
        house_power_w=3000,
        battery_power_w=-2000,
        grid_power_w=0,
    )

    assert widget.is_balanced is True
    assert widget.battery_state is BatteryState.DISCHARGING
    assert widget.grid_direction is PowerDirection.IDLE


def test_flow_widget_honours_balance_tolerance() -> None:
    widget = FlowWidget(
        id="energy-flow",
        title="Energy flow",
        solar_power_w=5000,
        house_power_w=4998,
        battery_power_w=0,
        grid_power_w=0,
        balance_tolerance_w=2,
    )

    assert widget.balance_w == 2
    assert widget.is_balanced is True


def test_flow_widget_detects_unbalanced_flow() -> None:
    widget = FlowWidget(
        id="energy-flow",
        title="Energy flow",
        solar_power_w=5000,
        house_power_w=4500,
        battery_power_w=0,
        grid_power_w=0,
        balance_tolerance_w=10,
    )

    assert widget.balance_w == 500
    assert widget.is_balanced is False


def test_flow_widget_renders_energy_flow() -> None:
    widget = FlowWidget(
        id="energy-flow",
        title="Energy flow",
        solar_power_w=8200,
        house_power_w=2400,
        battery_power_w=3100,
        grid_power_w=-2700,
    )

    assert widget.render() == (
        "Energy flow: "
        "solar=8.2 kW, "
        "house=2.4 kW, "
        "battery=3.1 kW (charging), "
        "grid=2.7 kW (export)"
    )


@pytest.mark.parametrize(
    ("field", "value", "message"),
    [
        ("solar_power_w", -1, "Solar power cannot be negative."),
        ("house_power_w", -1, "House power cannot be negative."),
        (
            "balance_tolerance_w",
            -1,
            "Balance tolerance cannot be negative.",
        ),
    ],
)
def test_flow_widget_rejects_invalid_values(
    field: str,
    value: float,
    message: str,
) -> None:
    values = {
        "solar_power_w": 1000,
        "house_power_w": 1000,
        "battery_power_w": 0,
        "grid_power_w": 0,
        "balance_tolerance_w": 1,
    }
    values[field] = value

    with pytest.raises(ValueError, match=message):
        FlowWidget(
            id="energy-flow",
            title="Energy flow",
            **values,
        )