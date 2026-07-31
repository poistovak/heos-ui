from heos_ui.widgets import LabelWidget, ValueWidget


def test_label_widget() -> None:
    widget = LabelWidget(
        id="label",
        title="Status",
        text="Online",
    )

    assert widget.render() == "Online"


def test_value_widget() -> None:
    widget = ValueWidget(
        id="power",
        title="PV",
        value=8.4,
        unit="kW",
    )

    assert widget.render() == "8.4 kW"