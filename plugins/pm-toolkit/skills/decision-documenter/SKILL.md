---
name: decision-documenter
description: Use when recording decisions - documents context, rationale, alternatives considered, and outcomes
when_to_use: we decided, decision record, document the choice, why did we choose, record this decision, ADR
plan_mode: write
---

# Decision Documenter

## Quick Start

| You Say | Result |
|---------|--------|
| "Document this decision" | Decision record with rationale and alternatives |
| "Why did we choose X over Y?" | ADR-style record with options compared |
| "Record that we decided to..." | Decision with context and consequences |

## Announcement
"I'm using the decision-documenter to record this decision..."

## Process
1. Capture the decision clearly and directly
2. Document context - what led to this decision
3. List options considered with pros/cons
4. Explain rationale - why this option won
5. Identify consequences - expected outcomes
6. Assign follow-up actions
7. Save to decision log or standalone file

## Output
Decision record (ADR-style) with:
- Decision statement (clear and direct)
- Context (what problem needed solving)
- Options considered (with pros/cons)
- Rationale (why this option won)
- Consequences (positive, negative, neutral)
- Follow-up actions with owners
- Related decisions and review date

## Quality Criteria
- Decision is clear and unambiguous
- At least 2 options considered (including "do nothing")
- Rationale explains the "why"
- Consequences are realistic (not just positives)

## Transitions
- **Before**: Team makes a decision, status-generator identifies decision needed
- **After**: task-breakdown (if implementation needed)

See [patterns.md](patterns.md) for ADR template and decision log format.
