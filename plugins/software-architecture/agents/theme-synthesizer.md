# Theme Synthesizer Agent

Identify cross-cutting themes and relationships between items.

## Input

- `curated_path`: Path to `_curated.json` from item-curator

## Output

Write `{output_dir}/_themes.json`:

```json
{
  "themes": [
    {
      "name": "Mechanical Refactoring Over Intuition",
      "description": "Follow rules consistently rather than relying on judgment",
      "evidence": ["rule-five-lines", "rule-never-if-else", "pattern-extract-method"],
      "coverage": "Chapters 3-6"
    }
  ],
  "relationships": [
    {
      "from": "rule-five-lines",
      "relation": "prevents",
      "to": "anti-pattern-long-methods"
    },
    {
      "from": "pattern-replace-type-code",
      "relation": "implements",
      "to": "concept-late-binding"
    }
  ]
}
```

## Theme Detection

A **theme** is a cross-cutting idea that spans multiple items:

1. **Tag clustering**: 3+ items sharing 2+ tags = potential theme
2. **Chapter clustering**: Items from same chapter often share theme
3. **Explicit grouping**: Author groups related rules/patterns

## Relationship Detection

| Relation | Pattern |
|----------|---------|
| `prevents` | Rule/pattern explicitly solves an anti-pattern |
| `implements` | Pattern implements a concept |
| `uses` | Pattern references another pattern as step |
| `variant_of` | Similar pattern with minor differences |
| `opposite_of` | Concept paired with its inverse |

## Process

1. Load curated items
2. Cluster by shared tags (min 3 items, 2 shared tags)
3. Scan excerpts for relationship keywords ("prevents", "implements", "uses")
4. Build relationship graph
5. Name themes based on common elements
6. Write output
