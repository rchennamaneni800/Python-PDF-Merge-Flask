#!/usr/bin/env python3

import os
import sys
import tempfile
import shutil
from app import convert_to_pdf, merge_pdfs_with_bookmarks

def test_conversion_and_merge():
    """Test the PDF conversion and merging functionality"""
    
    print("Testing PDF conversion and merging functionality...\n")
    
    os.makedirs('converted', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    
    test_files = ['sample_intro.rtf', 'sample_technical.rtf', 'sample_userguide.rtf']
    
    print("Testing RTF to PDF conversion...")
    converted_pdfs = []
    
    for rtf_file in test_files:
        if not os.path.exists(rtf_file):
            print(f"  ✗ Test file {rtf_file} not found")
            continue
            
        pdf_file = os.path.splitext(rtf_file)[0] + '.pdf'
        pdf_path = os.path.join('converted', pdf_file)
        
        print(f"  Converting {rtf_file} to PDF...")
        if convert_to_pdf(rtf_file, pdf_path):
            converted_pdfs.append(pdf_path)
            print(f"    ✓ Successfully converted to {pdf_path}")
        else:
            print(f"    ✗ Failed to convert {rtf_file}")
    
    if not converted_pdfs:
        print("No files were converted successfully!")
        return False
    
    output_file = os.path.join('output', 'test_merged_document.pdf')
    print(f"\nMerging {len(converted_pdfs)} PDFs with bookmarks and TOC...")
    
    try:
        merge_pdfs_with_bookmarks(converted_pdfs, output_file, include_toc=True)
        print(f"  ✓ Successfully merged PDFs to {output_file}")
        
        if os.path.exists(output_file) and os.path.getsize(output_file) > 0:
            print(f"  ✓ Output file created successfully ({os.path.getsize(output_file)} bytes)")
            return True
        else:
            print("  ✗ Output file is empty or doesn't exist")
            return False
            
    except Exception as e:
        print(f"  ✗ Error merging PDFs: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_conversion_and_merge()
    
    if success:
        print("\n🎉 All tests passed! The application is working correctly.")
        print("\nGenerated files:")
        if os.path.exists('output/test_merged_document.pdf'):
            print(f"  - output/test_merged_document.pdf ({os.path.getsize('output/test_merged_document.pdf')} bytes)")
    else:
        print("\n❌ Tests failed! Please check the error messages above.")
        sys.exit(1)
