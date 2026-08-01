from __future__ import annotations

from .energy import BatteryWidget, GridWidget, SolarWidget
from .flow import FlowWidget
from .status import StatusLevel, StatusWidget


class WidgetFactory:
    """Factory creating standard HEOS widgets."""

    @staticmethod
    def solar(power_w: float) -> SolarWidget:
        return SolarWidget(
            id="solar",
            title="Solar",
            power_w=power_w,
        )

    @staticmethod
    def battery(
        power_w: float,
        state_of_charge: float,
    ) -> BatteryWidget:
        return BatteryWidget(
            id="battery",
            title="Battery",
            power_w=power_w,
            state_of_charge=state_of_charge,
        )

    @staticmethod
    def grid(power_w: float) -> GridWidget:
        return GridWidget(
            id="grid",
            title="Grid",
            power_w=power_w,
        )

    @staticmethod
    def flow(
        solar_power_w: float,
        house_power_w: float,
        battery_power_w: float,
        grid_power_w: float,
    ) -> FlowWidget:
        return FlowWidget(
            id="flow",
            title="Energy Flow",
            solar_power_w=solar_power_w,
            house_power_w=house_power_w,
            battery_power_w=battery_power_w,
            grid_power_w=grid_power_w,
        )

    @staticmethod
    def status(
        title: str,
        status: str,
        level: StatusLevel = StatusLevel.INFO,
    ) -> StatusWidget:
        return StatusWidget(
            id=title.lower().replace(" ", "-"),
            title=title,
            status=status,
            level=level,
        )
