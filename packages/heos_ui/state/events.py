from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class StateChangeEvent:
    """Represents one committed state change."""

    key: str
    value: Any