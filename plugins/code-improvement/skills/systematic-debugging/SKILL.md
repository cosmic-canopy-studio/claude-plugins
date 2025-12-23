---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes - four-phase framework (root cause investigation, pattern analysis, hypothesis testing, implementation) that ensures understanding before attempting solutions (project) - bug, test failure, unexpected behavior, before proposing fixes, debugging, root cause
when_to_use: bug, test failure, unexpected behavior, before proposing fixes, debugging, root cause
---

# Systematic Debugging

**Core principle:** ALWAYS find root cause before attempting fixes. Symptom fixes are failure.

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

If you haven't completed Phase 1, you cannot propose fixes.

## Quick Start

| Phase | Key Action | Success Criteria |
|-------|------------|------------------|
| 1. Root Cause | Read errors, reproduce, trace | Understand WHAT and WHY |
| 2. Pattern | Find working examples, compare | Identify differences |
| 3. Hypothesis | Form theory, test minimally | Confirmed or reject |
| 4. Implementation | Create test, fix, verify | Bug resolved |

## When to Use

Use for ANY technical issue: test failures, bugs, unexpected behavior, performance problems, build failures.

**Especially when:**
- Under time pressure (emergencies make guessing tempting)
- "Just one quick fix" seems obvious
- Previous fix didn't work

## Red Flags - STOP

If you catch yourself:
- "Quick fix for now, investigate later"
- "Just try changing X"
- Proposing solutions before investigation
- 3+ fixes failed (question architecture instead)

**ALL mean:** Return to Phase 1.

## Detailed Process

See [patterns.md](patterns.md) for the four-phase framework.
See [reference.md](reference.md) for edge cases and rationalizations.
