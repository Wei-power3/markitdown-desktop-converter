# Excel Test Fixtures

This directory contains real-world Excel files for testing the Excel conversion functionality.

## Files

1. **Costing-template.xls.xlsx** (59KB)
   - Multi-sheet healthcare costing template
   - Tests: Multi-sheet handling, formulas, £ symbols
   - 4 sheets with complex structure

2. **Introduction-to-Evidence-Synthesis-Solutions.xls** (98KB)
   - Legacy .xls format (Excel 97-2003)
   - Tests: Legacy format support, statistical data
   - Meta-analysis data tables

3. **Reference_costs_index.xlsx** (156KB)
   - Large NHS reference costs dataset
   - Tests: Large files, many columns, real healthcare data
   - Multiple sheets with extensive tabular data

4. **MINERVA-Prolutamide.xlsx** (210KB)
   - Complex pharmaceutical financial model
   - Tests: Complex formulas, multiple sheets, financial data
   - Model structure with calculations

## Adding Files

**These test fixtures need to be uploaded manually** as they are binary files.

To add the Excel files:

```bash
# Copy your Excel files to this directory
cp /path/to/Costing-template.xls.xlsx tests/fixtures/sample_excel/
cp /path/to/Introduction-to-Evidence-Synthesis-Solutions.xls tests/fixtures/sample_excel/
cp /path/to/Reference_costs_index.xlsx tests/fixtures/sample_excel/
cp /path/to/MINERVA-Prolutamide.xlsx tests/fixtures/sample_excel/

# Commit and push
git add tests/fixtures/sample_excel/*.xls*
git commit -m "Add Excel test fixtures"
git push
```

## Running Tests

```bash
# Run all Excel tests
pytest tests/ -k "excel" -v

# Run specific test file
pytest tests/unit/test_excel_conversion.py -v
pytest tests/integration/test_excel_workflow.py -v
pytest tests/regression/test_excel_regression.py -v

# Run with coverage
pytest tests/ -k "excel" --cov=src --cov-report=html
```

## Test Coverage

- **Unit Tests:** 25+ tests covering basic conversion, multi-sheet, data types, error handling
- **Integration Tests:** 10+ tests covering end-to-end workflows, batch processing, quality
- **Regression Tests:** 10+ tests preventing quality degradation

**Total: 45+ tests for Excel functionality**
