---
name: workflow-implement
description: Execute implementation plans phase-by-phase with verification. Use when a plan file exists in docs/plans/ with unchecked items.
when_to_use:
  triggers:
    - "Plan file created"
    - "implement the plan"
    - "start implementation"
    - "execute the plan"
    - "begin work"
  symptoms:
    - "Plan file exists with unchecked items"
    - "Ready to implement"
    - "Plan was just created"
  context:
    - "docs/plans/*.md exists with [ ] items"
    - "After workflow-prepare"
    - "Implementation not complete"
  auto_invoke: always
  follows:
    - "workflow-prepare"
  leads_to:
    - "verification-before-completion"
    - "workflow-complete"
version: 1.0.0
---

# Workflow: Implement Plan

Execute an approved implementation plan phase-by-phase with verification checkpoints.

## Quick Reference

**Trigger:** Plan file exists with unchecked `[ ]` items
**Process:** Execute phases → verify → commit → repeat
**Chains to:** `verification-before-completion` → `workflow-complete`

## Plan Mode Behavior

When plan mode is active:
1. **This skill is blocked** - Implementation requires code modifications
2. **Call `ExitPlanMode` tool** to request user exit plan mode
3. Wait for user confirmation before executing any implementation

Plan mode is for research and planning only. Implementation must wait.

## State Detection

On activation, detect current state:

| Condition | Action |
|-----------|--------|
| Plan has only `[ ]` items | Fresh plan - start Phase 1 |
| Plan has mix of `[x]` and `[ ]` | Resume from first unchecked |
| Plan has only `[x]` items | Chain to workflow-complete |
| No plan file found | Announce "No active plan found" |

## Process

### Startup

1. **Detect active plan**: Find `docs/plans/*.md` with unchecked items
2. **Read plan completely**: Understand all phases
3. **Read all mentioned files**: Understand current codebase state
4. **Create todo list**: Track progress through phases

### Per-Phase Execution

For each phase:

#### 1. Implement Changes
- Follow the plan's intent
- Adapt to what you find in the codebase
- Make changes as specified

#### 2. Run Automated Verification
- Execute all success criteria commands
- Fix issues before proceeding
- Document what passed

#### 3. Commit and Push
- `git add` specific files (NEVER `-A` or `.`)
- Write focused commit message (imperative mood)
- `git push` to remote
- Verify clean tree with `git status`

#### 4. Update Progress
- Check off completed items in plan file: `[ ]` → `[x]`
- Update todo list

#### 5. Brief Pause for Manual Verification
Present status:
```
Phase [N] Complete

Automated checks passed:
- [list what passed with evidence]

Manual verification needed:
- [list items from plan]
```

Continue to next phase unless issues found.

### Phase Completion Detection

When ALL phases complete (`[x]` on all items):
1. `verification-before-completion` skill activates
2. Then `workflow-complete` skill activates

## Verification Gate

Before marking ANY phase complete:

1. **Run all automated checks** - Don't skip even if "obvious"
2. **Show evidence** - State what passed with output
3. **Check for regressions** - Did anything else break?

**Evidence, not belief.** Only mark complete when you have proof.

## Failure Handling

When implementation fails or produces unexpected results:

1. **STOP** - Don't try random fixes
2. **Investigate systematically**:
   - What was expected?
   - What actually happened?
   - What's the earliest divergence point?

3. **Present findings**:
   ```
   Implementation Issue:
   Expected: [X]
   Actual: [Y]
   Divergence point: [file:line]

   Proposed fix: [approach]
   ```

4. **Apply fix** and continue (no confirmation gate in auto mode)

## Mismatch Handling

If codebase doesn't match plan expectations:

1. **Adapt to what's found** - Plans are guidelines, not rigid scripts
2. **Document the adaptation** - Note in plan file what changed
3. **Continue execution** - Don't block on minor mismatches

For major mismatches that change scope:
1. Note the issue clearly
2. Complete current phase
3. Let user review at next natural break

## Constraints

- Default: One phase at a time
- Update checkboxes as you complete work
- Trust completed checkmarks when resuming
- Commit after each phase (atomic, reversible changes)
