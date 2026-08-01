from __future__ import annotations

from .dispatcher import RenderDispatcher
from .registry import RenderRegistry
from .service import RenderRuntime
from heos_ui.widgets.base import Widget


class RenderOrchestrator:
    """Coordinates the complete render runtime."""

    def __init__(
        self,
        runtime: RenderRuntime | None = None,
        registry: RenderRegistry | None = None,
        dispatcher: RenderDispatcher | None = None,
    ) -> None:
        self._runtime = runtime or RenderRuntime()
        self._registry = registry or RenderRegistry()
        self._dispatcher = dispatcher

    @property
    def widget_count(self) -> int:
        return self._registry.count

    def register(self, widget: Widget) -> None:
        self._registry.register(widget)

    def invalidate(self, widget_id: str) -> bool:
        widget = self._registry.get(widget_id)
        if widget is None:
            return False
        return self._runtime.invalidate(widget)

    def render(self):
        if self._dispatcher is not None:
            return self._dispatcher.dispatch()
        return self._runtime.tick()