from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class ConfigurationService:
    """Central HEOS configuration store."""

    _values: dict[str, Any] = field(
        default_factory=dict,
        init=False,
        repr=False,
    )

    def set(
        self,
        key: str,
        value: Any,
    ) -> None:
        if not key:
            raise ValueError(
                "Configuration key cannot be empty."
            )

        self._values[key] = value

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:
        return self._values.get(
            key,
            default,
        )

    def require(
        self,
        key: str,
    ) -> Any:
        if key not in self._values:
            raise KeyError(
                f"Missing configuration key '{key}'."
            )

        return self._values[key]

    def has(
        self,
        key: str,
    ) -> bool:
        return key in self._values

    def remove(
        self,
        key: str,
    ) -> bool:
        if key not in self._values:
            return False

        del self._values[key]
        return True

    def update(
        self,
        values: dict[str, Any],
    ) -> None:
        for key, value in values.items():
            self.set(
                key,
                value,
            )

    @property
    def count(self) -> int:
        return len(self._values)

    def snapshot(self) -> dict[str, Any]:
        return dict(self._values)

    def clear(self) -> None:
        self._values.clear()