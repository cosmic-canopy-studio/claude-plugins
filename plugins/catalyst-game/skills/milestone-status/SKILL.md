---
name: milestone-status
description: Generate milestone progress reports from the issue catalog, tracking completion percentages, blockers, and recommended next actions
allowed-tools: Read, Glob, Grep, Write
version: 1.0.0
---

# Milestone Status Reports

## Overview

Generate progress reports for project milestones by analyzing the issue catalog at `docs/issues/`.

**Announce at start:** "I'm using the milestone-status skill to generate a progress report."

## Process

### Phase 1: Parse Issue Catalog
1. Read all issue files from `docs/issues/*/`
2. Extract metadata: number, title, state, milestone
3. Group issues by milestone

### Phase 2: Calculate Metrics
For each milestone:
- Count open vs closed issues
- Calculate completion percentage
- Identify issues by category
- Note recent completions (closed in last 30 days)

### Phase 3: Identify Blockers
From `docs/issues/dependencies.md`:
- Find open issues that block other open issues
- Calculate "blocking score" (number of dependents)
- Identify critical path

### Phase 4: Generate Recommendations
Based on analysis:
- Prioritize high-blocking issues
- Suggest parallel work streams
- Note quick wins (small, no blockers)

### Phase 5: Write Report
Create `docs/issues/milestones/[milestone-name]-status.md`

## Output Format

```markdown
# [Milestone Name] Status Report

**Generated:** YYYY-MM-DD
**Milestone Description:** [From GitHub milestone]

## Progress Summary

| Metric | Value |
|--------|-------|
| Total Issues | X |
| Closed | X |
| Open | X |
| Progress | X% |

## Progress Bar

▓▓▓▓▓▓▓▓░░░░░░░░░░░░ 40%

## Issues by Category

| Category | Open | Closed | Progress |
|----------|------|--------|----------|
| Team Features | X | X | X% |
| Gameplay | X | X | X% |
| CI/CD | X | X | X% |
| UI/UX | X | X | X% |

## Open Issues

| # | Title | Category | Blocking |
|---|-------|----------|----------|
| XX | Title | Cat | X issues |
| ... | ... | ... | ... |

## Recently Closed

Issues closed in the last 30 days:

| # | Title | Closed | Duration |
|---|-------|--------|----------|
| XX | Title | YYYY-MM-DD | X days |

## Blockers & Risks

### Critical Blockers
Issues blocking 3+ other issues:

1. **#XX [Title]** - Blocks X issues
   - Blocked by: [dependencies if any]
   - Status: [In progress / Not started]

### Risks
- [Risk 1]: [Description and mitigation]
- [Risk 2]: [Description and mitigation]

## Recommended Next Actions

### High Priority
1. **Complete #XX [Title]** - Unblocks X issues
2. **Start #XX [Title]** - On critical path

### Quick Wins
- #XX [Title] - No blockers, small complexity

### Parallel Work Streams
- **Stream A:** #XX, #XX, #XX (Team features)
- **Stream B:** #XX, #XX (Gameplay)

## Timeline Projection

Based on velocity of X issues/month:
- Estimated completion: [date range]
- Remaining effort: ~X issues

## Notes

- [Any relevant observations]
- [Changes since last report]
```

## Milestones to Track

- **Initial MLP** - Single-player offline functionality (Complete)
- **Team MLP** - Multi-user team features (In Progress)

## Output Location

- `docs/issues/milestones/initial-mlp-status.md`
- `docs/issues/milestones/team-mlp-status.md`

## Remember

- Include visual progress indicators
- Highlight actionable next steps
- Calculate blocking relationships
- Note risks and mitigations
- Keep reports scannable
