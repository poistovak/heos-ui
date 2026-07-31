from heos_ui.binding import BoundValueWidget, StateBinding, WidgetObserver
from heos_ui.state import ObservableState


def test_widget_observer_refreshes_widget() -> None:
    state = ObservableState()

    binding = StateBinding(
        store=state,
        key="pv_power",
        default=0.0,
    )

    widget = BoundValueWidget(
        id="pv",
        title="PV",
        value=0.0,
        unit="kW",
        binding=binding,
    )

    observer = WidgetObserver(
        state=state,
        key="pv_power",
        widget=widget,
    )

    state.set("pv_power", 8.2)

    assert widget.value == 8.2

    observer.dispose()