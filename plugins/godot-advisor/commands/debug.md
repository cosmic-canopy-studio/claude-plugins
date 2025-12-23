---
description: Fix bugs and test failures using systematic debugging - invokes systematic-debugging skill
argument-hint: [problem description or test name]
---

# Debug: $ARGUMENTS

Systematic debugging for any issue. Auto-invoked when `/test` or `/build` encounter failures.

## Core Principle

**NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST**

Random fixes waste time. This command enforces the `systematic-debugging` skill.

## When Auto-Invoked

This command is suggested automatically when:
- `/test` reports failures
- `/build` encounters errors
- Error messages appear in output
- User mentions "not working", "broken", "bug"

## Process

### Step 1: Load Systematic Debugging Skill

```
Read and follow: .claude/skills/systematic-debugging/SKILL.md
```

The skill enforces four phases:
1. Root Cause Investigation
2. Pattern Analysis
3. Hypothesis and Testing
4. Implementation

### Step 2: Gather Context

```bash
# For test failures
cd demo/dungeon_delve && ./run_tests.sh 2>&1 | head -100

# For script errors
cd demo/dungeon_delve && godot --headless --path . --check-only 2>&1

# For recent changes
git diff HEAD~3 --stat
git log --oneline -5
```

### Step 3: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read error messages carefully**
   - Don't skip past errors
   - Note line numbers, file paths
   - Read stack traces completely

2. **Reproduce consistently**
   - Can you trigger it reliably?
   - What are exact steps?

3. **Check recent changes**
   - What changed that could cause this?
   - `git diff`, recent commits

4. **Trace data flow**
   - Where does bad value originate?
   - Keep tracing up until source found

### Step 4: Form Hypothesis

State clearly:
```
Hypothesis: [X] is the root cause because [Y]

Evidence:
- [observation 1]
- [observation 2]

Test: [smallest change to verify]
```

### Step 5: Test Minimally

- Make the SMALLEST possible change
- One variable at a time
- DON'T fix multiple things at once

### Step 6: Verify Fix

```bash
# Run failing test
cd demo/dungeon_delve && ./run_tests.sh test/test_specific.gd

# Run all tests (check for regressions)
cd demo/dungeon_delve && ./run_tests.sh
```

## Failure Escalation

### After 3+ Failed Fix Attempts

**STOP and question architecture:**

```
3+ fix attempts failed. This indicates an architectural problem.

Attempted fixes:
1. [fix 1] - [why it failed]
2. [fix 2] - [why it failed]
3. [fix 3] - [why it failed]

Pattern: [what these failures reveal]

Recommendation: Discuss architecture before more fixes
```

Use AskUserQuestion:
- Question: "3 fixes failed. Question the architecture?"
- Options: "Yes, discuss approach" / "Try one more fix" / "Get external help"

### When Blocked

If systematic investigation reveals issue is environmental, timing-dependent, or external:

1. Document what you investigated
2. Implement appropriate handling (retry, timeout, error message)
3. Add monitoring/logging for future

## Integration with Other Commands

| After /debug | Action |
|--------------|--------|
| Issue resolved | `/test` to verify, then `/commit` |
| Architecture problem | `/plan` to redesign |
| External issue | Document and `/complete` |

## Red Flags - Return to Investigation

If you catch yourself thinking:
- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Skip the test, I'll manually verify"
- "I don't fully understand but this might work"
- "One more fix attempt" (when already tried 2+)

**ALL of these mean: STOP. Return to root cause investigation.**

## Example Session

```
/debug player clips through walls

1. Root Cause Investigation:
   - Error: No explicit error, just wrong behavior
   - Reproduce: Player walks into wall corner, clips through
   - Recent changes: None to player code
   - Data flow: collision_mask set to 0, should be 4

2. Hypothesis:
   Player's collision_mask is not set correctly.
   Evidence: inspector shows mask = 0
   Test: Set collision_mask = 4 in _ready()

3. Fix Applied:
   func _ready() -> void:
       collision_mask = 4  # Layer 4 = walls

4. Verification:
   ./run_tests.sh test/test_player_collision.gd → PASS
   ./run_tests.sh → All 12 tests pass

Issue resolved. Suggest /commit.
```

## Constraints

- Must complete Phase 1 before proposing fixes
- Must form explicit hypothesis before changing code
- Must verify fix with tests, not just "it works"
- Auto-escalate after 3 failed attempts
