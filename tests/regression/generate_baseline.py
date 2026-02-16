#!/usr/bin/env python3
"""
Generate baseline quality scores for v2.2.1.

This script:
1. Converts all test PDFs using current (v2.2.1) converter
2. Calculates quality metrics
3. Saves baseline scores to baseline_scores_v2.2.1.json

Run this ONCE on v2.2.1 to establish baseline.
Future changes are compared against this baseline.

Usage:
    python tests/regression/generate_baseline.py
"""

import sys
import json
from pathlib import Path
import hashlib

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from converter import DocumentConverter


def calculate_quality_score(markdown: str) -> dict:
    """
    Calculate quality metrics for markdown output.
    
    Returns:
        dict with quality scores
    """
    if not markdown:
        return {
            'length': 0,
            'line_count': 0,
            'avg_line_length': 0,
            'has_content': False
        }
    
    lines = markdown.split('\n')
    non_empty_lines = [l for l in lines if l.strip()]
    
    # Calculate hash for exact comparison
    content_hash = hashlib.sha256(markdown.encode('utf-8')).hexdigest()
    
    return {
        'length': len(markdown),
        'line_count': len(non_empty_lines),
        'avg_line_length': len(markdown) / len(lines) if lines else 0,
        'has_content': len(markdown) > 100,
        'content_hash': content_hash,
        
        # Check for known artifacts (should be 0 in v2.2.1)
        'ligature_artifacts': sum([
            markdown.lower().count('arti fi cial'),
            markdown.lower().count('de fi ned'),
            markdown.lower().count('speci fi c')
        ]),
        
        # Check for internal link pollution (should be 0)
        'internal_link_pollution': sum([
            markdown.count('[the](#page-'),
            markdown.count('[and](#page-'),
            markdown.count('[or](#page-')
        ])
    }


def generate_baseline():
    """
    Generate baseline scores for all test documents.
    """
    print("Generating v2.2.1 Quality Baseline")
    print("="*50)
    
    # Setup
    converter = DocumentConverter()
    fixtures_dir = Path(__file__).parent.parent / "fixtures" / "sample_pdfs"
    
    if not fixtures_dir.exists():
        print(f"ERROR: Fixtures directory not found: {fixtures_dir}")
        sys.exit(1)
    
    pdf_files = list(fixtures_dir.glob("*.pdf"))
    
    if not pdf_files:
        print(f"ERROR: No PDF files found in {fixtures_dir}")
        sys.exit(1)
    
    print(f"Found {len(pdf_files)} PDF files\n")
    
    # Generate baseline for each document
    baseline = {
        'version': 'v2.2.1',
        'generated_at': None,  # Will be set when saved
        'documents': {}
    }
    
    for pdf_path in pdf_files:
        print(f"Processing: {pdf_path.name}...")
        
        try:
            markdown, error = converter.convert_file(pdf_path)
            
            if error:
                print(f"  ERROR: {error}")
                baseline['documents'][pdf_path.name] = {
                    'error': error,
                    'success': False
                }
            else:
                scores = calculate_quality_score(markdown)
                baseline['documents'][pdf_path.name] = {
                    'success': True,
                    'scores': scores
                }
                
                print(f"  ✓ Length: {scores['length']:,} chars")
                print(f"  ✓ Lines: {scores['line_count']}")
                print(f"  ✓ Ligature artifacts: {scores['ligature_artifacts']}")
                print(f"  ✓ Link pollution: {scores['internal_link_pollution']}")
                
                # Warnings
                if scores['ligature_artifacts'] > 0:
                    print(f"  ⚠️  WARNING: Found {scores['ligature_artifacts']} ligature artifacts!")
                if scores['internal_link_pollution'] > 0:
                    print(f"  ⚠️  WARNING: Found {scores['internal_link_pollution']} internal link pollution!")
        
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            baseline['documents'][pdf_path.name] = {
                'error': str(e),
                'success': False
            }
        
        print()
    
    # Save baseline
    output_file = Path(__file__).parent / "baseline_scores_v2.2.1.json"
    
    import datetime
    baseline['generated_at'] = datetime.datetime.now().isoformat()
    
    with open(output_file, 'w') as f:
        json.dump(baseline, f, indent=2)
    
    print("="*50)
    print(f"✓ Baseline saved to: {output_file}")
    print(f"✓ Processed {len(pdf_files)} documents")
    
    success_count = sum(1 for doc in baseline['documents'].values() if doc.get('success'))
    print(f"✓ Successful conversions: {success_count}/{len(pdf_files)}")
    
    # Summary of quality issues
    total_ligature = sum(
        doc.get('scores', {}).get('ligature_artifacts', 0)
        for doc in baseline['documents'].values()
        if doc.get('success')
    )
    total_pollution = sum(
        doc.get('scores', {}).get('internal_link_pollution', 0) 
        for doc in baseline['documents'].values()
        if doc.get('success')
    )
    
    print(f"\nQuality Summary:")
    print(f"  Ligature artifacts: {total_ligature} (should be 0 in v2.2.1)")
    print(f"  Internal link pollution: {total_pollution} (should be 0 in v2.2.1)")
    
    if total_ligature > 0 or total_pollution > 0:
        print(f"\n⚠️  WARNING: Quality issues detected! Review before using as baseline.")
    else:
        print(f"\n✓ Clean baseline - ready for regression testing!")


if __name__ == '__main__':
    generate_baseline()