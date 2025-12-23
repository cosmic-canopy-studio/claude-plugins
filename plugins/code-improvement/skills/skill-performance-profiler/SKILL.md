---
name: skill-performance-profiler
description: Profile skill token usage and execution performance. USE WHEN skill slow, context full, token usage high, optimizing skills, reducing skill size, profiling skill performance, context overflow.
when_to_use: skill slow, context full, token usage high, optimizing skills, profiling skill performance, reducing skill size, context overflow
version: 1.0.0
---

# Skill Performance Profiler

Analyze skill token usage and identify optimization opportunities.

## Token Budgets

| File | Target | Maximum | Action if Exceeded |
|------|--------|---------|-------------------|
| **SKILL.md** | <200 words | 300 words | Split to reference files |
| **patterns.md** | <300/pattern | 500/pattern | Break into multiple patterns |
| **reference.md** | Unlimited | - | OK for heavy content |

## Iron Law

```
SKILL.md MUST be <300 words (ideally <200)
NEVER force-load with @ syntax in SKILL.md
ALWAYS use relative links for progressive disclosure
```

## Profiling Metrics

| Metric | Good | Warning | Critical |
|--------|------|---------|----------|
| SKILL.md words | <200 | 200-300 | >300 |
| Total skill tokens | <500 | 500-1000 | >1000 |
| @ force-references | 0 | 1-2 | >2 |

## Quick Start

1. Provide skill path to analyze
2. Measure token counts and structure
3. Identify violations of size guidelines
4. Recommend specific optimizations

See [patterns.md](patterns.md) for analysis process and optimization techniques.
See [reference.md](reference.md) for token estimation and file organization patterns.
