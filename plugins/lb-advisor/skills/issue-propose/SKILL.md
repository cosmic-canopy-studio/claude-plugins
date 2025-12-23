---
name: issue-propose
description: Create issue proposals with minimal, outcome-focused user stories. Trust the implementer - define WHAT users need, not HOW to build it.
when_to_use:
  triggers:
    - "create issue proposal"
    - "propose issue"
    - "new issue for"
    - "write up an issue"
  auto_invoke: always
version: 2.0.0
---

# Skill: Issue Proposal Creation

Create issue proposals that define user needs while leaving implementation to designer/developer judgment.

## Philosophy

**Trust the implementer.** Issues define *what* the user needs, not *how* to build it.

## The Template

```markdown
## User Story
As a [role], I want [an action or feature], so that [a reason or benefit].

## Acceptance Criteria
- [ ] **Given** [initial state] **When** [action] **Then** [result]
```

That's it. Additional context only when genuinely helpful.

## Process

1. **Understand the need** - What does the user want to accomplish?
2. **Write user story** - Role, action, benefit
3. **Define outcomes** - Testable criteria (not UI specs)
4. **Add context only if needed** - Constraints, prior art, non-obvious requirements

## Style Principles

### Write Outcomes, Not Implementations

**Too prescriptive:**
> Given main menu When I tap "Create Plays" Then I see two prominent buttons

**Better:**
> Given I want to create a play When I'm on the main menu Then I can easily access the play creator

The implementer decides: buttons vs tabs, labels, layout.

### One Criterion = One Capability

**Cluttered:**
```
- [ ] Given main menu Then see "Create Plays" button
- [ ] Given main menu Then see "Practice Plays" button
- [ ] Given main menu Then buttons are prominent
```

**Clean:**
```
- [ ] Given main menu When I want to create or practice plays Then the options are clear and accessible
```

### Context is Optional

Only add when:
- Problem isn't obvious from user story
- Critical constraint implementer must know
- Historical context prevents repeating mistakes

## What NOT to Include

| Skip | Why |
|------|-----|
| ASCII UI mockups | Constrains design |
| File paths | Implementation detail |
| Button/label text | Designer's choice |
| Technical specs | Save for planning |

## When More Detail Helps

Brief notes only:
- **Constraints**: "Must work on mobile"
- **Prior art**: "Similar to Roster screen"
- **Requirements**: "Needs offline support"

## Example

```markdown
## User Story
As a coach, I want to practice the plays I create, so that I can test my designs with actual fielders.

## Acceptance Criteria
- [ ] Given I've saved a play When I enter practice mode Then my play loads and executes
- [ ] Given my play is invalid When I try to practice Then I get a helpful error
```

*Core functionality. No UI prescription. Trust the team.*

## Output

Save to `docs/proposed-issues/[descriptive-name].md`
