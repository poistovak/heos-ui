from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DiagnosticResult:
    component: str
    healthy: bool
    message: str = ""


@dataclass(slots=True)
class DiagnosticsEngine:
    _results: list[DiagnosticResult] = field(
        default_factory=list,
        init=False,
    )

    def record(
        self,
        result: DiagnosticResult,
    ) -> None:
        self._results.append(result)

    def report(self) -> tuple[DiagnosticResult, ...]:
        return tuple(self._results)

    def healthy(self) -> bool:
        return all(
            result.healthy
            for result in self._results
        )

    @property
    def count(self) -> int:
        return len(self._results)

    def clear(self) -> None:
        self._results.clear()