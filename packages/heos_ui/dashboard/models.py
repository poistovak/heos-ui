from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class DashboardCard:
    """Represents one dashboard card."""

    title: str
    value: str
    icon: str


@dataclass(slots=True)
class Dashboard:
    """Simple dashboard container."""

    cards: list[DashboardCard]