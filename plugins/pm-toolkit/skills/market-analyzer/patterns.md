# Market Analyzer - Detailed Patterns

## Input Types

- Industry reports
- Market research data
- Analyst reports
- Public company filings
- News and trend articles
- Government statistics

## Output Template

```markdown
# Market Analysis: [Market/Segment]

**Date:** YYYY-MM-DD
**Analyst:** [Name]
**Data Sources:** [List of sources]

---

## Executive Summary

[2-3 sentences: market size, growth rate, key opportunity]

---

## Market Size

### TAM (Total Addressable Market)

**Size:** $[X]B (YYYY)

**Definition:** [What's included in TAM]

**Source:** [Citation]

### SAM (Serviceable Addressable Market)

**Size:** $[X]B (YYYY)

**Definition:** [Geographic/segment constraints]

**Calculation:** [How derived from TAM]

### SOM (Serviceable Obtainable Market)

**Size:** $[X]M (YYYY)

**Definition:** [Realistic capture target]

**Assumptions:** [Key assumptions]

---

## Market Growth

### Historical Growth

| Year | Market Size | Growth Rate |
|------|-------------|-------------|
| YYYY | $XB | X% |
| YYYY | $XB | X% |

### Projected Growth

**CAGR:** [X]% (YYYY-YYYY)

**Drivers:**
1. [Growth driver 1]
2. [Growth driver 2]

**Constraints:**
1. [Growth constraint 1]

---

## Market Trends

### Trend 1: [Trend Name]

**Description:** [What's happening]

**Impact:** [How it affects the market]

**Timeline:** [When expected to materialize]

**Evidence:** [Supporting data/sources]

---

## Market Segments

### Segment 1: [Segment Name]

**Size:** $[X]B

**Growth:** [X]% CAGR

**Characteristics:**
- [Characteristic 1]
- [Characteristic 2]

**Opportunity:** [Why this segment matters]

---

## Adoption Patterns

### Current Adoption

**Penetration rate:** [X]%

**Adoption curve stage:** [Innovators/Early Adopters/Early Majority/Late Majority]

### Adoption Drivers

1. [Driver 1]
2. [Driver 2]

### Adoption Barriers

1. [Barrier 1]
2. [Barrier 2]

---

## Key Players

| Company | Market Share | Position |
|---------|--------------|----------|
| [Company 1] | X% | Leader |
| [Company 2] | X% | Challenger |

---

## Opportunities

1. **[Opportunity]**
   - Size: $[X]M potential
   - Timeline: [When]
   - Evidence: [Supporting data]

---

## Risks

1. **[Risk]**
   - Impact: High | Medium | Low
   - Probability: High | Medium | Low
   - Mitigation: [Approach]

---

## Recommendations

1. **[Recommendation]**
   - Rationale: [Why]
   - Priority: High | Medium | Low

---

## Data Quality Notes

**Confidence level:** High | Medium | Low

**Limitations:**
- [Limitation 1]
- [Limitation 2]

**Data freshness:** [Most recent data date]
```

## Quality Rules

- Cite all quantitative claims
- Note data freshness and reliability
- Mark projections vs. historical data
- Include confidence levels

---

**Template:** `templates/market-data-template.md`
**Output:** `research/market-YYYY-MM-DD-{market}.md`
