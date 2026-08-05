from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Plugin:
    name: str
    version: str = "1.0.0"


@dataclass(slots=True)
class PluginManager:
    _plugins: dict[str, Plugin] = field(
        default_factory=dict,
        init=False,
    )

    def load(self, plugin: Plugin) -> None:
        if plugin.name in self._plugins:
            raise ValueError(
                f"Plugin '{plugin.name}' already loaded."
            )

        self._plugins[plugin.name] = plugin

    def unload(self, name: str) -> None:
        self._plugins.pop(name, None)

    def get(self, name: str) -> Plugin | None:
        return self._plugins.get(name)

    def loaded(self) -> tuple[Plugin, ...]:
        return tuple(self._plugins.values())

    @property
    def count(self) -> int:
        return len(self._plugins)