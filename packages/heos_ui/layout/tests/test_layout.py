from heos_ui.layout import VerticalLayout
from heos_ui.widgets import LabelWidget


def test_vertical_layout_add() -> None:
    layout = VerticalLayout()

    layout.add(
        LabelWidget(
            id="status",
            title="Status",
            text="Online",
        )
    )

    assert len(layout) == 1
    assert next(iter(layout)).render() == "Online"