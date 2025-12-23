---
name: workflow-router
description: Routes user intent to appropriate workflow skill automatically. Use when user describes what they want to accomplish without specifying a command, or when natural language task descriptions need to be mapped to workflow-prepare, workflow-complete, systematic-debugging, or other skills.
---

# Workflow Router

Automatically route user requests to the correct workflow skill based on intent detection.

## Core Principle

Users shouldn't need to remember skill names. Describe what you want, get routed to the right workflow.

## Intent Detection

When a user describes a task without explicit direction, analyze their intent:

| Intent Patterns | Route To | Auto-Invoke |
|-----------------|----------|-------------|
| "I want to add", "implement", "build", "create", "make X work" | `workflow-prepare` skill | always |
| "done", "finished", "wrap up", "what's next" | `workflow-complete` skill | always |
| "commit", "save changes", "push" | `workflow-complete` skill | always |
| "fix", "broken", "failing", "error", "bug", "not working" | `systematic-debugging` skill | suggest |
| "what is", "how does", "where is", "find", "understand" | Natural exploration | N/A |
| "run tests", "check if", "verify", "test X" | `/test` command | suggest |
| "document", "write docs", "explain how to" | `/docs` command | suggest |
| "best way to", "idiomatic way", "recommended approach", "best practice" | `godot-pattern-research` flow | always |
| "how should I", "what's the right way", "how do I implement" | `godot-pattern-research` flow | always |
| "what pattern for", "which approach" | `godot-pattern-research` flow | always |

## Routing Logic

### Step 1: Check for Explicit Command

If user message starts with `/`, don't route - execute the command directly.

### Step 2: Detect Intent

Scan message for intent patterns. Multiple matches? Use priority:

1. **Debug** (highest) - Error keywords override other intents
2. **Test** - Test-related keywords are specific
3. **Best Practice/Pattern** - Implementation questions about Godot (auto-invoke research)
4. **Build/Implement** - Routes to `workflow-prepare` (auto-chain handles rest)
5. **Research** - Natural exploration behavior
6. **Complete/Commit** (lowest) - Routes to `workflow-complete`

### Step 3: Trigger Appropriate Skill

**Always-invoke skills (no confirmation):**
- `workflow-prepare` - For implementation requests
- `workflow-complete` - For completion/commit requests

**Suggest-invoke skills (present option):**
- `systematic-debugging` - For bug/error descriptions
- `/test` command - For testing requests

## Godot Pattern Research Flow

When best-practice or implementation pattern questions are detected, this flow runs automatically.

### Step 1: Quick Lookup (godot skill)

1. Parse question for keywords matching `godot/index.yaml` entries
2. Route through appropriate dispatcher:
   - 2D gameplay → `dispatchers/2d-gameplay.md`
   - 3D gameplay → `dispatchers/3d-gameplay.md`
   - UI/menus → `dispatchers/ui-systems.md`
   - Audio → `dispatchers/audio-systems.md`
   - Architecture/patterns → `dispatchers/game-patterns.md`
3. Load referenced `reference/*.md` file

### Step 2: Assess Depth

If quick lookup finds a clear pattern → format response immediately.

If deeper research needed (no match, complex topic, spans multiple areas):
- Invoke `pattern-researcher` agent for multi-source synthesis
- Sources: official Godot docs, godot_node_essentials, community patterns

### Step 3: Format Response (Summary + User Doc)

**In the reply** - provide a concise summary:
1. **One-liner**: Direct answer to the question
2. **Quick Start**: Minimal code snippet (5-10 lines max)
3. **Reference**: Link to the user documentation

**Write user documentation** using `docs-writer` skill:
- **Reference** → `docs/references/godot/{topic}.md` (API-style lookup)
- **Guide** → `docs/guides/godot/{topic}.md` (step-by-step tutorial)
- User docs are **temporal** - regenerate fresh each time (don't check for existing)

Choose reference vs guide based on:
- "How does X work?" → Reference
- "How do I build X?" → Guide
- Quick lookup (< 5 min) → Reference
- Full tutorial (> 5 min) → Guide

**Source of truth**: Claude's internal knowledge (`.claude/skills/godot/reference/`) is the permanent source. User docs are generated output artifacts.

## Implicit Best Practice Detection

Assume "best practice" is desired for any Godot implementation question.

### Explicit Triggers (definitely pattern research)
- "What's the best way to..."
- "How should I implement..."
- "What's the idiomatic way to..."
- "Recommended approach for..."

### Implicit Triggers (treat as pattern research)
- "How do I..." + Godot concept
- "How to implement..." + game feature
- "I want to add..." + Godot system
- Questions containing: autoload, signal, singleton, state machine, scene, save/load

### Context Indicators
- Working in `demo/dungeon_delve/` project
- Previous Godot development discussion
- .gd files referenced in conversation

## Workflow Chain

When `workflow-prepare` triggers, the full chain executes automatically:

```
User: "I want to add X"
         ↓
  workflow-prepare   ← creates plan
         ↓
  workflow-implement ← executes phases
         ↓
  verification-before-completion
         ↓
  workflow-complete  ← commits, archives
```

User only needs to describe the goal. Chain handles the rest.

## Examples

### Implementation Request
```
User: "I want to add dash ability to the player"
→ Detected: "I want to add" + feature description
→ Route: workflow-prepare skill (auto-invoke)
→ Action: Skill creates plan, chains to implementation
```

### Completion Request
```
User: "I'm done with this feature"
→ Detected: "done" keyword
→ Route: workflow-complete skill (auto-invoke)
→ Action: Skill commits, archives, shows next
```

### Debug Request
```
User: "Player clips through walls sometimes"
→ Detected: Problem description
→ Route: systematic-debugging skill (suggest)
→ Action: "This sounds like a bug. Investigate with systematic debugging?"
```

### Research Request
```
User: "How does the combat system work?"
→ Detected: "how does" + system name
→ Route: Natural exploration (Explore agents)
→ Action: Explore codebase, synthesize findings
```

### Pattern Research Request
```
User: "What's the best way to implement scene loading for main menu?"
→ Detected: "best way to" + "scene" + "menu" (Godot concepts)
→ Route: godot-pattern-research flow (auto-invoke)
→ Action: Quick lookup via godot skill dispatchers/index.yaml
→ Response: Explain SceneManager autoload pattern, then show code
```

## Integration with Workflow Skills

| Skill | Triggers |
|-------|----------|
| `workflow-prepare` | Feature descriptions, implementation requests |
| `workflow-implement` | Plan file exists with unchecked items |
| `workflow-complete` | Completion keywords, all phases done |
| `verification-before-completion` | Before any completion claims |
| `systematic-debugging` | Bug reports, error descriptions |
| `godot-pattern-research` | Best practice queries, implementation questions about Godot |

## When Not to Route

Don't intercept when:
- User gives explicit command (`/build`, `/test`, etc.)
- User asks a direct question (not a task)
- User is in the middle of an existing workflow
- Active plan exists and implementation is in progress

## Plan Mode Awareness

When plan mode is active, only route to plan-mode-compatible skills:

| Intent | Plan Mode Routing |
|--------|-------------------|
| Research/exploration | Route normally - plan-safe |
| Pattern research | `godot-pattern-research` - plan-safe (read-only lookup) |
| Bug investigation | `systematic-debugging` (research phases only) |
| Feature request | `workflow-prepare` (research only, defer plan writing) |
| Implementation | Suggest exiting plan mode first |
| Completion/commit | Suggest exiting plan mode first |

**Plan-safe skills:** brainstorming, when-stuck, systematic-debugging (phases 1-3), godot-pattern-research, all research skills

**Blocked in plan mode:** workflow-implement, workflow-complete, gdscript-formatter (write mode)
