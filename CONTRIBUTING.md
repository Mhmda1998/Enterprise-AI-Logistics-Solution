# Contributing to Enterprise AI Logistics Solution

Thank you for your interest in contributing! 🎉

## How to Contribute

1. **Fork** the repository
2. **Create a feature branch** (`git checkout -b feature/amazing-feature`)
3. **Commit your changes** (`git commit -m 'feat: add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open a Pull Request**

## Development Setup

```bash
# Clone your fork
git clone https://github.com/your-username/Enterprise-AI-Logistics-Solution.git
cd Enterprise-AI-Logistics-Solution

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Run linter
ruff check src tests
```

## Coding Standards

- **Style:** PEP 8, enforced via `ruff`
- **Type hints:** Required for all public functions
- **Docstrings:** Google-style for all modules, classes, and functions
- **Tests:** Required for new features (maintain >80% coverage)
- **Commits:** [Conventional Commits](https://www.conventionalcommits.org/) format

## Commit Convention

```
feat: add new feature
fix: bug fix
docs: documentation only
test: add or update tests
refactor: code change that neither fixes a bug nor adds a feature
chore: build, CI, or tooling changes
```

## Pull Request Process

1. Update the README.md with details of changes (if applicable)
2. Add tests for new functionality
3. Ensure CI passes (linting + tests)
4. Request review from a maintainer

## Reporting Bugs

Use [GitHub Issues](https://github.com/Mhmda1998/Enterprise-AI-Logistics-Solution/issues) with the `bug` label.

## Suggesting Features

Open an issue with the `enhancement` label and describe:
- The problem you're trying to solve
- Your proposed solution
- Any alternatives considered

## Code of Conduct

Be respectful, inclusive, and constructive. We're all here to learn and build great software together.

## Questions?

Open a discussion or reach out to the maintainer.
