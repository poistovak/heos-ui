from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ButtonVariant(str, Enum):
    PRIMARY = "primary"
    SECONDARY = "secondary"
    DANGER = "danger"


class ButtonSize(str, Enum):
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@dataclass(frozen=True)
class Button:
    label: str
    variant: ButtonVariant = ButtonVariant.PRIMARY
    size: ButtonSize = ButtonSize.MEDIUM
    disabled: bool = False

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("Button label must not be empty.")