# Workflow Prepare - Reference

Detailed documentation for the prepare phase of the workflow.

## Exploration Strategy

When the user describes a feature to build, exploration happens implicitly:

### Quick Exploration (Default)
- 1-2 Explore agents for targeted searches
- 3-5 key file reads maximum
- Focus on understanding, not exhaustive discovery

### Deep Exploration (Complex Features)
- 3-5 Explore agents with specific focus areas
- Pattern analysis across related files
- Architecture understanding before planning

## Plan Quality Checklist

Before writing the plan:

- [ ] Understood the user's actual intent (not just their words)
- [ ] Identified key files that will be modified
- [ ] Determined what's in scope vs out of scope
- [ ] Designed phases that are independently testable
- [ ] Included both automated and manual success criteria

## Phase Design Principles

### Good Phase Boundaries
- Single logical change
- Can be tested independently
- Has clear success criteria
- Rollback is straightforward

### Bad Phase Boundaries
- "Do all the refactoring"
- Multiple unrelated changes
- Success criteria: "it works"
- Dependencies between phases not clear

## Success Criteria Split

### Automated (Commands)
- Linter passes: `gdlint path/to/file.gd`
- Tests pass: `godot --headless --script run_tests.gd`
- Build succeeds: `godot --headless --export`
- Type checking: strict typing enabled

### Manual (Human Verification)
- Visual behavior matches expectation
- Performance is acceptable
- Edge cases handled correctly
- User experience is intuitive

## Out of Scope Template

Always include explicit boundaries:

```markdown
## Out of Scope

The following are explicitly NOT part of this implementation:
- [Related feature that might seem included]
- [Optimization that can wait]
- [Edge case we're deferring]
- [Refactoring that's separate concern]
```

## Integration with Existing Patterns

This skill replaces the `/prepare` command with automatic invocation. Key differences:

| Old Command | New Skill |
|-------------|-----------|
| `/prepare` invoked manually | Triggers on feature description |
| AskUserQuestion for confirmation | Automatic flow, no gates |
| Standalone operation | Chains to workflow-implement |
| Recon was separate | Exploration is implicit |
