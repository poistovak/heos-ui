from __future__ import annotations

from .models import (
    Dashboard,
    DashboardCard,
    DashboardPage,
    DashboardSection,
)


class DashboardBuilder:
    """Fluent builder for dashboards."""

    def __init__(self, title: str) -> None:
        self._title = title
        self._pages: list[DashboardPage] = []

        self._current_page_title: str | None = None
        self._current_page_id: str | None = None
        self._sections: list[DashboardSection] = []

        self._current_section_title: str | None = None
        self._cards: list[DashboardCard] = []

    def page(self, title: str, page_id: str | None = None) -> "DashboardBuilder":
        self._flush_section()
        self._flush_page()

        self._current_page_title = title
        self._current_page_id = page_id or title.lower()

        return self

    def section(self, title: str) -> "DashboardBuilder":
        self._flush_section()

        self._current_section_title = title

        return self

    def card(
        self,
        title: str,
        value: str,
        icon: str = "",
    ) -> "DashboardBuilder":
        self._cards.append(
            DashboardCard(
                title=title,
                value=value,
                icon=icon,
            )
        )

        return self

    def build(self) -> Dashboard:
        self._flush_section()
        self._flush_page()

        return Dashboard(
            title=self._title,
            pages=tuple(self._pages),
        )

    def _flush_section(self) -> None:
        if self._current_section_title is None:
            return

        self._sections.append(
            DashboardSection(
                title=self._current_section_title,
                cards=tuple(self._cards),
            )
        )

        self._current_section_title = None
        self._cards = []

    def _flush_page(self) -> None:
        if self._current_page_title is None:
            return

        self._pages.append(
            DashboardPage(
                id=self._current_page_id or self._current_page_title.lower(),
                title=self._current_page_title,
                sections=tuple(self._sections),
            )
        )

        self._current_page_title = None
        self._current_page_id = None
        self._sections = []