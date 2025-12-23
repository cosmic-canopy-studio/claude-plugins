# Workflow Implement - Reference

Detailed documentation for the implementation phase of the workflow.

## Plan Detection Logic

```
1. Glob for docs/plans/*.md (exclude archive/)
2. For each plan file:
   a. Parse for [ ] and [x] patterns
   b. If any [ ] exists → candidate for implementation
3. If multiple candidates:
   a. Use most recently modified
   b. Or ask user which to implement
4. If no candidates:
   a. Announce "No active plan found"
   b. Suggest workflow-prepare
```

## Git Workflow Per Phase

### Commit Strategy
- One commit per phase (atomic, reversible)
- Specific file additions: `git add path/to/file.gd`
- NEVER use: `git add -A` or `git add .`

### Commit Message Format
```
[type]: [brief description]

[body explaining why, not what]
```

Types: `feat`, `fix`, `refactor`, `docs`, `test`, `chore`

### Push Strategy
- Push after each phase completes
- Keeps remote in sync
- Enables early feedback

## Verification Evidence Patterns

### Good Evidence
```
Automated checks passed:
- gdlint src/player.gd → 0 errors, 0 warnings
- godot --headless --script test.gd → 12/12 tests pass
- git status → working tree clean
```

### Bad Evidence
```
Automated checks passed:
- Linting should be fine
- Tests probably pass
- I think it works
```

## Resumption Logic

When resuming a partially completed plan:

1. **Trust existing checkmarks** - Don't re-verify completed phases
2. **Start from first unchecked** - Continue where left off
3. **Read context** - Understand what was done before

## Adaptation vs Blocking

### Adapt Automatically
- File renamed but same purpose
- Method signature slightly different
- Additional parameters with defaults
- Different but equivalent pattern

### Note and Continue
- Missing expected file (create it)
- Different architecture than expected
- Additional work discovered

### Stop and Clarify (Major Issues)
- Scope fundamentally different
- Core assumption invalid
- Security/safety concerns

## Integration Points

### Before Implementation
- `workflow-prepare` creates the plan
- Plan file exists at `docs/plans/*.md`

### After All Phases
- `verification-before-completion` validates everything
- `workflow-complete` wraps up and archives

### Chain Trigger
When last phase checkbox is marked `[x]`:
```
All phases complete. Triggering final verification...
```
→ `verification-before-completion` activates
→ `workflow-complete` activates
