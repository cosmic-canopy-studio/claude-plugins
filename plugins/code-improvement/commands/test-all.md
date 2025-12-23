---
name: test-all
description: Run comprehensive tests on all Claude Code artifacts (skills, hooks, agents, commands)
---

# Artifact Testing

Run the unified test suite to validate all Claude Code artifacts.

## Arguments

- `(empty)` - Test all artifact types
- `skills` - Test only skills (22 total)
- `hooks` - Test only hooks (7 total)
- `agents` - Test only agents (9 total)
- `commands` - Test only commands (21 total)
- `--verbose` - Show all checks and issues

## Process

1. Run the test runner:
   ```bash
   python .claude/testing/test_runner.py $ARGUMENTS
   ```

2. Review the generated report showing:
   - Executive summary with overall score
   - Results by artifact type with individual scores
   - Critical issues requiring attention

3. Present findings to the user with actionable recommendations

## Rating Thresholds

| Score | Rating | Meaning |
|-------|--------|---------|
| 90-100 | PRODUCTION | Ready for use |
| 75-89 | REVIEW | Minor issues to address |
| 60-74 | DRAFT | Significant work needed |
| <60 | BLOCKED | Critical issues |

## Output Format

Markdown report with:
- Summary table (total artifacts, pass rate, average score)
- Per-type results with score and issue count
- Critical issues section for BLOCKED artifacts

## Example

```
# Artifact Test Results

## Summary
| Metric | Value |
|--------|-------|
| Total Artifacts | 59 |
| Passed | 52 |
| Average Score | 82.5 |

## Skills
| Name | Score | Rating | Issues |
|------|-------|--------|--------|
| token-budget-advisor | 95.0 | PRODUCTION | - |
| skill-security-analyzer | 88.5 | REVIEW | 1 issue |
```
