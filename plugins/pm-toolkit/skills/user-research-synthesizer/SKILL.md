---
name: user-research-synthesizer
description: Use when synthesizing user feedback or interview data - produces evidence-based insights with quotes and behavioral patterns
when_to_use: user feedback, interview findings, persona, customer pain points, user needs, behavioral patterns, what do users think
plan_mode: read_only
---

# User Research Synthesizer

## Quick Start

| You Say | Result |
|---------|--------|
| "Synthesize these interview notes" | User insights doc with patterns and quotes |
| "What are the pain points from this feedback?" | Pain points with evidence and severity |
| "Create a persona from this research" | Persona grounded in actual user data |

## Announcement
"I'm using the user-research-synthesizer to analyze [data source]..."

## Process
1. Read all provided research data
2. Identify behavioral patterns with evidence
3. Extract pain points with severity ratings
4. Capture verbatim quotes with context
5. Save to `research/user-insights-YYYY-MM-DD-{topic}.md`

## Core Principle
**Evidence-based insights only.** No fabricated statistics or unsupported claims.

## Output
User insights document with:
- Executive summary (2-3 sentences)
- User segments observed with counts
- Behavioral patterns with quotes
- Pain points with severity and frequency
- Recommendations with evidence links

## Quality Rules
- Cite specific sources for all claims
- Include verbatim quotes
- Note sample size limitations
- Mark inferences as hypotheses

## Transitions
- **Before**: User provides research data (interviews, surveys, feedback)
- **After**: prd-generator (requirements) or competitive-analyzer (market context)

See [patterns.md](patterns.md) for output template and detailed workflow.
