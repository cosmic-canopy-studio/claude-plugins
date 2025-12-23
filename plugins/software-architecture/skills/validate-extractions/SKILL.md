---
name: validate-extractions
description: |
  Re-validate all extracted books for quality and completeness.
  TRIGGERS: "validate extractions", "check extraction quality", "verify books", "troubleshoot extraction", "quality check".
  PROACTIVE: Use when extraction issues are suspected or before running analysis on old extractions.
---

# Validate Extractions

Re-validate all extracted books for quality and completeness.

## Examples

- "validate the extracted books"
- "check extraction quality"
- "verify book extractions are complete"

## Behavior

1. **Scan Extracted Directory**
   - Find all book directories in `references/extracted/`
   - Read each book's `_meta.json` for metadata

2. **Parallel Validation**
   - Spawn `content-validator` agent for each book in parallel
   - Collect validation results

3. **Generate Summary Report**
   - Aggregate all validation results
   - Highlight any critical issues
   - Show warnings across all books

## Output

```markdown
# Extraction Validation Summary

**Date:** 2025-12-20
**Books Validated:** 10

## Overall Status

| Status | Count |
|--------|-------|
| Pass | 8 |
| Warnings | 1 |
| Critical | 1 |

## Books with Issues

### Five Lines of Code (Warnings)
- Chapter 3, Section 2: Possible extraction artifact on line 45
- Missing alt text for fig_03_02.png

### SICP JavaScript (Critical)
- 12 TOC links broken
- assets/ directory missing

## Recommendations

1. Re-extract SICP JavaScript from source
2. Review Five Lines of Code chapter 3 manually
```

## Error Handling

- If extracted/ directory doesn't exist, report and exit
- If a book can't be validated, report the error and continue
- Always produce a summary even with failures
