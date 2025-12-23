---
name: prd-generator
description: Use when creating product requirements - generates PRD with problem statement, user stories, requirements, and success metrics
when_to_use: need a PRD, product requirements, feature spec, define the feature, create requirements document, document this feature
plan_mode: write
---

# PRD Generator

## Quick Start

| You Say | Result |
|---------|--------|
| "I need a PRD for notifications" | PRD at `prds/YYYY-MM-DD-notifications.md` |
| "Create product requirements for X" | PRD with user stories and acceptance criteria |
| "Define this feature" | Structured PRD with problem/solution/requirements |

## Announcement
"I'm using the prd-generator to create product requirements for [feature]..."

## Process
1. Gather feature context (ask if unclear)
2. Read research if available
3. Generate: Executive Summary, Problem Statement, 3-5 User Stories, 3-5 Requirements
4. Leave placeholders for evidence and metrics
5. Validate completeness
6. Save to `prds/YYYY-MM-DD-{feature-slug}.md`

## Generation Scope
**GENERATE:** Executive summary, problem statement, user stories, requirements
**PLACEHOLDER:** Evidence, specific metrics, design details, launch plan

## Quality Target
PRDs require ~25-30% manual editing to be production-ready.

## Common Mistakes
- Fabricating evidence (leave as placeholder)
- Including implementation details (PRD = WHAT, not HOW)
- Vague acceptance criteria ("fast" vs "< 2s P95")

## Transitions
- **Before**: general-synthesizer (research) or user-research-synthesizer
- **After**: task-breakdown (implementation planning) or requirements-writer (detailed specs)

See [patterns.md](patterns.md) for content patterns and validation checklist.
