---
name: skill-test_nt
description: Run skill tests in background (non-terminal variant)
---

# Skill Test (Background)

Non-terminal variant of /skill-test. Runs skill tests and returns results without interactive output.

## Arguments

$ARGUMENTS should be:
- A skill name (e.g., `skill-debugging-assistant`)
- A path to a skill directory
- `all` to test all skills

## Process

Same as /skill-test but optimized for:
- Batch processing of multiple skills
- CI/CD pipeline integration
- Background execution in agent workflows

## Output Format

Returns structured JSON for programmatic consumption:

```json
{
  "skill": "skill-name",
  "status": "PASS|WARN|FAIL",
  "tests": {
    "trigger": {"passed": 4, "total": 5, "details": []},
    "negative": {"passed": 2, "total": 2, "details": []},
    "output": {"passed": 3, "total": 3, "details": []},
    "budget": {"passed": 2, "total": 3, "details": []}
  },
  "summary": {
    "total_passed": 11,
    "total_tests": 13,
    "coverage": 84.6
  }
}
```

## Iron Law

```
ALWAYS return valid JSON
NEVER include interactive prompts or formatting
```
