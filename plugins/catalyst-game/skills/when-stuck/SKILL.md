---
name: when-stuck
description: Dispatch to the right problem-solving technique based on how you're stuck - when stuck and unsure which technique to apply
allowed-tools: Read, Grep, Glob, Bash
when_to_use:
  triggers:
    - "I'm stuck"
    - "don't know how to"
    - "can't figure out"
  symptoms:
    - "User expressing confusion"
    - "Multiple failed attempts"
  auto_invoke: suggest
  leads_to:
    - "systematic-debugging"
    - "assumption-testing"
    - "pattern-thinking"
    - "ideation"
version: 2.0.0
---

# When Stuck - Problem-Solving Dispatch

## Overview

Match your stuck-type to the right technique.

## Stuck-Type → Technique

| How You're Stuck | Use This Skill |
|------------------|----------------|
| **Code broken** - Wrong behavior, test failing, unexpected output | systematic-debugging |
| **Complexity spiraling** - Same thing 5+ ways, growing special cases | assumption-testing |
| **Forced by assumptions** - "Must be done this way" | assumption-testing |
| **Need innovation** - Conventional solutions inadequate | ideation (metaphor-mixing) |
| **Recurring patterns** - Same issue different places | pattern-thinking |
| **Questioning history** - "Why do we use X?" | pattern-thinking |

## Quick Diagnostic

1. **Is code behaving unexpectedly?** → systematic-debugging
2. **Am I implementing the same thing multiple ways?** → assumption-testing
3. **Am I forced into an approach that feels wrong?** → assumption-testing
4. **Have I tried everything conventional?** → ideation
5. **Does this feel familiar from other contexts?** → pattern-thinking

## Process

1. Identify stuck-type from table above
2. Use that skill
3. If still stuck, try a different technique

## Remember

- Match symptom to technique
- One technique at a time
- Document what you tried
