from dashboard_layout import DashboardLayout


def test_grid_import() -> None:
    layout = DashboardLayout(
        solar_power_kw=5.0,
        battery_soc=80,
        house_power_kw=3.0,
        grid_power_kw=1.2,
    )

    assert layout.is_grid_import() is True
    assert layout.is_grid_export() is False


def test_grid_export() -> None:
    layout = DashboardLayout(
        solar_power_kw=6.0,
        battery_soc=75,
        house_power_kw=2.5,
        grid_power_kw=-3.5,
    )

    assert layout.is_grid_import() is False
    assert layout.is_grid_export() is True


def test_neutral_grid_flow() -> None:
    layout = DashboardLayout(
        solar_power_kw=3.0,
        battery_soc=65,
        house_power_kw=3.0,
        grid_power_kw=0.0,
    )

    assert layout.is_grid_import() is False
    assert layout.is_grid_export() is False


def test_total_local_power_during_import() -> None:
    layout = DashboardLayout(
        solar_power_kw=4.5,
        battery_soc=90,
        house_power_kw=5.0,
        grid_power_kw=0.5,
    )

    assert layout.total_local_power() == 4.5


def test_total_local_power_during_export() -> None:
    layout = DashboardLayout(
        solar_power_kw=4.5,
        battery_soc=90,
        house_power_kw=2.0,
        grid_power_kw=-2.0,
    )

    assert layout.total_local_power() == 6.5