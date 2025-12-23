# Competitive Analyzer - Detailed Patterns

## Input Types

- Competitor product documentation
- Feature lists from websites
- Pricing information
- Marketing materials
- Industry reports
- User reviews of competitors

## Output Template

```markdown
# Competitive Analysis: [Market/Category]

**Date:** YYYY-MM-DD
**Analyst:** [Name]
**Competitors Analyzed:** [List]

---

## Executive Summary

[2-3 sentences: competitive position, key differentiators, main opportunity]

---

## Market Landscape

### Overview

[Brief description of the competitive landscape]

### Competitor Categories

**Direct Competitors:**
- [Competitor 1] - [One-line description]
- [Competitor 2] - [One-line description]

**Indirect Competitors:**
- [Competitor 3] - [One-line description]

**Emerging Players:**
- [Competitor 4] - [One-line description]

---

## Competitor Profiles

### [Competitor 1]

**Overview:** [Brief description]

**Target Market:** [Who they serve]

**Strengths:**
- [Strength 1]
- [Strength 2]

**Weaknesses:**
- [Weakness 1]
- [Weakness 2]

**Pricing:** [Pricing model/range]

**Key Features:** [Notable features]

---

## Feature Comparison Matrix

| Feature | Our Product | Competitor 1 | Competitor 2 | Competitor 3 |
|---------|-------------|--------------|--------------|--------------|
| [Feature 1] | ✓ / ✗ / Partial | ✓ / ✗ | ✓ / ✗ | ✓ / ✗ |
| [Feature 2] | ✓ / ✗ / Partial | ✓ / ✗ | ✓ / ✗ | ✓ / ✗ |

**Legend:** ✓ = Full support, ✗ = Not available, Partial = Limited support

---

## Positioning Analysis

### Our Position

**Current positioning:** [How we're positioned]

**Differentiators:**
1. [Differentiator 1]
2. [Differentiator 2]

### Positioning Map

```
                    High Price
                        |
           [Competitor 2]  |  [Competitor 1]
                        |
    Low Features -------+------- High Features
                        |
           [Us]         |  [Competitor 3]
                        |
                    Low Price
```

---

## Competitive Gaps

### Where We Lead

| Gap | Our Advantage | Competitor Status |
|-----|---------------|-------------------|
| [Gap 1] | [Our capability] | [Competitor limitation] |

### Where We Trail

| Gap | Competitor Advantage | Our Status |
|-----|---------------------|------------|
| [Gap 1] | [Their capability] | [Our limitation] |

---

## Opportunities

1. **[Opportunity 1]**
   - Gap: [What's missing in market]
   - Evidence: [Supporting observation]
   - Impact: High | Medium | Low

---

## Threats

1. **[Threat 1]**
   - Source: [Competitor or trend]
   - Risk: [What could happen]
   - Mitigation: [How to address]

---

## Recommendations

1. **[Recommendation]**
   - Rationale: [Why]
   - Priority: High | Medium | Low

---

## Data Sources

- [Source 1] - [Date accessed]
- [Source 2] - [Date accessed]
```

## Quality Rules

- Cite sources for all competitor information
- Note when information is inferred vs. confirmed
- Mark speculation clearly
- Update date for all pricing/feature claims

---

**Template:** `templates/competitive-analysis-template.md`
**Output:** `research/competitive-YYYY-MM-DD-{market}.md`
