---
name: tracing-knowledge-lineages
description: Understand how ideas evolved over time to find old solutions for new problems and avoid repeating past failures (project) - when questioning "why do we use X", before abandoning approaches, or evaluating "new" ideas that might be revivals
when_to_use: when questioning "why do we use X", before abandoning approaches, or evaluating "new" ideas that might be revivals
version: 1.1.0
---

# Tracing Knowledge Lineages

Ideas have history. Understanding why we arrived at current approaches prevents repeating failures.

**Core principle:** Before judging current approaches or proposing "new" ones, trace their lineage.

## When to Trace

| Trigger | Action |
|---------|--------|
| "This seems overcomplicated" | Trace: Why did it grow? |
| "Why don't we just..." | Check: Someone probably tried |
| "This is the modern way" | Ask: What did the old way teach? |
| "We should switch to X" | Investigate: Why did we leave X? |

## Techniques Overview

| Technique | Use When |
|-----------|----------|
| Decision Archaeology | Finding when/why approach was chosen |
| Failed Attempt Analysis | Evaluating "we tried X, didn't work" |
| Revival Detection | Checking if "new" idea is rebranded old |
| Paradigm Shift Mapping | Understanding major transitions |

See [patterns.md](patterns.md) for detailed technique workflows.

## Quick Search Strategy

1. Check `docs/decisions/`, `docs/adr/`, `.decisions/`
2. Git archaeology: `git log --grep="keyword"`
3. Issue/PR discussions
4. Ask team: "Has anyone tried this before?"

See [reference.md](reference.md) for search patterns and examples.

## Red Flags

- "Let's rewrite without understanding why it's complex"
- "The old way was obviously wrong"
- "Nobody uses X anymore"
- Dismissing because "old" or adopting because "new"

**All mean: STOP. Trace the lineage first.**
