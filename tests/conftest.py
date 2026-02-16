"""
Shared pytest fixtures and configuration for all tests.

Provides reusable test fixtures, helper functions, and test setup/teardown.
"""

import pytest
import tempfile
import shutil
from pathlib import Path
import sys

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))


@pytest.fixture
def temp_output_dir():
    """
    Fixture providing a temporary output directory for test conversions.
    
    Automatically cleaned up after test completes.
    
    Yields:
        Path: Temporary directory path
    """
    tmpdir = tempfile.mkdtemp(prefix="markitdown_test_")
    yield Path(tmpdir)
    # Cleanup
    shutil.rmtree(tmpdir, ignore_errors=True)


@pytest.fixture
def fixtures_dir():
    """
    Fixture providing path to test fixtures directory.
    
    Returns:
        Path: tests/fixtures directory
    """
    return Path(__file__).parent / "fixtures"


@pytest.fixture
def sample_pdfs_dir(fixtures_dir):
    """
    Fixture providing path to sample PDFs directory.
    
    Returns:
        Path: tests/fixtures/sample_pdfs directory
    """
    return fixtures_dir / "sample_pdfs"


@pytest.fixture
def sample_pptx_dir(fixtures_dir):
    """
    Fixture providing path to sample PowerPoint files directory.
    
    Returns:
        Path: tests/fixtures/sample_pptx directory
    """
    return fixtures_dir / "sample_pptx"


@pytest.fixture
def expected_outputs_dir(fixtures_dir):
    """
    Fixture providing path to expected output files directory.
    
    Returns:
        Path: tests/fixtures/expected_outputs directory
    """
    return fixtures_dir / "expected_outputs"


@pytest.fixture
def medical_paper_pdf(sample_pdfs_dir):
    """
    Fixture providing path to TIM-HF3 medical research paper.
    
    Complex academic paper with:
    - Tables and figures
    - Academic structure (Abstract, Methods, Results)
    - Medical terminology
    - References section
    
    Returns:
        Path: TIM-HF3-fcvm-11-1457995.pdf
    """
    pdf_path = sample_pdfs_dir / "TIM-HF3-fcvm-11-1457995.pdf"
    if not pdf_path.exists():
        pytest.skip(f"Test fixture not found: {pdf_path}")
    return pdf_path


@pytest.fixture
def review_paper_pdf(sample_pdfs_dir):
    """
    Fixture providing path to heart failure review paper.
    
    Medical review article with:
    - Academic structure
    - Medical terminology
    - Literature review format
    
    Returns:
        Path: heart_failure_disease_management_program__a_review.17.pdf
    """
    pdf_path = sample_pdfs_dir / "heart_failure_disease_management_program__a_review.17.pdf"
    if not pdf_path.exists():
        pytest.skip(f"Test fixture not found: {pdf_path}")
    return pdf_path


@pytest.fixture
def presentation_pdf(sample_pdfs_dir):
    """
    Fixture providing path to Boston JP Morgan presentation.
    
    Business presentation with:
    - Slide-like structure
    - Charts and graphics
    - Business terminology
    
    Returns:
        Path: Boston-jp-morgan-healthcare-conference-2025.pdf
    """
    pdf_path = sample_pdfs_dir / "Boston-jp-morgan-healthcare-conference-2025.pdf"
    if not pdf_path.exists():
        pytest.skip(f"Test fixture not found: {pdf_path}")
    return pdf_path


@pytest.fixture(scope="session")
def baseline_scores_file():
    """
    Fixture providing path to baseline quality scores file.
    
    This file stores v2.2.1 quality benchmarks for regression testing.
    
    Returns:
        Path: tests/regression/baseline_scores_v2.2.1.json
    """
    return Path(__file__).parent / "regression" / "baseline_scores_v2.2.1.json"


def pytest_configure(config):
    """
    Pytest configuration hook.
    
    Executed before test collection.
    """
    # Register custom markers
    config.addinivalue_line(
        "markers", "quality: Quality assurance and benchmarking tests"
    )


def pytest_collection_modifyitems(config, items):
    """
    Modify test collection to apply markers automatically.
    
    Args:
        config: Pytest config object
        items: List of collected test items
    """
    for item in items:
        # Auto-mark regression tests as quality tests
        if "regression" in str(item.fspath):
            item.add_marker(pytest.mark.quality)
            item.add_marker(pytest.mark.regression)
        
        # Auto-mark slow tests
        if "large" in item.name or "benchmark" in item.name:
            item.add_marker(pytest.mark.slow)