# Contributing Guide

Thank you for your interest in contributing to robotframework-webservice! This guide will help you set up your local development environment.

## Prerequisites

- **[uv](https://docs.astral.sh/uv/getting-started/installation/)** installed (fast Python package manager and project manager)

## Local Development Setup

### 1. Clone the repository

```bash
git clone https://github.com/your-org/robotframework-webservice.git
cd robotframework-webservice
```

### 2. Install dependencies with uv

```bash
# Install main dependencies and dev tools
uv sync
```

This installs all project and development dependencies into a virtual environment.

### 3. Activate the virtual environment (optional)

```bash
# On Linux/macOS
source .venv/bin/activate

# On Windows
.venv\Scripts\activate
```

Or prefix commands with `uv run`:

```bash
uv run python --version
```

## Running Tests

Run the test suite using Python's unittest discovery:

```bash
# Run all tests
uv run python -m unittest discover -s tests -p "test_*.py"

# Run a specific test file
uv run python -m unittest tests.test_app

# Run a specific test class
uv run python -m unittest tests.test_app.EndpointTesttest_s

# Run a specific test method
uv run python -m unittest tests.test_app.EndpointTesttest_s.test_is_service_available
```

### In VS Code

- Install the **Python** extension (ms-python.python)
- Open the Testing panel (beaker icon in sidebar)
- Tests should auto-discover; click **Refresh Tests** if needed
- Click on any test to run it, or run all tests

## Running the Service

Start the FastAPI web service:

```bash
uv run uvicorn RobotFrameworkService.main:app --reload
```

The service will be available at `http://localhost:8000`. View API docs at `http://localhost:8000/docs`.

## Code Quality

The project uses:

- **[RobotCode](https://robotcode.io/)** – Language server and linter for Robot Framework
- **[Robocop](https://robocop.readthedocs.io/)** – Static analysis for Robot Framework

Run checks:

```bash
# Lint Robot Framework files
uv run robocop examples/ tests/

# Use RobotCode for analysis (via VS Code extension or CLI)
uv run robotcode --help
```

## Development Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make your changes and add tests
3. Run tests locally: `uv run python -m unittest discover -s tests -p "test_*.py"`
4. Commit and push: `git push origin feature/your-feature`
5. Open a pull request

## Troubleshooting

**Tests not discovered in VS Code?**
- Ensure `tests/__init__.py` exists
- Run `Python: Discover Tests` from the command palette
- Reload VS Code if needed

**Module import errors?**
- Verify the virtual environment is active: `uv run python -c "import sys; print(sys.executable)"`
- Install dependencies: `uv sync`
