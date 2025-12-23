---
description: Design implementation before building - creates phased plan with success criteria (plan-mode compatible)
argument-hint: [feature description]
---

# Plan: $ARGUMENTS

Design before implementing. Creates a structured plan with phases and success criteria.

**Plan-mode compatible** - works in plan mode (design only, no code changes).

## When to Use

- Complex features requiring design
- Changes affecting multiple files
- Need documented approach before building
- Want to break work into verifiable phases

## Process

### Step 1: Understand the Task

1. **If no research provided**, do quick exploration:
   ```
   Task Explore "Find relevant code for [feature]"
   ```

2. **Read key files** (max 3-5)

3. **Summarize understanding:**
   ```
   I understand we need to [summary].

   Key files involved:
   - `path/to/file.gd` - [why relevant]
   - `path/to/other.gd` - [why relevant]
   ```

4. **Confirm via AskUserQuestion:**
   - Question: "Does this match your intent?"
   - Options: "Yes, proceed" / "Need more exploration" / "Adjust understanding"

### Step 2: Outline Approach

Present brief outline:
```
## Proposed Approach

### Phases
1. [Phase name] - [what it accomplishes]
2. [Phase name] - [what it accomplishes]

### Out of Scope
- [What we're NOT doing]

### Risks
- [Potential issues to watch for]
```

Confirm via AskUserQuestion:
- Question: "Does this phasing make sense?"
- Options: "Yes, write the plan" / "Adjust phases" / "Add/remove scope"

### Step 3: Write the Plan

After approval, write to `docs/plans/YYYY-MM-DD-description.md`:

```markdown
# [Feature] Implementation Plan

## Overview
[1-2 sentence summary]

## Current State
[What exists, key files]

## Out of Scope
- [Explicitly list what we're NOT doing]

---

## Phase 1: [Name]

### Changes
- `path/to/file.gd` - [specific change]

### Success Criteria

**Automated:**
- [ ] `./run_tests.sh test/test_feature.gd` passes
- [ ] `godot --headless --path . --check-only` succeeds

**Manual:**
- [ ] [Human verification step]

---

## Phase 2: [Name]
[Same structure...]

---

## Testing Strategy
[How to verify the full implementation]

## Related Skills
- [skill-name] - [how it helps]
```

### Step 4: Present for Review

```
Plan written to `docs/plans/YYYY-MM-DD-description.md`

Summary:
- Phase 1: [name] - [brief]
- Phase 2: [name] - [brief]
- Estimated changes: [N] files

Ready to implement?
```

AskUserQuestion:
- Question: "Review the plan?"
- Options: "Looks good, /build it" / "I want to review first" / "Modify the plan"

## Plan Template

Each phase includes:

| Section | Purpose |
|---------|---------|
| Changes | Specific files and modifications |
| Success Criteria - Automated | Commands that must pass |
| Success Criteria - Manual | Human verification steps |

## Guidelines

- **Be interactive** - Don't write full plan without confirmation
- **Be specific** - Include file paths, not vague descriptions
- **Keep phases small** - Each independently testable
- **Include Out of Scope** - Prevent scope creep
- **Link skills** - Reference relevant skills for implementation

## Integration with Other Commands

| After /plan | Action |
|-------------|--------|
| Plan approved | `/build docs/plans/[plan-file].md` |
| Need more info | `/research [topic]` |
| Plan too complex | Split into multiple plans |

## Examples

### Simple Feature
```
/plan add player stamina system

→ Explore codebase for player.gd
→ Outline: 2 phases (data model, mechanics)
→ Write plan to docs/plans/2024-12-19-player-stamina.md
→ Ready for /build
```

### Complex Feature
```
/plan combat system with multiple attack types

→ Explore codebase extensively
→ Outline: 4 phases (base damage, melee, ranged, combos)
→ Write detailed plan with test strategy
→ User reviews, requests adjustments
→ Update plan
→ Ready for /build
```

## Constraints

- Plan-mode compatible (read-only research)
- Always include Out of Scope section
- Phases must have testable success criteria
- Get confirmation at each step
