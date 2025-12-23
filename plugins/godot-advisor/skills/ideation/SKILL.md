---
name: ideation
description: Transform rough ideas into designs through structured questioning and metaphor-based exploration - use before /plan when an idea needs refinement
allowed-tools: Read, Grep, Glob, Bash
when_to_use:
  triggers:
    - "I have an idea"
    - "What if we"
    - "brainstorm"
    - "design this"
  symptoms:
    - "Feature idea described"
    - "Project concept mentioned"
  context:
    - "Before /plan"
    - "Before /build"
  auto_invoke: suggest
  leads_to:
    - "/plan"
    - "/build"
version: 1.0.0
---

# Ideation: Ideas to Designs

## Overview

Transform rough ideas into designs through structured questioning and creative exploration.

**Core principle:** Ask questions to understand, explore alternatives with metaphor-mixing, present design incrementally.

## The Process

### Phase 1: Understanding
- Check current project state in working directory
- Ask ONE question at a time to refine the idea
- Prefer multiple choice when possible
- Gather: Purpose, constraints, success criteria

### Phase 2: Exploration

**Standard approach:**
- Propose 2-3 different approaches
- For each: Core architecture, trade-offs, complexity assessment
- Ask which approach resonates

**When stuck or need breakthrough:**
Use metaphor-mixing - force unrelated concepts together:
- Pick two unrelated concepts from different domains
- "What if we treated [A] like [B]?"
- Explore emergent properties
- Test where the metaphor breaks

| Stuck On | Try Treating As | Might Discover |
|----------|-----------------|----------------|
| Code organization | DNA/genetics | Evolutionary algorithms |
| Service architecture | Lego bricks | Composable microservices |
| Data management | Water flow | Streaming, data lakes |
| Request handling | Postal mail | Message queues, async |
| Error handling | Circuit breakers | Fault isolation |

### Phase 3: Design Presentation
- Present in 200-300 word sections
- Cover: Architecture, components, data flow, error handling
- Ask after each section: "Does this look right?"

### Phase 4: Handoff
When design is approved: "Ready to create the implementation plan with /plan?"

## When to Revisit Earlier Phases

Go backward when:
- Partner reveals new constraint during Phase 2 or 3 → Return to Phase 1
- Partner questions approach during Phase 3 → Return to Phase 2
- Something doesn't make sense → Go back and clarify

Don't force forward linearly when going backward would give better results.

## Remember

- One question per message during Phase 1
- Apply YAGNI ruthlessly
- Explore 2-3 alternatives before settling
- Present incrementally, validate as you go
- Wild metaphor combinations often yield best insights
