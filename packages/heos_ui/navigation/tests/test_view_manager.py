from heos_ui.layout import VerticalLayout
from heos_ui.navigation import ViewManager
from heos_ui.views import DashboardView


def test_view_manager_switch() -> None:
    manager = ViewManager()

    home = DashboardView(
        title="Home",
        layout=VerticalLayout(),
    )

    energy = DashboardView(
        title="Energy",
        layout=VerticalLayout(),
    )

    manager.register("home", home)
    manager.register("energy", energy)

    assert manager.active_view.title == "Home"

    manager.activate("energy")

    assert manager.active_view.title == "Energy"