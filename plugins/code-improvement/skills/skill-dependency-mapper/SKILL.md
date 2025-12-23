---
name: skill-dependency-mapper
description: Map skill interactions and detect dependency issues. USE WHEN skill not working with other skills, unexpected skill behavior after changes, circular dependency suspected, auditing skill portfolio, skill triggers another skill wrongly, cleaning up unused skills, refactoring skill structure. (project) - skill not working together, skill conflict, circular dependency, skill audit, skill interactions broken, unused skills
when_to_use: when mapping skill dependencies, detecting circular references, checking skill interactions, auditing skill portfolio, visualizing skill relationships, skill not working with other skills, skill conflict suspected
version: 1.0.0
---

# Skill Dependency Mapper

## Overview

Visualize skill interactions and detect dependency issues including circular references, orphaned skills, and overloaded dependencies.

## Quick Start

```
1. Scan .claude/skills/ for all skills
2. Parse references between skills
3. Build dependency graph
4. Report issues
```

## Dependency Types

| Type | Pattern | Example |
|------|---------|---------|
| **Direct** | Skill A references Skill B | "Use with skill-testing-framework" |
| **Chained** | A → B → C | Workflow sequences |
| **Circular** | A → B → A | Problematic loops |
| **Orphan** | No references to/from | Potentially unused |

## Iron Law

```
REPORT all circular dependencies as CRITICAL
FLAG skills with >5 incoming references (overloaded)
WARN about orphaned skills (no connections)
```

## Issue Detection

| Issue | Severity | Threshold |
|-------|----------|-----------|
| Circular dependency | CRITICAL | Any loop |
| Overloaded skill | WARNING | >5 refs |
| Orphaned skill | INFO | 0 connections |
| Broken reference | ERROR | Missing target |

## Output Format

```
Skill Dependency Map
====================

skill-a → skill-b, skill-c
skill-b → skill-d
skill-c → (none)
skill-d → skill-a  [CIRCULAR: skill-a → skill-b → skill-d → skill-a]

Issues Found:
- CRITICAL: Circular dependency detected
- WARNING: skill-b has 6 incoming references (overloaded)
- INFO: skill-e is orphaned (no connections)
```

See reference.md for dependency type details and resolution strategies.
