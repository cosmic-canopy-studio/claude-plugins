---
description: Implement features using TDD workflow - propose tests first, then implement to make them pass, with automatic verification
argument-hint: [description or plan path]
---

# Build: $ARGUMENTS

Unified implementation command using Test-Driven Development.

## Workflow

```
1. Understand scope → 2. Propose tests (TDD Red) → 3. Implement (TDD Green) → 4. Verify → 5. Suggest /complete
```

## Step 1: Understand Scope

### If Plan Path Provided
```
/build docs/plans/2024-12-19-feature.md
```
1. Read the plan completely
2. Check for existing checkmarks (resume from first unchecked)
3. Read all files mentioned in the plan
4. Create todo list to track progress

### If Description Provided
```
/build player dash ability
```
1. Research the codebase for related code
2. Check for existing tests
3. Invoke `skill-advisor` for recommended skills
4. Summarize understanding before proceeding

## Step 2: Propose Tests (TDD Red Phase)

Before writing implementation code, propose failing tests:

1. **Identify testable behaviors:**
   - What should this feature DO?
   - What inputs/outputs matter?
   - What edge cases exist?

2. **Write test proposals:**
   ```
   ## Test Proposals for [Feature]

   ### Test: [behavior_description]
   Given: [preconditions]
   When: [action]
   Then: [expected outcome]

   ### Test: [edge_case]
   ...
   ```

3. **Get approval via AskUserQuestion:**
   - Question: "These tests capture the requirements?"
   - Options: "Yes, write tests" / "Add more tests" / "Modify tests"

4. **Write tests to test/ directory**

5. **Run tests - confirm they FAIL:**
   ```bash
   cd demo/dungeon_delve && ./run_tests.sh
   ```
   Tests MUST fail before implementation.

## Step 3: Implement (TDD Green Phase)

Write minimal code to make failing tests pass:

1. **For each failing test:**
   - Understand what behavior it verifies
   - Write the minimum code needed
   - Run tests after each change

2. **Skill auto-triggering:**
   Based on feature keywords, relevant skills activate:

   | Feature | Skills |
   |---------|--------|
   | CharacterBody2D | `godot-character-body-2d`, `godot-8-way-movement` |
   | Collision | `godot-collision-shape-2d`, `godot-collision-layers` |
   | Input | `godot-input-actions` |
   | Animation | `godot-animation-player`, `godot-animated-sprite-2d` |
   | Audio | `godot-audio-stream-player` |
   | UI | `godot-button`, `godot-box-container` |

3. **TDD discipline:**
   - DO: Write minimal code to pass tests
   - DO: Run tests after each change
   - DON'T: Add features not covered by tests
   - DON'T: Refactor before tests pass

## Step 4: Verify

### Automated Verification
```bash
# Run all tests
cd demo/dungeon_delve && ./run_tests.sh

# Validate project structure
cd demo/dungeon_delve && godot --headless --path . --check-only
```

### Scene Integration Check
TDD oversight: Scripts work in tests but aren't attached to main scene.

```bash
# Check that scripts are in main.tscn, not just test scenes
grep "scripts/player.gd" demo/dungeon_delve/scenes/main.tscn
```

### Manual Verification Pause
Present status:
```
Build Phase Complete - Ready for Verification

Automated checks:
- [ ] All tests pass
- [ ] Project validates
- [ ] Scripts attached to main.tscn

Please verify manually:
- [ ] [feature-specific checks]
```

Use AskUserQuestion:
- Question: "Verification complete?"
- Options: "Yes, continue" / "Found issues"

## Step 5: Completion

On successful verification:
```
Implementation complete!

Summary:
- Tests added: [N]
- Files modified: [list]
- Features implemented: [list]

Suggested next steps:
- /commit to save changes
- /complete to wrap up
```

## Failure Handling

### Tests Won't Pass (>3 attempts)

After 3 failed fix attempts:
1. STOP trying fixes
2. Invoke `systematic-debugging` skill
3. Question architecture: Is this approach sound?

### Implementation Mismatch

If reality differs from plan/tests:
1. STOP immediately
2. Present the mismatch:
   ```
   Mismatch Found:
   Expected: [what was planned]
   Actual: [what codebase shows]
   Impact: [why this matters]
   ```
3. Use AskUserQuestion:
   - Question: "How to handle this mismatch?"
   - Options: "Adapt to reality" / "Update plan/tests" / "Discuss first"

## Constraints

- Never skip test verification
- Auto-suggest /debug on test failures
- Update checkboxes in plan files
- One phase at a time unless told otherwise

## Examples

### Feature from description
```
/build player can dash with shift key
```
→ Research → Propose tests → Write tests → Implement → Verify

### Feature from plan
```
/build docs/plans/2024-12-19-combat-system.md
```
→ Read plan → Resume from checkpoint → Execute phases → Verify each
