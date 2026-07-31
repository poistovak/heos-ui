from heos_ui.dashboard import (
    Dashboard,
    DashboardCard,
    DashboardRenderer,
)

dashboard = Dashboard(
    cards=[
        DashboardCard("PV", "8.4 kW", "☀"),
        DashboardCard("Battery", "83 %", "🔋"),
        DashboardCard("House", "2.7 kW", "⚡"),
        DashboardCard("Grid", "Export", "🌍"),
    ]
)

renderer = DashboardRenderer()

print(renderer.render(dashboard))