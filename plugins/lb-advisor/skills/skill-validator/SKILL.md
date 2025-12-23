---
name: skill-validator
description: Validate skill configurations for plan mode awareness, YAML frontmatter, and required sections. Use when adding or modifying skills.
allowed-tools: Read, Grep, Glob
when_to_use:
  triggers:
    - "validate skills"
    - "check skill config"
    - "verify skills"
  context:
    - "After modifying skills"
    - "Before committing skill changes"
  auto_invoke: suggest
---

# Skill Validator

Validate skill configurations using Claude Code's native tools instead of shell scripts.

## Core Principle

**Use Claude Code native tools, not shell wrappers:**
- Grep tool for pattern matching
- Read tool for content inspection
- Glob tool for file discovery
- Parallel tool calls for efficiency

## Validation Checks

### 1. Discover All Skills

Use Glob to find all skill files:
```
Glob(pattern="**/SKILL.md", path="/home/sam/code/godot_advisor/.claude/skills")
```

### 2. Plan-Safe Skills Have allowed-tools

Plan-safe skills must have `allowed-tools:` in YAML frontmatter.

**Skills to check:**
- brainstorming
- collision-zone-thinking
- code-review
- godot
- godot-pattern-researcher
- inversion-exercise
- meta-pattern-recognition
- simplification-cascades
- tracing-knowledge-lineages
- when-stuck
- systematic-debugging
- godot-image-validator (Read, Grep, Glob only)

**Validation approach:**
Use parallel Grep calls - one per skill file:
```
Grep(pattern="allowed-tools:", path="skills/brainstorming/SKILL.md", output_mode="content")
Grep(pattern="allowed-tools:", path="skills/when-stuck/SKILL.md", output_mode="content")
... (all in parallel)
```

### 3. Implementation Skills Have Plan Mode Section

Implementation skills must have "Plan Mode Behavior" section.

**Skills to check:**
- workflow-prepare
- workflow-implement
- workflow-complete
- gdscript-formatter
- verification-before-completion

**Validation approach:**
```
Grep(pattern="Plan Mode Behavior", path="skills/workflow-prepare/SKILL.md")
Grep(pattern="Plan Mode Behavior", path="skills/workflow-implement/SKILL.md")
... (all in parallel)
```

### 4. YAML Frontmatter Valid

Every SKILL.md must:
- Start with `---` on line 1
- Have exactly 2 `---` delimiters

**Validation approach:**
```
Read(file_path="skills/[skill]/SKILL.md", limit=1)  # Check first line is ---
Grep(pattern="^---$", path="skills/[skill]/SKILL.md", output_mode="count")  # Should be 2
```

### 5. Workflow Router Has Plan Mode Awareness

```
Grep(pattern="Plan Mode Awareness", path="skills/workflow-router/SKILL.md")
```

## Execution Steps

When invoked, perform these steps:

### Step 1: Discover Skills
```
Glob(pattern="**/SKILL.md", path="/home/sam/code/godot_advisor/.claude/skills")
```

### Step 2: Parallel Validation
Launch all checks in parallel using multiple tool calls in a single message:
- 12 Grep calls for `allowed-tools:` on plan-safe skills
- 5 Grep calls for `Plan Mode Behavior` on implementation skills
- 1 Grep call for `Plan Mode Awareness` on workflow-router

### Step 3: Report Results

Format results as a table:

```markdown
## Validation Results

### Plan-Safe Skills (allowed-tools check)
| Skill | Status |
|-------|--------|
| brainstorming | ✓ |
| collision-zone-thinking | ✓ |
...

### Implementation Skills (Plan Mode Behavior section)
| Skill | Status |
|-------|--------|
| workflow-prepare | ✓ |
| workflow-implement | ✓ |
...

### Conditional Skills
| Skill | Check | Status |
|-------|-------|--------|
| workflow-router | Plan Mode Awareness | ✓ |
| godot-image-validator | allowed-tools | ✓ |

### Summary
- Total skills checked: N
- Passing: N
- Failing: 0
```

## Why Native Tools?

| Approach | Problem | Native Alternative |
|----------|---------|-------------------|
| `grep -q` in bash | Shell syntax issues (zsh vs bash) | Grep tool with output_mode |
| `for skill in ...` loop | Variable interpolation failures | Parallel Grep tool calls |
| `head -1` | Requires bash subprocess | Read tool with limit: 1 |
| Shell scripts | External to Claude workflow | Integrated tool calls |

## Related Skills

- workflow-prepare - Creates plans (validate after modifying)
- workflow-implement - Executes plans (validate plan mode config)
- verification-before-completion - Evidence-based verification pattern
