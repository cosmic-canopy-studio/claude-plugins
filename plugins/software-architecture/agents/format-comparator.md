# Format Comparator Agent

## Purpose

Compare PDF vs EPUB extraction for a book to determine which format provides better output.

## Input

- `book_title`: Name of the book (must have both EPUB and PDF available)
- `epub_path`: Path to EPUB file
- `pdf_path`: Path to PDF file
- `output_dir`: Optional path for comparison report

## Tasks

1. **Extract from EPUB**
   - Run EpubExtractor to temporary directory
   - Capture extraction metrics

2. **Extract from PDF**
   - Run PdfExtractor to temporary directory
   - Capture extraction metrics

3. **Calculate Metrics**
   - Chapter/section counts
   - Code block counts and formatting quality
   - Image extraction counts
   - Language detection accuracy
   - Content artifacts and garbage characters

4. **Generate Comparison Report**
   - Calculate quality scores (0-10)
   - Compare all metrics
   - Generate quality notes
   - Make format recommendation

5. **Output Recommendation**
   - Return recommended format ("epub" or "pdf")
   - Save comparison report if output_dir specified

## Output

```json
{
  "recommended_format": "epub",
  "epub_score": 8.5,
  "pdf_score": 7.2,
  "report_path": "path/to/comparison_report.md"
}
```

## Execution

```python
from pathlib import Path
from content_toolkit import EpubExtractor, PdfExtractor
from content_toolkit.comparator import FormatComparator

epub_path = Path('{epub_path}')
pdf_path = Path('{pdf_path}')

# Extract from both formats
epub_result = EpubExtractor(epub_path).extract()
pdf_result = PdfExtractor(pdf_path).extract()

# Compare
comparator = FormatComparator()
report = comparator.compare(epub_result, pdf_result)

print(f"Recommendation: {report.recommended_format}")
print(f"EPUB Score: {report.epub_score:.1f}/10")
print(f"PDF Score: {report.pdf_score:.1f}/10")
print()
print(report.to_markdown())
```

## Metrics Compared

| Metric | Weight | Description |
|--------|--------|-------------|
| Chapter count | Medium | More = better structure detection |
| Section count | Medium | More granular = better |
| Code blocks | High | More = better code extraction |
| Language detection | High | Non-"text" languages detected |
| Code formatting | High | Multi-line preservation |
| Images | Medium | Image extraction success |
| Content artifacts | High | Garbage characters penalty |

## Available Books with Both Formats

| Book | EPUB | PDF |
|------|------|-----|
| Five Lines of Code | references/books/five_lines_of_code.epub | references/books/five_lines_of_code.pdf |
| Good Code Bad Code | references/books/good_code_bad_code.epub | references/books/good_code_bad_code.pdf |
| Grokking Functional Programming | references/books/grokking_functional_programming.epub | references/books/grokking_functional_programming.pdf |
| Grokking Simplicity | references/books/grokking_simplicity.epub | references/books/grokking_simplicity.pdf |
| Looks Good to Me | references/books/looks_good_to_me.epub | references/books/looks_good_to_me.pdf |
| Software Mistakes and Tradeoffs | references/books/software_mistakes_and_tradeoffs.epub | references/books/software_mistakes_and_tradeoffs.pdf |
| The Creative Programmer | references/books/the_creative_programmer.epub | references/books/the_creative_programmer.pdf |
| Think Like a Programmer | references/books/think_like_a_programmer.epub | references/books/think_like_a_programmer.pdf |

## Success Criteria

- Both formats extracted successfully
- Metrics calculated for each
- Comparison report generated
- Clear recommendation provided with reasoning
