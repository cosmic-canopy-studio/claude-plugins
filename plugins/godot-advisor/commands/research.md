---
description: Explore codebase, patterns, or documentation - works in plan mode (read-only)
argument-hint: [question or topic]
---

# Research: $ARGUMENTS

Explore and understand before building. Plan-mode compatible (read-only operations only).

## Research Types

| Question Pattern | Research Type | Method |
|------------------|---------------|--------|
| "how does X work" | Codebase | Explore agents |
| "where is X" | Codebase | Glob + Grep |
| "X pattern for Y" | Patterns | pattern-researcher |
| "Godot X documentation" | External | godot-docs-fetcher |
| "best practice for X" | Combined | Multiple sources |

## Type 1: Codebase Exploration

```
/research how does player input work
/research where is the combat system
```

### Process

1. **Spawn Explore agents** for comprehensive search:
   ```
   Task Explore "Find how player input is handled in this codebase"
   ```

2. **Synthesize findings** with file:line references:
   ```
   ## Player Input System

   The player input is handled in several files:

   1. scripts/player.gd:45 - _unhandled_input() captures key events
   2. scripts/input_handler.gd:12 - Centralized input mapping
   3. project.godot - Input action definitions

   Flow: Input → InputHandler → Player._unhandled_input()
   ```

3. **Offer next steps:**
   ```
   Ready to continue:
   - /plan to design changes
   - /build to implement directly
   ```

## Type 2: Pattern Research

```
/research singleton pattern for game managers
/research state machine patterns in Godot
```

### Process

1. **Invoke pattern-researcher agent:**
   ```
   Task pattern-researcher "Research singleton pattern for game managers in Godot 4"
   ```

2. **Sources checked:**
   - Official Godot documentation
   - Existing skills in .claude/skills/
   - Community patterns (GDQuest, etc.)
   - This codebase for existing implementations

3. **Output format:**
   ```markdown
   ## Singleton Pattern for Game Managers

   ### Official Approach (Autoloads)
   - Use Project Settings > Autoloads
   - Global access via node name
   - Example: GameManager.instance

   ### Skill Reference
   See: .claude/skills/godot-autoloads/SKILL.md

   ### Existing Implementation
   This codebase uses:
   - scripts/autoloads/game_manager.gd (line 1-45)
   - Pattern: Autoload with exported config

   ### Recommendation
   Follow existing pattern for consistency.
   ```

## Type 3: Godot Documentation

```
/research Godot CharacterBody2D move_and_slide
/research Godot AnimationTree state machine
```

### Process

1. **Invoke godot-docs-fetcher agent:**
   ```
   Task godot-docs-fetcher "Fetch CharacterBody2D.move_and_slide documentation"
   ```

2. **Output:**
   - Method signature
   - Parameters and return values
   - Official example code
   - Related methods

## Type 4: Combined Research

```
/research best practice for player health system
```

### Process

1. **Check multiple sources:**
   - Codebase: Existing implementations
   - Skills: Relevant patterns
   - Docs: Official guidance

2. **Synthesize with recommendations:**
   ```markdown
   ## Player Health System: Best Practices

   ### This Codebase
   No existing health system found.

   ### Relevant Skills
   - godot-custom-resources - For HealthData resource
   - godot-signals - For health_changed signal

   ### Pattern Recommendation
   Use Resource-based approach:
   1. Create HealthData resource (max_health, current_health)
   2. Create Health component node
   3. Emit signals for UI binding

   ### Implementation Sketch
   [See patterns.md in godot-custom-resources skill]
   ```

## Plan Mode Behavior

This command is **plan-mode compatible**:
- Only read operations (Glob, Grep, Read, WebFetch)
- No file modifications
- No test execution
- No code generation

Use in plan mode to gather context before designing.

## Output Format

All research outputs follow this structure:

```markdown
## [Topic]

### Summary
[1-2 sentence answer]

### Details
[Organized findings with file:line references]

### Relevant Skills
[Links to applicable skills]

### Next Steps
[Suggested commands: /plan, /build, etc.]
```

## Examples

### Codebase Question
```
/research where are enemy types defined

## Enemy Types Location

### Summary
Enemy types are defined as Resources in `scripts/resources/enemy_types/`.

### Details
- scripts/resources/enemy_data.gd:1 - Base EnemyData resource
- scripts/resources/enemy_types/goblin.tres - Goblin definition
- scripts/resources/enemy_types/skeleton.tres - Skeleton definition
- scripts/enemy.gd:15 - Enemy scene loads EnemyData

### Next Steps
- /build new enemy type
- /docs reference for enemy system
```

### Pattern Question
```
/research damage number popup pattern

## Damage Number Pattern

### Summary
Floating damage numbers use Label with Tween for animation.

### Relevant Skills
See: .claude/skills/godot-damage-numbers/SKILL.md

### Pattern
1. Spawn Label at damage position
2. Tween: move up, fade out, scale
3. queue_free() on completion

### Next Steps
- /build damage numbers for combat
```

## Constraints

- Read-only operations only
- Always provide file:line references
- Suggest next steps after research
- Works in plan mode
