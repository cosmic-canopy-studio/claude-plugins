---
description: Research multiple related topics simultaneously using parallel subagent execution
argument-hint: [comma-separated list of topics]
allowed-tools: Task, TodoWrite, Write
model: opus
---

# Parallel Multi-Topic Research

Research these related topics in parallel: $ARGUMENTS

## Parallel Execution Strategy

1. Parse topics from comma-separated list
2. Spawn topic-researcher for EACH topic simultaneously
3. Spawn academic-researcher for EACH topic simultaneously
4. Wait for all subagents to complete
5. Synthesize findings across all topics

## Expected Output

- Individual topic reports
- Cross-topic analysis
- Combined synthesis report
- Comprehensive source list

Use extended thinking to plan the optimal research strategy.