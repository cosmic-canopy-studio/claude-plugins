# Workflow Complete - Reference

Detailed documentation for the completion phase of the workflow.

## Completion Detection

The skill activates when:
1. `workflow-implement` has marked all phases `[x]`
2. `verification-before-completion` has passed
3. User says "done", "finished", or similar

## Commit Strategy

### Single vs Multiple Commits

**Single commit when:**
- All changes are related
- One logical unit of work
- Small scope

**Multiple commits when:**
- Distinct logical changes
- Different areas of codebase
- Makes history clearer

### Commit Message Quality

**Good:**
```
feat: add player dash with cooldown

Enables quick directional movement during combat.
Uses existing stamina system for resource management.
Dash distance scales with player level.
```

**Bad:**
```
update player
fixed stuff
wip
```

## Archive Structure

```
project/
├── docs/
│   ├── plans/           # Active plans
│   │   └── 2024-01-15-dash-ability.md
│   └── retrospectives/  # Completion notes
│       └── 2024-01-16-dash-ability.md
└── archive/
    └── docs/
        └── plans/       # Completed plans
            └── 2024-01-10-movement-refactor.md
```

## Retrospective Template

```markdown
# [Task Name] Retrospective

**Date:** YYYY-MM-DD
**Duration:** [time from plan creation to completion]

## Summary
[What was built and why it matters]

## What Went Well
- [Specific success with example]
- [Process that worked]
- [Tool or pattern that helped]

## What Didn't Go Well
- [Challenge with specific example]
- [Time sink or blocker]
- [Assumption that was wrong]

## Lessons Learned
- [Actionable insight for future]
- [Pattern to repeat]
- [Anti-pattern to avoid]

## Follow-up Items
- [ ] [Deferred work item]
- [ ] [Future enhancement]
- [ ] [Technical debt to address]
```

## Next Task Detection

```
1. Glob docs/plans/*.md (exclude archive/)
2. For each file:
   a. Parse for [ ] patterns
   b. If any unchecked → incomplete
3. Sort by modification date (oldest first)
4. Return first incomplete plan
5. If none → "Ready for new task"
```

## Integration with Workflow Chain

### Incoming Chain
```
workflow-implement (all phases done)
         ↓
verification-before-completion (passes)
         ↓
workflow-complete (this skill)
```

### Outgoing Suggestions
After completion, suggest based on context:
- Incomplete plan exists → "Next: [plan name]"
- No plans → "Ready for new task. Describe what to build."
- User mentioned follow-up → Reference the follow-up

## Absorbed Commit Behavior

This skill absorbs the `/commit` command functionality:
- Same commit rules apply
- Same message format
- Same file-specific additions
- No separate commit skill needed

For standalone commits outside workflow:
- User can use git directly
- Or describe what to commit
