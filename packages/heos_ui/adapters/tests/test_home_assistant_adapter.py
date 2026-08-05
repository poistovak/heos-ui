from heos_ui.adapters import (
    HomeAssistantAdapter,
    HomeAssistantSnapshot,
)


def test_builds_core_graph() -> None:
    graph = HomeAssistantAdapter().build_graph(
        HomeAssistantSnapshot()
    )

    assert graph.node("pv") is not None
    assert graph.node("house") is not None
    assert graph.node("grid") is not None


def test_pv_supplies_house() -> None:
    graph = HomeAssistantAdapter().build_graph(
        HomeAssistantSnapshot(
            pv_power=5000.0,
            house_power=3000.0,
        )
    )

    flows = graph.outgoing("pv")

    assert len(flows) == 2
    assert flows[0].destination == "house"
    assert flows[0].power == 3000.0
    assert flows[1].destination == "grid"
    assert flows[1].power == 2000.0


def test_grid_import_supplies_house() -> None:
    graph = HomeAssistantAdapter().build_graph(
        HomeAssistantSnapshot(
            house_power=3200.0,
            grid_power=3200.0,
        )
    )

    flows = graph.outgoing("grid")

    assert len(flows) == 1
    assert flows[0].destination == "house"
    assert flows[0].power == 3200.0


def test_battery_charging_uses_surplus() -> None:
    graph = HomeAssistantAdapter().build_graph(
        HomeAssistantSnapshot(
            pv_power=6000.0,
            house_power=2000.0,
            battery_power=2500.0,
            battery_online=True,
        )
    )

    flows = graph.incoming("battery")

    assert len(flows) == 1
    assert flows[0].source == "pv"
    assert flows[0].power == 2500.0


def test_battery_discharge_supplies_house() -> None:
    graph = HomeAssistantAdapter().build_graph(
        HomeAssistantSnapshot(
            house_power=2500.0,
            battery_power=-1800.0,
            battery_online=True,
        )
    )

    flows = graph.outgoing("battery")

    assert len(flows) == 1
    assert flows[0].destination == "house"
    assert flows[0].power == 1800.0


def test_optional_devices_are_added() -> None:
    graph = HomeAssistantAdapter().build_graph(
        HomeAssistantSnapshot(
            ev_online=True,
            heat_pump_online=True,
            battery_online=True,
        )
    )

    assert graph.node("ev") is not None
    assert graph.node("heat_pump") is not None
    assert graph.node("battery") is not None


def test_pv_supplies_ev_and_heat_pump() -> None:
    graph = HomeAssistantAdapter().build_graph(
        HomeAssistantSnapshot(
            pv_power=7000.0,
            house_power=6500.0,
            ev_power=3500.0,
            heat_pump_power=2000.0,
            ev_online=True,
            heat_pump_online=True,
        )
    )

    assert graph.incoming_power("heat_pump") == 2000.0
    assert graph.incoming_power("ev") == 3500.0