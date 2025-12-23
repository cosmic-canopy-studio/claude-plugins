---
name: workflow-complete
description: Finalize implementation with commit, archive, and next steps. Use after all plan phases are complete and verification has passed.
when_to_use:
  triggers:
    - "done"
    - "finished"
    - "complete"
    - "wrap up"
    - "what's next"
  symptoms:
    - "All plan phases checked"
    - "Verification passed"
    - "Implementation complete"
  context:
    - "After workflow-implement"
    - "After verification-before-completion"
    - "All [x] in plan file"
  auto_invoke: always
  follows:
    - "workflow-implement"
    - "verification-before-completion"
version: 1.0.0
---

# Workflow: Complete Implementation

Finalize the current implementation by committing changes, archiving the plan, and identifying next steps.

## Quick Reference

**Trigger:** All plan phases complete + verification passed
**Process:** Commit → Archive → Retrospective → Next
**Chains to:** Next task (or ready state)

## Plan Mode Behavior

When plan mode is active:
1. **This skill is blocked** - Completion requires commits and file operations
2. **Call `ExitPlanMode` tool** to request user exit plan mode
3. Wait for user confirmation before committing or archiving

Plan mode is for research and planning only. Completion actions must wait.

## Process

### Step 1: Verify Completion

1. Confirm `verification-before-completion` passed
2. Check plan file: all items have `[x]`
3. If not complete, defer to appropriate skill

### Step 2: Commit Changes

Check for uncommitted work:
```bash
git status
git diff
```

If changes exist:
1. Group related files logically
2. Create focused commit(s)
3. Use imperative mood, explain "why"
4. Push to remote

**Commit rules:**
- `git add` specific files (NEVER `-A` or `.`)
- No Claude attribution in messages
- Keep commits atomic

### Step 3: Archive Plan

If plan at `docs/plans/[name].md` has all `[x]`:
1. Create archive directory: `mkdir -p archive/docs/plans`
2. Move completed plan: `mv docs/plans/[name].md archive/docs/plans/`

### Step 4: Write Retrospective

Create `docs/retrospectives/YYYY-MM-DD-[task-name].md`:

```markdown
# [Task Name] Retrospective

## Summary
[1-2 sentence overview of what was accomplished]

## What Went Well
- [Key success point]
- [Another success]

## What Didn't Go Well
- [Challenge encountered]
- [What could improve]

## Lessons Learned
- [Pattern or insight discovered]
- [Process improvement]

## Follow-up Items
- [Deferred work, if any]
- [Future improvements identified]
```

### Step 5: Show Next

Check `docs/plans/` for incomplete plans:
1. Glob for `docs/plans/*.md` (exclude `archive/`)
2. Find plans with unchecked `[ ]` items
3. If found: Announce next task
4. If none: Announce "Ready for new task"

### Step 6: Present Summary

```
## Completed
[Task name] - [brief overview]
- [Phase 1 summary]
- [Phase 2 summary]

Additional fixes:
- [Bug fixes discovered during implementation]

Deferred work:
- [Feature] → [where tracked]

## Retrospective
Created `docs/retrospectives/YYYY-MM-DD-[task].md`
- What went well: [key point]
- What didn't: [key point]

## Next Up
[Next item] - [brief description]
OR
Ready for new task. Describe what you'd like to build.
```

## Commit Message Format

```
[type]: [brief description]

[body explaining why, not what]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `refactor`: Code restructuring
- `docs`: Documentation
- `test`: Tests
- `chore`: Maintenance

**Example:**
```
feat: add dash ability to player

Enables quick directional movement with cooldown.
Integrates with existing stamina system.
```

## Constraints

- No confirmation gates - automatic flow
- No file lists, branch names, or commit hashes in summary
- Only recommend incomplete plans from `docs/plans/`
- Never recommend archived plans
