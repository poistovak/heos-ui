from __future__ import annotations

from .models import Dashboard


class DashboardRenderer:
    """Simple text renderer for a dashboard."""

    WIDTH = 42

    def render(self, dashboard: Dashboard) -> str:
        inner_width = self.WIDTH - 2

        lines = [
            "╔" + "═" * inner_width + "╗",
            "║" + "HEOS HOME".center(inner_width) + "║",
            "╠" + "═" * inner_width + "╣",
        ]

        for card in dashboard.cards:
            content = f"{card.icon} {card.title:<10} {card.value}"
            lines.append("║" + content.ljust(inner_width) + "║")

        lines.append("╚" + "═" * inner_width + "╝")

        return "\n".join(lines)
