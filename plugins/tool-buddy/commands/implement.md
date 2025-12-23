---
description: Implement technical plans from docs/plans/ with verification
---

# Implement Plan

Execute an approved plan phase-by-phase with verification checkpoints.

## Getting Started

When given a plan path:
1. Read the plan completely
2. Check for existing checkmarks (resume from first unchecked item)
3. Read all files mentioned in the plan
4. Create a todo list to track progress

If no plan path provided, ask for one.

## Execution

For each phase:

1. **Implement the changes**
   - Follow the plan's intent
   - Adapt to what you find in the codebase

2. **Run automated verification**
   - Execute success criteria commands
   - Fix issues before proceeding

3. **Commit and push changes**
   - `git add` specific files (never `-A` or `.`)
   - Write focused commit message (imperative mood, explain "why")
   - `git push` to remote
   - Verify clean working tree with `git status`

4. **Update progress**
   - Check off completed items in the plan file
   - Update your todo list

5. **Pause for manual verification**

   Present status in text:
   ```
   Phase [N] Complete - Ready for Manual Verification

   Automated checks passed:
   - [list what passed]

   Please verify manually:
   - [list manual checks from plan]
   ```

   Then use `AskUserQuestion`:
   - Question: "Manual verification complete?"
   - Options: "Yes, continue to Phase [N+1]" / "Found issues to address"

## Verification Gate

Before marking ANY phase complete:

1. **Run all automated checks** - Don't skip even if "obvious"
2. **Confirm output explicitly** - State what passed, not just "it works"
3. **Check for regressions** - Did anything else break?

Only mark complete when you have EVIDENCE, not belief.

## Failure Handling

When implementation fails or produces unexpected results:

1. **STOP** - Don't try random fixes
2. **Investigate systematically**:
   - What was the expected behavior?
   - What actually happened?
   - What's the earliest point of divergence?
3. **Present findings** before attempting fix:
   ```
   Implementation Issue:
   Expected: [X]
   Actual: [Y]
   Divergence point: [file:line]

   Proposed fix: [approach]
   ```

   Then use `AskUserQuestion`:
   - Question: "How should I proceed with this issue?"
   - Options: "Apply the proposed fix" / "Try a different approach" / "Skip and continue"

4. **Get confirmation** before applying fix

## Handling Mismatches

If something doesn't match the plan:

1. STOP immediately
2. Present the issue in text:
   ```
   Issue in Phase [N]:
   Expected: [what plan says]
   Found: [actual situation]
   Why this matters: [explanation]
   ```

3. Use `AskUserQuestion`:
   - Question: "How should I handle this mismatch?"
   - Options: "Adapt to what's found" / "Update the plan first" / "Stop and discuss"

4. Wait for guidance before continuing

## Constraints

- Default: One phase at a time (unless told otherwise)
- Never skip manual verification pause
- Update checkboxes as you complete work
- Trust completed checkmarks when resuming
