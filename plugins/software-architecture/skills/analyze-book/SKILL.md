---
name: analyze-book
description: |
  Full two-phase extraction for one book: extract candidates then curate.
  TRIGGERS: "analyze [book]", "extract knowledge from", "process [book]".
  NEXT: After all books analyzed, run build-knowledge for unified index.
---

# Analyze Book

Full two-phase extraction pipeline for one book.

## Arguments

- `book_name`: Directory name under `references/extracted/`

## Process

1. Validate `references/extracted/{book_name}/` exists
2. Run `/extract-candidates {book_name}` (Phase 1: parallel extraction)
3. Run `/curate-knowledge {book_name}` (Phase 2: sequential curation)
4. Report final summary

## Output

```
{book}/
├── _candidates/       # Phase 1 output
│   └── {section}.json
└── _analysis/         # Phase 2 output (3-level progressive disclosure)
    ├── _index.json    # Level 1: Cards
    ├── {type}.md      # Level 2: Structured
    └── items/         # Level 3: Rich detail
```

## Validation Gate

Before claiming complete:
- [ ] `_candidates/` has JSON files
- [ ] `_analysis/` has all 5 category files
- [ ] `_index.json` has all items
- [ ] Sample 3 items are actionable
