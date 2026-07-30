from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def test_validator_passes() -> None:
    validator = (
        Path(__file__).resolve().parent.parent
        / "validator"
        / "validate.py"
    )

    result = subprocess.run(
        [sys.executable, str(validator)],
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr