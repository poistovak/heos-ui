from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True, frozen=True)
class Overlay:
    """Overlay layer."""

    id: str
    visible: bool = True


@dataclass(slots=True)
class OverlayManager:
    """Manages overlay stack."""

    _stack: list[Overlay] = field(
        default_factory=list,
        init=False,
        repr=False,
    )

    def show(self, overlay: Overlay) -> None:
        self._stack.append(overlay)

    def hide(self, overlay_id: str) -> bool:
        for index, overlay in enumerate(self._stack):
            if overlay.id == overlay_id:
                del self._stack[index]
                return True
        return False

    @property
    def count(self) -> int:
        return len(self._stack)

    @property
    def top(self) -> Overlay | None:
        if not self._stack:
            return None
        return self._stack[-1]

    @property
    def overlays(self) -> tuple[Overlay, ...]:
        return tuple(self._stack)

    def clear(self) -> None:
        self._stack.clear()