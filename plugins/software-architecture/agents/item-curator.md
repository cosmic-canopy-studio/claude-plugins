# Item Curator Agent

Merge duplicates, pick best definitions, format items for 3-level output.

## Usage Modes

### Full Dataset Mode (Original)
- Process all validated items from entire book
- Cross-section deduplication included

### Per-Chapter Mode (Batched)
- Process validated items from ONE chapter only
- `validated_path`: Path to `_chapters/{ch}/_validated.json`
- `output_dir`: Path to `_chapters/{ch}/`
- Intra-chapter deduplication only
- Cross-chapter deduplication happens later via `chapter-merger` agent

## Input

- `validated_path`: Path to `_validated.json` from candidate-validator
- `output_dir`: Path to output directory (either `_analysis/` or `_chapters/{ch}/`)

## Output

Write `{output_dir}/_curated.json`:

```json
{
  "items": [
    {
      "id": "rule-five-lines",
      "name": "Five Lines",
      "type": "rule",
      "level_1": {
        "summary": "Methods should have no more than 5 lines.",
        "category": "Code Structure",
        "tags": ["method-length", "readability", "refactoring"]
      },
      "level_2": {
        "statement": "A method should not contain more than five lines, excluding { and }.",
        "explanation": "A line refers to if, for, while, or anything ending with semicolon...",
        "when_to_apply": "Any method exceeding 5 lines",
        "related_smell": "Long Methods"
      },
      "sources": ["03_.../01_31_five_lines.md:5-20"]
    }
  ],
  "stats": {"total": 82, "merged": 12, "final": 70}
}
```

## Deduplication Rules

1. **Same name** (case-insensitive) across sections = merge
2. Keep excerpt with most complete definition
3. Combine source locations into array
4. Semantic match (different words, same concept) = merge with note

## Level Formatting

### Level 1 (Card)
- `summary`: 1 sentence, <100 chars
- `category`: Code Structure | Refactoring | Design | Testing
- `tags`: 2-5 keywords for search

### Level 2 (Structured)
- `statement`: The core rule/pattern/concept in 1-2 sentences
- `explanation`: Why it matters, 2-4 sentences
- `when_to_apply`: Context for application
- `related_smell` or `related_pattern`: Cross-reference

## Process

1. Load validated items
2. Group by normalized name
3. For each group: pick best excerpt, merge sources
4. Generate id from type + slugified name
5. Format Level 1 and Level 2 fields
6. Write output
