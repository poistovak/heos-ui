from __future__ import annotations

from dataclasses import dataclass

from .base import Widget


@dataclass(slots=True, kw_only=True)
class BadgeWidget(Widget):
    """Compact widget displaying a short label."""

    text: str

    def render(self) -> str:
        """Return the badge text."""

        return f"[{self.text}]"