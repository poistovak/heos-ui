from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SpacingTokens:
    """Consistent spacing scale used across the HEOS UI."""

    none: int = 0
    xs: int = 4
    sm: int = 8
    md: int = 12
    lg: int = 16
    xl: int = 24
    xxl: int = 32
    huge: int = 48

    def resolve(self, token: str) -> int:
        """Resolve a spacing token name to its pixel value."""
        try:
            value = getattr(self, token)
        except AttributeError as exc:
            raise ValueError(f"Unknown spacing token: {token}") from exc

        if not isinstance(value, int):
            raise ValueError(f"Invalid spacing token: {token}")

        return value


SPACING = SpacingTokens()