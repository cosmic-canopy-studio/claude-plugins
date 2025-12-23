---
name: when-stuck
description: Dispatch to the right problem-solving technique based on how you're stuck - when stuck and unsure which problem-solving technique to apply for your specific type of stuck-ness
allowed-tools: Read, Grep, Glob, Bash
version: 1.0.0
when_to_use:
  triggers:
    - "I'm stuck"
    - "don't know how to"
    - "can't figure out"
    - "not sure what approach"
  symptoms:
    - "User expressing confusion"
    - "Multiple failed attempts mentioned"
    - "Blocked on decision"
  context:
    - "Problem-solving in progress"
    - "Implementation uncertainty"
  auto_invoke: suggest
  follows:
    - "Any failed attempt"
  leads_to:
    - "systematic-debugging"
    - "simplification-cascades"
    - "collision-zone-thinking"
    - "meta-pattern-recognition"
    - "inversion-exercise"
version: 1.2.0
---

# When Stuck - Problem-Solving Dispatch

## Overview

Different stuck-types need different techniques. This skill helps you quickly identify which problem-solving skill to use.

**Core principle:** Match stuck-symptom to technique.

## Stuck-Type → Technique

| How You're Stuck | Use This Skill |
|------------------|----------------|
| **Complexity spiraling** - Same thing 5+ ways, growing special cases | simplification-cascades |
| **Need innovation** - Conventional solutions inadequate, can't find fitting approach | collision-zone-thinking |
| **Recurring patterns** - Same issue different places, reinventing wheels | meta-pattern-recognition |
| **Forced by assumptions** - "Must be done this way", can't question premise | inversion-exercise |
| **Code broken** - Wrong behavior, test failing, unexpected output | systematic-debugging |

## Quick Diagnostic

Ask yourself:

1. **Am I implementing the same thing multiple ways?** → simplification-cascades
2. **Have I tried everything conventional?** → collision-zone-thinking
3. **Does this feel familiar from other contexts?** → meta-pattern-recognition
4. **Am I being forced into an approach that feels wrong?** → inversion-exercise
5. **Is code behaving unexpectedly?** → systematic-debugging

## Process

1. **Identify stuck-type** - What symptom matches above?
2. **Load that skill** - The skill will auto-load based on context
3. **Apply technique** - Follow its process
4. **If still stuck** - Try different technique or combine

## Combining Techniques

Some problems need multiple techniques:

- **Simplification + Meta-pattern**: Find pattern, then simplify all instances
- **Collision + Inversion**: Force metaphor, then invert its assumptions
- **Meta-pattern + Simplification**: Recognize you're reinventing, then simplify to the known solution

## Remember

- Match symptom to technique
- One technique at a time
- Combine if first doesn't work
- Document what you tried
