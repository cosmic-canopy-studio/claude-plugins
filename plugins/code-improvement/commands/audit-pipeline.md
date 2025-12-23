---
name: audit-pipeline
description: Audit pipeline by validating analyses, synthesis, calculating quality scores, and generating trend report
model: opus
---

# Audit Pipeline

You are performing a comprehensive audit of the entire analysis-to-synthesis pipeline.

## Process Overview

```
Step 1: Validate Analyses ────────┐
                                  ├──► Step 4: Calculate Scores
Step 2: Validate Synthesis ───────┘          │
                                             ▼
Step 3: Cross-Validate Pipeline ──────► Step 5: Generate Report
                                             │
                                             ▼
                                   Step 6: Track Trends (if history exists)
```

## Step 1: Analysis Validation

Run analysis validation on all `references/analysis_*.md` documents.

**Capture:**
- Total documents
- Pass/fail count by type (transcript, repo)
- Average scores
- Critical issues list
- Broken references list

**Key Metrics:**
- Analysis Pass Rate: (passing / total * 100)
- Average Analysis Score: (sum of scores / count)
- Evidence Density: (total insights / total documents)

## Step 2: Synthesis Validation

Run synthesis validation on all `guides/use-cases/*/index.md` guides.

**Capture:**
- Total guides
- Structure completeness per guide
- Attribution accuracy percentages
- Agreement verification results
- Coverage percentages
- Cross-reference validity

**Key Metrics:**
- Synthesis Pass Rate: (passing / total * 100)
- Average Attribution Accuracy: (sum / count)
- Average Coverage: (sum / count)
- False Agreement Count

## Step 3: Cross-Validate Pipeline

Check pipeline consistency:

**3a. Analysis → Synthesis Coverage**
For each analysis document:
- Is it cited in at least one synthesis guide?
- Are its key insights represented?
- Are novel patterns flagged for inclusion?

Calculate: Analysis Utilization Rate = (cited analyses / total analyses * 100)

**3b. INTAKE.md Consistency**
- Every "Analyzed = Yes" entry has a corresponding `analysis_*.md` file
- Every analysis file is listed in INTAKE.md
- Dates are consistent

**3c. Source Freshness**
- Note any analyses older than 30 days without synthesis
- Flag sources marked "Analyzed" but not contributing to guides

## Step 4: Calculate Aggregate Scores

### Analysis Quality Score (0-100)

```
AQ = (pass_rate * 0.40) +
     (avg_evidence_density / 2 * 0.30) +  # Normalized to 100
     (100 - broken_ref_rate * 0.30)
```

### Synthesis Quality Score (0-100)

```
SQ = (structure_complete_rate * 0.25) +
     (avg_attribution_accuracy * 0.25) +
     (agreement_accuracy_rate * 0.25) +
     (avg_coverage * 0.25)
```

### Pipeline Health Score (0-100)

```
PH = (AQ * 0.30) +
     (SQ * 0.40) +
     (analysis_utilization * 0.20) +
     (intake_consistency * 0.10)
```

### Quality Tier

| Score Range | Tier | Meaning |
|-------------|------|---------|
| 90-100 | Excellent | Ship with confidence |
| 80-89 | Good | Minor polish needed |
| 70-79 | Acceptable | Address noted issues |
| 60-69 | Needs Work | Significant improvements required |
| <60 | Critical | Major remediation needed |

## Step 5: Generate Report

```markdown
# Pipeline Audit Report

**Generated**: [Date]
**Audit ID**: [UUID or timestamp]

## Executive Summary

| Metric | Score | Trend | Status |
|--------|-------|-------|--------|
| Analysis Quality | 82/100 | ▲ +5 | Good |
| Synthesis Quality | 76/100 | ▼ -2 | Acceptable |
| Pipeline Health | 78/100 | ▲ +3 | Acceptable |

### Quick Actions Required

| Priority | Issue | Location | Action |
|----------|-------|----------|--------|
| Critical | Misrepresented claim | debugging:L67 | Revise wording |
| High | Missing section | debugging | Add Conflicting Advice |
| High | Coverage gap | team-setup | Add Enterprise OIDC |

---

## Analysis Validation Summary

**Documents**: [N] total
**Pass Rate**: [X%]
**Average Score**: [Y]/100

### By Type
| Type | Count | Pass | Fail | Avg Score |
|------|-------|------|------|-----------|
| Transcript | N | X | Y | Z |
| Repository | N | X | Y | Z |

### Score Distribution
| Tier | Count | Percentage |
|------|-------|------------|
| Production (≥85) | N | X% |
| Review (70-84) | N | X% |
| Draft (50-69) | N | X% |
| Skeleton (<50) | N | X% |

### Top Issues
1. [Issue from analysis validation]
2. [Issue from analysis validation]
3. [Issue from analysis validation]

---

## Synthesis Validation Summary

**Guides**: [N] total
**Average Score**: [X]/100

### By Guide
| Guide | Structure | Attribution | Agreement | Coverage | Score |
|-------|-----------|-------------|-----------|----------|-------|
| context-management | 9/9 | 95% | High | 100% | 92 |
| debugging | 8/9 | 87% | Medium | 75% | 78 |
| ... | ... | ... | ... | ... | ... |

### Attribution Issues
- [N] misrepresentations found
- [N] broken source references

### False Agreements
| Guide | Pattern | Claimed | Actual |
|-------|---------|---------|--------|
| ... | ... | ... | ... |

### Coverage Gaps
| Guide | Missing Topics |
|-------|----------------|
| debugging | Hypothesis testing |
| team-setup | Enterprise OIDC |

---

## Pipeline Coverage

### Analysis Utilization
- **Total analyses**: [N]
- **Cited in guides**: [X]
- **Utilization rate**: [Y%]

**Unused Analyses:**
| Analysis | Key Topics | Suggested Guide |
|----------|------------|-----------------|
| analysis_X.md | [topics] | context-management |

### INTAKE.md Consistency
- Entries with "Analyzed=Yes": [N]
- Matching analysis files: [X]
- Discrepancies: [list any]

---

## Aggregate Scores

| Component | Formula Weight | Raw Score | Weighted |
|-----------|----------------|-----------|----------|
| Analysis Pass Rate | 40% | 87% | 34.8 |
| Evidence Density | 30% | 78% | 23.4 |
| Reference Validity | 30% | 92% | 27.6 |
| **Analysis Quality** | | | **85.8** |

| Component | Formula Weight | Raw Score | Weighted |
|-----------|----------------|-----------|----------|
| Structure Complete | 25% | 89% | 22.3 |
| Attribution Accuracy | 25% | 91% | 22.8 |
| Agreement Accuracy | 25% | 75% | 18.8 |
| Coverage Rate | 25% | 83% | 20.8 |
| **Synthesis Quality** | | | **84.5** |

| Component | Formula Weight | Raw Score | Weighted |
|-----------|----------------|-----------|----------|
| Analysis Quality | 30% | 85.8 | 25.7 |
| Synthesis Quality | 40% | 84.5 | 33.8 |
| Analysis Utilization | 20% | 80% | 16.0 |
| INTAKE Consistency | 10% | 100% | 10.0 |
| **Pipeline Health** | | | **85.5** |

---

## Trend Analysis

### Historical Comparison
| Date | Analysis | Synthesis | Pipeline | Notes |
|------|----------|-----------|----------|-------|
| 2025-12-01 | 75 | 72 | 73 | Baseline |
| 2025-12-10 | 77 | 74 | 75 | +2 avg |
| 2025-12-20 | 86 | 85 | 86 | +11 avg |

### Trend Direction
- Analysis: ▲ Improving (+11 over 3 audits)
- Synthesis: ▲ Improving (+13 over 3 audits)
- Pipeline: ▲ Improving (+13 over 3 audits)

---

## Remediation Plan

### Critical (Fix immediately)
| Priority | Issue | Location | Action | Owner |
|----------|-------|----------|--------|-------|
| 1 | Misrepresented claim | debugging:L67 | Revise to match source | - |
| 2 | Missing section | debugging | Add Conflicting Advice | - |

### High (Fix within 1 week)
| Priority | Issue | Location | Action |
|----------|-------|----------|--------|
| 1 | Coverage gap | debugging | Add hypothesis testing |
| 2 | Coverage gap | team-setup | Expand OIDC section |
| 3 | Broken refs | debugging | Fix source paths |

### Medium (Fix within 1 month)
| Priority | Issue | Location | Action |
|----------|-------|----------|--------|
| 1 | Low utilization | analysis_X.md | Synthesize into guides |
| 2 | Agreement overstatement | parallel-agents | Lower confidence levels |

---

## Recommendations

### Process Improvements
1. Add pre-synthesis checklist to `/batch-synthesize`
2. Implement automated reference validation in CI
3. Create monthly audit schedule

### Quality Gates
Add these checks before marking work complete:
- [ ] Analysis: 5+ distinct insights extracted
- [ ] Analysis: All file:line references validated
- [ ] Synthesis: 100% source attribution
- [ ] Synthesis: Coverage ≥80% for expected topics

---

## Appendix

### Audit Configuration
```json
{
  "analysis": {
    "min_insights": 5,
    "min_quotes": 5,
    "min_file_refs": 10
  },
  "synthesis": {
    "min_principles": 2,
    "min_steps": 3,
    "min_mistakes": 2,
    "required_attribution": 1.0
  },
  "pipeline": {
    "min_utilization": 0.8,
    "max_stale_days": 30
  }
}
```

### Full Validation Outputs
[Link to or include full outputs from /validate-analyses and /validate-synthesis]
```

## Step 6: Track Trends

**If `references/audit_history.json` exists:**
1. Read previous audit results
2. Calculate trend (improving/declining/stable)
3. Include comparison in report

**If first audit:**
1. Create `references/audit_history.json` with this audit as baseline
2. Note "First audit - no trend data available"

**History Format:**
```json
{
  "audits": [
    {
      "date": "2025-12-20",
      "analysis_score": 85.8,
      "synthesis_score": 84.5,
      "pipeline_score": 85.5,
      "critical_issues": 2,
      "notes": "Initial validation system deployment"
    }
  ]
}
```

## Success Criteria

Audit is complete when:
- [ ] All analyses validated
- [ ] All synthesis guides validated
- [ ] Pipeline coverage calculated
- [ ] Aggregate scores calculated
- [ ] Trend comparison included (if history exists)
- [ ] Prioritized remediation list produced
- [ ] History updated
