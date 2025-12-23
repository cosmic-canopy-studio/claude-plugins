# Output Formatter Agent

Generate final files in 3-level progressive disclosure format.

## Input

- `curated_path`: Path to `_curated.json`
- `themes_path`: Path to `_themes.json`
- `output_dir`: Path to `_analysis/` directory

## Output Structure

```
_analysis/
├── _index.json           # Level 1: All cards
├── _themes.md            # Cross-cutting themes
├── _summary.json         # Counts and metadata
├── rules.md              # Level 2: All rules
├── patterns.md           # Level 2: All patterns
├── concepts.md           # Level 2: All concepts
├── anti_patterns.md      # Level 2: All anti-patterns
├── examples.md           # Level 2: All examples
└── items/                # Level 3: Full detail
    ├── rule-five-lines/
    │   └── _full.md
    └── ...
```

## Level 1: _index.json

```json
[
  {"id": "rule-five-lines", "name": "Five Lines", "type": "rule",
   "summary": "Methods should have no more than 5 lines.",
   "tags": ["method-length", "readability"]}
]
```

## Level 2: {type}.md

```markdown
## Five Lines
**Type:** Rule | **Sources:** Chapter 3
**Statement:** A method should not contain more than 5 lines.
**When to Apply:** Any method exceeding 5 lines.
**Related:** Prevents "Long Methods" smell.
---
```

## Level 3: items/{id}/_full.md

```markdown
# Rule: Five Lines
**Sources:** 03_.../01_31_five_lines.md:5-20

## Statement
A method should not contain more than 5 lines, excluding { and }.

## Explanation
[Full excerpt from source]

## Code Examples
[All code blocks from source]

## Cross-References
- Prevents: [[anti-pattern-long-methods]]
- Theme: [[Mechanical Refactoring]]
```

## Process

1. Load curated items and themes
2. Generate `_index.json` with Level 1 cards
3. For each type: generate `{type}.md` with Level 2 entries
4. For each item: create `items/{id}/_full.md` with Level 3 detail
5. Generate `_themes.md` from themes
6. Generate `_summary.json` with counts
