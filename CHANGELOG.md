# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-06-11

### Added
- Modular project structure (`src/` package)
- Pydantic v2 models for request/response validation
- Configuration management via environment variables
- Comprehensive test suite (models, API, utilities)
- GitHub Actions CI/CD pipeline (lint, test, build)
- API documentation (`docs/API.md`)
- Architecture documentation (`docs/ARCHITECTURE.md`)
- Contributing guide (`CONTRIBUTING.md`)
- Python API client example (`examples/api_client.py`)
- Sample logistics data (`examples/sample_data.json`)
- `.gitignore` for Python projects
- CHANGELOG to track project history

### Changed
- Refactored `main.py` into modular components (`api.py`, `services.py`, `models.py`, `config.py`, `utils.py`)
- Improved dashboard with custom CSS, metrics, and better UX
- Enhanced README with comprehensive bilingual documentation
- Updated requirements with versioned dependencies

### Security
- Added input validation via Pydantic
- Improved API key handling
- Added CORS configuration
