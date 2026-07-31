from power_flow_indicator import PowerFlowIndicator, PowerNode


def test_formatted_power() -> None:
    flow = PowerFlowIndicator(
        source=PowerNode.SOLAR,
        target=PowerNode.HOUSE,
        power_kw=4.26,
    )

    assert flow.formatted_power() == "4.3 kW"


def test_custom_precision() -> None:
    flow = PowerFlowIndicator(
        source=PowerNode.BATTERY,
        target=PowerNode.HOUSE,
        power_kw=2.456,
        precision=2,
    )

    assert flow.formatted_power() == "2.46 kW"


def test_direction_label() -> None:
    flow = PowerFlowIndicator(
        source=PowerNode.SOLAR,
        target=PowerNode.HEAT_PUMP,
        power_kw=3.2,
    )

    assert flow.direction_label() == "Solar → Heat Pump"


def test_grid_import() -> None:
    flow = PowerFlowIndicator(
        source=PowerNode.GRID,
        target=PowerNode.HOUSE,
        power_kw=1.8,
    )

    assert flow.is_grid_import() is True
    assert flow.is_grid_export() is False


def test_grid_export() -> None:
    flow = PowerFlowIndicator(
        source=PowerNode.SOLAR,
        target=PowerNode.GRID,
        power_kw=5.1,
    )

    assert flow.is_grid_import() is False
    assert flow.is_grid_export() is True