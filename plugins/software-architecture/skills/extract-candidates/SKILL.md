---
name: extract-candidates
description: |
  Phase 1: Extract candidates from all sections in parallel. Permissive, no filtering.
  TRIGGERS: "extract candidates", "phase 1", "find candidates".
  NEXT: Run curate-knowledge to filter and format.
---

# Extract Candidates

Phase 1 of two-phase extraction. Be permissive - capture everything.

## Arguments

- `book_name`: Directory name under `references/extracted/`

## Process

1. Validate `references/extracted/{book_name}/` exists
2. Create `_candidates/` directory (clear if exists)
3. Find all `**/*.md` excluding `_*.md` and `summary.md`
4. Spawn `candidate-extractor` agent for EACH section (max 10 parallel)
5. Report counts when done

## Output

```
{book}/_candidates/
├── {section}.json     # One per section
└── _summary.json      # Counts
```

## Next Step

Run `/curate-knowledge {book_name}` to filter and format.
