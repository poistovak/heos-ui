from __future__ import annotations

from heos_ui.widgets.base import Widget

from .orchestrator import RenderOrchestrator


class RenderCoordinator:
    """Top-level render coordinator."""

    def __init__(
        self,
        orchestrator: RenderOrchestrator | None = None,
    ) -> None:
        self._orchestrator = orchestrator or RenderOrchestrator()

    @property
    def widget_count(self) -> int:
        return self._orchestrator.widget_count

    def add(self, widget: Widget) -> None:
        self._orchestrator.register(widget)

    def invalidate(self, widget: Widget) -> bool:
        return self._orchestrator.invalidate(widget.id)

    def render(self):
        return self._orchestrator.render()