from __future__ import annotations

import json
from pathlib import Path
from typing import Any

TOKENS_DIR = Path(__file__).resolve().parent.parent / "tokens"


def validate_token(token: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []

    if "$type" not in token:
        errors.append(f"{path}: missing $type")

    if "$value" not in token:
        errors.append(f"{path}: missing $value")

    return errors


def walk(data: Any, path: str = "") -> list[str]:
    errors: list[str] = []

    if not isinstance(data, dict):
        return errors

    if "$type" in data or "$value" in data:
        errors.extend(validate_token(data, path))
        return errors

    for key, value in data.items():
        if key == "$schema":
            continue

        next_path = f"{path}.{key}" if path else key
        errors.extend(walk(value, next_path))

    return errors


def validate_file(file: Path) -> bool:
    try:
        data = json.loads(file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        print(f"ERROR {file.name}: invalid JSON ({exc})")
        return False

    if not isinstance(data, dict):
        print(f"ERROR {file.name}: root must be an object")
        return False

    if "$schema" not in data:
        print(f"ERROR {file.name}: missing $schema")
        return False

    errors = walk(data)

    if errors:
        print(f"ERROR {file.name}")
        for error in errors:
            print(f"  - {error}")
        return False

    print(f"OK {file.name}")
    return True


def main() -> int:
    files = sorted(TOKENS_DIR.glob("*.json"))

    if not files:
        print(f"ERROR: no JSON token files found in {TOKENS_DIR}")
        return 1

    all_valid = True

    for file in files:
        if not validate_file(file):
            all_valid = False

    return 0 if all_valid else 1


if __name__ == "__main__":
    raise SystemExit(main())