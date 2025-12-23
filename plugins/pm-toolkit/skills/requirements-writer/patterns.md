# Requirements Writer - Detailed Patterns

## Requirements Template

```markdown
# Feature Requirements: [Feature Name]

**Date:** YYYY-MM-DD
**Author:** [Name]
**PRD:** [Link to PRD if exists]
**Status:** Draft

---

## Overview

[Brief description of feature and requirements scope]

---

## Functional Requirements

### FR-001: [Requirement Title]

**Description:**
[What the system must do]

**Rationale:**
[Why this requirement exists]

**User Story:** [Reference if applicable]

**Acceptance Criteria:**
- [ ] Given [precondition], when [action], then [result]
- [ ] Given [precondition], when [action], then [result]

**Edge Cases:**
- [Edge case] → [Expected behavior]

**Priority:** Must Have | Should Have | Nice to Have

---

### FR-002: [Requirement Title]

[Continue pattern...]

---

## Non-Functional Requirements

### Performance

| Metric | Target | Measurement |
|--------|--------|-------------|
| Response time | < X ms P95 | [Tool] |
| Throughput | X req/sec | Load testing |

### Security

- [ ] [Security requirement]
- [ ] [Security requirement]

### Scalability

- [ ] [Scalability requirement]

### Accessibility

- [ ] WCAG [Level] compliance
- [ ] [Specific requirement]

---

## User Scenarios

### Scenario 1: [Scenario Name]

**Actor:** [User type]
**Precondition:** [Starting state]

**Steps:**
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected Result:** [Outcome]

---

## Constraints

- [Technical constraint]
- [Business constraint]

---

## Dependencies

- [Dependency 1]
- [Dependency 2]

---

## Appendix

### Glossary

- **[Term]**: [Definition]
```

## Process Steps

1. **Read PRD** if provided, extract user stories and requirements
2. **Expand requirements** into detailed functional specifications
3. **Add non-functional requirements** with specific targets
4. **Create user scenarios** for key workflows
5. **Validate** completeness and testability
6. **Write to** `requirements/YYYY-MM-DD-{feature-slug}.md`

## Quality Criteria

- Every requirement is testable
- Every requirement has acceptance criteria
- No implementation details (HOW)
- Clear traceability to user stories

---

**Template:** `templates/feature-requirements-template.md`
**Output:** `requirements/YYYY-MM-DD-{feature-slug}.md`
