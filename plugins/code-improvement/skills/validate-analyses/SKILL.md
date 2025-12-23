---
name: validate-analyses
description: Validate analysis documents for completeness, evidence quality, and accuracy (project) - when validating analysis documents, checking analysis quality, before updating INTAKE.md with "Analyzed: Yes", or running pipeline audits
when_to_use: when validating analysis documents, checking analysis quality, before updating INTAKE.md with "Analyzed: Yes", or running pipeline audits
---

# Validate Analyses

Check all `references/analysis_*.md` documents for quality and completeness.

## Quick Reference

| Type | Required Sections | Evidence Thresholds |
|------|-------------------|---------------------|
| Transcript | 6 (Overview, Insights, Patterns, Conflicts, Takeaways, Cross-Refs) | 5+ quotes, 3+ tags |
| Repository | 8 (Structure, Commands, Agents, Skills, CLAUDE.md, Patterns, Takeaways, Cross-Refs) | 10+ file refs, 2+ templates, 3+ ratings |

## Scoring Formula

```
Score = (sections/total × 40) + (evidence_pass × 40) + (refs_valid × 10) + (10 - concerns × 2)
```

| Tier | Score | Meaning |
|------|-------|---------|
| Production | ≥85 | Ready for synthesis |
| Review | 70-84 | Minor fixes needed |
| Draft | 50-69 | Significant gaps |
| Skeleton | <50 | Major remediation |

## Validation Steps

1. **Inventory**: `Glob references/analysis_*.md` → categorize by type
2. **Check Sections**: Verify all required sections present
3. **Count Evidence**: Quotes, tags, file refs, templates
4. **Spot-Check Refs**: Verify 3-5 file:line references exist
5. **Note Concerns**: Repetition, vagueness, unattributed claims
6. **Calculate Score**: Apply formula
7. **Generate Report**: Pass/fail with remediation list

## Validation Report Template

```markdown
## Analysis Validation: [PASS/FAIL]

**Document**: [path]
**Type**: [Transcript/Repo]
**Score**: [N]/100 ([Tier])

### Checks
- Sections: [X]/[total] [✓/✗]
- Evidence: [details] [✓/✗]
- Validation Status: [Present/Missing] [✓/✗]

### Issues
1. [Issue with remediation]

### Next Step
[Proceed/Fix first]
```

## When to Trigger

- Before claiming ANY analysis is complete
- Before marking "Analyzed: Yes" in INTAKE.md
- When running `/audit-pipeline`
- When troubleshooting synthesis quality issues

## See Also

- `/validate-analyses` command - Full validation process
- `quality-gate` skill - Workflow boundary enforcement
- `analysis-validator` agent - Per-document validation
