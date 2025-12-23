# Issue Analysis Reference

## Analysis Template

```markdown
# Analysis: [Title] (#XX)

> Generated: YYYY-MM-DD
> Issue: docs/issues/[category]/XXX-title.md

## Summary
Brief 2-3 sentence assessment of the issue.

## Implicit Requirements

### UI/UX
- [Requirement 1]

### Data/State
- [Requirement 1]

### Integration
- [Requirement 1]

## Technical Challenges

### [Challenge Name]
**Risk:** High/Medium/Low
**Description:** What makes this challenging
**Mitigation:** How to address it

## Suggested Acceptance Criteria

- [ ] **Given** [state] **When** [action] **Then** [result]
- [ ] **Given** [error] **When** [action] **Then** [handling]

## Complexity Assessment

**Size:** Small/Medium/Large/XL

**Justification:**
- [Reason 1]
- [Reason 2]

**Effort Breakdown:**
| Component | Effort |
|-----------|--------|
| Design | Low/Med/High |
| Implementation | Low/Med/High |
| Testing | Low/Med/High |
| Integration | Low/Med/High |

## Related Codebase Areas

### Files to Modify
- `repos/lacrosse-bosse/path/file.gd` - Purpose

### Patterns to Follow
- [Pattern] from `file:line`

## Dependencies

### Requires First
- #XX [Title] - Why needed

### Enables
- #XX [Title] - What this unblocks

## Recommendations

1. **[Recommendation]** - Brief explanation
```

## Complexity Sizing Guide

| Size | Criteria | Examples |
|------|----------|----------|
| **Small** | Single file, < 4 hours | Bug fix, config change, simple UI |
| **Medium** | 2-5 files, 1-3 days | New feature, refactor, integration |
| **Large** | Multiple subsystems, 1-2 weeks | Major feature, architecture change |
| **XL** | Cross-cutting, 2+ weeks | Platform integration, new system |

## Acceptance Criteria Patterns

### Given-When-Then Format
```
**Given** [precondition/state]
**When** [action performed]
**Then** [expected outcome]
```

### Common Patterns

**Happy Path:**
```
**Given** a valid input **When** processing **Then** success result
```

**Error Handling:**
```
**Given** invalid input **When** processing **Then** clear error message
```

**Edge Cases:**
```
**Given** empty/null input **When** processing **Then** graceful handling
```

**State Transitions:**
```
**Given** state A **When** event occurs **Then** transitions to state B
```

## Detecting Incomplete Issues

### Placeholder Patterns
- `**Given** [initial state]` - Template not filled
- `**When** [action]` - Generic placeholder
- Empty acceptance criteria section
- Only `- [ ]` without content

### Missing Sections
- No "Acceptance Criteria" heading
- No "User Story" section
- Missing technical notes for complex issues

## Issue Categories

| Category | Indicators |
|----------|------------|
| gameplay | play, practice, field, objective, fielder |
| ci-cd | GitHub Actions, build, pipeline, lint, deploy |
| team-features | auth, subscription, team, coach, member |
| ui-ux | menu, button, UI, screen, indicator |
| platforms | iOS, Android, mobile, export |
| audio-visual | audio, sound, VFX, splash, music |
| design | Figma, design, roster, mockup |
| technical | refactor, bug, performance, logging |

## Agent Invocation

### Single Issue
```
Launch issue-analyzer agent with:
- Issue file path
- Related codebase context
- Output path for analysis
```

### Batch Mode
```
For issues in batches of 3:
  Launch 3 parallel issue-analyzer agents
  Wait for completion
  Collect results
  Report progress
```

## Output Locations

| Type | Location |
|------|----------|
| Individual analysis | `docs/recommendations/issues/XXX-title-analysis.md` |
| Catalog report | `docs/recommendations/issue-catalog.md` |
| Summary | Console output |
