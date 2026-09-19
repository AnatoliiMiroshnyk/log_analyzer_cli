
# Log Analyzer & Visualizer CLI

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue.svg)](https://www.python.org/)
[![Status](https://img.shields.io/badge/status-beta-yellow.svg)]()

A small but realistic DevOps-oriented tool that parses application and access logs, computes useful statistics, and generates charts to visualize issues over time.

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [Installation](#installation)
- [Quickstart](#quickstart)
- [Configuration](#configuration)
- [Examples](#examples)
- [Tests](#tests)
- [Development](#development)
- [Roadmap](#roadmap)
- [License](#license)

## Overview

Modern DevOps workflows rely heavily on log analysis to detect problems, understand performance, and correlate incidents.[cite:17][cite:20] This tool is designed as a portfolio-friendly example of how Python can be used to:

- parse logs from different sources;
- structure them into a DataFrame;
- compute summary metrics;
- render PNG charts that can be attached to tickets or reports.[cite:18]

It supports a simple custom log format and a lightweight nginx/access-log format for demonstration, and can be extended to other formats as needed.[cite:17]

## Key Features

- Recursive scan of files/directories containing logs.
- Support for a generic "simple" format and a simplified nginx/access format.
- Automatic detection in `pattern="auto"` mode.
- Filtering of DEBUG messages (ignored by default to focus on higher-severity issues).
- Summary statistics: total entries, counts by level, hourly error distribution.
- PNG charts for level distribution and hourly error counts using matplotlib.
- Typer-based CLI with clear help and examples.

## Architecture

Project layout:

```text
src/
  log_analyzer/
    __init__.py
    __main__.py          # entry point: python -m log_analyzer
    cli.py               # Typer CLI: arguments, options, wiring
    parser.py            # log parsing utilities (simple + nginx-like)
    stats.py             # computation of summary statistics
    visualization.py     # matplotlib-based charts (PNG)

sample_logs/
  app_simple.log         # example application log in simple format
  nginx_access.log       # example nginx-style access log

tests/
  test_parser.py         # tests for parsing logic
  test_stats.py          # tests for statistics computation
  test_visualization.py  # tests for chart generation

pyproject.toml           # project metadata and scripts
requirements.txt         # runtime dependencies
.gitignore               # common ignores
README.md                # this document
```

## Installation

### Clone and create a virtual environment

```bash
git clone https://github.com/<your-username>/log-analyzer-cli.git
cd log-analyzer-cli

python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -r requirements.txt
```

### Install as a package (optional)

```bash
pip install .
```

After this, the `log-analyzer` script defined in `pyproject.toml` will be available on your PATH.

## Quickstart

Analyze sample logs included in the repository:

```bash
# Analyze sample application log and nginx access log
log-analyzer analyze sample_logs/app_simple.log sample_logs/nginx_access.log
```

Or using the module directly:

```bash
python -m log_analyzer sample_logs/app_simple.log sample_logs/nginx_access.log
```

Output will include a textual summary in the terminal and PNG charts in the `./reports` folder by default.

## Configuration

CLI options:

- `sources`: one or more files or directories to analyze.
- `--output / -o`: directory for generated reports and charts (default: `./reports`).
- `--pattern`: `auto`, `simple`, or `nginx`.
- `--include-debug`: include DEBUG-level messages in analysis.
- `--charts`: enable/disable chart generation.

Example:

```bash
log-analyzer analyze ./logs         --output ./reports         --pattern simple         --include-debug         --charts
```

## Examples

- **Focus on application logs only:**

  ```bash
  log-analyzer analyze sample_logs/app_simple.log --pattern simple
  ```

- **Analyze nginx access logs for error spikes:**

  ```bash
  log-analyzer analyze sample_logs/nginx_access.log --pattern nginx
  ```

- **Run analysis in CI for regression detection:**

  ```bash
  log-analyzer analyze ./logs --output ./reports --pattern auto --charts
  ```

## Tests

This project uses `pytest`.

```bash
pip install -r requirements.txt
pip install pytest
pytest
```

Test suite covers:

- parsing of simple and nginx-like log lines;
- auto pattern detection and DataFrame creation;
- summary statistics computation;
- chart generation (PNG files exist and have correct extension).

## Development

Recommended development workflow:

```bash
git clone https://github.com/<your-username>/log-analyzer-cli.git
cd log-analyzer-cli
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pip install pytest

# run tests
pytest

# run the CLI against sample logs
log-analyzer analyze sample_logs/app_simple.log sample_logs/nginx_access.log
```

Git workflow:

- use `main` as the stable branch;
- create feature branches (`feature/more-formats`, `feature/json-report`, etc.);
- use Pull Requests to review changes and keep commit history clean.

## Roadmap

Potential extensions:

- support for additional log formats (e.g. structured JSON logs);
- export of CSV/JSON reports with aggregated metrics;
- integration with alerting systems (Slack, email) for thresholds;
- web UI (Dash/Streamlit) for interactive exploration.

## License

This project is primarily intended as a learning and portfolio artifact. You may adapt it for your own use under MIT-style license terms.
