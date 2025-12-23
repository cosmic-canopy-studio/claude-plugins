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
| "how do I", "how can I", "how should I", "what's the way to" | `research` skill | always |
| "best practice", "idiomatic", "recommended way", "best way to" | `research` skill | always |
| "what is", "where is", "find" | Natural exploration | N/A |
| "run tests", "check if", "verify", "test X" | `/test` command | suggest |
| "document", "write docs", "explain how to" | `/docs` command | suggest |

## Routing Logic

### Step 1: Check for Explicit Command

If user message starts with `/`, don't route - execute the command directly.

### Step 2: Detect Intent

Scan message for intent patterns. Multiple matches? Use priority:

1. **Debug** (highest) - Error keywords override other intents
2. **Test** - Test-related keywords are specific
3. **Research** - "How do I" questions → `research` skill (assumes best practice)
4. **Build/Implement** - Routes to `workflow-prepare` (auto-chain handles rest)
5. **Explore** - "What is", "Where is" → Natural exploration
6. **Complete/Commit** (lowest) - Routes to `workflow-complete`

### Step 3: Trigger Appropriate Skill

**Always-invoke skills (no confirmation):**
- `workflow-prepare` - For implementation requests
- `workflow-complete` - For completion/commit requests
- `research` - For "how do I" and best practice questions

**Suggest-invoke skills (present option):**
- `systematic-debugging` - For bug/error descriptions
- `/test` command - For testing requests

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

### Research Request (Best Practice)
```
User: "How do I handle scene loading from main menu?"
→ Detected: "how do I" + implementation context
→ Route: research skill (auto-invoke)
→ Action: Chain research tools, write doc, provide inline answer
→ Note: Best practice / Godot idiomatic is ALWAYS implied
```

### Exploration Request
```
User: "What is the combat system?"
→ Detected: "what is" + system name
→ Route: Natural exploration (Explore agents)
→ Action: Explore codebase, synthesize findings
```

## Integration with Workflow Skills

| Skill | Triggers |
|-------|----------|
| `workflow-prepare` | Feature descriptions, implementation requests |
| `workflow-implement` | Plan file exists with unchecked items |
| `workflow-complete` | Completion keywords, all phases done |
| `verification-before-completion` | Before any completion claims |
| `systematic-debugging` | Bug reports, error descriptions |
| `research` | "How do I", best practice questions (always implies Godot idiomatic) |

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
| Bug investigation | `systematic-debugging` (research phases only) |
| Feature request | `workflow-prepare` (research only, defer plan writing) |
| Implementation | Suggest exiting plan mode first |
| Completion/commit | Suggest exiting plan mode first |

**Plan-safe skills:** brainstorming, when-stuck, systematic-debugging (phases 1-3), research, all exploration

**Blocked in plan mode:** workflow-implement, workflow-complete, gdscript-formatter (write mode)
