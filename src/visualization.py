
"""Simple chart rendering for log statistics.

Uses matplotlib to generate PNG charts suitable for embedding into reports
or attaching to tickets.
"""

from __future__ import annotations

from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import pandas as pd


def render_charts(df: pd.DataFrame, output_dir: Path) -> List[Path]:
    """Render basic charts and save them as PNG files in *output_dir*.

    Currently renders:
        - bar chart: count by level
        - line chart: hourly error count
    """
    chart_paths: List[Path] = []

    # Chart 1: count by level
    by_level = df["level"].value_counts().sort_index()
    if not by_level.empty:
        fig, ax = plt.subplots(figsize=(6, 4))
        by_level.plot(kind="bar", ax=ax, color="#007acc")
        ax.set_title("Log entries by level")
        ax.set_xlabel("Level")
        ax.set_ylabel("Count")
        ax.grid(True, axis="y", alpha=0.3)
        path = output_dir / "by_level.png"
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)
        chart_paths.append(path)

    # Chart 2: hourly error count
    errors_df = df[df["level"] == "ERROR"].copy()
    if not errors_df.empty:
        errors_df["hour"] = errors_df["timestamp"].dt.floor("H")
        by_hour = errors_df["hour"].value_counts().sort_index()

        fig, ax = plt.subplots(figsize=(8, 4))
        by_hour.plot(kind="line", ax=ax, marker="o", color="#cc3300")
        ax.set_title("ERROR entries per hour")
        ax.set_xlabel("Hour")
        ax.set_ylabel("Error count")
        ax.grid(True, alpha=0.3)
        fig.autofmt_xdate(rotation=45)
        path = output_dir / "errors_by_hour.png"
        fig.tight_layout()
        fig.savefig(path)
        plt.close(fig)
        chart_paths.append(path)

    return chart_paths
