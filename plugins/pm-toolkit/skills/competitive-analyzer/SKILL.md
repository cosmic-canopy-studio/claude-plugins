---
name: competitive-analyzer
description: Use when comparing products or analyzing market position - generates feature matrices and positioning analysis
when_to_use: competitor comparison, vs alternatives, market position, feature gap, how do we compare, what competitors do
plan_mode: read_only
---

# Competitive Analyzer

## Quick Start

| You Say | Result |
|---------|--------|
| "Compare us to Competitor X" | Feature matrix with positioning analysis |
| "What's the competitive landscape?" | Market overview with player profiles |
| "Where do we have feature gaps?" | Gap analysis with opportunities |

## Announcement
"I'm using the competitive-analyzer to research [competitors/market]..."

## Process
1. Gather competitor information from provided sources
2. Build competitor profiles (strengths, weaknesses, pricing)
3. Create feature comparison matrix
4. Identify gaps and opportunities
5. Save to `research/competitive-YYYY-MM-DD-{market}.md`

## Core Principle
**Cite sources for all claims.** Mark speculation clearly.

## Output
Competitive analysis with:
- Executive summary (position + opportunity)
- Competitor profiles with SWOT
- Feature comparison matrix
- Positioning map
- Gap analysis (where we lead/trail)
- Opportunities and threats

## Quality Rules
- Note when information is inferred vs. confirmed
- Include data freshness dates
- Mark speculation clearly
- Update pricing/feature claims with dates

## Transitions
- **Before**: User asks about competitors or market position
- **After**: prd-generator (feature specs) or brief-generator (strategy summary)

See [patterns.md](patterns.md) for output template and detailed workflow.
