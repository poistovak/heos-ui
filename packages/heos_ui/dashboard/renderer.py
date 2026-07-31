from __future__ import annotations

from .models import Dashboard


class DashboardRenderer:
    """Simple text renderer for a dashboard."""

    WIDTH = 42

    def render(self, dashboard: Dashboard) -> str:
        inner_width = self.WIDTH - 2

        lines = [
            "╔" + "═" * inner_width + "╗",
            "║" + dashboard.title.center(inner_width) + "║",
            "╠" + "═" * inner_width + "╣",
        ]

        for page in dashboard.pages:
            lines.append("║ " + f"[{page.title}]".ljust(inner_width - 1) + "║")

            for section in page.sections:
                lines.append("║ " + f"• {section.title}".ljust(inner_width - 1) + "║")

                for card in section.cards:
                    content = (
                        f"  {card.icon} {card.title:<12} {card.value}"
                    ).rstrip()
                    lines.append("║" + content.ljust(inner_width) + "║")

        lines.append("╚" + "═" * inner_width + "╝")

        return "\n".join(lines)