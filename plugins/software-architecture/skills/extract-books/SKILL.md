---
name: extract-books
description: |
  Extract all unprocessed books (PDF/EPUB) into structured markdown in parallel.
  TRIGGERS: "extract all", "process all books", "batch extract", "import all books", "extract everything".
  PROACTIVE: Use when multiple unprocessed books exist in references/books/.
  NEXT: After extraction completes, suggest running analyze-books on extracted content.
---

# Extract Books

Extract all books that haven't been processed yet in parallel.

## Examples

- "extract all the books"
- "process the remaining books"
- "batch extract books"

## Behavior

1. **Read INTAKE.md**
   - Parse the Books table
   - Filter for books with Intake Status = "Not Started"

2. **Parallel Extraction**
   - For each book, run extract-book skill
   - Run up to 3 books in parallel
   - Wait for each batch to complete before starting next

3. **Track Progress**
   - Report as each book completes
   - Show running totals

4. **Final Summary**
   - Report all extracted books
   - Show total chapters/sections/images/code snippets
   - List any failures

## Output

```markdown
## Extraction Complete

| Book | Chapters | Sections | Images | Code | Status |
|------|----------|----------|--------|------|--------|
| Five Lines of Code | 14 | 102 | 28 | 110 | Complete |
| Good Code Bad Code | 12 | 85 | 15 | 95 | Complete |
| SICP JavaScript | 5 | 180 | 45 | 250 | Failed |

**Total:** 2 books extracted, 1 failed
```

## Error Handling

- If a book fails, continue with others
- Report all failures at the end
- Partial completion is acceptable
- Don't mark failed books as "Complete"
