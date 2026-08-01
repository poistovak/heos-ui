from __future__ import annotations

from heos_ui.dashboard import DashboardComposer
from heos_ui.widgets import WidgetFactory


class EnergyDashboard:
    """Standard HEOS Energy dashboard."""

    @staticmethod
    def create(
        *,
        solar_power_w: float,
        battery_power_w: float,
        state_of_charge: float,
        house_power_w: float,
        grid_power_w: float,
    ):
        return (
            DashboardComposer("HEOS HOME")
            .page("Energy")
            .section("Production")
            .widget(WidgetFactory.solar(solar_power_w))
            .widget(
                WidgetFactory.battery(
                    battery_power_w,
                    state_of_charge,
                )
            )
            .widget(
                WidgetFactory.grid(
                    grid_power_w,
                )
            )
            .section("Flow")
            .widget(
                WidgetFactory.flow(
                    solar_power_w=solar_power_w,
                    house_power_w=house_power_w,
                    battery_power_w=battery_power_w,
                    grid_power_w=grid_power_w,
                )
            )
            .build()
        )