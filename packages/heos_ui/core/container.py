from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Container:
    _services: dict[type[Any], Any] = field(
        default_factory=dict,
        init=False,
    )

    def register(
        self,
        service: Any,
    ) -> None:
        service_type = type(service)

        if service_type in self._services:
            raise ValueError(
                f"{service_type.__name__} already registered."
            )

        self._services[service_type] = service

    def resolve(
        self,
        service_type: type[Any],
    ) -> Any:
        try:
            return self._services[service_type]
        except KeyError as exc:
            raise LookupError(
                f"{service_type.__name__} not registered."
            ) from exc

    def has(
        self,
        service_type: type[Any],
    ) -> bool:
        return service_type in self._services

    @property
    def count(self) -> int:
        return len(self._services)

    def clear(self) -> None:
        self._services.clear()