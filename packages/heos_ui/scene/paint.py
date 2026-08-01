from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

from heos_ui.layout import Rect

PaintCommandType = Literal[
    "rect",
    "text",
    "image",
]


@dataclass(slots=True, frozen=True)
class PaintCommand:
    """One drawing command."""

    command: PaintCommandType
    rect: Rect


class PaintList:
    """Collection of paint commands."""

    def __init__(self) -> None:
        self._commands: list[PaintCommand] = []

    def add(
        self,
        command: PaintCommand,
    ) -> None:
        self._commands.append(command)

    def clear(self) -> None:
        self._commands.clear()

    @property
    def count(self) -> int:
        return len(self._commands)

    @property
    def commands(self) -> tuple[PaintCommand, ...]:
        return tuple(self._commands)

    def __iter__(self):
        return iter(self._commands)