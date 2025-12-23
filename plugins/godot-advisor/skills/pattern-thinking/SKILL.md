---
name: pattern-thinking
description: Find universal principles across domains and trace how ideas evolved - when noticing patterns or questioning "why do we use X"
allowed-tools: Read, Grep, Glob, Bash
when_to_use:
  triggers:
    - "why do we use"
    - "same pattern in"
    - "have we tried before"
  symptoms:
    - "Pattern appearing in multiple places"
    - "Questioning existing approaches"
    - "Evaluating new ideas"
  auto_invoke: suggest
version: 1.0.0
---

# Pattern Thinking

## Overview

Two complementary techniques for finding deep patterns:
1. **Meta-Pattern Recognition** - Spot patterns appearing in 3+ domains
2. **Knowledge Lineages** - Understand how ideas evolved over time

## Technique 1: Meta-Pattern Recognition

When the same pattern appears in 3+ domains, it's probably universal.

### Process
1. Spot repetition - See same shape in 3+ places
2. Extract abstract form - Describe independent of domain
3. Identify variations - How does it adapt per domain?
4. Check applicability - Where else might this help?

### Quick Reference

| Pattern Appears In | Abstract Form | Where Else? |
|-------------------|---------------|-------------|
| CPU/DB/HTTP/DNS caching | Store frequently-accessed closer | LLM prompts, CDN |
| Layering (network/storage) | Separate into abstraction levels | Organization |
| Queuing (message/task) | Decouple producer/consumer | Events, async |
| Pooling (connection/thread) | Reuse expensive resources | Memory, governance |

### Example
**Pattern:** Rate limiting in API throttling, circuit breakers, admission control
**Abstract form:** Bound resource consumption to prevent exhaustion
**New application:** LLM token budgets (prevent context window exhaustion)

## Technique 2: Knowledge Lineages

Ideas have history. Understanding why we arrived at current approaches prevents repeating failures.

### When to Trace
- Before replacing existing approach (understand why it exists)
- Before dismissing "old" patterns (might be abandoned for wrong reasons)
- Before implementing "new" ideas (might be revivals)

### Tracing Techniques

**Decision Archaeology:**
1. Check decision records (`docs/decisions/`, `docs/adr/`)
2. Git archaeology (`git log --all --full-history -- path`)
3. Ask the person who wrote it

**Failed Attempt Analysis:**
When someone says "we tried X":
- What was the context? (constraints that no longer apply)
- What specifically failed? (whole approach or one aspect?)
- Has context changed? (new tools, different requirements)

**Revival Detection:**
For "new" approaches:
- Search for historical precedents (same thing, different name?)
- Understand why it died
- Check if resurrection conditions exist

### Common Revivals
- Microservices ← SOA ← Distributed Objects
- GraphQL ← SOAP ← RPC
- Serverless ← CGI scripts ← Cloud functions

### Red Flags
- "Let's rewrite this" (without understanding why it's complex)
- "The old way was wrong" (without understanding context)
- "Nobody uses X anymore" (without checking why it died)
- Dismissing because "old" (age ≠ quality)

## When to Override History

Override lineage when:
- Context fundamentally changed (tech that didn't exist now available)
- We learned critical lessons (industry understanding evolved)
- Original reasoning was flawed (cargo-culting without understanding)

**But document WHY** - future you needs to know this was deliberate.

## Remember

- 3+ domains = likely universal pattern
- Current approaches exist for reasons (trace them)
- Past failures might work now (context changes)
- "New" might be revival (check precedents)
