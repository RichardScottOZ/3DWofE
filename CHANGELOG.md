# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-11

### Added
- Complete package restructure with proper Python packaging
- Modern `pyproject.toml` configuration
- Modular architecture with separate modules:
  - `core.py`: Core mathematical functions
  - `wofe.py`: Standard Weights of Evidence
  - `fuzzy_wofe.py`: Fuzzy Weights of Evidence
  - `io.py`: Input/output operations
  - `cli.py`: Command-line interface
- Command-line interface with subcommands
- Type hints throughout the codebase
- Comprehensive docstrings
- Python API for programmatic access
- Example scripts demonstrating usage
- Professional README with quick start guide
- `.gitignore` for Python projects
- Logging instead of print statements

### Changed
- Removed hardcoded file paths (now use parameters)
- Modernized Python 2 code to Python 3
- Replaced `csv.writer` with "w" mode instead of "wb"
- Improved code organization and separation of concerns
- Enhanced error handling and validation
- Made all paths configurable

### Improved
- Code clarity with better naming conventions
- Efficiency with optimized algorithms
- Documentation with examples and API reference
- Robustness with input validation
- Maintainability with modular structure

### Removed
- Python 2 specific code (e.g., `itertools.izip`)
- Hardcoded Windows paths (D:/, C:/)
- Script-style code in favor of reusable modules

## [0.1.0] - 2020 (Original)

### Initial Release
- Original collection of Python scripts
- Separate folders for WofE and Fuzzy WofE
- Basic functionality for 3D WofE calculations
