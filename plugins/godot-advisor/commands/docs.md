---
description: Create documentation - how-to guides, tutorials, references, or explanations
argument-hint: [type] [topic]
---

# Docs: $ARGUMENTS

Unified documentation command. Creates appropriate documentation type based on intent.

## Documentation Types

| Type | Purpose | Audience |
|------|---------|----------|
| how-to | Task completion steps | Working developers |
| tutorial | Learning journey | Beginners |
| reference | Technical details | Looking up specifics |
| explanation | Conceptual understanding | Understanding "why" |

## Type Detection

| Arguments | Type | Example |
|-----------|------|---------|
| "how to X", "guide for X" | how-to | `/docs how to add new enemy types` |
| "tutorial X", "learn X" | tutorial | `/docs tutorial player movement` |
| "reference X", "api X" | reference | `/docs reference combat system` |
| "explain X", "why X" | explanation | `/docs explain state machine pattern` |

If type is ambiguous, ask via AskUserQuestion.

## How-To Guide

```
/docs how to add new enemy types
```

### Structure
```markdown
# How to Add New Enemy Types

## Overview
[What this guide covers]

## Prerequisites
- [What you need before starting]

## Steps

### Step 1: Create Enemy Resource
[Action + code example]

### Step 2: Configure Properties
[Action + code example]

### Step 3: Add to Scene
[Action + code example]

## Verification
[How to confirm it works]

## Common Issues
- [Problem → Solution]

## Related
- [Links to related docs]
```

### Process
1. Research existing implementation
2. Identify key steps
3. Write with code examples
4. Add troubleshooting

## Tutorial

```
/docs tutorial player movement
```

### Structure
```markdown
# Tutorial: Player Movement

## What You'll Learn
- [Learning outcome 1]
- [Learning outcome 2]

## Prerequisites
- [Required knowledge]
- [Required setup]

## Part 1: Setting Up the Player
[Explanation + guided coding]

## Part 2: Adding Movement
[Build on previous, explain concepts]

## Part 3: Handling Collisions
[Continue building]

## What's Next
[Further learning paths]

## Complete Code
[Final code for reference]
```

### Process
1. Define learning objectives
2. Structure as building journey
3. Explain concepts, don't just list steps
4. Include "why" alongside "how"

## Reference

```
/docs reference combat system
```

### Structure
```markdown
# Combat System Reference

## Overview
[Brief description]

## Classes

### DamageCalculator
[Class description]

#### Methods

##### calculate_damage(attacker, defender) → int
[Parameters, return value, example]

##### apply_modifiers(base_damage, modifiers) → int
[Parameters, return value, example]

## Signals

### damage_dealt(amount: int, target: Node)
[When emitted, what to connect]

## Constants

### DamageType
- PHYSICAL
- MAGICAL
- TRUE

## Examples
[Common usage patterns]
```

### Process
1. Document all public APIs
2. Include method signatures
3. Show example usage
4. Link to related references

## Explanation

```
/docs explain state machine pattern
```

### Structure
```markdown
# Understanding State Machines

## What is a State Machine?
[Conceptual introduction]

## Why Use State Machines?
[Problems they solve]

## How State Machines Work
[Detailed explanation]

## State Machine vs Alternatives
[When to use, when not to use]

## Implementation in Godot
[How the concept applies here]

## Further Reading
[Links for deeper understanding]
```

### Process
1. Start with "why" not "how"
2. Build conceptual framework
3. Use analogies and diagrams
4. Connect to practical application

## Output Location

Documentation is written to `docs/`:
```
docs/
├── how-to/
│   └── add-enemy-types.md
├── tutorials/
│   └── player-movement.md
├── reference/
│   └── combat-system.md
└── explanations/
    └── state-machines.md
```

## Integration with Other Commands

| After /docs | Action |
|-------------|--------|
| How-to written | User follows guide |
| Tutorial written | User learns feature |
| Reference written | User looks up specifics |
| Explanation written | User understands concepts |

## Guidelines

- **Research first** - Understand what you're documenting
- **Code examples** - Always include working code
- **Verify accuracy** - Test code examples work
- **Link related** - Connect to other docs and skills
- **Keep focused** - One topic per document

## Examples

### Quick How-To
```
/docs how to save game state

→ Research save system in codebase
→ Identify key steps
→ Write to docs/how-to/save-game-state.md
```

### Learning Tutorial
```
/docs tutorial creating UI menus

→ Plan learning journey (4 parts)
→ Write progressively building tutorial
→ Include exercises
→ Write to docs/tutorials/ui-menus.md
```

### Technical Reference
```
/docs reference player.gd

→ Document all public methods
→ Document signals
→ Document exports
→ Write to docs/reference/player.md
```
