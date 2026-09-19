
"""Log parsing utilities.

The goal of this module is not to support every possible log format, but to
provide a small set of simple, well-documented parsers that can handle:

- a generic "simple" format: `LEVEL YYYY-MM-DD HH:MM:SS component - message`
- a lightweight nginx/access-style format for demonstration purposes.

Parsed logs are returned as a pandas DataFrame with at least the following
columns: `timestamp`, `level`, `component`, `message`.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable, List, Literal

import re
import pandas as pd


Level = Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]


@dataclass
class ParsedLog:
    """Single parsed log entry."""

    timestamp: datetime
    level: str
    component: str
    message: str


SIMPLE_PATTERN = re.compile(
    r"^(?P<level>DEBUG|INFO|WARNING|ERROR|CRITICAL)\s+"  # level
    r"(?P<date>\d{4}-\d{2}-\d{2})\s+"                  # date
    r"(?P<time>\d{2}:\d{2}:\d{2})\s+"                  # time
    r"(?P<component>[\w\-\.]+)\s+-\s+"                # component
    r"(?P<message>.*)$"                                   # message
)

# Very simple nginx-like access log pattern for demonstration:
# 127.0.0.1 - - [2024-01-01T12:34:56] "GET /api/resource" 500
NGINX_PATTERN = re.compile(
    r"^(?P<ip>[\d\.]+)\s+-\s+-\s+"                         # IP
    r"\[(?P<ts>[^\]]+)\]\s+"                               # timestamp
    r"\"(?P<method>[A-Z]+)\s+(?P<path>[^\"]+)\"\s+"        # method/path
    r"(?P<status>\d{3})"                                   # status
)


def _iter_log_files(sources: Iterable[Path]) -> Iterable[Path]:
    """Yield all log files from a list of paths.

    - If a path is a file, it is yielded directly.
    - If a path is a directory, all files under it are yielded recursively.
    """
    for src in sources:
        if src.is_file():
            yield src
        elif src.is_dir():
            for path in src.rglob("*"):
                if path.is_file():
                    yield path


def _parse_simple_line(line: str) -> ParsedLog | None:
    """Parse a single line in the "simple" log format.

    Returns a ParsedLog instance or None if the line does not match.
    """
    m = SIMPLE_PATTERN.match(line.strip())
    if not m:
        return None

    date_str = m.group("date")
    time_str = m.group("time")
    ts = datetime.fromisoformat(f"{date_str} {time_str}")
    level = m.group("level")
    component = m.group("component")
    message = m.group("message")
    return ParsedLog(timestamp=ts, level=level, component=component, message=message)


def _parse_nginx_line(line: str) -> ParsedLog | None:
    """Parse a single line in the simplified nginx/access log format.

    We treat 2xx/3xx as INFO, 4xx as WARNING, 5xx as ERROR.
    """
    m = NGINX_PATTERN.match(line.strip())
    if not m:
        return None

    ts_raw = m.group("ts")  # e.g. 2024-01-01T12:34:56
    try:
        ts = datetime.fromisoformat(ts_raw)
    except ValueError:
        # fallback: unknown timestamp format
        return None

    status = int(m.group("status"))
    if 200 <= status < 400:
        level = "INFO"
    elif 400 <= status < 500:
        level = "WARNING"
    else:
        level = "ERROR"

    component = "nginx"  # simplified
    method = m.group("method")
    path = m.group("path")
    message = f"{method} {path} [{status}]"
    return ParsedLog(timestamp=ts, level=level, component=component, message=message)


def parse_logs(
    sources: Iterable[Path],
    pattern: str = "auto",
    include_debug: bool = False,
) -> pd.DataFrame:
    """Parse logs from given file or directory paths into a DataFrame.

    Parameters:
        sources: list of files or directories to scan.
        pattern: 'auto', 'simple', or 'nginx'. In 'auto' mode we try both
                 parsers and accept whichever matches.
        include_debug: if False, DEBUG-level entries are filtered out.

    Returns:
        pandas.DataFrame with columns: timestamp (datetime64), level, component, message.
    """
    entries: List[ParsedLog] = []

    for file_path in _iter_log_files(sources):
        with file_path.open("r", encoding="utf-8", errors="ignore") as fh:
            for line in fh:
                parsed: ParsedLog | None = None

                if pattern == "simple":
                    parsed = _parse_simple_line(line)
                elif pattern == "nginx":
                    parsed = _parse_nginx_line(line)
                else:  # auto
                    parsed = _parse_simple_line(line) or _parse_nginx_line(line)

                if parsed is None:
                    continue

                if not include_debug and parsed.level == "DEBUG":
                    continue

                entries.append(parsed)

    if not entries:
        return pd.DataFrame(columns=["timestamp", "level", "component", "message"])

    df = pd.DataFrame([
        {
            "timestamp": e.timestamp,
            "level": e.level,
            "component": e.component,
            "message": e.message,
        }
        for e in entries
    ])
    df.sort_values("timestamp", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
