# Decision Documenter - Detailed Patterns

## Decision Record Template (ADR-style)

```markdown
# Decision: [Short Title]

**Date:** YYYY-MM-DD
**Status:** Proposed | Accepted | Deprecated | Superseded
**Decision ID:** DEC-YYYY-NNN
**Participants:** [Names]

---

## Context

[Background: What situation led to this decision? What problem needed solving?]

---

## Decision

[The decision that was made, stated clearly and directly]

---

## Options Considered

### Option 1: [Name]

**Description:** [What this option entails]

**Pros:**
- [Pro 1]
- [Pro 2]

**Cons:**
- [Con 1]
- [Con 2]

**Estimated Effort:** [If relevant]

---

### Option 2: [Name]

[Continue pattern...]

---

### Option 3: Do Nothing

**Description:** Maintain status quo

**Pros:**
- No effort required
- No risk of change

**Cons:**
- [Problems that persist]

---

## Rationale

[Why this option was chosen over others. What factors were most important?]

**Key factors:**
1. [Factor 1 and how it influenced decision]
2. [Factor 2 and how it influenced decision]

---

## Consequences

### Positive

- [Expected positive outcome 1]
- [Expected positive outcome 2]

### Negative

- [Trade-off or cost 1]
- [Trade-off or cost 2]

### Neutral

- [Side effect that's neither good nor bad]

---

## Follow-up Actions

- [ ] [Action 1] - Owner: [Name] - Due: [Date]
- [ ] [Action 2] - Owner: [Name] - Due: [Date]

---

## Related Decisions

- [DEC-YYYY-NNN]: [Related decision and how it connects]

---

## Review Date

[When this decision should be revisited, if applicable]
```

## Decision Log Integration

Decisions can be appended to a central decision log:

```markdown
# Decision Log

| ID | Date | Decision | Status |
|----|------|----------|--------|
| DEC-2025-001 | 2025-12-21 | Use JWT for auth | Accepted |
| DEC-2025-002 | 2025-12-21 | Defer mobile app | Accepted |
```

## Process Steps

1. **Capture the decision** clearly and directly
2. **Document context** - what led to this decision
3. **List options considered** with pros/cons
4. **Explain rationale** - why this option won
5. **Identify consequences** - expected outcomes
6. **Assign follow-up actions**
7. **Write to** decision log or standalone file

## Quality Criteria

- Decision is clear and unambiguous
- Context explains why decision was needed
- At least 2 options considered (including "do nothing")
- Rationale explains the "why"
- Consequences are realistic (not just positives)

---

**Template:** `templates/decision-record-template.md`
