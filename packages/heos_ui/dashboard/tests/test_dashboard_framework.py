from heos_ui.dashboard import (
    Dashboard,
    DashboardCard,
    DashboardPage,
    DashboardRenderer,
    DashboardSection,
)


def test_dashboard_renderer() -> None:
    dashboard = Dashboard(
        title="HEOS HOME",
        pages=(
            DashboardPage(
                id="energy",
                title="Energy",
                sections=(
                    DashboardSection(
                        title="Production",
                        cards=(
                            DashboardCard(
                                title="PV",
                                value="9.8 kW",
                                icon="PV",
                            ),
                            DashboardCard(
                                title="Battery",
                                value="82 %",
                                icon="BAT",
                            ),
                            DashboardCard(
                                title="Grid",
                                value="-2.1 kW",
                                icon="GRID",
                            ),
                        ),
                    ),
                ),
            ),
        ),
    )

    result = DashboardRenderer().render(dashboard)

    assert "HEOS HOME" in result
    assert "[Energy]" in result
    assert "Production" in result
    assert "PV" in result
    assert "9.8 kW" in result
    assert "Battery" in result
    assert "82 %" in result
    assert "Grid" in result
    assert "-2.1 kW" in result


def test_dashboard_models_are_immutable() -> None:
    dashboard = Dashboard(title="HEOS HOME")

    try:
        dashboard.title = "Changed"  # type: ignore[misc]
    except AttributeError:
        pass
    else:
        raise AssertionError("Dashboard must be immutable.")


def test_empty_dashboard_can_be_rendered() -> None:
    dashboard = Dashboard(title="HEOS HOME")

    result = DashboardRenderer().render(dashboard)

    assert "HEOS HOME" in result
    assert result.startswith("╔")
    assert result.endswith("╝")
