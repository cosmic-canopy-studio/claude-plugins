---
name: skill-debugging-assistant
description: Debug skill failures including trigger failures, wrong output, iron law violations, and context overflow (project) - when skill not loading, skill trigger failing, skill wrong output, skill broken, debugging skill, skill not working, skill doesn't activate
when_to_use: when skill not loading, skill trigger failing, skill wrong output, skill broken, debugging skill, skill not working, skill doesn't activate
version: 1.1.0
---

# Skill Debugging Assistant

Systematic skill debugging following root cause investigation before fixes.

## Quick Start

```
1. Describe the skill problem
2. I investigate in priority order (most common causes first)
3. Identify root cause before proposing fixes
4. Verify fix resolves the issue
```

## Investigation Order

Check in this order (most common failures first):

| Priority | Check | Common Issue |
|----------|-------|--------------|
| **1** | YAML frontmatter syntax | Missing quotes, bad indentation |
| **2** | Description keywords | Vague terms, buried intent |
| **3** | when_to_use field | Abstract concepts, missing symptoms |
| **4** | Tool access permissions | Missing required tools |
| **5** | File path correctness | Wrong location, missing files |
| **6** | Token budget | Skill too large, context overflow |
| **7** | Conflicting skills | Another skill triggering instead |

## Iron Law

```
ALWAYS check in investigation order above
NO FIXES without identifying root cause first
NEVER skip to "try this fix" without diagnosis
```

## Common Fixes

| Problem | Root Cause | Fix |
|---------|------------|-----|
| Skill never loads | Vague description | Add specific trigger keywords |
| Wrong skill loads | Keyword overlap | Add negative triggers |
| Context overflow | Skill too large | Apply progressive disclosure |

## Integration

- Use after skill-testing-framework finds failures
- Pair with skill-performance-profiler for size issues

See patterns.md for failure patterns and diagnostic steps.
See reference.md for checklists and error messages.
