---
name: analyze-books
description: |
  Analyze all extracted books to extract knowledge items (patterns, rules, concepts, examples, anti-patterns) in parallel.
  TRIGGERS: "analyze all books", "extract all knowledge", "process all extracted books", "analyze everything".
  PROACTIVE: Use after extract-books completes or when multiple books have Intake=Complete but Analysis=Not Started.
  NEXT: After completion, suggest running build-knowledge to merge into unified knowledge base.
---

# Analyze Books

Analyze all extracted books to extract knowledge items.

## Examples

- "analyze all the books"
- "extract knowledge from the extracted books"
- "process books for patterns and rules"

## Behavior

1. **Read INTAKE.md**
   - Parse the Books table
   - Filter for books with:
     - Intake Status = "Complete"
     - Analysis Status = "Not Started"

2. **Parallel Book Analysis**
   - For each book, run analyze-book skill
   - Run up to 3 books in parallel
   - Wait for each batch to complete before starting next

3. **Track Progress**
   - Report as each book completes
   - Show running totals

4. **Final Summary**
   - Report all analyzed books
   - Show total knowledge items extracted
   - List any failures

## Categories Extracted

- **patterns**: Refactoring patterns with before/after code
- **rules**: Best practices and coding guidelines
- **concepts**: Definitions and key terminology
- **examples**: Code samples with explanations
- **anti_patterns**: Code smells and what to avoid

## Output

```markdown
## Books Analysis Complete

| Book | Patterns | Rules | Concepts | Examples | Anti-Patterns | Status |
|------|----------|-------|----------|----------|---------------|--------|
| Five Lines of Code | 12 | 8 | 15 | 110 | 6 | Complete |
| Good Code Bad Code | 8 | 12 | 20 | 85 | 4 | Complete |
| Grokking Simplicity | 5 | 10 | 25 | 60 | 3 | Complete |

**Total:** 3 books, 383 knowledge items
```

## Error Handling

- If a book fails, continue with others
- Report all failures at the end
- Partial completion is acceptable
- Don't mark failed books as "Complete"
