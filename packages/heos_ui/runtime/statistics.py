from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class RenderStatistics:
    """Immutable render engine statistics."""

    attempted: int
    rendered: int
    skipped: int
    batches: int
