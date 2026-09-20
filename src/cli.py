
"""Typer-based command-line interface for the Log Analyzer project.

The CLI exposes a single command `analyze` which reads one or more log
files, parses them into a structured DataFrame, computes summary statistics,
and optionally generates visualizations.
"""

import typer
from pathlib import Path
from typing import Optional, List

from src.parser import parse_logs
from src.stats import compute_stats
from src.visualization import render_charts


app = typer.Typer(help="Log Analyzer: parse logs, compute stats, and visualize issues.")


@app.command()
def analyze(
    sources: List[Path] = typer.Argument(
        ..., exists=True, readable=True,
        help="One or more log files or directories to analyze. Directories are scanned recursively."
    ),
    output: Optional[Path] = typer.Option(
        None,
        "--output",
        "-o",
        file_okay=False,
        dir_okay=True,
        help="Directory where reports and charts will be written. Defaults to ./reports.",
    ),
    pattern: str = typer.Option(
        "auto",
        "--pattern",
        help=(
            "Log format pattern: 'auto' (try to detect), 'simple' (LEVEL timestamp component - message), "
            "or 'nginx' (common nginx/access style)."
        ),
    ),
    include_debug: bool = typer.Option(
        False,
        "--include-debug",
        help="Include DEBUG level messages in analysis (ignored by default).",
    ),
    charts: bool = typer.Option(
        True,
        "--charts",
        help="Generate PNG charts for error rate and level distribution.",
    ),
) -> None:
    """Analyze one or more log files and print a textual summary.

    Examples:

        log-analyzer analyze logs/access.log logs/error.log
        log-analyzer analyze ./logs --output ./reports --pattern simple
    """
    if output is None:
        output = Path("reports")
    output.mkdir(parents=True, exist_ok=True)

    typer.echo("[log-analyzer] starting analysis...")

    df = parse_logs(sources, pattern=pattern, include_debug=include_debug)
    if df.empty:
        typer.echo("No log entries parsed. Check your pattern or sources.")
        raise typer.Exit(code=1)

    summary, by_level, by_hour = compute_stats(df)

    typer.echo("Summary:")
    for key, value in summary.items():
        typer.echo(f"  {key}: {value}")

    typer.echo("By level:")
    for level, count in by_level.items():
        typer.echo(f"  {level}: {count}")

    typer.echo("Top hours by errors (up to 10):")
    for hour, count in list(by_hour.items())[:10]:
        typer.echo(f"  {hour}: {count}")

    if charts:
        typer.echo("Rendering charts...")
        chart_paths = render_charts(df, output_dir=output)
        for p in chart_paths:
            typer.echo(f"  chart: {p}")

    typer.echo("[log-analyzer] done.")
