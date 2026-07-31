from __future__ import annotations

from dataclasses import dataclass, field

from heos_ui.views import View


@dataclass(slots=True)
class ViewManager:
    """Registers and manages application views."""

    _views: dict[str, View] = field(default_factory=dict)
    _active: str | None = None

    def register(self, name: str, view: View) -> None:
        self._views[name] = view

        if self._active is None:
            self._active = name

    def activate(self, name: str) -> None:
        if name not in self._views:
            raise KeyError(f"Unknown view: {name}")

        self._active = name

    @property
    def active_view(self) -> View:
        if self._active is None:
            raise RuntimeError("No active view.")

        return self._views[self._active]