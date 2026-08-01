import pytest
from heos_ui.widgets import (
    BadgeWidget,
    ProgressWidget,
    StatusLevel,
    StatusWidget,
)


def test_status_widget_renders_status() -> None:
    widget = StatusWidget(
        id="inverter-status",
        title="Inverter",
        status="Online",
        level=StatusLevel.SUCCESS,
    )

    assert widget.status == "Online"
    assert widget.level is StatusLevel.SUCCESS
    assert widget.render() == "Inverter: Online"


def test_status_widget_uses_info_level_by_default() -> None:
    widget = StatusWidget(
        id="grid-status",
        title="Grid",
        status="Connected",
    )

    assert widget.level is StatusLevel.INFO


def test_badge_widget_renders_compact_label() -> None:
    widget = BadgeWidget(
        id="charging-badge",
        title="Charging state",
        text="CHARGING",
    )

    assert widget.render() == "[CHARGING]"


def test_progress_widget_renders_percentage() -> None:
    widget = ProgressWidget(
        id="battery-progress",
        title="Battery",
        value=82,
    )

    assert widget.render() == "Battery: 82%"


@pytest.mark.parametrize("value", [-1, 101])
def test_progress_widget_rejects_invalid_value(value: float) -> None:
    with pytest.raises(
        ValueError,
        match="Progress value must be between 0 and 100.",
    ):
        ProgressWidget(
            id="invalid-progress",
            title="Invalid",
            value=value,
        )