# How to Add More Test PDFs

## Method 1: Add Your Own PDFs

1. Copy any PDF files to the `input/` folder
2. Run the test: `& "C:/Users/BADAL ORAON/AppData/Local/Microsoft/WindowsApps/python3.11.exe" test_local.py`

## Method 2: Create Test PDFs

Run this to create more test documents:

```powershell
& "C:/Users/BADAL ORAON/AppData/Local/Microsoft/WindowsApps/python3.11.exe" create_test_pdf.py
```

## Method 3: Download Sample PDFs

Find academic papers, reports, or documentation PDFs online and place them in `input/`

## What to Look For in Results:

- ✅ Title extraction from first page
- ✅ H1, H2, H3 headings with correct levels
- ✅ Accurate page numbers
- ✅ Processing time < 10 seconds per 50-page PDF
- ✅ Valid JSON output format

## Current Test Results:

- sample-research-report.pdf: Title detected, 0 headings (may need heading detection tuning)
- test_document.pdf: Title + 2 headings detected perfectly
- Processing speed: 0.06 seconds total (excellent performance)
