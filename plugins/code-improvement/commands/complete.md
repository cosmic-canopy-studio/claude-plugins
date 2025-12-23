---
name: complete
description: Complete implementation with docs update, commit, and next steps. Runs quality-gate validation first for knowledge pipeline work.
model: sonnet
---

# Complete Implementation

Wrap up the current implementation task by updating documentation, committing changes, and planning next steps.

## Process

1. **Summarize what was accomplished:**

   - Review conversation history
   - List the key changes made
   - Note any test cases added

2. **Check for uncommitted changes:**

   - Run `git status` in relevant directories
   - If changes exist, commit them following `/commit` conventions

3. **Update project tracking (if exists):**

   - Look for tracking files: `docs/IMPLEMENTATION_PLAN.md`, `docs/BACKLOG.md`, or similar
   - Mark completed items
   - Commit the tracking updates

4. **Archive completed plan:**

   - If the just-completed task has a plan in `docs/plans/`, check if ALL checkboxes are marked `[x]`
   - If complete (no `[ ]` items remaining), move to `docs/plans/archive/`
   - Create archive directory if needed: `mkdir -p docs/plans/archive`

5. **Write retrospective:**

   - Create `docs/retrospectives/[date]-[task-name].md`
   - Document what went well and what didn't
   - Include any lessons learned or patterns discovered

6. **Show what's next:**

   - Check `docs/plans/` for INCOMPLETE plans only (ignore `archive/` subdirectory)
   - A plan is incomplete if it has any `[ ]` (unchecked) items
   - Identify the next uncompleted item
   - Briefly describe what the work involves
   - Recommend next command:
     - `/implement` if an incomplete plan exists in `docs/plans/`
     - `/recon` if codebase exploration is needed first
     - `/prepare` if the task is well-understood and ready for planning

7. **Present summary:**

   ```
   ## Completed
   [task name] - [brief overview]
   - [Phase/item 1]
   - [Phase/item 2]
   - ...

   Additional fixes:
   - [Bug fixes discovered during implementation]

   Deferred work tracked:
   - [Feature] → [path to plan/issue]

   ## Retrospective
   Created `docs/retrospectives/[date]-[task].md`
   - What went well: [1-2 key points]
   - What didn't: [1-2 key points]

   ## Next Up
   [Next item name] - [brief description of what it involves]

   → /[recommended command] [task name]
   ```

## Output Format

```markdown
## Completed
[task name] - [brief overview]
- [Phase/item 1]
- [Phase/item 2]

Additional fixes:
- [Bug fixes discovered during implementation]

## Retrospective
Created `docs/retrospectives/[date]-[task].md`

## Next Up
[Next item name] - [brief description]

→ /[recommended command] [task name]
```

## Constraints

- Do not use AskUserQuestion - just do the work
- Follow `/commit` conventions
- Include phases/items completed and any deferred work
- Do NOT include: file lists, branch names, commit hashes, or per-repo breakdowns
- Only recommend plans from `docs/plans/` that have unchecked `[ ]` items
- Never recommend archived plans from `docs/plans/archive/`
