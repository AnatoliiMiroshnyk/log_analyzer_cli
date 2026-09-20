
"""Tests for log_analyzer.visualization module."""

from datetime import datetime
from pathlib import Path

import pandas as pd

from log_analyzer.visualization import render_charts


def test_render_charts_creates_png(tmp_path):
    data = [
        {"timestamp": datetime(2024, 1, 1, 10, 0, 0), "level": "INFO", "component": "api", "message": "ok"},
        {"timestamp": datetime(2024, 1, 1, 10, 10, 0), "level": "ERROR", "component": "db", "message": "fail"},
        {"timestamp": datetime(2024, 1, 1, 11, 0, 0), "level": "ERROR", "component": "worker", "message": "fail"},
    ]
    df = pd.DataFrame(data)

    output_dir = tmp_path / "charts"
    output_dir.mkdir()

    paths = render_charts(df, output_dir=output_dir)
    assert paths
    for p in paths:
        assert p.is_file()
        assert p.suffix == ".png"
