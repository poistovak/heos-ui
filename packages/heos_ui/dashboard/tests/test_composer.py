import pytest
from heos_ui.dashboard import DashboardComposer, DashboardRenderer
from heos_ui.widgets import (
    BatteryWidget,
    GridWidget,
    SolarWidget,
    StatusLevel,
    StatusWidget,
)


def test_composer_builds_complete_energy_screen() -> None:
    dashboard = (
        DashboardComposer("HEOS HOME")
        .page("Energy")
        .section("Live power")
        .widget(
            SolarWidget(
                id="solar",
                title="Solar",
                power_w=8200,
            ),
            icon="PV",
        )
        .widget(
            BatteryWidget(
                id="battery",
                title="Battery",
                power_w=3100,
                state_of_charge=82,
            ),
            icon="BAT",
        )
        .widget(
            GridWidget(
                id="grid",
                title="Grid",
                power_w=-2700,
            ),
            icon="GRID",
        )
        .build()
    )

    assert dashboard.title == "HEOS HOME"
    assert len(dashboard.pages) == 1

    page = dashboard.pages[0]
    assert page.id == "energy"
    assert page.title == "Energy"

    section = page.sections[0]
    assert section.title == "Live power"
    assert len(section.cards) == 3

    assert section.cards[0].title == "Solar"
    assert section.cards[0].value == "8.2 kW"
    assert section.cards[0].icon == "PV"

    assert section.cards[1].title == "Battery"
    assert section.cards[1].value == "82% · 3.1 kW (charging)"

    assert section.cards[2].title == "Grid"
    assert section.cards[2].value == "2.7 kW (export)"


def test_composer_builds_multiple_pages() -> None:
    dashboard = (
        DashboardComposer("HEOS HOME")
        .page("Energy")
        .section("Power")
        .widget(
            SolarWidget(
                id="solar",
                title="Solar",
                power_w=5000,
            )
        )
        .page("System Status")
        .section("Devices")
        .widget(
            StatusWidget(
                id="inverter",
                title="Inverter",
                status="Online",
                level=StatusLevel.SUCCESS,
            )
        )
        .build()
    )

    assert len(dashboard.pages) == 2
    assert dashboard.pages[0].id == "energy"
    assert dashboard.pages[1].id == "system-status"


def test_composer_supports_custom_page_id() -> None:
    dashboard = (
        DashboardComposer("HEOS")
        .page("Electric vehicle", page_id="ev")
        .section("Charging")
        .build()
    )

    assert dashboard.pages[0].id == "ev"


def test_composed_dashboard_can_be_rendered() -> None:
    dashboard = (
        DashboardComposer("HEOS HOME")
        .page("Energy")
        .section("Production")
        .widget(
            SolarWidget(
                id="solar",
                title="Solar",
                power_w=8400,
            )
        )
        .build()
    )

    result = DashboardRenderer().render(dashboard)

    assert "HEOS HOME" in result
    assert "[Energy]" in result
    assert "Production" in result
    assert "Solar" in result
    assert "8.4 kW" in result


def test_composer_requires_page_before_section() -> None:
    composer = DashboardComposer("HEOS")

    with pytest.raises(
        RuntimeError,
        match="A page must be created before adding a section.",
    ):
        composer.section("Production")


def test_composer_requires_section_before_widget() -> None:
    composer = DashboardComposer("HEOS").page("Energy")

    with pytest.raises(
        RuntimeError,
        match="A section must be created before adding a widget.",
    ):
        composer.widget(
            SolarWidget(
                id="solar",
                title="Solar",
                power_w=5000,
            )
        )


@pytest.mark.parametrize(
    ("action", "message"),
    [
        ("dashboard", "Dashboard title cannot be empty."),
        ("page", "Page title cannot be empty."),
        ("section", "Section title cannot be empty."),
    ],
)
def test_composer_rejects_empty_titles(
    action: str,
    message: str,
) -> None:
    with pytest.raises(ValueError, match=message):
        if action == "dashboard":
            DashboardComposer(" ")
        elif action == "page":
            DashboardComposer("HEOS").page(" ")
        else:
            DashboardComposer("HEOS").page("Energy").section(" ")


def test_composer_cannot_be_reused_after_build() -> None:
    composer = (
        DashboardComposer("HEOS")
        .page("Energy")
        .section("Production")
    )

    composer.build()

    with pytest.raises(
        RuntimeError,
        match="Dashboard composer has already been built.",
    ):
        composer.page("Climate")