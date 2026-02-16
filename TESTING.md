# Testing Guide

Comprehensive guide for running and writing tests for MarkItDown Desktop Converter.

## Table of Contents

- [Quick Start](#quick-start)
- [Test Categories](#test-categories)
- [Running Tests Locally](#running-tests-locally)
- [Writing New Tests](#writing-new-tests)
- [Regression Testing](#regression-testing)
- [CI/CD Pipeline](#cicd-pipeline)
- [Troubleshooting](#troubleshooting)

## Quick Start

```bash
# Install test dependencies
pip install -r requirements-test.txt

# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Open coverage report
open htmlcov/index.html  # macOS
# or
start htmlcov/index.html  # Windows
```

## Test Categories

### Unit Tests (`tests/unit/`)
**Individual module testing without external dependencies**

- `test_text_cleaner.py` - 40+ tests for text cleaning
  - Ligature fixing
  - Hyphenation artifacts
  - Medical term preservation
  - Special character handling

Run: `pytest tests/unit/ -v`

### Integration Tests (`tests/integration/`)
**End-to-end conversion workflows with real documents**

- `test_converter.py` - 20+ tests for full conversion pipeline
  - PDF to Markdown conversion
  - PowerPoint conversion
  - Error handling
  - Output quality validation

Run: `pytest tests/integration/ -v`

### Regression Tests (`tests/regression/`)
**CRITICAL: Prevents quality degradation (v2.3.2 incident prevention)**

- `test_quality_regression.py` - 15+ tests preventing regressions
  - Known artifact prevention
  - Internal link pollution detection
  - Quality baseline enforcement
  - Output determinism

Run: `pytest tests/regression/ -v -m regression`

## Running Tests Locally

### Prerequisites

```bash
# System dependencies
# Ubuntu/Debian:
sudo apt-get install ghostscript python3-tk poppler-utils

# macOS:
brew install ghostscript tcl-tk poppler

# Windows:
choco install ghostscript

# Python dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt
```

### Basic Commands

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/unit/test_text_cleaner.py

# Run specific test
pytest tests/unit/test_text_cleaner.py::TestLigatureFixing::test_fix_artificial_lowercase

# Run tests matching pattern
pytest -k "ligature"

# Run with verbose output
pytest -v

# Run only regression tests
pytest -m regression

# Run only quality tests
pytest -m quality

# Skip slow tests
pytest -m "not slow"
```

### Coverage Reports

```bash
# Generate coverage report
pytest --cov=src --cov-report=html --cov-report=term-missing

# Check coverage threshold (70%)
pytest --cov=src --cov-fail-under=70

# Coverage for specific module
pytest tests/unit/test_text_cleaner.py --cov=src/text_cleaner
```

### Performance Testing

```bash
# Run benchmark tests
pytest tests/unit/test_text_cleaner.py::TestPerformance -v

# With benchmark plugin
pip install pytest-benchmark
pytest --benchmark-only
```

## Writing New Tests

### Test Structure

```python
import pytest
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from your_module import YourClass

class TestYourFeature:
    """Test suite for your feature"""
    
    @pytest.fixture
    def setup(self):
        """Setup for each test"""
        return YourClass()
    
    def test_basic_functionality(self, setup):
        """Test basic functionality"""
        result = setup.your_method()
        assert result is not None
```

### Using Fixtures

```python
# Use built-in fixtures from conftest.py
def test_with_pdf(medical_paper_pdf):
    """Test using medical paper PDF fixture"""
    assert medical_paper_pdf.exists()

def test_with_temp_dir(temp_output_dir):
    """Test using temporary directory"""
    output_file = temp_output_dir / "output.md"
    output_file.write_text("test")
    assert output_file.exists()
```

### Test Markers

```python
@pytest.mark.slow
def test_large_file():
    """Slow test - skipped in quick runs"""
    pass

@pytest.mark.quality
@pytest.mark.regression
def test_quality_baseline():
    """Critical quality test"""
    pass

@pytest.mark.requires_ghostscript
def test_table_extraction():
    """Test requiring Ghostscript"""
    pass
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input_text,expected", [
    ("arti fi cial", "artificial"),
    ("de fi ned", "defined"),
    ("speci fi c", "specific"),
])
def test_ligature_patterns(cleaner, input_text, expected):
    result = cleaner.clean(input_text)
    assert expected in result.lower()
```

## Regression Testing

### Creating Baseline

**IMPORTANT: Only run this on v2.2.1 (current stable version)**

```bash
# Generate baseline scores
python tests/regression/generate_baseline.py

# This creates: tests/regression/baseline_scores_v2.2.1.json
```

### Baseline Format

```json
{
  "version": "v2.2.1",
  "generated_at": "2026-02-16T19:00:00",
  "documents": {
    "TIM-HF3 fcvm-11-1457995.pdf": {
      "success": true,
      "scores": {
        "length": 45230,
        "line_count": 892,
        "ligature_artifacts": 0,
        "internal_link_pollution": 0
      }
    }
  }
}
```

### Regression Test Workflow

1. **Baseline exists** → Tests compare against baseline
2. **No baseline** → Tests check for known issues only
3. **Degradation detected** → Test fails with detailed message

### Critical Regression Checks

✅ **PASS Criteria:**
- No ligature artifacts ("arti fi cial")
- No internal link pollution ([the](#page-7))
- No hyphenation artifacts ("non- invasive")
- Medical terms properly formatted
- Deterministic output (same input = same output)

❌ **FAIL Criteria:**
- Any known artifact reappears
- Quality scores degrade >2%
- Non-deterministic output
- Output length changes significantly (±10%)

## CI/CD Pipeline

### GitHub Actions Workflow

Automatically runs on:
- Every push to `main` or `develop`
- All pull requests
- Manual trigger

### Test Matrix (9 environments)

| OS | Python 3.10 | Python 3.11 | Python 3.12 |
|----|-------------|-------------|-------------|
| Ubuntu | ✅ | ✅ | ✅ |
| Windows | ✅ | ✅ | ✅ |
| macOS | ✅ | ✅ | ✅ |

### Workflow Steps

1. **Setup**: Install system dependencies
2. **Unit Tests**: Fast feedback (2-5 min)
3. **Integration Tests**: Real document conversion (5-10 min)
4. **Regression Tests**: Quality validation (2-5 min)
5. **Coverage**: Report generation and upload
6. **Quality**: Code formatting and linting

### CI Status

Check CI status:
- View badge in README
- Check Actions tab: https://github.com/Wei-power3/markitdown-desktop-converter/actions

### Coverage Reporting

- Uploaded to Codecov after each run
- 70% minimum coverage required
- View detailed coverage: Click badge in README

## Troubleshooting

### Common Issues

**Import errors:**
```bash
# Ensure src is in Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/src"
# Or add to pytest.ini
```

**Missing test files:**
```bash
# Ensure test PDFs are downloaded
git lfs pull
# Or check tests/fixtures/sample_pdfs/
```

**Ghostscript not found:**
```bash
# Ubuntu:
sudo apt-get install ghostscript
# macOS:
brew install ghostscript
# Windows:
choco install ghostscript
```

**Tests pass locally but fail in CI:**
- Check Python version (CI uses 3.10, 3.11, 3.12)
- Check system dependencies
- Check file paths (use Path objects, not strings)
- Check for OS-specific issues

### Getting Help

1. Check test output: `pytest -v --tb=long`
2. Check coverage: `pytest --cov=src --cov-report=html`
3. Run specific failing test: `pytest -k test_name -v`
4. Check GitHub Issues

## Test Quality Standards

### Code Coverage Targets

| Module | Target Coverage |
|--------|----------------|
| text_cleaner.py | 90%+ |
| converter.py | 80%+ |
| table_extractor.py | 75%+ |
| Overall | 70%+ |

### Test Requirements for PRs

✅ **Required:**
- All existing tests pass
- Coverage ≥70%
- New features have tests
- Bug fixes have regression tests

✅ **Recommended:**
- Add integration test for major features
- Add regression test if fixing quality issue
- Update baseline if intentionally changing output

## Best Practices

1. **Test names should be descriptive**
   - ✅ `test_ligature_artifacts_are_fixed`
   - ❌ `test_cleaning`

2. **One assertion per test (when possible)**
   - Makes failures easier to diagnose

3. **Use fixtures for setup**
   - Reduces code duplication
   - Makes tests more maintainable

4. **Mark slow tests**
   - `@pytest.mark.slow` for tests >5 seconds
   - Allows quick test runs: `pytest -m "not slow"`

5. **Write regression tests for bugs**
   - Every bug fix should have a test
   - Prevents regression

6. **Keep tests independent**
   - Tests should not depend on each other
   - Use fixtures for shared setup

## Contributing Tests

See [CONTRIBUTING.md](CONTRIBUTING.md) for:
- Testing requirements for pull requests
- Code quality standards
- Review process