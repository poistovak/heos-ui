from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Metric:
    name: str
    value: float


@dataclass(slots=True)
class TelemetryService:
    _metrics: dict[str, float] = field(
        default_factory=dict,
        init=False,
    )

    def record(
        self,
        name: str,
        value: float,
    ) -> None:
        self._metrics[name] = value

    def get(
        self,
        name: str,
    ) -> float | None:
        return self._metrics.get(name)

    def has(
        self,
        name: str,
    ) -> bool:
        return name in self._metrics

    def snapshot(self) -> dict[str, float]:
        return dict(self._metrics)

    @property
    def count(self) -> int:
        return len(self._metrics)

    def clear(self) -> None:
        self._metrics.clear()