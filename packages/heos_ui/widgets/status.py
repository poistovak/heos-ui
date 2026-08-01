from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from .base import Widget


class StatusLevel(str, Enum):
    """Visual severity level of a status widget."""

    INFO = "info"
    SUCCESS = "success"
    WARNING = "warning"
    ERROR = "error"


@dataclass(slots=True, kw_only=True)
class StatusWidget(Widget):
    """Widget displaying a named system status."""

    status: str
    level: StatusLevel = StatusLevel.INFO

    def render(self) -> str:
        """Return the formatted status."""

        return f"{self.title}: {self.status}"