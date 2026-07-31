import pytest
from status_chip import StatusChip, StatusState


def test_default_status_chip() -> None:
    chip = StatusChip(label="PV Online")

    assert chip.label == "PV Online"
    assert chip.state is StatusState.ONLINE
    assert chip.icon is None


def test_custom_status_chip() -> None:
    chip = StatusChip(
        label="Charging",
        state=StatusState.CHARGING,
        icon="battery",
    )

    assert chip.state is StatusState.CHARGING
    assert chip.icon == "battery"


def test_empty_label() -> None:
    with pytest.raises(ValueError):
        StatusChip(label=" ")