---
name: curate-chapter
description: |
  Curate candidates for ONE chapter. Part of batched Phase 2 processing.
  TRIGGERS: "curate chapter", "process chapter [N]".
  INTERNAL: Called by curate-knowledge orchestrator.
---

# Curate Chapter

Process one chapter's candidates through validation and curation.

## Arguments

- `book_name`: Directory name under `references/extracted/`
- `chapter`: Chapter identifier (e.g., "ch03", "appendix")

## Chapter Prefix Mapping

| Chapter ID | File Prefix |
|------------|-------------|
| ch00 | 00_ |
| ch01 | 01_ |
| ch02 | 02_ |
| ... | ... |
| ch11 | 11_ |
| appendix | appendix_ |

## Process

1. **Find candidates**: List `_candidates/{prefix}*.json` files for this chapter
2. **Load candidates**: Read all matching JSON files, combine into single list
3. **Validate**: Apply actionability tests (same as candidate-validator)
   - Glossary test for concepts
   - Cookbook test for patterns/rules
   - Mistakes test for anti-patterns
   - Code presence for examples
4. **Curate**: Merge duplicates within chapter, format Level 1/2 (same as item-curator)
5. **Write output**: Save to `_analysis/_chapters/{chapter}/`

## Input

```
_candidates/
├── {prefix}01_section.json
├── {prefix}02_section.json
└── ...
```

## Output

```
_analysis/_chapters/{chapter}/
├── _validated.json    # Validated candidates with test results
└── _curated.json      # Curated items with Level 1/2 formatting
```

## _validated.json Format

```json
{
  "chapter": "ch03",
  "validated": [
    {
      "name": "Code Contracts",
      "type": "concept",
      "source": "03_33_code_contracts.md",
      "excerpt": "...",
      "tests": {
        "glossary": {"pass": true, "reason": "Clear term + definition"}
      },
      "verdict": "PASS",
      "keep": true
    }
  ],
  "stats": {"total": 25, "passed": 20, "failed": 5}
}
```

## _curated.json Format

```json
{
  "chapter": "ch03",
  "items": [
    {
      "id": "concept-code-contracts",
      "name": "Code Contracts",
      "type": "concept",
      "level_1": {
        "summary": "Explicit specifications of what code expects and guarantees.",
        "category": "Design",
        "tags": ["contracts", "preconditions", "postconditions"]
      },
      "level_2": {
        "statement": "Code contracts define the expectations...",
        "explanation": "Contracts help prevent misuse...",
        "when_to_apply": "Public APIs and boundaries",
        "related_pattern": null
      },
      "sources": ["03_33_code_contracts.md:5-25"]
    }
  ],
  "stats": {"validated": 20, "merged": 2, "final": 18}
}
```

## Idempotency

If `_curated.json` exists and is newer than all source candidate files, skip processing and report "Chapter already curated".

## Error Handling

- If no candidate files match the chapter prefix: Report error, skip chapter
- If chapter directory exists but is incomplete: Reprocess from scratch
