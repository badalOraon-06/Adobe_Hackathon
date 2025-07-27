# Test Results - Adobe Hackathon Round 1A

This directory contains test results demonstrating the PDF outline extractor performance.

## Input PDFs (7 files)
- **Academic Content**: 5 organic chemistry textbook chapters  
- **Research Report**: 1 sample research document
- **Test Document**: 1 synthetic test PDF

## Output Results (7 JSON files)
Each PDF produces a corresponding JSON file with extracted title and hierarchical outline.

## Performance Summary
- **Total Processing Time**: 12.86 seconds for 7 PDFs
- **Average per PDF**: ~1.84 seconds  
- **Largest PDF**: 3.08 seconds (under 10s requirement ✓)
- **Total Headings Extracted**: 245 headings across all documents
- **Success Rate**: 100% (all PDFs processed successfully)

## Key Achievements
✅ Fast processing (all under 10-second limit)  
✅ Hierarchical heading detection (H1, H2, H3)  
✅ Accurate page number tracking  
✅ Perfect JSON format compliance  
✅ Works with complex academic content
