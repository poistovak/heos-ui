from heos_ui.layout import VerticalLayout
from heos_ui.views import DashboardView


def test_dashboard_view() -> None:
    layout = VerticalLayout()

    view = DashboardView(
        title="Home",
        layout=layout,
    )

    assert view.title == "Home"
    assert view.layout is layout