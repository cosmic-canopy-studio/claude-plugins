---
name: analyze-skill-gaps
description: Analyze conversation patterns to identify automation opportunities
---

# Analyze Skill Gaps

Identify opportunities for new skills, commands, or documentation based on conversation patterns.

## Arguments

$ARGUMENTS should be:
- `session` - Analyze current session only
- `recent` - Analyze recent sessions (if logs available)
- A specific pattern to look for (e.g., "test" to find testing-related gaps)

## Process

### Phase 1: Pattern Extraction

1. Scan conversation for repeated patterns:
   - Same explanations given 3+ times
   - Same corrections made 2+ times
   - Similar workflows executed 3+ times
   - Same questions asked 2+ times

2. Score each pattern:
   - User correction: +3 points
   - Repeated explanation: +2 points
   - Similar workflow: +1 point
   - Same question: +1 point

### Phase 2: Gap Classification

Categorize identified gaps:

| Category | Pattern Type | Recommended Action |
|----------|--------------|-------------------|
| Behavioral | "Always/never do X" | Skill with Iron Law |
| Informational | "Here's how X works" | Reference skill |
| Procedural | Multi-step workflow | Command |
| Contextual | Project-specific knowledge | CLAUDE.md entry |

### Phase 3: Prioritization

Rank gaps by impact:

1. **HIGH**: User corrections (costly mistakes)
2. **MEDIUM**: Repeated explanations (wasted context)
3. **LOW**: Similar workflows (convenience improvement)

## Output Report

```markdown
## Skill Gap Analysis Report

**Session**: Current / Recent
**Patterns Analyzed**: [N]
**Gaps Identified**: [M]

### Confirmed Gaps (HIGH Confidence)

#### Gap 1: [Name]
- **Pattern**: [What was repeated]
- **Frequency**: [N occurrences]
- **Category**: Behavioral / Informational / Procedural / Contextual
- **Confidence**: [X points]
- **Recommended Action**: Create [skill/command/CLAUDE.md entry]
- **Proposed Name**: [name]
- **Sample Content**:
  ```markdown
  [Draft skill/command/entry]
  ```

### Potential Gaps (MEDIUM Confidence)

| Pattern | Frequency | Category | Need More Data |
|---------|-----------|----------|----------------|
| ... | ... | ... | ... |

### Monitoring List (LOW Confidence)

These patterns may become gaps with more occurrences:
- [Pattern 1] (1 occurrence)
- [Pattern 2] (1 occurrence)

### Summary

| Priority | Gap | Action | Effort |
|----------|-----|--------|--------|
| 1 | [Gap A] | Create skill | Medium |
| 2 | [Gap B] | Add to CLAUDE.md | Low |
| 3 | [Gap C] | Create command | Medium |
```

## Iron Law

```
NEVER recommend a skill for patterns with <3 occurrences
ALWAYS prioritize user corrections over explanations
VERIFY pattern is generalizable, not task-specific
```

## Integration

After running this command:
1. Review identified gaps
2. Approve high-priority candidates
3. Use `/skill-test` to validate new skills
4. Use `/skill-validate` before deployment
