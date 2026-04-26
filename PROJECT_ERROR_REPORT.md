# SOC Alert Automation Pipeline Error Report

Prepared by: Brian Bovell

## 1. Executive Summary

This report documents the major errors identified and corrected in the SOC Alert Automation Pipeline project. The issues affected syntax, runtime behavior, command-line execution, data validation, parsing, caching, scoring, reporting, tests, and local development workflow.

Several defects prevented the application from running successfully, including invalid Python syntax, incomplete functions, undefined variables, inconsistent model values, and incorrect file handling. After remediation, the core validation command, pipeline execution, and automated tests completed successfully.

## 2. Project Scope

The review covered the following project areas:

- Command-line interface
- IOC extraction and parsing
- Enrichment result scoring
- Pydantic data models
- Report generation
- Disk cache handling
- Logging setup
- Unit tests
- Local shell commands and file path usage
- Automation file placement

## 3. Summary Of Corrected Issues

### 3.1 Command-Line Interface Issues

File reviewed: `socbot/cli.py`

The command-line interface contained invalid Python syntax in the logging statement. This prevented the module from importing and stopped the application before any command could run.

The CLI also referenced variables that were not defined, including `config_path`, `config_file`, and `handle`. There was also a typo in `cofig_file`, which caused the intended config variable to be unavailable.

The original pipeline function was incomplete and stopped before enrichment, scoring, case creation, and report writing were fully connected.

Corrective actions:

- Rebuilt the CLI with working `validate` and `run` subcommands.
- Added proper argument parsing.
- Added config loading with safe fallback behavior.
- Connected alert loading, IOC deduplication, enrichment, scoring, severity assignment, recommendations, and report generation.
- Added a proper `main()` entry point for `python -m socbot.cli`.

### 3.2 Scoring Module Issues

File reviewed: `socbot/scoring.py`

The scoring module contained several syntax and logic errors. One variable name contained a space, which is invalid Python syntax. The module also referenced undefined names and ended with an incomplete function definition.

Examples of issues found:

- Invalid variable name: `bad count`
- Incorrect import of `severity`
- Missing import of `Severity`
- Undefined variable `enrichments`
- Undefined variable `weights`
- Misspelled function name `severrity_from_score`
- Incomplete function definition at the end of the file

Corrective actions:

- Rebuilt `compute_score()`.
- Added `severity_from_score()`.
- Added default risk weights.
- Added score clamping between `0` and `100`.
- Added `recommendation_from_severity()`.
- Added support for the `suspicious` verdict.

### 3.3 Data Model Issues

File reviewed: `socbot/models.py`

The `Verdict` type did not include `suspicious`, even though the scoring test and scoring logic expected it to be a valid enrichment result.

Original accepted values:

```python
"malicious", "benign", "unknown"
```

Corrected accepted values:

```python
"malicious", "suspicious", "benign", "unknown"
```

Corrective action:

- Updated the `Verdict` literal type to include `suspicious`.

### 3.4 Alert Parsing Issues

File reviewed: `socbot/parse.py`

The parser had indentation and control flow problems. CSV files were not handled cleanly, the unsupported file type error was unreachable, and IOC extraction was not correctly scoped inside the alert loop.

Corrective actions:

- Fixed CSV loading control flow.
- Added JSON input support.
- Improved missing file error handling.
- Corrected IOC extraction indentation.
- Removed an unused IOC extraction variable.
- Ensured each alert receives its own parsed IOC list.

### 3.5 Cache Handling Issues

File reviewed: `socbot/cache.py`

The disk cache path was incorrectly assigned.

Original issue:

```python
self.PATH = Path(Path)
```

This did not use the configured cache directory and would prevent proper cache file handling.

Corrective action:

- Changed the cache path to use the configured cache directory and write to `cache.json`.

### 3.6 Report Generation Issues

File reviewed: `socbot/report.py`

The JSON report writer double-encoded JSON output. The Markdown report writer also placed the `encoding` argument outside the `write_text()` function call.

Corrective actions:

- Wrote JSON directly from `model_dump_json()`.
- Fixed Markdown writing with the correct `encoding="utf-8"` argument placement.

### 3.7 Logging Setup Issue

File reviewed: `socbot/logging_setup.py`

The logging setup used `path` instead of `Path`, which caused a runtime failure.

Corrective action:

- Replaced `path(out_dir)` with `Path(out_dir)`.

### 3.8 Python Version Compatibility Issues

The project metadata specifies Python 3.10 or newer. However, the local environment was using Python 3.9.6. Some syntax was incompatible with Python 3.9, including union type syntax such as `IOC | None`.

Corrective actions:

- Replaced incompatible union syntax with `Optional[...]` where needed.
- Verified the CLI commands using the project virtual environment.

Recommendation:

- Recreate the virtual environment with Python 3.10 or newer to match the project metadata.

### 3.9 Test Alignment Issue

File reviewed: `tests/test_scoring.py`

The scoring test expected capitalized severity values, but the application model defines severity values in lowercase.

Expected by test before correction:

```python
"Medium", "High", "Critical"
```

Actual model values:

```python
"medium", "high", "critical"
```

Corrective action:

- Updated the test to match the application model contract.

### 3.10 Local Shell And Path Issues

There were local command issues involving relative paths and heredoc usage.

The systemd service file existed at:

```text
socbot/automation/systemd/socbot.service
```

When the terminal was already inside the `systemd` directory, the correct relative path was:

```text
socbot.service
```

The README heredoc issue occurred because the closing marker `EOF` was missing. The shell continued to display `heredoc>` while waiting for the closing marker.

Corrective guidance:

- Use paths relative to the current terminal directory.
- Close heredoc blocks with the exact marker on its own line.

## 4. Validation Results

The validation command completed successfully:

```bash
python -m socbot.cli validate --input data/alerts.csv
```

Result:

```text
OK: loaded 3 alerts and extracted 5 IOCs
```

The full pipeline command completed successfully:

```bash
python -m socbot.cli run --input data/alerts.csv --output out --config config.yaml
```

Generated outputs:

- `out/case.json`
- `out/report.md`

The test suite completed successfully:

```bash
pytest -q
```

Result:

```text
6 passed
```

## 5. Professional Recommendations

1. Use Python 3.10 or newer consistently for this project.
2. Add continuous integration with `pytest` and `ruff`.
3. Add CLI tests for both `validate` and `run`.
4. Add a sample `config.yaml`.
5. Keep verdict and severity values centralized in `models.py`.
6. Ensure tests match the application data model.
7. Move deployment assets to a top-level `automation/` directory if they are not intended to be part of the Python package.
8. Avoid large shell heredocs for project documentation when direct file editing is available.

## 6. Conclusion

The project had multiple issues that affected basic execution, data processing, scoring, and reporting. The most critical blockers were corrected, and the project now supports validation, full pipeline execution, and passing unit tests. Additional cleanup and environment standardization are recommended before production or portfolio presentation.
