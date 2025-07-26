# Adobe Hackathon - Round 1A: PDF Outline Extractor

## Overview

This solution extracts structured outlines from PDF documents, identifying titles and hierarchical headings (H1, H2, H3) along with their page numbers.

## Approach

Our solution uses PyMuPDF (fitz) for PDF parsing and implements a multi-step approach:

1. **Title Extraction**: Identifies the largest font text on the first page as the document title
2. **Font Analysis**: Determines the body font size by analyzing the most common font sizes across the document
3. **Heading Detection**: Uses font size comparison, formatting (bold), and textual patterns to classify headings:
   - H1: Font size ≥ body_size + 6
   - H2: Font size ≥ body_size + 3
   - H3: Font size ≥ body_size + 1
4. **Context-Aware Filtering**: Considers line positioning and content to avoid false positives

## Key Features

- **Multi-criteria Heading Detection**: Combines font size, formatting, and positional analysis
- **Robust Title Extraction**: Identifies titles from the largest font elements on first page
- **Context Filtering**: Removes numbers-only text and validates heading structure
- **Performance Optimized**: Designed to process 50-page PDFs within 10 seconds

## Models and Libraries Used

- **PyMuPDF (fitz) 1.23.8**: Primary PDF processing library
- **Python Standard Libraries**: re, collections, json, os, time

## Docker Build and Run

### Build Command

```bash
docker build --platform linux/amd64 -t mysolutionname:somerandomidentifier .
```

### Run Command

```bash
docker run --rm -v $(pwd)/input:/app/input -v $(pwd)/output:/app/output --network none mysolutionname:somerandomidentifier
```

## Input/Output Specification

- **Input**: PDF files in `/app/input` directory
- **Output**: JSON files in `/app/output` directory with format:

```json
{
  "title": "Document Title",
  "outline": [
    { "level": "H1", "text": "Heading Text", "page": 1 },
    { "level": "H2", "text": "Sub Heading", "page": 2 }
  ]
}
```

## Constraints Met

- ✅ CPU-only execution (amd64 architecture)
- ✅ No internet access required (offline processing)
- ✅ Model size < 200MB (using lightweight PyMuPDF)
- ✅ Processing time < 10 seconds per 50-page PDF
- ✅ 8 CPU, 16GB RAM compatible

## Project Structure

```
├── Dockerfile
├── README.md
├── app/
│   ├── main.py          # Entry point and file processing
│   ├── extractor.py     # Core outline extraction logic
│   └── requirements.txt # Python dependencies
├── input/               # PDF input directory
└── output/              # JSON output directory
```

## Testing

The solution has been designed to handle:

- Various font sizes and styles
- Multi-language documents
- Complex document layouts
- Edge cases in heading detection

## Performance Notes

- Efficient memory usage through streaming PDF processing
- Optimized font analysis using Counter for statistical analysis
- Early filtering to reduce computational overhead
