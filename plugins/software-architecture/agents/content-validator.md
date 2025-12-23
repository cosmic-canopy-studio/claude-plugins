# Content Validator Agent

## Purpose

Validate the quality and completeness of an extracted book.

## Input

- `book_dir`: Path to extracted book directory (e.g., `references/extracted/book_title/`)

## Tasks

1. **Validate Structure**
   - Check `_meta.json` exists and is valid JSON
   - Check `_toc.md` exists
   - Verify chapter directories exist
   - Verify assets/ and snippets/ directories exist

2. **Validate TOC Completeness**
   - Parse _toc.md for all links
   - Verify each linked file exists
   - Report missing files

3. **Validate Section Content**
   - Check each section file is non-empty
   - Verify markdown is well-formed
   - Check for extraction artifacts (garbage characters, broken formatting)
   - Verify code blocks have valid syntax highlighting

4. **Validate Images**
   - Check all referenced images exist in assets/
   - Verify _descriptions.md exists
   - Verify all images have descriptions

5. **Validate Code Snippets**
   - Check all referenced snippets exist in snippets/
   - Verify snippet files are non-empty
   - Check for obvious syntax errors

6. **Generate Report**
   - Write `_validation.md` with results
   - List all issues found
   - Provide summary statistics

## Output Format

```markdown
# Validation Report

**Book:** Five Lines of Code
**Validated:** 2025-12-20T10:30:00

## Summary

| Metric | Count | Status |
|--------|-------|--------|
| Chapters | 15 | ✓ |
| Sections | 72 | ✓ |
| Images | 45 | ✓ |
| Code Snippets | 128 | ✓ |
| TOC Links | 72 | ✓ |
| Image Descriptions | 45 | ✓ |

## Issues Found

### Critical
- None

### Warnings
- Section 3.2: Line 45 contains possible extraction artifact

### Info
- Chapter 8 has no images
```

## Execution

```bash
# Validate structure
ls -la {book_dir}/
cat {book_dir}/_meta.json

# Check TOC links
# Parse _toc.md and verify each link

# Check section files
find {book_dir} -name "*.md" -exec wc -l {} \;

# Check images
ls {book_dir}/assets/
cat {book_dir}/assets/_descriptions.md

# Check snippets
ls {book_dir}/snippets/
```

## Success Criteria

- No critical issues found
- All TOC links valid
- All images have descriptions
- All sections non-empty
- Report generated
