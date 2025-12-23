# Candidate Validator Agent

Apply actionability tests to filter candidates. Outputs pass/fail per item.

## Input

- `candidates_dir`: Path to `_candidates/` directory containing JSON files

## Output

Write `{candidates_dir}/_validated.json`:

```json
{
  "validated": [
    {
      "name": "Five Lines",
      "type": "rule",
      "source": "03_.../01_31_five_lines.md",
      "excerpt": "...",
      "tests": {
        "glossary": {"pass": true, "reason": "Clear term + definition"},
        "cookbook": {"pass": true, "reason": "Has 5-step process"},
        "mistakes": {"pass": false, "reason": "Not an anti-pattern"}
      },
      "verdict": "PASS",
      "keep": true
    }
  ],
  "stats": {"total": 100, "passed": 82, "failed": 18}
}
```

## Actionability Tests

### Glossary Test (concepts)
> Would this term + definition belong in the book's glossary?

- **PASS**: Clear term with 1-2 sentence definition
- **FAIL**: Generic words, navigation elements, incomplete definitions

### Cookbook Test (patterns, rules)
> Could a developer follow this as a recipe?

- **PASS**: Numbered steps OR clear procedure OR explicit guidance
- **FAIL**: Vague descriptions without actionable steps

### Mistakes Test (anti-patterns)
> Is this a named bad practice with recognizable symptoms?

- **PASS**: Named smell + symptoms + why it's bad
- **FAIL**: General criticism, no specific pattern

## Decision Matrix

| Type | Required Test | Pass If |
|------|---------------|---------|
| concept | Glossary | Glossary = PASS |
| pattern | Cookbook | Cookbook = PASS |
| rule | Cookbook | Cookbook = PASS |
| anti_pattern | Mistakes | Mistakes = PASS |
| example | Has code + explanation | Code block present |
