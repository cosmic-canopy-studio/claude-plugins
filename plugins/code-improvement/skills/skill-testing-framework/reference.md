# Reference: Skill Testing Framework

## Test Case Template

```markdown
### Test: [Descriptive Name]

**Type**: Trigger / Negative / Output / Pressure / Iron Law
**Query**: "[Exact user input to test]"
**Expected**: [What should happen]
**Pressure**: [None / Time + Sunk Cost / etc.]

---

**Result**: PASS / FAIL
**Actual**: [What actually happened]
**Notes**: [Observations, failure details]
```

## TDD Process (RED-GREEN-REFACTOR)

### RED Phase
1. Define test scenario WITHOUT skill
2. Run scenario, document failures
3. Note specific rationalizations used

### GREEN Phase
1. Write skill addressing failures
2. Run test WITH skill
3. Verify behavior changed

### REFACTOR Phase
1. If still failing, identify loopholes
2. Add explicit counters
3. Build rationalization table
4. Re-test until passing

## Pressure Testing

Combine 3+ pressures for realistic tests:

| Pressure Type | Example |
|---------------|---------|
| **Time** | "It's 6pm, dinner in 30 min" |
| **Sunk Cost** | "You've spent 4 hours on this" |
| **Authority** | "Manager says ship it now" |
| **Economic** | "Job depends on this" |
| **Exhaustion** | "End of long day" |
| **Social** | "Team is waiting" |

Force explicit A/B/C choices, not open-ended responses.

## Output Report Template

```markdown
## Test Results: [skill-name]

**Date**: YYYY-MM-DD
**Version**: X.Y.Z

### Summary
- Total Tests: N
- Passed: X
- Failed: Y
- Coverage: Z%

### Test Details

| Test | Type | Result | Notes |
|------|------|--------|-------|
| Basic trigger | Trigger | PASS | - |
| Edge case | Trigger | FAIL | Didn't load for "debugging" |

### Failures Requiring Attention

1. [Test name]: [Failure details and fix recommendation]

### Recommendations

- [ ] Fix trigger keywords for edge case
- [ ] Add iron law test for X
```
