from heos_ui.templates import EnergyDashboard


def _create_dashboard():
    return EnergyDashboard.create(
        solar_power_w=8200,
        battery_power_w=3100,
        state_of_charge=82,
        house_power_w=2400,
        grid_power_w=-2700,
    )


def test_energy_dashboard_title() -> None:
    dashboard = _create_dashboard()

    assert dashboard.title == "HEOS HOME"


def test_energy_dashboard_has_energy_page() -> None:
    dashboard = _create_dashboard()

    assert dashboard.pages[0].id == "energy"
    assert dashboard.pages[0].title == "Energy"


def test_energy_dashboard_has_two_sections() -> None:
    dashboard = _create_dashboard()

    assert len(dashboard.pages[0].sections) == 2


def test_energy_dashboard_has_production_section() -> None:
    dashboard = _create_dashboard()

    assert dashboard.pages[0].sections[0].title == "Production"


def test_energy_dashboard_has_flow_section() -> None:
    dashboard = _create_dashboard()

    assert dashboard.pages[0].sections[1].title == "Flow"


def test_energy_dashboard_contains_solar_card() -> None:
    dashboard = _create_dashboard()
    cards = dashboard.pages[0].sections[0].cards

    assert cards[0].title == "Solar"
    assert cards[0].value == "8.2 kW"


def test_energy_dashboard_contains_battery_card() -> None:
    dashboard = _create_dashboard()
    cards = dashboard.pages[0].sections[0].cards

    assert cards[1].title == "Battery"
    assert cards[1].value == "82% · 3.1 kW (charging)"


def test_energy_dashboard_contains_grid_card() -> None:
    dashboard = _create_dashboard()
    cards = dashboard.pages[0].sections[0].cards

    assert cards[2].title == "Grid"
    assert cards[2].value == "2.7 kW (export)"


def test_energy_dashboard_contains_flow_card() -> None:
    dashboard = _create_dashboard()
    card = dashboard.pages[0].sections[1].cards[0]

    assert card.title == "Energy Flow"
    assert "solar=8.2 kW" in card.value
    assert "grid=2.7 kW (export)" in card.value
def test_energy_dashboard_zero_values() -> None:
    dashboard = EnergyDashboard.create(
        solar_power_w=0,
        battery_power_w=0,
        state_of_charge=0,
        house_power_w=0,
        grid_power_w=0,
    )

    assert dashboard.title == "HEOS HOME"
    assert len(dashboard.pages) == 1


def test_energy_dashboard_full_battery() -> None:
    dashboard = EnergyDashboard.create(
        solar_power_w=10000,
        battery_power_w=5000,
        state_of_charge=100,
        house_power_w=4000,
        grid_power_w=-1000,
    )

    cards = dashboard.pages[0].sections[0].cards

    assert cards[1].title == "Battery"
    assert "100%" in cards[1].value