---
name: general-synthesizer
description: Use when exploring codebase or documentation - synthesizes findings into actionable insights with file:line references
when_to_use: exploring codebase, understanding patterns, how does X work, what exists for Y, research the architecture, investigate how
plan_mode: read_only
---

# General Synthesizer

## Quick Start

| You Say | Result |
|---------|--------|
| "How does authentication work?" | Research doc with architecture findings |
| "Explore the API patterns" | Synthesis of patterns with file references |
| "What exists for notifications?" | Inventory of relevant code and docs |

## Announcement
"I'm using the general-synthesizer to research [topic]..."

## Process
1. Read any mentioned files FULLY first
2. Spawn parallel Explore agents for different areas
3. Wait for ALL agents to complete
4. Synthesize findings with file:line references
5. Save to `research/recon-YYYY-MM-DD-{topic}.md`

## Core Principle
**Document what exists, not what should exist.**

## Output
Research document with:
- Executive summary (2-3 sentences)
- Evidence-based findings with `file:line` refs
- Key files prioritized
- Patterns identified
- Gaps and unknowns

## Transitions
- **Before**: User asks research question
- **After**: prd-generator (requirements) or task-breakdown (planning)

See [patterns.md](patterns.md) for detailed workflow.
