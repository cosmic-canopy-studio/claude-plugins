---
name: assumption-testing
description: Challenge current thinking through inversion and simplification - when feeling forced into "the only way" or when complexity is spiraling
allowed-tools: Read, Grep, Glob, Bash
when_to_use:
  triggers:
    - "there's only one way"
    - "this is getting complex"
    - "we need to handle A, B, C differently"
  symptoms:
    - "Same thing implemented multiple ways"
    - "Growing special cases"
    - "Forced by assumptions"
  auto_invoke: suggest
version: 1.0.0
---

# Assumption Testing

## Overview

Two complementary techniques for breaking through stuck thinking:
1. **Inversion** - Flip assumptions to reveal hidden constraints
2. **Simplification** - Find unifying principles that eliminate complexity

## Technique 1: Inversion

Flip every assumption and see what still works.

### Process
1. List core assumptions - What "must" be true?
2. Invert each - "What if opposite were true?"
3. Explore implications - What would we do differently?
4. Find valid inversions - Which actually work?

### Quick Reference

| Normal Assumption | Inverted | What It Reveals |
|-------------------|----------|-----------------|
| Cache to reduce latency | Add latency to enable caching | Debouncing patterns |
| Pull data when needed | Push data before needed | Prefetching |
| Handle errors when occur | Make errors impossible | Type systems, contracts |
| Build features users want | Remove features they don't need | Simplicity wins |
| Optimize for common case | Optimize for worst case | Resilience patterns |

### Red Flags for Inversion
- "There's only one way to do this"
- Forcing solution that feels wrong
- Can't articulate why approach is necessary

## Technique 2: Simplification Cascades

Find one insight that eliminates multiple components.

### Process
1. List the variations - What's implemented multiple ways?
2. Find the essence - What's the same underneath?
3. Extract abstraction - What's the domain-independent pattern?
4. Test it - Do all cases fit cleanly?
5. Measure cascade - How many things become unnecessary?

### Examples

**Stream Abstraction:**
- Before: Separate handlers for batch/real-time/file/network
- Insight: "All inputs are streams"
- After: One processor, multiple sources
- Eliminated: 4 implementations

**Resource Governance:**
- Before: Session tracking, rate limiting, file validation (all separate)
- Insight: "All are per-entity resource limits"
- After: One ResourceGovernor with resource types
- Eliminated: 4 enforcement systems

### Red Flags for Simplification
- "We just need to add one more case..."
- "These are all similar but different"
- Refactoring feels like whack-a-mole
- Growing configuration file

## Remember

- Strategic slowness can improve UX (from inversion)
- Simplification cascades = 10x wins, not 10% improvements
- One powerful abstraction > ten clever hacks
- Measure in "how many things can we delete?"
