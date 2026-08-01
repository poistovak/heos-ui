from heos_ui.widgets import (
    BatteryWidget,
    FlowWidget,
    GridWidget,
    SolarWidget,
    StatusLevel,
    StatusWidget,
    WidgetFactory,
)


def test_factory_creates_solar_widget() -> None:
    widget = WidgetFactory.solar(8400)

    assert isinstance(widget, SolarWidget)
    assert widget.power_w == 8400


def test_factory_creates_battery_widget() -> None:
    widget = WidgetFactory.battery(
        power_w=1800,
        state_of_charge=82,
    )

    assert isinstance(widget, BatteryWidget)
    assert widget.state_of_charge == 82


def test_factory_creates_grid_widget() -> None:
    widget = WidgetFactory.grid(-2100)

    assert isinstance(widget, GridWidget)
    assert widget.power_w == -2100


def test_factory_creates_flow_widget() -> None:
    widget = WidgetFactory.flow(
        solar_power_w=8200,
        house_power_w=2400,
        battery_power_w=3100,
        grid_power_w=-2700,
    )

    assert isinstance(widget, FlowWidget)
    assert widget.is_balanced


def test_factory_creates_status_widget() -> None:
    widget = WidgetFactory.status(
        title="Inverter",
        status="Online",
        level=StatusLevel.SUCCESS,
    )

    assert isinstance(widget, StatusWidget)
    assert widget.level is StatusLevel.SUCCESS