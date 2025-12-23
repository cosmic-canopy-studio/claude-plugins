---
description: Validate workflow commands and skills - runs structural, schema, and cross-reference tests
---

# Test Workflow

Validate the workflow system by running structural, schema, and cross-reference tests using Read, Glob, and Grep tools.

## Process

Run all test suites in order, reporting pass/fail for each test.

### Suite 1: Command Structure Tests

**Validate each command file independently (parallelizable):**

Commands to validate:
- `build.md`, `test.md`, `debug.md`, `research.md`
- `plan.md`, `docs.md`, `commit.md`, `complete.md`

**Per-file validation task:**
```
Input: Single command file path (e.g., `.claude/commands/build.md`)
Process:
  1. Read the file
  2. Verify YAML frontmatter (starts with `---`)
  3. Verify `description:` field exists in frontmatter
  4. Verify markdown content after frontmatter
Output: {file: "build.md", status: "PASS/FAIL", reason: "..."}
```

**Execution:** Run 8 parallel Read operations, one per command file.

**Report format:**
```
Suite 1: Command Structure
  [PASS] build.md - has frontmatter and description
  [PASS] test.md - has frontmatter and description
  ... (all 8 commands)
```

### Suite 2: Skill Structure Tests

**For workflow-router skill**, verify:
1. `.claude/skills/workflow-router/SKILL.md` exists
2. Has `name:` field (lowercase, hyphens only)
3. Has `description:` field

**Report format:**
```
Suite 2: Skill Structure
  [PASS] workflow-router - has name and description
```

### Suite 3: Schema Compliance Tests

**Validate each skill independently (parallelizable):**

Skills to validate:
- `systematic-debugging`, `when-stuck`
- `verification-before-completion`, `brainstorming`

**Per-skill validation task:**
```
Input: Single skill path (e.g., `.claude/skills/systematic-debugging/SKILL.md`)
Process:
  1. Read the SKILL.md file
  2. Verify `when_to_use:` block exists
  3. Verify `triggers:` array exists within when_to_use
  4. Verify `auto_invoke:` field has valid value (always/suggest/never)
Output: {skill: "systematic-debugging", status: "PASS/FAIL", reason: "..."}
```

**Execution:** Run 4 parallel Read operations, one per skill.

**Report format:**
```
Suite 3: Schema Compliance
  [PASS] systematic-debugging - has when_to_use with auto_invoke: suggest
  [PASS] when-stuck - has when_to_use with auto_invoke: suggest
  [PASS] verification-before-completion - has when_to_use with auto_invoke: always
  [PASS] brainstorming - has when_to_use with auto_invoke: suggest
```

### Suite 4: Cross-Reference Tests

**Validate cross-references in parallel categories:**

**Category A: Commands in workflow-router (parallelizable)**
```
Input: workflow-router SKILL.md
Process: Extract all `/command` references, verify each exists in .claude/commands/
Output: {ref: "/build", status: "PASS/FAIL"}
```

**Category B: Skills referenced in commands (parallelizable)**
For each command file, extract skill references and verify they exist:
- `debug.md` → `systematic-debugging`
- `build.md` → `skill-advisor`
- `test.md` → `gameplay-test-writer`, `test-architect`
- `research.md` → `godot-pattern-researcher`

**Category C: Follows/leads_to in when_to_use skills (parallelizable)**
For each skill with when_to_use, validate its references:

| Skill | follows | leads_to |
|-------|---------|----------|
| systematic-debugging | /test, /build | /test, /commit |
| when-stuck | Any failed attempt | systematic-debugging, simplification-cascades, etc. |
| verification-before-completion | /build, /debug | /commit, /complete |
| brainstorming | Initial feature request | /plan, /build |

**Per-reference validation task:**
```
Input: Single reference (e.g., "systematic-debugging")
Process: Verify .claude/skills/{ref}/SKILL.md exists OR .claude/commands/{ref}.md exists
Output: {ref: "systematic-debugging", status: "PASS/FAIL"}
```

**Report format:**
```
Suite 4: Cross-References
  [PASS] workflow-router → /build exists
  [PASS] workflow-router → /test exists
  ... (all 8 command refs)
  [PASS] debug.md → systematic-debugging exists
  [PASS] systematic-debugging leads_to → /commit exists
  ... (all follows/leads_to refs)
```

### Suite 5: Routing Logic Tests

**Test workflow-router intent detection by verifying routing table exists:**

| Test Input | Expected Route |
|------------|----------------|
| "I want to add X" | `/build` |
| "How does X work" | `/research` |
| "Design X" | `/plan` |
| "X is broken" | `/debug` |
| "Run tests" | `/test` |
| "Document X" | `/docs` |
| "Commit changes" | `/commit` |
| "I'm done" | `/complete` |

**Validation (parallelizable per route):**
```
Input: Single route mapping (e.g., {"pattern": "build/implement", "route": "/build"})
Process:
  1. Read workflow-router SKILL.md
  2. Search for pattern keywords in Intent Detection table
  3. Verify they map to expected command
Output: {pattern: "build/implement", route: "/build", status: "PASS/FAIL"}
```

**Report format:**
```
Suite 5: Routing Logic
  [PASS] "build/implement" → /build
  [PASS] "what is/how does" → /research
  [PASS] "design/architect" → /plan
  [PASS] "fix/broken" → /debug
  [PASS] "run tests/verify" → /test
  [PASS] "document/write docs" → /docs
  [PASS] "commit/save" → /commit
  [PASS] "done/finished" → /complete
```

---

## Functional Test Suites (6-12)

These suites test the validation mini-project at `demo/validation_project/`.

### Suite 6: Agent Existence Tests

**Validate each agent file independently (parallelizable):**

1. Use Glob to get list: `.claude/agents/*.md`
2. For EACH agent file, spawn discrete validation task

**Per-agent validation task:**
```
Input: Single agent file path (e.g., `.claude/agents/skill-scaffolder.md`)
Process:
  1. Read the file
  2. Verify YAML frontmatter exists (starts with `---`)
  3. Verify `name:` field exists
  4. Verify `description:` field exists
Output: {agent: "skill-scaffolder", status: "PASS/FAIL", reason: "..."}
```

**Execution:** Run N parallel Read operations, one per agent file.

**Report format:**
```
Suite 6: Agent Existence
  [PASS] skill-scaffolder - has name and description
  [PASS] gdscript-analyzer - has name and description
  [PASS] skill-content-writer - has name and description
  ... (all N agents)
  Summary: N/N agents valid
```

### Suite 7: GDScript Syntax Validation

**Verify validation project scripts parse without errors:**

1. Run syntax check (requires xvfb-run for display):
   ```bash
   cd demo/validation_project && xvfb-run --auto-servernum godot --headless --path . --check-only 2>&1
   ```
2. Check exit code is 0
3. Verify no parse errors in output

**Alternative validation via test runner:**
If syntax is valid, the test runner in Suites 9-10 will execute. Script parse errors would cause immediate failure.

**Report format:**
```
Suite 7: GDScript Syntax
  [PASS] player.gd - valid syntax
  [PASS] coin.gd - valid syntax
  [PASS] All scripts parse successfully
```

### Suite 8: Spec-Driven Test Writing Validation

**Verify tests are derived from input spec:**

1. Read `demo/validation_project/specs/player_dash.md`
2. Extract requirements from spec
3. Read `demo/validation_project/test/test_player.gd`
4. Verify tests reference spec requirements in comments:
   - `test_player_can_dash` → Spec requirement 1
   - `test_player_dash_activates` → Spec requirement 3
   - `test_player_dash_speed` → Spec requirement 2

**Report format:**
```
Suite 8: Spec-Driven Tests
  [PASS] Spec file exists with 3 requirements
  [PASS] test_player_can_dash references spec
  [PASS] test_player_dash_activates references spec
  [PASS] test_player_dash_speed references spec
```

### Suite 9: TDD Cycle Test

**Complete red-green TDD cycle in single execution (consolidates old Suites 9/10/11):**

**1. Pre-flight Checks (parallelizable reads):**
- Verify spec exists: `demo/validation_project/specs/player_dash.md`
- Verify spec exists: `demo/validation_project/specs/enemy_patrol.md`
- Verify tests exist: `demo/validation_project/test/test_player.gd`
- Verify tests exist: `demo/validation_project/test/test_enemy.gd`
- Verify incomplete stubs: `player.gd` and `enemy.gd` have STUB comments
- Verify complete versions: `player_complete.gd` and `enemy_complete.gd` exist

**2. Red Phase:**
```bash
cd demo/validation_project && xvfb-run --auto-servernum godot --headless --path . -s addons/gdUnit4/bin/GdUnitCmdTool.gd --add "res://test/" --ignoreHeadlessMode
```
- Capture output
- Verify 7 tests PASS (baseline: 3 enemy + 2 player + 2 coin)
- Verify 8 tests FAIL (spec-derived: 5 enemy + 3 player)

**3. Green Phase:**
```bash
cp demo/validation_project/scripts/player_complete.gd demo/validation_project/scripts/player.gd
cp demo/validation_project/scripts/enemy_complete.gd demo/validation_project/scripts/enemy.gd
cd demo/validation_project && xvfb-run --auto-servernum godot --headless --path . -s addons/gdUnit4/bin/GdUnitCmdTool.gd --add "res://test/" --ignoreHeadlessMode
```
- Capture output
- Verify ALL 15 tests PASS
- **Evidence captured:** Extract pass count (e.g., "15 test cases | 0 failures")

**4. Cleanup:**
```bash
git checkout demo/validation_project/scripts/player.gd
# enemy.gd is new, restore manually by copying stub content
```
- Verify restoration to red phase state

**Report format:**
```
Suite 9: TDD Cycle Test
  [PASS] Pre-flight: specs, tests, and fixtures exist
  [PASS] Red phase: 7 baseline pass, 8 spec-derived fail
  [PASS] Green phase: 15/15 tests pass
  [PASS] Evidence: "15 test cases | 0 failures"
  [PASS] Cleanup: stubs restored to red phase state
```

### Suite 10: Workflow Journey Tests

**Validate complete workflow chains by reading skill files (read-only validation):**

**Journey A: Feature Implementation Flow**
1. Read `workflow-router` SKILL.md
2. Verify "I want to add" maps to `workflow-prepare`
3. Read `workflow-prepare` SKILL.md (if exists)
4. Verify chain: workflow-prepare → workflow-implement → verification → workflow-complete

**Journey B: Debug Flow**
1. Read `workflow-router` SKILL.md
2. Verify "fix/broken/bug" patterns map to `systematic-debugging`
3. Read `systematic-debugging` SKILL.md
4. Verify `leads_to` includes "/test", "/commit"
5. Verify `follows` includes failure scenarios

**Journey C: Completion Flow**
1. Read `verification-before-completion` SKILL.md
2. Verify `auto_invoke` is "always"
3. Verify `follows` includes implementation workflows
4. Verify `leads_to` includes `workflow-complete`

**Report format:**
```
Suite 10: Workflow Journey Tests
  [PASS] Journey A: workflow-router → workflow-prepare chain exists
  [PASS] Journey B: debug flow (fix/broken → systematic-debugging → /commit)
  [PASS] Journey C: verification-before-completion leads to workflow-complete
```

### Suite 11: Failure Mode Tests

**Validate error detection capabilities (meta-tests on validation rules):**

**Test 11.1: Command Validation Requirements**
- Read a known-good command file (e.g., `build.md`)
- Verify Suite 1 checks for `description:` field
- Document that missing description would cause failure

**Test 11.2: Agent Validation Requirements**
- Read a known-good agent file
- Verify Suite 6 checks for `name:` and `description:` fields
- Document that missing fields would cause failure

**Test 11.3: Cross-Reference Bidirectionality**
- From Suite 4 results, verify:
  - Commands reference skills that exist
  - Skills reference commands that exist
  - `follows` and `leads_to` references are valid

**Test 11.4: when_to_use Schema Enforcement**
- Read skills with `when_to_use` blocks
- Verify `auto_invoke` values are valid (always/suggest/never)
- Verify `triggers` is an array
- Document that invalid values would cause failure

**Report format:**
```
Suite 11: Failure Mode Tests
  [PASS] Command validation requires description field
  [PASS] Agent validation requires name and description fields
  [PASS] Cross-references are bidirectional and valid
  [PASS] when_to_use schema enforces valid auto_invoke values
```

---

## Output Format

```
=== Workflow Validation Tests ===

--- Structural Tests ---

Suite 1: Command Structure
  [PASS/FAIL] ... (8 parallel checks)

Suite 2: Skill Structure
  [PASS/FAIL] ...

Suite 3: Schema Compliance
  [PASS/FAIL] ... (4 parallel checks)

Suite 4: Cross-References
  [PASS/FAIL] ... (parallel by category)

Suite 5: Routing Logic
  [PASS/FAIL] ... (8 parallel checks)

--- Functional Tests ---

Suite 6: Agent Existence
  [PASS/FAIL] ... (N parallel checks)

Suite 7: GDScript Syntax
  [PASS/FAIL] ...

Suite 8: Spec-Driven Tests
  [PASS/FAIL] ...

Suite 9: TDD Cycle Test
  [PASS/FAIL] ... (consolidated red/green/cleanup)

Suite 10: Workflow Journeys
  [PASS/FAIL] ... (3 journey validations)

Suite 11: Failure Modes
  [PASS/FAIL] ... (4 meta-tests)

=== Results ===
Total: N tests
Passed: N
Failed: N

[All tests passed! | N tests failed - see above for details]
```

## Execution Notes

- **Parallel execution:** Suites 1, 3, 4, 5, 6 support parallel validation tasks
- Run suites sequentially, but parallelize within suites where noted
- Stop on first failure within a test, but continue to next test
- Report all failures at the end
- Use Glob for file discovery, Read for content inspection, Grep for pattern matching
- **xvfb-run required:** Godot headless mode still requires a display server
  ```bash
  xvfb-run --auto-servernum godot --headless --path . ...
  ```
- Restore validation project state after green phase tests:
  ```bash
  git checkout demo/validation_project/scripts/player.gd
  # enemy.gd is untracked - restore by overwriting with stub content
  ```
- **Test counts:** Validation project has 15 tests (7 baseline, 8 spec-derived)
