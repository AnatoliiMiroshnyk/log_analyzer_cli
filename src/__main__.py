
"""Entry point for the Log Analyzer CLI.

This module simply delegates to the Typer-based CLI application.
"""

from src.cli import app


if __name__ == "__main__":
    app()
