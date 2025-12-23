---
name: token-budget-advisor
description: Monitor token usage and warn about dumb zone thresholds. USE WHEN responses getting worse, model repeating itself, same corrections needed repeatedly, conversation feels sluggish, hitting token limits, need to compact context, starting a long session. (project) - context full, token limit, dumb zone, context degraded, session slow, responses worse, model repeating, need compaction
when_to_use: when context full, token limit approaching, avoiding dumb zone, context degraded, session slow, optimizing context usage, responses getting worse, model repeating itself, same corrections needed
version: 1.0.0
---

# Token Budget Advisor

## Overview

Monitor context window usage and provide actionable guidance to stay in the "smart zone." Performance degrades around 40% context usage.

## Quick Start

```
1. Estimate current context usage (messages × avg tokens)
2. Check against threshold zones
3. Recommend action based on zone
```

## Threshold Zones

| Zone | Usage | Status | Action |
|------|-------|--------|--------|
| **Green** | 0-35% | Optimal | Continue normally |
| **Yellow** | 35-50% | Caution | Consider compacting |
| **Orange** | 50-60% | Warning | Compact now |
| **Red** | 60%+ | Critical | Reset or handoff |

## Iron Law

```
WARN at 35% - suggest proactive measures
ALERT at 50% - recommend compaction
CRITICAL at 60% - strongly recommend reset
```

## Token Estimation

Quick estimate: `tokens ≈ words × 1.33`

| Content Type | Tokens per 100 words |
|--------------|---------------------|
| Plain prose | ~133 |
| Technical docs | ~154 |
| Code | ~200 |
| JSON/YAML | ~222 |

## Compaction Strategies

1. **Handoff document**: Summarize context for new session
2. **Sub-agent delegation**: Fork context for isolated work
3. **Selective reset**: Keep only essential context
4. **On-demand research**: Replace cached context with fresh queries

## Warning Signs

- Response quality declining
- Model repeating earlier suggestions
- Increased latency
- Model losing track of conversation
- Same corrections needed repeatedly

See reference.md for detailed thresholds and calculation methods.
