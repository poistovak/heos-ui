from __future__ import annotations

from dataclasses import dataclass

from .base import View


@dataclass(slots=True)
class DashboardView(View):
    """Main dashboard view."""