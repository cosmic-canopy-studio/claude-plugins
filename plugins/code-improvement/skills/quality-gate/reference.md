# Quality Gate Reference

## Validation Report Formats

### Analysis Document Report
```markdown
## Quality Gate: [PASS/FAIL]

**Document**: [path]
**Type**: Analysis (Transcript/Repo)

### Checks
- [x] Required sections: 6/6 (or 8/8 for repos)
- [x] Evidence thresholds: Quotes [N]/5, Tags [N]/3
- [x] Validation Status section: Present

### Score: [N]/100
- Sections: ([present]/[total]) × 40 = [X]
- Evidence: ([pass]/[total]) × 40 = [Y]
- Quality: 20 - (concerns × 2) = [Z]

### Next Step
[Proceed/Fix issues first]
```

### Synthesis Guide Report
```markdown
## Quality Gate: [PASS/FAIL]

**Guide**: [path]
**Type**: Synthesis

### Checks
- [x] Structure: 8/8 sections
- [x] Attribution: [N] claims checked, [N] accurate ([%])
- [x] Agreement: [N] patterns verified, [N] false claims
- [x] Coverage: [N]/[total] expected topics

### Score: [N]/100
- Structure: ([present]/8) × 25 = [X]
- Attribution: (accuracy %) × 25 = [Y]
- Agreement: (1 - false/total) × 100 × 25 = [Z]
- Coverage: (covered/expected) × 100 × 25 = [W]

### Issues Found
1. [Issue with location and remediation]

### Next Step
[Proceed/Fix issues first]
```

---

## Common Mistakes

### Rushing Past the Gate
"I'll validate later" → Later never comes, bad content ships

**Instead**: Gate is non-negotiable. No claims without evidence.

### Partial Validation
"Sections look okay, skip evidence count" → Incomplete analyses

**Instead**: Run full checklist every time.

### Ignoring Low Scores
"65% is close enough" → Quality debt accumulates

**Instead**: Fix to ≥70% before proceeding.

### False Agreement Claims
"Sources agree" but they only mention similar topics

**Instead**: Verify explicit agreement on specific claims.

---

## Related Commands

- `/validate-analyses` - Full analysis validation
- `/validate-synthesis` - Full synthesis validation
- `/audit-pipeline` - Complete pipeline audit
