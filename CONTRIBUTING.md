# Contributing to MarkItDown Desktop Converter

Thank you for your interest in contributing! This project prioritizes **quality over speed**, with automated testing ensuring reliability.

## Code of Conduct

Be respectful, professional, and constructive in all interactions.

## Getting Started

### 1. Fork and Clone

```bash
git clone https://github.com/YOUR_USERNAME/markitdown-desktop-converter.git
cd markitdown-desktop-converter
```

### 2. Set Up Development Environment

```bash
# Install dependencies
pip install -r requirements.txt
pip install -r requirements-test.txt

# System dependencies (Ubuntu)
sudo apt-get install ghostscript python3-tk poppler-utils

# System dependencies (macOS)
brew install ghostscript tcl-tk poppler

# System dependencies (Windows)
choco install ghostscript
```

### 3. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-number-description
```

## Development Workflow

### Making Changes

1. **Write tests first** (TDD approach recommended)
2. **Implement feature/fix**
3. **Run tests locally**
4. **Update documentation**
5. **Commit with clear messages**

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test category
pytest tests/unit/ -v          # Unit tests
pytest tests/integration/ -v   # Integration tests
pytest tests/regression/ -v    # Regression tests

# Check coverage meets 70% threshold
pytest --cov=src --cov-fail-under=70
```

### Code Quality

```bash
# Format code with Black
black src/ tests/

# Lint with Flake8
flake8 src/ tests/ --max-line-length=100

# Type check (optional but recommended)
mypy src/ --ignore-missing-imports
```

## Testing Requirements

### For All Pull Requests

✅ **Required:**
- All existing tests must pass
- Code coverage ≥70%
- No regression in quality metrics
- Tests for new functionality
- Regression tests for bug fixes

✅ **Recommended:**
- Integration tests for major features
- Performance benchmarks for optimizations
- Documentation updates

### Test Categories

#### Unit Tests
**When to write:**
- New utility functions
- New classes or methods
- Bug fixes in isolated modules

**Example:**
```python
def test_new_text_cleaning_feature(cleaner):
    """Test new text cleaning feature"""
    input_text = "example with issue"
    result = cleaner.clean(input_text)
    assert "expected output" in result
```

#### Integration Tests
**When to write:**
- New conversion features
- Changes to conversion pipeline
- File format support

**Example:**
```python
def test_new_format_conversion(converter, tmp_path):
    """Test conversion of new file format"""
    input_file = tmp_path / "test.newformat"
    markdown, error = converter.convert_file(input_file)
    assert error is None
    assert len(markdown) > 0
```

#### Regression Tests
**When to write:**
- Fixing quality issues
- Preventing known bugs
- Critical bug fixes

**Example:**
```python
@pytest.mark.regression
@pytest.mark.quality
def test_issue_123_no_longer_occurs(converter):
    """Test that issue #123 (artifact reappearance) is fixed"""
    markdown, _ = converter.convert_file(test_file)
    assert "bad artifact" not in markdown
```

## Pull Request Process

### Before Submitting

- [ ] All tests pass locally
- [ ] Code coverage ≥70%
- [ ] Code formatted with Black
- [ ] No Flake8 warnings (critical)
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (if applicable)

### PR Title Format

```
[Type] Short description

Types:
- Feature: New functionality
- Fix: Bug fix
- Docs: Documentation changes
- Test: Test additions/changes
- Refactor: Code refactoring
- Quality: Quality improvements
```

**Examples:**
- `[Feature] Add support for DOCX files`
- `[Fix] Resolve ligature artifacts in medical terms`
- `[Test] Add regression tests for v2.3.2 issues`
- `[Quality] Improve text cleaning accuracy`

### PR Description Template

```markdown
## Description
Brief description of changes

## Motivation
Why is this change needed?

## Changes Made
- List specific changes
- Include file changes

## Testing
- [ ] Added unit tests
- [ ] Added integration tests
- [ ] Added regression tests (if bug fix)
- [ ] All tests pass locally
- [ ] Coverage ≥70%

## Related Issues
Closes #123
Fixes #456

## Screenshots (if applicable)
```

### Review Process

1. **Automated checks** run on PR (GitHub Actions)
2. **Code review** by maintainer
3. **Testing** on multiple platforms
4. **Approval** and merge

## Quality Standards

### Code Style

- **PEP 8** compliance
- **Black** formatting (line length: 100)
- **Type hints** encouraged
- **Docstrings** for public functions

### Testing Standards

- **Descriptive test names**: `test_ligatures_are_fixed_in_medical_papers`
- **One concept per test**: Test one thing at a time
- **Arrange-Act-Assert** pattern
- **Use fixtures**: Avoid code duplication

### Documentation Standards

- **Clear docstrings** for public APIs
- **README updates** for new features
- **TESTING.md updates** for new test patterns
- **Inline comments** for complex logic

## Common Contribution Types

### Adding Text Cleaning Rules

1. Add pattern to `src/text_cleaner.py`
2. Add unit test to `tests/unit/test_text_cleaner.py`
3. Add regression test if fixing known issue
4. Update documentation

### Fixing Quality Issues

1. **Identify root cause**
2. **Write regression test** that fails
3. **Implement fix**
4. **Verify test passes**
5. **Check for side effects**

### Adding File Format Support

1. Add conversion logic to `src/converter.py`
2. Add integration test with sample file
3. Update README with supported formats
4. Add format-specific error handling

### Improving Performance

1. **Benchmark current performance**
2. **Implement optimization**
3. **Add benchmark test**
4. **Verify no quality regression**
5. **Document performance gains**

## Issue Reporting

### Bug Reports

```markdown
**Description**
Clear description of the bug

**To Reproduce**
1. Steps to reproduce
2. Expected behavior
3. Actual behavior

**Environment**
- OS: [e.g., Windows 11]
- Python version: [e.g., 3.11]
- Version: [e.g., v2.2.1]

**Sample File**
Attach file that reproduces issue (if possible)
```

### Feature Requests

```markdown
**Feature Description**
What feature would you like?

**Use Case**
Why is this feature needed?

**Proposed Solution**
How might this be implemented?

**Alternatives Considered**
What alternatives did you consider?
```

## Priority System

### Critical
- Quality regressions
- Data loss issues
- Security issues

### High
- Bug fixes
- Performance issues
- Major feature requests

### Medium
- Minor bugs
- Feature enhancements
- Documentation improvements

### Low
- Code refactoring
- Nice-to-have features
- Cosmetic improvements

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Credited in relevant documentation

## Questions?

- **Documentation**: Check [TESTING.md](TESTING.md) and README
- **Issues**: Open a GitHub issue
- **Discussions**: Use GitHub Discussions

## License

By contributing, you agree that your contributions will be licensed under the same license as the project.

Thank you for helping make MarkItDown Desktop Converter better! 🚀