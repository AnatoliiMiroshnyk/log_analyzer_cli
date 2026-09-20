
"""Tests for log_analyzer.stats module."""

from datetime import datetime

import pandas as pd

from log_analyzer.stats import compute_stats


def test_compute_stats_basic():
    data = [
        {"timestamp": datetime(2024, 1, 1, 10, 0, 0), "level": "INFO", "component": "api", "message": "ok"},
        {"timestamp": datetime(2024, 1, 1, 10, 5, 0), "level": "WARNING", "component": "api", "message": "slow"},
        {"timestamp": datetime(2024, 1, 1, 10, 10, 0), "level": "ERROR", "component": "db", "message": "fail"},
        {"timestamp": datetime(2024, 1, 1, 11, 0, 0), "level": "ERROR", "component": "worker", "message": "fail"},
    ]
    df = pd.DataFrame(data)

    summary, by_level, by_hour = compute_stats(df)

    assert summary["total_count"] == 4
    assert summary["error_count"] == 2
    assert summary["warning_count"] == 1
    assert by_level["INFO"] == 1
    assert by_level["WARNING"] == 1
    assert by_level["ERROR"] == 2
    # hourly error counts should have 2 distinct hours
    assert len(by_hour) == 2
