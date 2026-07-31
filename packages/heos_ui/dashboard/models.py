from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DashboardCard:
    """Single dashboard card."""

    title: str
    value: str
    icon: str = ""


@dataclass(frozen=True, slots=True)
class DashboardSection:
    """Logical group of dashboard cards."""

    title: str
    cards: tuple[DashboardCard, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class DashboardPage:
    """Single dashboard page."""

    id: str
    title: str
    sections: tuple[DashboardSection, ...] = field(default_factory=tuple)


@dataclass(frozen=True, slots=True)
class Dashboard:
    """Root dashboard object."""

    title: str
    pages: tuple[DashboardPage, ...] = field(default_factory=tuple)