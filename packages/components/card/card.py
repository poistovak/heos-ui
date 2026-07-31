from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CardVariant(str, Enum):
    DEFAULT = "default"
    ELEVATED = "elevated"
    OUTLINED = "outlined"


class CardPadding(str, Enum):
    NONE = "none"
    SMALL = "small"
    MEDIUM = "medium"
    LARGE = "large"


@dataclass(frozen=True)
class Card:
    title: str
    content: str
    variant: CardVariant = CardVariant.DEFAULT
    padding: CardPadding = CardPadding.MEDIUM

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Card title must not be empty.")

        if not self.content.strip():
            raise ValueError("Card content must not be empty.")