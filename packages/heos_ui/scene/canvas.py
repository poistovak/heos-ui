from __future__ import annotations

from dataclasses import dataclass, field

from .paint import PaintCommand


@dataclass(slots=True)
class CanvasBackend:
    """Abstract canvas backend collecting paint commands."""

    _commands: list[PaintCommand] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def begin_frame(self) -> None:
        """Begin rendering a frame."""
        self._commands.clear()

    def submit(self, command: PaintCommand) -> None:
        """Submit one paint command."""
        self._commands.append(command)

    def end_frame(self) -> tuple[PaintCommand, ...]:
        """Finish rendering and return submitted commands."""
        return tuple(self._commands)

    @property
    def command_count(self) -> int:
        return len(self._commands)