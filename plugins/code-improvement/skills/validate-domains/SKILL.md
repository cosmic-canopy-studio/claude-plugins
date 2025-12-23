---
name: validate-domains
description: Validate domain documents for completeness, source agreement, and cross-domain consistency (project) - when validating domain extraction, before synthesis from domains, during audits, or when checking domain quality
when_to_use: when validating domain documents, checking domain quality, before synthesis, or running pipeline audits
---

# Validate Domains

Check all `knowledge/*/domain.md` documents for quality and completeness.

## Quick Reference

| Metric | Minimum | Method |
|--------|---------|--------|
| Patterns per domain | 5 | Count `### {ID}:` sections |
| Sources per pattern | 1 | Check `**Sources**:` has entries |
| Provenance coverage | 100% | Every pattern in provenance.md |
| Cross-domain links | 2 | Count `→` or `#` references |
| Confidence distribution | 50%+ High/VeryHigh | Check `**Confidence**:` tags |

## Scoring Formula

```
Score = (patterns × 10) + (provenance_complete × 30) + (cross_refs × 10) + (freshness × 20) + (confidence_dist × 20) + (structure × 10)
```

| Component | Points | How Scored |
|-----------|--------|------------|
| Patterns | 0-10 | min(pattern_count/5, 1) × 10 |
| Provenance | 0-30 | (patterns_with_provenance / total_patterns) × 30 |
| Cross-refs | 0-10 | min(cross_refs/2, 1) × 10 |
| Freshness | 0-20 | 20 if updated after latest analysis, else 0 |
| Confidence | 0-20 | (high_confidence_count / total_patterns) × 20 |
| Structure | 0-10 | 2 per required section present |

| Tier | Score | Meaning |
|------|-------|---------|
| Production | ≥85 | Ready for guide synthesis |
| Review | 70-84 | Minor gaps in provenance or links |
| Draft | 50-69 | Significant patterns missing |
| Skeleton | <50 | Domain not usable for synthesis |

## Required Sections

Each `domain.md` must have:
1. YAML frontmatter (domain, version, last_updated, pattern_count, source_count)
2. Core Principles section
3. Patterns section (with at least 5 patterns)
4. Tensions & Trade-offs section
5. Cross-Domain Links section

## Validation Steps

1. **Inventory**: `Glob knowledge/*/domain.md` → list all domains
2. **Check Structure**: All required sections present?
3. **Count Patterns**: Parse pattern IDs (e.g., CTX-001)
4. **Verify Provenance**: Every pattern ID appears in corresponding provenance.md?
5. **Check Freshness**: Compare `last_updated` to latest analysis date
6. **Assess Confidence**: Count Very High / High / Medium distribution
7. **Validate Links**: Cross-domain references resolve?
8. **Calculate Score**: Apply formula
9. **Generate Report**: Pass/fail with remediation list

## Validation Report Template

```markdown
## Domain Validation: [PASS/FAIL]

### Summary
| Domain | Score | Tier | Patterns | Issues |
|--------|-------|------|----------|--------|
| context-management | 92 | Production | 8 | 0 |
| workflow-patterns | 78 | Review | 6 | 1 |
...

### Domain Details

#### context-management
- **Score**: 92/100 (Production)
- **Patterns**: 8 (✓)
- **Provenance**: 8/8 (100%) (✓)
- **Cross-refs**: 4 (✓)
- **Freshness**: Updated 2025-12-21 (✓)
- **Confidence**: 5 VeryHigh, 2 High, 1 Medium (✓)

#### workflow-patterns
- **Score**: 78/100 (Review)
- **Issues**:
  1. WFL-003 missing from provenance.md
  2. Last updated before analysis_transcript_ABC123.md

### Remediation Required
1. [workflow-patterns] Add provenance entry for WFL-003
2. [workflow-patterns] Run domain-extractor to integrate new analysis

### Overall Status
- Domains passing: 5/7
- Domains needing review: 2/7
- Proceed to synthesis: [Yes/No]
```

## Spot-Check Verification

For each domain, verify 2-3 patterns:
1. Navigate to provenance.md entry
2. Read source file at referenced line
3. Confirm pattern description matches source meaning
4. Flag: out of context, overstated, reversed, unsupported

## When to Trigger

- Before running `/batch-synthesize` (draws from domains)
- After running `/batch-extract-domains`
- When running `/audit-pipeline`
- When troubleshooting guide accuracy issues

## See Also

- `validate-analyses` skill - Validates source analyses
- `validate-synthesis` skill - Validates output guides
- `quality-gate` skill - Workflow boundary enforcement
- `domain-extractor` agent - Populates domains
