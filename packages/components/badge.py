from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class BadgeVariant(str, Enum):
    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class Badge:
    label: str
    variant: BadgeVariant = BadgeVariant.INFO

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("Badge label must not be empty.")