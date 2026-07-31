from heos_ui.dashboard import DashboardBuilder


def test_builder_creates_dashboard() -> None:
    dashboard = (
        DashboardBuilder("HEOS HOME")
        .page("Energy")
        .section("Production")
        .card("PV", "9.8 kW")
        .card("Battery", "82 %")
        .build()
    )

    assert dashboard.title == "HEOS HOME"

    page = dashboard.pages[0]
    assert page.title == "Energy"

    section = page.sections[0]
    assert section.title == "Production"

    assert len(section.cards) == 2
    assert section.cards[0].title == "PV"
    assert section.cards[1].title == "Battery"


def test_builder_multiple_sections() -> None:
    dashboard = (
        DashboardBuilder("HEOS")
        .page("Energy")
        .section("Production")
        .card("PV", "10")
        .section("Consumption")
        .card("House", "4")
        .build()
    )

    page = dashboard.pages[0]

    assert len(page.sections) == 2
    assert page.sections[0].title == "Production"
    assert page.sections[1].title == "Consumption"