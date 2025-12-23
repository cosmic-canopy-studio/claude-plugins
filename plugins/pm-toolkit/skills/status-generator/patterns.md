# Status Generator - Detailed Patterns

## Status Template

```markdown
# Status Update: [Topic]

**Period:** [Date range]
**Author:** [Name]
**Date:** YYYY-MM-DD

---

## Summary

[2-3 sentences: overall status, key highlight, any blockers]

**Overall Status:** 🟢 On Track | 🟡 At Risk | 🔴 Blocked

---

## Completed This Period

- [x] [Accomplishment 1]
- [x] [Accomplishment 2]
- [x] [Accomplishment 3]

---

## In Progress

- [ ] [Work item 1] - [Status: X% complete]
- [ ] [Work item 2] - [Status: X% complete]

---

## Blockers & Risks

### Active Blockers

| Blocker | Impact | Owner | Resolution Path |
|---------|--------|-------|-----------------|
| [Blocker] | [Impact] | [Name] | [How to resolve] |

### Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| [Risk] | H/M/L | H/M/L | [Approach] |

---

## Decisions Needed

1. **[Decision]**
   - Context: [Background]
   - Options: [A, B, C]
   - Recommendation: [If any]
   - Needed by: [Date]

---

## Next Period

- [ ] [Planned work 1]
- [ ] [Planned work 2]
- [ ] [Planned work 3]

---

## Metrics

| Metric | Target | Current | Trend |
|--------|--------|---------|-------|
| [Metric] | [Target] | [Current] | ↑/↓/→ |

---

## Notes

[Any additional context]
```

## Process Steps

1. **Gather context** from plans, conversations, or user input
2. **Summarize accomplishments** since last update
3. **Identify blockers and risks** with resolution paths
4. **List decisions needed** with context
5. **Plan next period** work items
6. **Write to** standard output or specified location

## Audience Tailoring

**For Leadership:**
- Focus on outcomes and metrics
- Highlight strategic blockers
- Include decisions needed from them

**For Team:**
- More tactical detail
- Include dependencies
- Technical context OK

---

**Template:** `templates/status-update-template.md`
