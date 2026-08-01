from __future__ import annotations

from heos_ui.widgets import Widget

from .models import (
    Dashboard,
    DashboardCard,
    DashboardPage,
    DashboardSection,
)


class DashboardComposer:
    """Compose complete dashboard screens from HEOS UI widgets."""

    def __init__(self, title: str) -> None:
        if not title.strip():
            raise ValueError("Dashboard title cannot be empty.")

        self._title = title
        self._pages: list[DashboardPage] = []

        self._current_page_id: str | None = None
        self._current_page_title: str | None = None
        self._current_sections: list[DashboardSection] = []

        self._current_section_title: str | None = None
        self._current_cards: list[DashboardCard] = []

        self._built = False

    def page(
        self,
        title: str,
        page_id: str | None = None,
    ) -> DashboardComposer:
        """Start a new dashboard page."""

        self._require_not_built()

        if not title.strip():
            raise ValueError("Page title cannot be empty.")

        self._flush_section()
        self._flush_page()

        self._current_page_title = title
        self._current_page_id = page_id or self._create_id(title)

        return self

    def section(self, title: str) -> DashboardComposer:
        """Start a new section on the current page."""

        self._require_not_built()
        self._require_page()

        if not title.strip():
            raise ValueError("Section title cannot be empty.")

        self._flush_section()
        self._current_section_title = title

        return self

    def widget(
        self,
        widget: Widget,
        *,
        icon: str = "",
    ) -> DashboardComposer:
        """Add a widget to the current section."""

        self._require_not_built()
        self._require_section()

        self._current_cards.append(
            DashboardCard(
                title=widget.title,
                value=self._render_widget_value(widget),
                icon=icon,
            )
        )

        return self

    def build(self) -> Dashboard:
        """Build and return the complete dashboard."""

        self._require_not_built()
        self._flush_section()
        self._flush_page()

        self._built = True

        return Dashboard(
            title=self._title,
            pages=tuple(self._pages),
        )

    def _flush_section(self) -> None:
        if self._current_section_title is None:
            return

        self._current_sections.append(
            DashboardSection(
                title=self._current_section_title,
                cards=tuple(self._current_cards),
            )
        )

        self._current_section_title = None
        self._current_cards = []

    def _flush_page(self) -> None:
        if self._current_page_title is None:
            return

        self._pages.append(
            DashboardPage(
                id=self._current_page_id
                or self._create_id(self._current_page_title),
                title=self._current_page_title,
                sections=tuple(self._current_sections),
            )
        )

        self._current_page_id = None
        self._current_page_title = None
        self._current_sections = []

    def _require_page(self) -> None:
        if self._current_page_title is None:
            raise RuntimeError(
                "A page must be created before adding a section."
            )

    def _require_section(self) -> None:
        if self._current_section_title is None:
            raise RuntimeError(
                "A section must be created before adding a widget."
            )

    def _require_not_built(self) -> None:
        if self._built:
            raise RuntimeError(
                "Dashboard composer has already been built."
            )

    @staticmethod
    def _render_widget_value(widget: Widget) -> str:
        rendered = widget.render()
        prefix = f"{widget.title}: "

        if rendered.startswith(prefix):
            return rendered[len(prefix) :]

        return rendered

    @staticmethod
    def _create_id(title: str) -> str:
        return "-".join(title.strip().lower().split())
