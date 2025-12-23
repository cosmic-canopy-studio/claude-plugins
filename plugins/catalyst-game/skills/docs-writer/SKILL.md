---
name: docs-writer
description: Write user-facing documentation to docs/references/ or docs/guides/. Use after pattern research to create human-readable documentation separate from Claude's internal knowledge.
---

# Docs Writer

Write user-facing documentation for Godot patterns and features.

## When to Use

Use this skill after pattern research to document findings for user consumption.

## Important: Temporal vs Permanent Docs

| Location | Nature | Purpose |
|----------|--------|---------|
| `docs/references/godot/` | **Temporal** | User-facing output, regenerated as needed |
| `docs/guides/godot/` | **Temporal** | User-facing output, regenerated as needed |
| `.claude/skills/godot/reference/` | **Permanent** | Claude's internal knowledge base |

**Key principle**: Claude's internal references are the source of truth. User docs are output artifacts generated from that knowledge - not duplicates to be kept in sync.

## Document Types

### References (`docs/references/godot/`)

**Use for**: API-style quick lookups
- Method signatures
- Property tables
- Signal definitions
- Minimal code examples (5-15 lines)

**Naming**: Topic-oriented (e.g., `scene-transitions.md`, `autoloads.md`)

### Guides (`docs/guides/godot/`)

**Use for**: Step-by-step tutorials
- Full feature implementations
- Contextual explanations
- Multiple approaches compared
- Complete working examples

**Naming**: Mixed - task or topic oriented
- Task: `building-a-main-menu.md`
- Topic: `scene-management.md`

## Decision Tree

```
Is this answering "how does X work?"
    → Reference

Is this answering "how do I build X?"
    → Guide

Is it a quick lookup (< 5 min read)?
    → Reference

Is it a full tutorial (> 5 min read)?
    → Guide
```

## Reference Template

```markdown
# {Topic Name}

Brief description (1-2 sentences).

## Quick Start

\`\`\`gdscript
# Minimal working example
\`\`\`

## Methods

| Method | Description |
|--------|-------------|
| `method()` | What it does |

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|

## Signals

| Signal | Parameters | When Emitted |
|--------|------------|--------------|

## Examples

### Basic Usage
### With Configuration

## Related

- [Related Ref](other.md)
- [Related Guide](../guides/godot/guide.md)
```

## Guide Template

```markdown
# {Guide Title}

What you'll build/learn.

## Prerequisites

- Required knowledge
- Required setup

## What You'll Build

Description or screenshot.

## Step 1: {First Step}

Why and what.

\`\`\`gdscript
# Code with comments
\`\`\`

## Step 2: {Next Step}

...

## Complete Code

Full example.

## Common Pitfalls

- Issue and solution

## Next Steps

- Related guides
- Advanced topics

## Related

- [API Reference](../references/godot/ref.md)
```

## Writing Guidelines

1. **Static typing**: All GDScript examples must use explicit types
2. **Working code**: Examples should be copy-paste ready
3. **Kebab-case filenames**: `scene-transitions.md` not `scene_transitions.md`
4. **Cross-link**: Always link to related refs/guides
5. **Update index**: Add new docs to the README.md index

## After Writing

1. Add entry to `docs/references/godot/README.md` or `docs/guides/godot/README.md` index
2. Optionally update Claude's internal knowledge in `.claude/skills/godot/reference/`
3. Commit with message: `docs: add {topic} reference/guide`
