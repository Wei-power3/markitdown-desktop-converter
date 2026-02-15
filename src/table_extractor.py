"""
Table extraction utilities for structured data from PDFs
"""
from pathlib import Path
from typing import List, Dict, Optional
import logging

try:
    import camelot
    CAMELOT_AVAILABLE = True
except ImportError:
    CAMELOT_AVAILABLE = False
    logging.warning("Camelot not available. Table extraction will be limited.")

try:
    import tabula
    TABULA_AVAILABLE = True
except ImportError:
    TABULA_AVAILABLE = False
    logging.warning("Tabula not available. Using fallback table extraction.")

import pandas as pd


class TableExtractor:
    """
    Extracts structured tables from PDF documents.
    
    Uses multiple extraction methods:
    1. Camelot (best for complex tables with borders)
    2. Tabula (good for borderless tables)
    3. Fallback to basic extraction
    """
    
    def __init__(self, min_accuracy: float = 0.5):
        """
        Args:
            min_accuracy: Minimum confidence score for table extraction (0-1)
        """
        self.min_accuracy = min_accuracy
        self.logger = logging.getLogger(__name__)
    
    def extract_tables(self, pdf_path: Path) -> List[Dict]:
        """
        Extract all tables from a PDF.
        
        Args:
            pdf_path: Path to PDF file
        
        Returns:
            List of dictionaries containing table data:
            [
                {
                    'page': int,
                    'table_num': int,
                    'markdown': str,
                    'accuracy': float,
                    'method': str,
                    'rows': int,
                    'cols': int
                },
                ...
            ]
        """
        tables = []
        
        # Try Camelot first (best quality)
        if CAMELOT_AVAILABLE:
            camelot_tables = self._extract_with_camelot(pdf_path)
            tables.extend(camelot_tables)
        
        # If no tables found, try Tabula
        if not tables and TABULA_AVAILABLE:
            tabula_tables = self._extract_with_tabula(pdf_path)
            tables.extend(tabula_tables)
        
        # Sort by page and table number
        tables.sort(key=lambda x: (x.get('page', 0), x.get('table_num', 0)))
        
        return tables
    
    def _extract_with_camelot(self, pdf_path: Path) -> List[Dict]:
        """
        Extract tables using Camelot (best for bordered tables).
        """
        tables = []
        
        try:
            # Try lattice method (tables with clear borders)
            camelot_tables = camelot.read_pdf(
                str(pdf_path),
                pages='all',
                flavor='lattice',
                strip_text='\n'
            )
            
            for i, table in enumerate(camelot_tables):
                if table.accuracy >= self.min_accuracy:
                    df = table.df
                    tables.append({
                        'page': table.page,
                        'table_num': i + 1,
                        'markdown': self._dataframe_to_markdown(df),
                        'accuracy': table.accuracy,
                        'method': 'camelot-lattice',
                        'rows': len(df),
                        'cols': len(df.columns)
                    })
            
            # If no tables found, try stream method (borderless tables)
            if not tables:
                camelot_tables = camelot.read_pdf(
                    str(pdf_path),
                    pages='all',
                    flavor='stream',
                    strip_text='\n'
                )
                
                for i, table in enumerate(camelot_tables):
                    if table.accuracy >= self.min_accuracy:
                        df = table.df
                        tables.append({
                            'page': table.page,
                            'table_num': i + 1,
                            'markdown': self._dataframe_to_markdown(df),
                            'accuracy': table.accuracy,
                            'method': 'camelot-stream',
                            'rows': len(df),
                            'cols': len(df.columns)
                        })
        
        except Exception as e:
            self.logger.warning(f"Camelot extraction failed: {e}")
        
        return tables
    
    def _extract_with_tabula(self, pdf_path: Path) -> List[Dict]:
        """
        Extract tables using Tabula (good fallback).
        """
        tables = []
        
        try:
            dfs = tabula.read_pdf(
                str(pdf_path),
                pages='all',
                multiple_tables=True,
                lattice=True,
                stream=False
            )
            
            for i, df in enumerate(dfs):
                if not df.empty and len(df) > 1:  # Skip single-row "tables"
                    tables.append({
                        'table_num': i + 1,
                        'markdown': self._dataframe_to_markdown(df),
                        'accuracy': 0.8,  # Tabula doesn't provide accuracy
                        'method': 'tabula',
                        'rows': len(df),
                        'cols': len(df.columns)
                    })
        
        except Exception as e:
            self.logger.warning(f"Tabula extraction failed: {e}")
        
        return tables
    
    def _dataframe_to_markdown(self, df: pd.DataFrame) -> str:
        """
        Convert pandas DataFrame to clean markdown table.
        """
        # Clean the dataframe
        df = df.copy()
        
        # Remove completely empty rows
        df = df.dropna(how='all')
        
        # Remove completely empty columns
        df = df.dropna(axis=1, how='all')
        
        # Replace NaN with empty string
        df = df.fillna('')
        
        # Clean cell contents
        for col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].str.replace('\n', ' ')  # Remove newlines in cells
            df[col] = df[col].str.replace('\r', '')
            df[col] = df[col].str.replace('  +', ' ', regex=True)  # Multiple spaces
        
        # Check if first row looks like header
        first_row_has_text = df.iloc[0].astype(str).str.len().sum() > 0
        
        if first_row_has_text and self._is_likely_header(df.iloc[0]):
            # Use first row as header
            df.columns = df.iloc[0]
            df = df[1:]
        
        # Convert to markdown
        try:
            markdown = df.to_markdown(index=False)
        except:
            # Fallback if to_markdown fails
            markdown = self._manual_markdown_table(df)
        
        return markdown
    
    def _is_likely_header(self, row) -> bool:
        """
        Determine if a row is likely a header row.
        """
        row_str = ' '.join(row.astype(str).values)
        
        # Headers usually have:
        # - Shorter text
        # - More capitals
        # - Fewer numbers
        
        if len(row_str) > 200:  # Too long for header
            return False
        
        capitals = sum(1 for c in row_str if c.isupper())
        letters = sum(1 for c in row_str if c.isalpha())
        
        if letters > 0 and capitals / letters > 0.3:  # 30%+ capitals
            return True
        
        return False
    
    def _manual_markdown_table(self, df: pd.DataFrame) -> str:
        """
        Manually create markdown table (fallback).
        """
        lines = []
        
        # Header
        header = '| ' + ' | '.join(str(col) for col in df.columns) + ' |'
        lines.append(header)
        
        # Separator
        separator = '| ' + ' | '.join('---' for _ in df.columns) + ' |'
        lines.append(separator)
        
        # Rows
        for _, row in df.iterrows():
            row_str = '| ' + ' | '.join(str(val) for val in row.values) + ' |'
            lines.append(row_str)
        
        return '\n'.join(lines)
    
    def format_tables_for_markdown(self, tables: List[Dict]) -> str:
        """
        Format extracted tables into a complete markdown section.
        
        Args:
            tables: List of table dictionaries from extract_tables()
        
        Returns:
            Formatted markdown string with all tables
        """
        if not tables:
            return ""
        
        output = ["\n\n---\n\n# Extracted Tables (Structured)\n\n"]
        output.append(f"*Found {len(tables)} table(s)*\n\n")
        
        for table in tables:
            # Table header
            page_info = f" (Page {table['page']})" if 'page' in table else ""
            output.append(f"## Table {table['table_num']}{page_info}\n\n")
            
            # Metadata
            metadata = []
            if 'accuracy' in table:
                metadata.append(f"Confidence: {table['accuracy']:.0%}")
            if 'method' in table:
                metadata.append(f"Method: {table['method']}")
            if 'rows' in table and 'cols' in table:
                metadata.append(f"Size: {table['rows']} rows × {table['cols']} columns")
            
            if metadata:
                output.append(f"*{' | '.join(metadata)}*\n\n")
            
            # Table content
            output.append(table['markdown'])
            output.append("\n\n")
        
        return ''.join(output)
