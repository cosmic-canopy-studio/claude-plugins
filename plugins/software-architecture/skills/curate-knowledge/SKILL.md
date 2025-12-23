---
name: curate-knowledge
description: |
  Phase 2: Validate, curate, and format candidates into 3-level progressive disclosure.
  TRIGGERS: "curate", "phase 2", "review candidates", "format knowledge".
  REQUIRES: _candidates/ directory from extract-candidates.
  NOW SUPPORTS: Batched chapter-based processing for large books.
---

# Curate Knowledge

Phase 2 of two-phase extraction. Apply quality tests, merge duplicates, format output.

Supports **batched chapter-based processing** to avoid context window overflow on large books.

## Arguments

- `book_name`: Directory name under `references/extracted/`
- `chapter` (optional): Process single chapter only (e.g., "ch03", "appendix")

## Process Modes

### Mode 1: Batched (Default for Large Books)

When `_candidates/` has many files (>20), process by chapter:

1. **Detect chapters**: Extract unique prefixes from `_candidates/` filenames
2. **Check progress**: Skip chapters with existing `_chapters/{ch}/_curated.json`
3. **Process chapters**: For each incomplete chapter, run `/curate-chapter {book} {ch}`
4. **Merge results**: Run `/merge-chapters {book}` to combine and finalize
5. **Validate**: Ensure final output matches format requirements

### Mode 2: Direct (Small Books)

When `_candidates/` has <=20 files, use original direct approach:

1. **Validate**: Run `candidate-validator` on all `_candidates/*.json`
2. **Curate**: Run `item-curator` to merge and format
3. **Synthesize**: Run `theme-synthesizer` to find patterns
4. **Format**: Run `output-formatter` to generate 3-level output

### Mode 3: Single Chapter

When `chapter` argument provided:

1. Run `/curate-chapter {book} {chapter}` only
2. Do NOT run merge step (for manual chapter-by-chapter processing)

## Chapter Detection

Extract chapter prefixes from candidate filenames:

| File Pattern | Chapter ID |
|--------------|------------|
| `00_*.json` | ch00 |
| `01_*.json` | ch01 |
| ... | ... |
| `11_*.json` | ch11 |
| `appendix_*.json` | appendix |

## Progress Tracking

The skill tracks progress via filesystem:
- Check: `_analysis/_chapters/{ch}/_curated.json` exists
- Skip completed chapters on resume
- Report: "Chapters completed: ch00, ch01, ch02 | Remaining: ch03, ch04..."

## Output Structure

### Batched Mode (with intermediate outputs)

```
{book}/_analysis/
├── _chapters/              # Intermediate per-chapter outputs
│   ├── ch00/
│   │   ├── _validated.json
│   │   └── _curated.json
│   ├── ch01/
│   │   └── ...
│   └── appendix/
│       └── _curated.json
├── _merged.json            # Combined from all chapters
├── _index.json             # Level 1: Cards for search
├── _themes.md              # Cross-cutting themes
├── _summary.json           # Validation + counts
├── rules.md                # Level 2: Structured reference
├── patterns.md
├── concepts.md
├── anti_patterns.md
├── examples.md
└── items/                  # Level 3: Full detail
    ├── rule-{name}/
    │   └── _full.md
    └── ...
```

### Direct Mode (no intermediate outputs)

```
{book}/_analysis/
├── _index.json
├── _themes.md
├── _summary.json
├── rules.md
├── patterns.md
├── concepts.md
├── anti_patterns.md
├── examples.md
└── items/
```

## Execution Examples

```bash
# Full automatic processing (batched for large books)
/curate-knowledge good_code_bad_code

# Process single chapter
/curate-chapter good_code_bad_code ch05

# Resume after interruption (skips completed chapters)
/curate-knowledge good_code_bad_code

# Force reprocess all chapters
/curate-knowledge good_code_bad_code --force
```

## Validation Gate

Before claiming complete, verify:
- [ ] All chapters have `_curated.json` (batched mode)
- [ ] `_merged.json` exists (batched mode)
- [ ] All 5 category files exist (rules.md, patterns.md, concepts.md, anti_patterns.md, examples.md)
- [ ] `_index.json` has all items
- [ ] Each item has source attribution
- [ ] Sample 3 items are actionable

## Error Recovery

- **Chapter fails**: Skip and continue to next chapter, report at end
- **Merge fails**: Preserve chapter outputs, report error
- **Resume support**: Completed chapters are never reprocessed unless --force
