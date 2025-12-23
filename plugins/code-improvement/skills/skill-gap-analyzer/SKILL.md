---
name: skill-gap-analyzer
description: Detect automation opportunities from repeated patterns in conversations (project) - when analyzing conversation patterns, finding automation opportunities, detecting skill gaps, identifying repeated explanations, reviewing session for automation
when_to_use: when analyzing conversation patterns, finding automation opportunities, detecting skill gaps, identifying repeated explanations, reviewing session for automation
version: 1.0.0
---

# Skill Gap Analyzer

## Overview

Detect patterns in conversation history that indicate opportunities for new skills, commands, or automation. Repetition is a signal.

## Quick Start

```
1. Analyze conversation or session logs
2. Identify repeated explanations or corrections
3. Score pattern frequency and impact
4. Recommend skill/command candidates
```

## Gap Detection Heuristics

| Pattern | Threshold | Confidence | Action |
|---------|-----------|------------|--------|
| Same explanation given | 3+ times | HIGH | Create skill |
| Same correction made | 2+ times | HIGH | Create skill with Iron Law |
| Similar workflow repeated | 3+ times | MEDIUM | Create command |
| Same question asked | 2+ times | MEDIUM | Add to CLAUDE.md |

## Iron Law

```
Gap CONFIRMED when: 3+ same explanations OR 2+ same corrections
NEVER propose skill for one-off patterns
ALWAYS verify pattern spans multiple sessions if possible
```

## Pattern Categories

| Category | Example | Skill Type |
|----------|---------|------------|
| **Behavioral** | "Remember to run tests first" | Iron Law skill |
| **Informational** | "Here's how X works..." | Reference skill |
| **Procedural** | "The steps are 1, 2, 3..." | Command |
| **Contextual** | "In this project we use..." | CLAUDE.md entry |

## Output Format

```markdown
## Gap Analysis Report

### Confirmed Gaps (High Confidence)
| Pattern | Frequency | Type | Recommended Action |
|---------|-----------|------|-------------------|
| Test reminder | 5x | Behavioral | skill: verification-reminder |
| API format | 3x | Informational | skill: api-conventions |

### Potential Gaps (Medium Confidence)
| Pattern | Frequency | Type | Verify With |
|---------|-----------|------|-------------|
| Git workflow | 2x | Procedural | Check more sessions |

### Recommendations
1. [Priority 1] Create skill-X addressing [gap]
2. [Priority 2] Add to CLAUDE.md: [convention]
```

See patterns.md for detailed detection heuristics.
