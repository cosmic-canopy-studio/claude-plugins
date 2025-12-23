# Brief Generator - Detailed Patterns

## Brief Structure Template

```markdown
# Feature Brief: [Topic]

**Date:** YYYY-MM-DD
**Author:** [Name]
**Status:** Draft

---

## Executive Summary

[2-3 sentences: what, why, expected impact]

---

## User Value

**Problem:**
[What pain point does this solve?]

**Solution:**
[How does this feature address it?]

**Benefit:**
[What value do users get?]

---

## Approach

**High-level approach:**
[Brief description of how we'll build this]

**Key components:**
- [Component 1]
- [Component 2]
- [Component 3]

---

## Effort & Timeline

**Complexity:** XS | S | M | L | XL

**Key milestones:**
- [Milestone 1]
- [Milestone 2]

---

## Dependencies

- [Dependency 1]
- [Dependency 2]

---

## Open Questions

1. [Question 1]
2. [Question 2]

---

## Next Steps

- [ ] [Action item 1]
- [ ] [Action item 2]
```

## Process Steps

1. **Gather context** from inputs and any research
2. **Synthesize value proposition** (problem → solution → benefit)
3. **Outline approach** at high level
4. **Estimate effort** using T-shirt sizing
5. **Identify dependencies and questions**
6. **Write to** `prds/brief-YYYY-MM-DD-{topic-slug}.md`

## T-Shirt Sizing Guide

| Size | Description | Typical Scope |
|------|-------------|---------------|
| XS | Trivial | Few hours, single change |
| S | Small | 1-2 days, isolated change |
| M | Medium | 3-5 days, some integration |
| L | Large | 1-2 weeks, cross-system |
| XL | Extra Large | 2+ weeks, significant scope |

## Quality Target

Brief should be scannable in 2-3 minutes. Focus on clarity over detail.

---

**Template:** `templates/feature-brief-template.md`
**Output:** `prds/brief-YYYY-MM-DD-{topic-slug}.md`
