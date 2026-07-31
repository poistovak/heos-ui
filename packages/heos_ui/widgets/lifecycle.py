from __future__ import annotations

from enum import Enum


class WidgetLifecycle(str, Enum):
    """Lifecycle states of a UI widget."""

    CREATED = "created"
    ATTACHED = "attached"
    VISIBLE = "visible"
    HIDDEN = "hidden"
    DISPOSED = "disposed"