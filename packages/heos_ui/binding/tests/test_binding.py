import pytest
from heos_ui.binding import BoundValueWidget, StateBinding
from heos_ui.state import StateStore


def test_state_binding_reads_value() -> None:
    store = StateStore()
    store.set("pv_power", 8.4)

    binding = StateBinding(
        store=store,
        key="pv_power",
    )

    assert binding.get() == 8.4


def test_bound_value_widget_refreshes_from_state() -> None:
    store = StateStore()
    store.set("pv_power", 8.4)

    widget = BoundValueWidget(
        id="pv",
        title="PV",
        value=0.0,
        unit="kW",
        binding=StateBinding(
            store=store,
            key="pv_power",
        ),
    )

    widget.refresh()

    assert widget.value == 8.4
    assert widget.render() == "8.4 kW"

    store.set("pv_power", 9.1)
    widget.refresh()

    assert widget.value == 9.1
    assert widget.render() == "9.1 kW"


def test_bound_value_widget_rejects_non_numeric_state() -> None:
    store = StateStore()
    store.set("pv_power", "unknown")

    widget = BoundValueWidget(
        id="pv",
        title="PV",
        value=0.0,
        unit="kW",
        binding=StateBinding(
            store=store,
            key="pv_power",
        ),
    )

    with pytest.raises(TypeError, match="Bound value must be numeric"):
        widget.refresh()