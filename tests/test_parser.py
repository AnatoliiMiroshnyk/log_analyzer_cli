
"""Tests for log_analyzer.parser module."""


import pandas as pd

from src.parser import parse_logs, _parse_simple_line, _parse_nginx_line


def test_parse_simple_line_valid():
    line = "ERROR 2024-01-01 12:00:00 api - Something went wrong"
    entry = _parse_simple_line(line)
    assert entry is not None
    assert entry.level == "ERROR"
    assert entry.component == "api"
    assert "Something went wrong" in entry.message


def test_parse_simple_line_invalid():
    line = "this is not a valid log line"
    entry = _parse_simple_line(line)
    assert entry is None


def test_parse_nginx_line_valid():
    line = "127.0.0.1 - - [2024-01-01T12:34:56] \"GET /api/resource\" 500"
    entry = _parse_nginx_line(line)
    assert entry is not None
    assert entry.level == "ERROR"
    assert entry.component == "nginx"
    assert "GET /api/resource" in entry.message


def test_parse_logs_auto(tmp_path):
    # create a small mixed log file
    log_file = tmp_path / "mixed.log"
    lines = [
        "INFO 2024-01-01 10:00:00 api - Start",
        "127.0.0.1 - - [2024-01-01T10:10:00] \"GET /api/health\" 200",
    ]
    log_file.write_text("".join(lines), encoding="utf-8")

    df = parse_logs([log_file], pattern="auto", include_debug=False)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 2
    assert set(df["level"]) == {"INFO"}
