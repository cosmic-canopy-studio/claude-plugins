---
name: brief-generator
description: Use when creating quick feature summaries - generates one-pagers for stakeholder communication
when_to_use: one-pager, quick summary, executive brief, stakeholder overview, feature summary, pitch this feature
plan_mode: write
---

# Brief Generator

## Quick Start

| You Say | Result |
|---------|--------|
| "Create a one-pager for X" | Brief at `prds/brief-YYYY-MM-DD-{topic}.md` |
| "Quick summary for leadership" | Executive brief with value proposition |
| "Pitch this feature" | Scannable brief with problem/solution/effort |

## Announcement
"I'm using the brief-generator to create a feature brief for [topic]..."

## Process
1. Gather context from inputs and any research
2. Synthesize value proposition (problem → solution → benefit)
3. Outline approach at high level
4. Estimate effort using T-shirt sizing
5. Identify dependencies and questions
6. Save to `prds/brief-YYYY-MM-DD-{topic-slug}.md`

## Output
Feature brief with:
- Executive summary (2-3 sentences)
- User value (problem/solution/benefit)
- High-level approach
- Effort estimate (T-shirt size)
- Dependencies and open questions
- Next steps

## Quality Target
Brief should be scannable in 2-3 minutes. Focus on clarity over detail.

## When to Use Brief vs PRD
- **Brief**: Early exploration, leadership communication, quick alignment
- **PRD**: Detailed requirements, engineering handoff, feature documentation

## Transitions
- **Before**: User has feature idea or research findings
- **After**: prd-generator (full requirements) or task-breakdown (planning)

See [patterns.md](patterns.md) for template and T-shirt sizing guide.
