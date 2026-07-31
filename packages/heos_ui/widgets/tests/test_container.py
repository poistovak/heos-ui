from heos_ui.widgets import LabelWidget, WidgetContainer


def test_container_add() -> None:
    container = WidgetContainer()

    container.add(
        LabelWidget(
            id="status",
            title="Status",
            text="Online",
        )
    )

    assert len(container) == 1
    assert next(iter(container)).render() == "Online"