from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Service:
    name: str


@dataclass(slots=True)
class ServiceRegistry:
    _services: dict[str, Service] = field(
        default_factory=dict,
        init=False,
    )

    def register(self, service: Service) -> None:
        if service.name in self._services:
            raise ValueError(
                f"Service '{service.name}' already registered."
            )

        self._services[service.name] = service

    def unregister(self, name: str) -> None:
        self._services.pop(name, None)

    def get(self, name: str) -> Service | None:
        return self._services.get(name)

    def has(self, name: str) -> bool:
        return name in self._services

    @property
    def count(self) -> int:
        return len(self._services)

    def all(self) -> tuple[Service, ...]:
        return tuple(self._services.values())