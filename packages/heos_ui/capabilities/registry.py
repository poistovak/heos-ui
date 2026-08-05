from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Capability:
    name: str


@dataclass(slots=True)
class CapabilityRegistry:
    _capabilities: dict[str, Capability] = field(
        default_factory=dict,
        init=False,
    )

    def register(self, capability: Capability) -> None:
        if capability.name in self._capabilities:
            raise ValueError(
                f"Capability '{capability.name}' already registered."
            )

        self._capabilities[capability.name] = capability

    def unregister(self, name: str) -> None:
        self._capabilities.pop(name, None)

    def get(self, name: str) -> Capability | None:
        return self._capabilities.get(name)

    def has(self, name: str) -> bool:
        return name in self._capabilities

    @property
    def count(self) -> int:
        return len(self._capabilities)