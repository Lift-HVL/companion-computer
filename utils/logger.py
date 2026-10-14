import os
import time
from pathlib import Path
from typing import Optional

LOG_DIR_ENV = "LIFT_LOG_DIR"
DEFAULT_LOG_DIR = Path(__file__).resolve().parents[1] / "logs"


class RunLogger:
    """One timestamped log file per run, one line per loop iteration.

    Log directory, first match wins: the `log_dir` argument, the
    LIFT_LOG_DIR environment variable, `<project root>/logs`.

    If the file cannot be opened or written, the logger silently becomes a
    no-op so a logging problem never stops the control loop.
    """

    def __init__(self, log_dir: Optional[str] = None, prefix: str = "run") -> None:
        self.path = None
        self._file = None
        self._start = time.monotonic()

        directory = Path(log_dir or os.environ.get(LOG_DIR_ENV) or DEFAULT_LOG_DIR)
        if not directory.is_absolute():
            directory = DEFAULT_LOG_DIR.parent / directory

        try:
            directory.mkdir(parents=True, exist_ok=True)
            stamp = time.strftime("%Y%m%d_%H%M%S")
            self.path = directory / f"{prefix}_{stamp}.txt"
            self._file = self.path.open("a", encoding="utf-8")
        except OSError:
            self._file = None

    def log(self, **fields) -> None:
        """Write one line: wall-clock time, elapsed seconds, key=value pairs."""
        if self._file is None:
            return
        wall = time.strftime("%Y-%m-%d %H:%M:%S")
        elapsed = time.monotonic() - self._start
        parts = [wall, f"t={elapsed:.3f}"]
        parts += [f"{key}={_format(value)}" for key, value in fields.items()]
        try:
            self._file.write(" ".join(parts) + "\n")
            self._file.flush()
        except OSError:
            pass

    def close(self) -> None:
        if self._file is None:
            return
        try:
            self._file.close()
        except OSError:
            pass
        self._file = None

    def __enter__(self) -> "RunLogger":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()


def _format(value: object) -> str:
    if value is None:
        return "-"
    if isinstance(value, float):
        return f"{value:.2f}"
    return str(value).replace(" ", "_")
