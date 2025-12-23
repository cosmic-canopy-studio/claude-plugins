# Task Breakdown - Detailed Patterns

## Implementation Plan Template

```markdown
# Implementation Plan: [Feature/Initiative]

**Date:** YYYY-MM-DD
**Author:** [Name]
**Source:** [PRD or research doc]
**Status:** Draft

---

## Executive Summary

[2-3 sentences: what we're implementing, approach, total complexity]

---

## Context

**Objective:** [What we're trying to achieve]

**Scope:**
- In scope: [What's included]
- Out of scope: [What's not included]

**Constraints:**
- [Constraint 1]
- [Constraint 2]

---

## Implementation Phases

### Phase 1: [Phase Name]

**Objective:** [What this phase achieves]

**Complexity:** XS | S | M | L | XL

**Dependencies:** [Prerequisites]

**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]
- [ ] [Deliverable 3]

**Acceptance Criteria:**
- [ ] [Criterion 1 - testable]
- [ ] [Criterion 2 - testable]

**Risks:**
- [Risk 1] → Mitigation: [Approach]

---

### Phase 2: [Phase Name]

**Objective:** [What this phase achieves]

**Complexity:** XS | S | M | L | XL

**Dependencies:** Phase 1 complete, [Other dependencies]

**Deliverables:**
- [ ] [Deliverable 1]
- [ ] [Deliverable 2]

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

---

## Complexity Summary

| Phase | Complexity | Key Risk |
|-------|------------|----------|
| Phase 1 | M | [Risk] |
| Phase 2 | L | [Risk] |
| Phase 3 | S | [Risk] |

**Total Estimated Complexity:** [Aggregate]

---

## Dependencies Map

```
Phase 1
   ↓
Phase 2 ──→ External Dependency
   ↓
Phase 3
```

---

## Critical Path

1. [Critical item 1]
2. [Critical item 2]
3. [Critical item 3]

---

## Parallelization Opportunities

- [Phase 2 and 3 can run in parallel if...]
- [These tasks within Phase 1 can parallelize...]

---

## Testing Strategy

### Per Phase

| Phase | Test Type | Coverage |
|-------|-----------|----------|
| Phase 1 | Unit + Integration | [Areas] |
| Phase 2 | Integration + E2E | [Areas] |

### Overall Validation

- [ ] [End-to-end test scenario]
- [ ] [Performance validation]

---

## Rollout Plan

**Strategy:** [Big bang | Phased | Feature flag]

**Stages:**
1. [Stage 1] - [Scope/audience]
2. [Stage 2] - [Scope/audience]

**Rollback Plan:** [How to revert if needed]

---

## Open Questions

1. [Question] - Owner: [Name]
2. [Question] - Owner: [Name]
```

## Complexity Estimation

**T-Shirt Sizing Guide:**

| Size | Description | Typical Scope |
|------|-------------|---------------|
| XS | Trivial | Few hours, single change |
| S | Small | 1-2 days, isolated change |
| M | Medium | 3-5 days, some integration |
| L | Large | 1-2 weeks, cross-system |
| XL | Extra Large | 2+ weeks, significant scope |

**Factors to Consider:**
- Novelty (new vs. familiar patterns)
- Integration points
- Testing complexity
- Risk and unknowns

---

**Template:** `templates/implementation-plan-template.md`
**Output:** `plans/YYYY-MM-DD-{feature}.md`
