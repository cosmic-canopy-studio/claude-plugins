---
name: validate-analyses
description: Validate all analysis documents for completeness, evidence quality, and reference accuracy
model: sonnet
---

# Validate Analyses

You are validating all analysis documents in `references/analysis_*.md` for quality and completeness.

## Process

### Step 1: Inventory Analysis Documents

Use Glob to find all analysis files:

```
references/analysis_*.md
```

Categorize by type:
- `analysis_transcript_*.md` - YouTube transcripts
- `analysis_repo_*.md` - Repository analyses
- Other `analysis_*.md` - Legacy or other sources

Create inventory showing: filename, type, last modified date.

### Step 2: Define Quality Criteria

**Required Sections by Type:**

| Section | Transcript | Repo |
|---------|:----------:|:----:|
| Header metadata | ✓ | ✓ |
| Overview/Summary | ✓ | ✓ |
| Key Insights/Patterns (3+) | ✓ | ✓ |
| Novel Patterns | ✓ | ✓ |
| Actionable Takeaways (3+) | ✓ | ✓ |
| Cross-References | ✓ | ✓ |
| Quotes with attribution (5+) | ✓ | - |
| File path references (10+) | - | ✓ |
| Template extractions (2+) | - | ✓ |

### Step 3: Validate Each Document

For each analysis document:

1. **Read the document** completely
2. **Check required sections** - mark present/missing
3. **Count evidence metrics**:
   - For transcripts: quotes, insights, use case tags
   - For repos: file paths, templates, transferability ratings
4. **Spot-check references** (3-5 file:line refs if present)
5. **Note quality concerns** (repetition, vagueness, unattributed claims)
6. **Calculate score** using formula below

**Scoring Formula:**
```
Score = (sections_present/total * 40) + (evidence_pass/total * 40) + (refs_valid/checked * 10) + (10 - concerns*2)
```

### Step 4: Generate Report

Output a comprehensive validation report:

```markdown
# Analysis Validation Report

**Generated**: [Date]
**Documents Analyzed**: [N]
**Overall Pass Rate**: [X/N] ([%])

## Summary by Type

| Type | Total | Pass | Fail | Avg Score |
|------|-------|------|------|-----------|
| Transcript | N | X | Y | Z |
| Repository | N | X | Y | Z |
| Other | N | X | Y | Z |

## Quality Distribution

| Tier | Count | Documents |
|------|-------|-----------|
| Production (≥85) | N | [list] |
| Review (70-84) | N | [list] |
| Draft (50-69) | N | [list] |
| Skeleton (<50) | N | [list] |

---

## Detailed Results

### [PASS] analysis_transcript_XYZ.md (Score: 88)

| Check | Result |
|-------|--------|
| Sections | 7/7 ✓ |
| Quotes | 8 (min 5) ✓ |
| Insights | 12 (min 5) ✓ |
| Tags | 5 (min 3) ✓ |

**Quality**: Production tier

---

### [FAIL] analysis_repo_ABC.md (Score: 62)

| Check | Result |
|-------|--------|
| Sections | 6/8 ✗ |
| File refs | 7 (min 10) ✗ |
| Templates | 1 (min 2) ✗ |

**Missing Sections**:
- Actionable Takeaways
- Cross-References

**Remediation**:
1. Add 3+ actionable takeaways with specific steps
2. Add Cross-References section linking to related analyses
3. Extract 1 more reusable template from repo

**Quality**: Draft tier

---

## Broken References

| Document | Reference | Issue |
|----------|-----------|-------|
| analysis_X.md | src/foo.ts:L45 | File not found |
| analysis_Y.md | bar.ts:L200 | Line exceeds file length |

## Remediation Priority

### Critical (Production blockers)
1. [Document]: [Issue] - [Fix]

### High (Review blockers)
1. [Document]: [Issue] - [Fix]

### Medium (Quality improvements)
1. [Document]: [Issue] - [Fix]

---

## Next Steps

1. Fix [N] documents with missing required sections
2. Fix [N] broken file references
3. Enhance [N] documents below evidence thresholds
4. Re-run validation after fixes: `/validate-analyses`
```

## Parallel Processing

To speed up validation:
- Process up to 5 documents in parallel using Task agents
- Use the `analysis-validator` agent for each document
- Aggregate results into final report

## Error Handling

- If a document cannot be read: Log error, mark as "Unreadable", continue
- If validation agent fails: Retry once, then log as "Validation failed"
- Include all errors in final report under "Errors Encountered"

## Success Criteria

Validation is complete when:
- [ ] All analysis documents have been checked
- [ ] Each document has pass/fail status with score
- [ ] All broken references are listed
- [ ] Remediation list is prioritized
- [ ] Summary statistics are calculated
