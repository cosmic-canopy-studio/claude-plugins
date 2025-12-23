---
name: validate-synthesis
description: Validate synthesis guides for attribution accuracy, source agreement, and coverage (project) - when validating synthesis guides, checking attribution accuracy, before marking guides as complete, or running pipeline audits
when_to_use: when validating synthesis guides, checking attribution accuracy, before marking guides as complete, or running pipeline audits
---

# Validate Synthesis

Check all `guides/use-cases/*/index.md` guides for accuracy and attribution.

## Quick Reference

### Required Sections (8)
1. Quick Answer (1 sentence)
2. The Problem + Signs (3+ symptoms)
3. The Solution + quote
4. Key Principles (2+ with source)
5. Step-by-Step Guide (3+ steps)
6. Patterns & Templates (1+)
7. Common Mistakes (2+)
8. Sources table

### Quality Dimensions
| Dimension | Target | Method |
|-----------|--------|--------|
| Structure | 8/8 sections | Section count |
| Attribution | 100% cited | Sample 5 claims |
| Agreement | No false claims | Verify multi-source patterns |
| Coverage | Topic-complete | Match expected topics |

## Scoring Formula

```
Score = (structure × 25) + (attribution × 25) + (agreement × 25) + (coverage × 25)
```

## Expected Topics by Guide

| Guide | Required Topics |
|-------|-----------------|
| context-management | dumb zone, compaction, progressive disclosure, subagent isolation |
| debugging-verification | evidence-first, root cause, quality gates, hypothesis testing |
| complex-codebases | RPI/EPCC workflow, research phase, planning, mental alignment |
| reusable-tooling | skills structure, progressive disclosure, trigger words, token budgets |
| team-setup | CLAUDE.md patterns, settings.json, permissions, enterprise config |
| parallel-agents | delegation patterns, model selection, context isolation, coordination |

## Validation Steps

1. **Inventory Guides**: `Glob guides/use-cases/*/index.md`
2. **Check Structure**: 8/8 sections present?
3. **Sample Attribution**: Pick 5 claims, verify against sources
4. **Verify Agreement**: Check "best practice" claims have 3+ sources
5. **Assess Coverage**: Match topics against expected list
6. **Check Cross-Refs**: Verify all links valid
7. **Generate Report**: Score with issues

## Attribution Verification

For each sampled claim:
1. Find cited source in `references/analysis_*.md`
2. Read relevant section
3. Verify claim matches source meaning
4. Flag: out of context, overstated, reversed, unsupported

## Validation Report Template

```markdown
## Synthesis Validation: [PASS/FAIL]

**Guide**: [path]
**Score**: [N]/100

### Checks
- Structure: [X]/8 [✓/✗]
- Attribution: [N] checked, [N]% accurate [✓/✗]
- Agreement: [N] verified, [N] false [✓/✗]
- Coverage: [X]/[Y] topics [✓/✗]

### Issues Found
1. [Location]: [Issue] → [Fix]

### Next Step
[Proceed/Fix first]
```

## When to Trigger

- Before claiming ANY guide is ready
- Before archiving completed synthesis work
- When running `/audit-pipeline`
- When troubleshooting guide quality issues

## See Also

- `/validate-synthesis` command - Full validation process
- `quality-gate` skill - Workflow boundary enforcement
- `synthesis-validator` agent - Deep guide validation
