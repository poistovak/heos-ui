from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class LogLevel(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


@dataclass(frozen=True, slots=True)
class LogEntry:
    level: LogLevel
    component: str
    message: str


@dataclass(slots=True)
class Logger:
    component: str
    _entries: list[LogEntry] = field(
        default_factory=list,
        init=False,
    )

    def log(
        self,
        level: LogLevel,
        message: str,
    ) -> None:
        self._entries.append(
            LogEntry(
                level=level,
                component=self.component,
                message=message,
            )
        )

    def debug(self, message: str) -> None:
        self.log(LogLevel.DEBUG, message)

    def info(self, message: str) -> None:
        self.log(LogLevel.INFO, message)

    def warning(self, message: str) -> None:
        self.log(LogLevel.WARNING, message)

    def error(self, message: str) -> None:
        self.log(LogLevel.ERROR, message)

    def entries(self) -> tuple[LogEntry, ...]:
        return tuple(self._entries)

    @property
    def count(self) -> int:
        return len(self._entries)

    def clear(self) -> None:
        self._entries.clear()