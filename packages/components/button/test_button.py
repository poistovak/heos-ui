import pytest
from button import Button, ButtonSize, ButtonVariant


def test_button_defaults() -> None:
    button = Button(label="Start")

    assert button.label == "Start"
    assert button.variant is ButtonVariant.PRIMARY
    assert button.size is ButtonSize.MEDIUM
    assert button.disabled is False


def test_button_rejects_empty_label() -> None:
    with pytest.raises(ValueError, match="must not be empty"):
        Button(label="   ")