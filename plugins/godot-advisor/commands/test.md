---
description: Run tests, propose tests (TDD), or design test strategy - unified testing command
argument-hint: [path | propose FEATURE | design SYSTEM]
---

# Test: $ARGUMENTS

Unified testing command with three modes.

## Mode Detection

| Arguments | Mode | Action |
|-----------|------|--------|
| (none) | Run | Execute all tests |
| `test/test_player.gd` | Run | Execute specific test file |
| `propose player dash` | TDD Propose | Write failing tests first |
| `design combat system` | Strategy | Design test architecture |

## Mode 1: Run Tests

### Run All Tests
```
/test
```

Execute test suite and report results:

```bash
cd demo/dungeon_delve && ./run_tests.sh
```

### Run Specific Tests
```
/test test/test_player.gd
/test test/test_combat.gd
```

Execute single test file:

```bash
cd demo/dungeon_delve && ./run_tests.sh test/test_player.gd
```

### Results Handling

**On Success:**
```
All tests passed (N tests)

Coverage:
- [list of tested behaviors]

Ready for /commit or /complete
```

**On Failure:**
```
Test failures detected:

FAILED: test_player_moves_with_input
  Expected: position changed
  Actual: position unchanged
  File: test/test_player.gd:25

Suggested action: /debug test_player_moves_with_input
```

Auto-suggest `/debug` when tests fail.

## Mode 2: TDD Propose

```
/test propose player dash ability
```

Write failing tests BEFORE implementation (TDD Red phase).

### Process

1. **Analyze feature requirements:**
   - What should this feature DO?
   - What inputs/outputs matter?
   - What edge cases exist?

2. **Research existing code:**
   - Related classes and methods
   - Existing test patterns
   - Relevant skills for guidance

3. **Propose test cases:**

   ```markdown
   ## Test Proposals: Player Dash Ability

   ### Test: player_can_dash_when_pressing_shift
   Given: Player is idle
   When: Shift key pressed
   Then: Player moves at dash_speed in facing direction

   ### Test: player_cannot_dash_during_cooldown
   Given: Player just finished dashing
   When: Shift key pressed within cooldown period
   Then: Player does not dash

   ### Test: player_dash_has_limited_duration
   Given: Player starts dashing
   When: dash_duration elapses
   Then: Player returns to normal speed
   ```

4. **Get approval via AskUserQuestion:**
   - Question: "These tests capture the requirements?"
   - Options: "Yes, write them" / "Add more tests" / "Modify these"

5. **Write test file:**

   ```gdscript
   # test/test_player_dash.gd
   extends GdUnitTestSuite

   var _player: Player

   func before_test() -> void:
       _player = auto_free(Player.new())
       add_child(_player)

   func test_player_can_dash_when_pressing_shift() -> void:
       var start_pos := _player.position
       Input.action_press("dash")
       await get_tree().physics_frame
       Input.action_release("dash")
       assert_that(_player.is_dashing).is_true()
   ```

6. **Verify tests FAIL:**
   ```bash
   cd demo/dungeon_delve && ./run_tests.sh test/test_player_dash.gd
   ```

   Tests MUST fail before implementation begins.

## Mode 3: Design Strategy

```
/test design combat system
```

Design comprehensive test architecture before writing tests.

### Process

1. **Invoke test-architect agent:**
   ```
   Task test-architect "Design test strategy for combat system"
   ```

2. **Deliverables:**
   - Test categories (unit, integration, gameplay)
   - Critical behaviors to test
   - Test fixtures needed
   - Mocking strategy
   - Test file organization

3. **Output format:**

   ```markdown
   # Test Strategy: Combat System

   ## Test Categories

   ### Unit Tests
   - Damage calculation
   - Health management
   - Attack timing

   ### Integration Tests
   - Player attacks enemy
   - Enemy attacks player
   - Multiple combatants

   ### Gameplay Tests
   - Combat loop completion
   - Death handling
   - Respawn behavior

   ## Test Fixtures Needed
   - TestEnemy: Minimal enemy for combat testing
   - TestArena: Enclosed area with combatants

   ## File Structure
   test/
   ├── test_damage_calculation.gd
   ├── test_health_system.gd
   ├── test_combat_integration.gd
   └── fixtures/
       ├── test_enemy.tscn
       └── test_arena.tscn
   ```

## Integration with Other Commands

| After /test | Suggest |
|-------------|---------|
| Tests fail | `/debug` to investigate |
| Tests pass | `/commit` or `/complete` |
| Propose done | `/build` to implement |
| Design done | `/test propose` for specific features |

## Constraints

- Always use `./run_tests.sh` (handles xvfb-run)
- Never mark tests as passing without running them
- TDD propose MUST verify tests fail before completing
- Auto-suggest /debug on any test failure
