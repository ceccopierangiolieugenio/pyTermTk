# ttkode Tests

This directory contains the test suite for the ttkode application.

## Test Structure

- **conftest.py** - Pytest configuration and fixtures
- **test_plugin.py** - Tests for the plugin system (TTkodePlugin and related classes)
- **test_config.py** - Tests for configuration management (TTKodeCfg)
- **test_proxy.py** - Tests for proxy functionality (TTKodeViewerProxy, TTKodeProxy)
- **test_search_file.py** - Tests for file search functionality
- **test_helper.py** - Tests for helper functions (TTkodeHelper)

## Running Tests

### Run all tests

```bash
cd apps/ttkode
pytest tests/
```

### Run specific test file

```bash
pytest tests/test_plugin.py
pytest tests/test_config.py
pytest tests/test_search_file.py
```

### Run with verbose output

```bash
pytest tests/ -v
```

### Run with coverage

```bash
pytest tests/ --cov=ttkode --cov-report=html
```

### Run specific test

```bash
pytest tests/test_plugin.py::TestTTkodePlugin::test_plugin_basic_creation
```

## Test Coverage

The test suite covers:

- **Plugin System**: Creation, registration, callbacks, widget management
- **Configuration**: Default values, saving, loading, path management
- **Proxy**: Viewer proxy functionality and file name management
- **File Search**: Pattern matching, .gitignore support, directory walking
- **Helpers**: Plugin loading and execution

## Notes

Some tests are marked as skipped (`@pytest.mark.skip`) because they require:
- Full TTKode UI instance setup
- Plugin folder and file system setup
- Complex UI mocking infrastructure

These integration tests can be completed when the UI testing infrastructure is available.

## Requirements

Tests require:
- pytest
- pyTermTk
- Python 3.9+

All dependencies are listed in the main `pyproject.toml` file.
