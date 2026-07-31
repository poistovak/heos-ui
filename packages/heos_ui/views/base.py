from __future__ import annotations

from dataclasses import dataclass

from heos_ui.layout import Layout


@dataclass(slots=True)
class View:
    """Base class for all HEOS UI views."""

    title: str
    layout: Layout