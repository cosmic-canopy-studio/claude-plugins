---
description: Wrap up current work - summarize, commit, archive, and suggest next steps
---

# Complete

Wrap up the current task with summary, commit, cleanup, and next steps.

## Process

### Step 1: Summarize Accomplishments

Review conversation and list what was done:
```
## Completed
[Task name] - [brief overview]

Changes:
- [Key change 1]
- [Key change 2]

Tests added:
- [Test 1]
- [Test 2]
```

### Step 2: Check for Uncommitted Changes

```bash
git status
```

If changes exist:
- Group related files
- Draft commit message(s)
- Use AskUserQuestion: "Commit these changes?"
- Options: "Yes, commit" / "Review first" / "Skip commit"

### Step 3: Archive Completed Plans

Check `docs/plans/` for completed plans:
- Plan is complete if ALL checkboxes are `[x]`
- If complete, move to `docs/plans/archive/`

```bash
mkdir -p docs/plans/archive
mv docs/plans/[completed-plan].md docs/plans/archive/
```

### Step 4: Cleanup (Merged from /cleanup)

Organize project documentation:

1. **Check for scattered docs:**
   ```bash
   ls -la docs/plans/
   ls -la docs/retrospectives/ 2>/dev/null || echo "No retrospectives yet"
   ```

2. **Archive old completed plans:**
   - Plans with all `[x]` checkboxes → `docs/plans/archive/`
   - Keep active/incomplete plans in `docs/plans/`

3. **Create directories if needed:**
   ```bash
   mkdir -p docs/plans/archive
   mkdir -p docs/retrospectives
   ```

### Step 5: Write Retrospective (Optional)

If significant work was completed:

Create `docs/retrospectives/YYYY-MM-DD-[task-name].md`:
```markdown
# [Task Name] Retrospective

## What was done
[Brief summary]

## What went well
- [Point 1]
- [Point 2]

## What didn't go well
- [Point 1]

## Lessons learned
- [Insight that helps future work]
```

### Step 6: Show Next Steps

Check for incomplete plans:
```bash
grep -l "\[ \]" docs/plans/*.md 2>/dev/null | grep -v archive
```

Present summary:
```
## Next Up

Incomplete plans found:
- docs/plans/[plan-name].md - [brief description]

Suggested command:
→ /build docs/plans/[plan-name].md

Or start something new:
→ /research [topic]
→ /plan [new feature]
```

## Output Format

```
## Completed
[Task name]
- [What was done]
- [Tests added]

## Changes Committed
[Commit summary or "No uncommitted changes"]

## Cleanup
- Archived: [plan name] → docs/plans/archive/
- Retrospective: docs/retrospectives/[date]-[name].md

## Next Up
[Next item from incomplete plans]
→ /build docs/plans/[next-plan].md

Or:
→ /research [suggested topic]
```

## Constraints

- Follow `/commit` conventions (no Claude attribution)
- Only recommend incomplete plans (have `[ ]` items)
- Never recommend archived plans
- Skip retrospective for small tasks

## Integration with Other Commands

| After /complete | Likely Next |
|-----------------|-------------|
| More plans exist | `/build` next plan |
| No plans | `/research` or `/plan` |
| Issues discovered | `/debug` |
