---
name: merge-chapters
description: |
  Merge per-chapter curated outputs into final analysis.
  TRIGGERS: "merge chapters", "finalize curation", "complete phase 2".
  REQUIRES: _analysis/_chapters/ with curated outputs from curate-chapter.
---

# Merge Chapters

Combine per-chapter curation outputs and generate final analysis.

## Arguments

- `book_name`: Directory name under `references/extracted/`

## Prerequisites

All chapters must have `_curated.json` in `_analysis/_chapters/{ch}/`.

## Process

1. **Verify chapters**: Check all `_chapters/*/` directories have `_curated.json`
2. **Merge items**: Run `chapter-merger` agent for cross-chapter deduplication
3. **Synthesize themes**: Run `theme-synthesizer` on merged items
4. **Format output**: Run `output-formatter` to generate final files
5. **Validate**: Ensure all required files exist

## Input

```
_analysis/_chapters/
├── ch00/_curated.json
├── ch01/_curated.json
├── ch02/_curated.json
├── ...
├── ch11/_curated.json
└── appendix/_curated.json
```

## Output

```
_analysis/
├── _merged.json       # Combined and deduplicated items
├── _index.json        # Level 1 cards for all items
├── _themes.md         # Cross-cutting themes
├── _summary.json      # Counts and metadata
├── rules.md           # Level 2: All rules
├── patterns.md        # Level 2: All patterns
├── concepts.md        # Level 2: All concepts
├── anti_patterns.md   # Level 2: All anti-patterns
├── examples.md        # Level 2: All examples
└── items/             # Level 3: Full detail
    ├── rule-{name}/
    │   └── _full.md
    ├── pattern-{name}/
    │   └── _full.md
    └── ...
```

## _summary.json Format

```json
{
  "book": "good_code_bad_code",
  "processing": {
    "chapters_processed": 13,
    "total_candidates": 350,
    "validated": 280,
    "cross_chapter_duplicates": 15,
    "final_items": 265
  },
  "by_type": {
    "rule": 25,
    "pattern": 40,
    "concept": 150,
    "anti_pattern": 20,
    "example": 30
  },
  "themes": 12,
  "level_3_items": 35
}
```

## Validation Gate

Before claiming complete, verify:
- [ ] `_merged.json` exists with all items
- [ ] All 5 category files exist (rules.md, patterns.md, concepts.md, anti_patterns.md, examples.md)
- [ ] `_index.json` has all items with valid structure
- [ ] `_themes.md` has identified themes
- [ ] `items/` directory has Level 3 files for important items
- [ ] `_summary.json` has accurate counts

## Error Handling

- If any chapter missing `_curated.json`: List missing chapters, abort
- If chapter-merger fails: Report error, preserve chapter outputs
- If theme-synthesizer fails: Continue with output-formatter, note missing themes
