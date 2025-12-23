---
name: task-breakdown
description: Use when planning implementation - breaks features into phased deliverables with acceptance criteria and complexity estimates
when_to_use: break down this, implementation phases, decompose into tasks, how should we build this, create implementation plan
plan_mode: write
---

# Task Breakdown

## Quick Start

| You Say | Result |
|---------|--------|
| "Break down this feature" | Phased implementation plan at `plans/YYYY-MM-DD-{feature}.md` |
| "How should we implement this?" | Phases with deliverables, acceptance criteria, risks |
| "Create an implementation plan" | Plan with complexity estimates and dependencies |

## Announcement
"I'm using the task-breakdown to create an implementation plan for [feature]..."

## Process
1. Read PRD or feature description
2. Identify implementation phases (typically 2-4)
3. Define deliverables and acceptance criteria per phase
4. Estimate complexity using T-shirt sizing
5. Map dependencies and critical path
6. Save to `plans/YYYY-MM-DD-{feature}.md`

## Output
Implementation plan with:
- Executive summary (what, approach, total complexity)
- Scope (in/out of scope, constraints)
- Phases with deliverables and acceptance criteria
- Complexity summary table
- Dependencies map and critical path
- Parallelization opportunities
- Testing strategy and rollout plan

## T-Shirt Sizing
| Size | Typical Scope |
|------|---------------|
| XS | Few hours, single change |
| S | 1-2 days, isolated |
| M | 3-5 days, some integration |
| L | 1-2 weeks, cross-system |
| XL | 2+ weeks, significant scope |

## Transitions
- **Before**: prd-generator or requirements-writer (requirements exist)
- **After**: Implementation begins, status-generator (tracking progress)

See [patterns.md](patterns.md) for plan template and estimation guide.
