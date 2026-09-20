
"""Computation of summary statistics for parsed logs.

This module focuses on simple but useful metrics:

- total count of entries
- count of entries by level
- count of ERROR entries per hour
"""

from __future__ import annotations

from typing import Dict, Tuple

import pandas as pd


def compute_stats(df: pd.DataFrame) -> Tuple[Dict[str, int], Dict[str, int], Dict[str, int]]:
    """Compute summary statistics from a parsed log DataFrame.

    Returns:
        summary: dict with total_count, error_count, warning_count
        by_level: dict mapping level -> count
        by_hour_errors: dict mapping ISO hour string -> error count
    """
    summary = {
        "total_count": int(len(df)),
    }

    by_level_series = df["level"].value_counts()
    by_level: Dict[str, int] = {str(idx): int(val) for idx, val in by_level_series.items()}

    summary["error_count"] = int(by_level.get("ERROR", 0))
    summary["warning_count"] = int(by_level.get("WARNING", 0))

    # Derive hourly error counts
    errors_df = df[df["level"] == "ERROR"].copy()
    if not errors_df.empty:
        errors_df["hour"] = errors_df["timestamp"].dt.floor("H")
        by_hour_series = errors_df["hour"].value_counts().sort_index()
        by_hour_errors: Dict[str, int] = {
            hour.isoformat(): int(count) for hour, count in by_hour_series.items()
        }
    else:
        by_hour_errors = {}

    return summary, by_level, by_hour_errors
