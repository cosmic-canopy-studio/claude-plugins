---
name: extract-book
description: |
  Extract a single book (PDF/EPUB) into structured markdown with chapters, sections, code blocks, and images.
  TRIGGERS: "extract [book]", "process [book]", "convert [book]", importing new books, PDF/EPUB file references, "add book to knowledge base".
  PROACTIVE: Use when user adds new books to references/books/ or mentions a book file.
  NEXT: After extraction completes, suggest running analyze-book on the extracted content.
---

# Extract Book

Extract a single book into structured markdown.

## Arguments

- `book_path`: Path to the book file (relative to references/books/)
- `--compare`: When both PDF and EPUB exist, compare formats and use the best one

## Examples

- "extract Five Lines of Code"
- "process the SICP book"
- "extract five_lines_of_code --compare"

## Behavior

1. **Resolve Paths**
   - Source: `references/books/{book_path}`
   - Output: `references/extracted/{book_name}/`

2. **Format Comparison (if --compare or both formats exist)**
   - Check if both EPUB and PDF exist for this book
   - If yes, run `format-comparator` agent
   - Use the recommended format for extraction
   - Save comparison report to output directory

3. **Run Extraction Pipeline**
   - Spawn `book-extractor` agent with source and output paths
   - Wait for extraction to complete
   - Spawn `image-describer` agent for assets/
   - Wait for descriptions to complete
   - Spawn `content-validator` agent
   - Report validation results

4. **Update INTAKE.md**
   - Set Intake Status to "Complete" for this book
   - Update Date Last Updated

## Output

Reports extraction statistics:
- Format used (and comparison results if applicable)
- Number of chapters extracted
- Number of sections created
- Number of images processed
- Number of code snippets extracted
- Validation summary

## Books with Both Formats

These books will automatically trigger format comparison:

| Book Name | EPUB | PDF |
|-----------|------|-----|
| five_lines_of_code | .epub | .pdf |
| good_code_bad_code | .epub | .pdf |
| grokking_functional_programming | .epub | .pdf |
| grokking_simplicity | .epub | .pdf |
| looks_good_to_me | .epub | .pdf |
| software_mistakes_and_tradeoffs | .epub | .pdf |
| the_creative_programmer | .epub | .pdf |
| think_like_a_programmer | .epub | .pdf |

## Error Handling

- If book file not found, report error and exit
- If extraction fails, keep Intake Status as "Not Started"
- If validation finds critical issues, report them prominently
- If comparison fails, fall back to EPUB (default preference)
