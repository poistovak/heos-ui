from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class StatusState(str, Enum):
    ONLINE = "online"
    OFFLINE = "offline"
    ACTIVE = "active"
    CHARGING = "charging"
    WARNING = "warning"
    ERROR = "error"


@dataclass(frozen=True)
class StatusChip:
    label: str
    state: StatusState = StatusState.ONLINE
    icon: str | None = None

    def __post_init__(self) -> None:
        if not self.label.strip():
            raise ValueError("Status label must not be empty.")