---
name: workflow-prepare
description: Create implementation plan when user describes a feature to build. Use when user says "I want to add...", "Let's implement...", "Build a...", or describes any implementation task.
when_to_use:
  triggers:
    - "I want to add"
    - "Let's implement"
    - "Build a"
    - "Create a"
    - "Add feature"
    - "I need to"
    - "Can you implement"
    - "Make a"
    - "We need to build"
  symptoms:
    - "Feature request described"
    - "Implementation goal stated"
    - "Task with implementation scope"
  context:
    - "No active plan in docs/plans/"
    - "User describes something to build"
    - "Start of feature work"
  auto_invoke: always
  leads_to:
    - "workflow-implement"
version: 1.0.0
---

# Workflow: Prepare Implementation Plan

Create a detailed implementation plan when the user describes a feature or task to build.

## Quick Reference

**Trigger:** User describes a feature to build
**Output:** Plan file at `docs/plans/YYYY-MM-DD-description.md`
**Chains to:** `workflow-implement` (automatic)

## Plan Mode Behavior

When plan mode is active:
1. **Perform research/analysis only** - Explore codebase, understand requirements
2. **Do NOT write plan file** - Plan mode restricts file modifications
3. **When ready to write plan**, call `ExitPlanMode` tool
4. Wait for user to exit plan mode before creating the plan file

## Process

### Step 1: Understand (Implicit Exploration)

1. **Read any provided files** completely
2. **If research needed**, spawn 1-2 Explore agents to find relevant code
3. **Read key files** (max 3-5)
4. **Summarize understanding** inline - no confirmation gate needed

### Step 2: Outline and Write Plan

1. **Present brief outline**:
   - Phases (what each accomplishes)
   - Out of scope (explicit boundaries)

2. **Write plan** to `docs/plans/YYYY-MM-DD-description.md`
   - Use standard template structure (see reference.md)
   - Include specific file paths
   - Split success criteria: Automated vs Manual

### Step 3: Chain to Implementation

After writing plan:
1. Announce: "Plan created at [path]. Starting implementation..."
2. `workflow-implement` skill activates automatically

## Plan File Structure

```markdown
# [Task Name] Implementation Plan

## Overview
[1-2 sentence summary]

## Current State
[What exists now, key files involved]

## Out of Scope
[Explicitly list what we're NOT doing]

---

## Phase 1: [Name]

### Changes
- `path/to/file.ts` - [what to change]

### Success Criteria

**Automated:**
- [ ] `[command]` passes

**Manual:**
- [ ] [Human verification step]

---

## Phase N: [Name]
[Same structure...]

---

## Testing Strategy
[How to verify the full implementation]
```

## Guidelines

- **Be specific** - Include file paths, not vague descriptions
- **Keep phases small** - Each phase should be independently testable
- **Scope control** - Always include "Out of Scope" section
- **No confirmation gates** - Flow is automatic in always mode
