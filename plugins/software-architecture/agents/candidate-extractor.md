# Candidate Extractor Agent

Extract ALL potential knowledge items from ONE section file. Be permissive.

## Input

- `section_path`: Absolute path to one markdown section file
- `output_dir`: Path to `_candidates/` directory

## Output

Write JSON to `{output_dir}/{section_filename}.json`:

```json
{
  "source": "03_3_shatter_long_functions/01_31_five_lines.md",
  "candidates": [
    {
      "type": "rule|pattern|concept|anti_pattern|example",
      "name": "Five Lines",
      "excerpt": "50-150 words of source context",
      "location": {"line_start": 5, "heading": "3.1.1 Rule: Five Lines"},
      "confidence": "high|medium|low",
      "notes": "Optional: uncertainty, cross-refs"
    }
  ]
}
```

## Extraction Triggers

| Type | Look For |
|------|----------|
| **rule** | `Rule:`, prescriptive language (should/never/always/must) |
| **pattern** | `Pattern:`, `Refactoring pattern:`, numbered steps, before/after code |
| **concept** | Bold terms with definitions, "X is...", "X means..." |
| **anti_pattern** | `Smell`, `avoid`, `don't`, problems that rules solve |
| **example** | Code blocks with language tags, `Listing X.Y` |

## Philosophy

**Be inclusive.** Extract 20 candidates and have 15 filtered later rather than miss 5 genuine items. Quality filtering happens in Phase 2.

## Process

1. Read the markdown file
2. Scan for anything matching triggers above
3. For each match: extract name, 50-150 words of context, line numbers
4. Note uncertainty ("might also be anti-pattern")
5. Write JSON output
