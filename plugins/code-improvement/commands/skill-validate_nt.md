---
name: skill-validate_nt
description: Validate skill comprehensively (non-terminal variant)
---

# Skill Validate (Background)

Non-terminal variant of /skill-validate for batch processing and CI/CD integration.

## Arguments

$ARGUMENTS should be:
- A skill name or path
- `all` to validate all skills

## Output Format

Returns structured JSON:

```json
{
  "skill": "skill-name",
  "rating": "PRODUCTION|REVIEW|DRAFT|BLOCKED",
  "total_score": 90.5,
  "scores": {
    "security": {"score": 95, "weight": 0.40, "weighted": 38.0},
    "performance": {"score": 80, "weight": 0.25, "weighted": 20.0},
    "triggers": {"score": 90, "weight": 0.25, "weighted": 22.5},
    "dependencies": {"score": 100, "weight": 0.10, "weighted": 10.0}
  },
  "issues": {
    "critical": [],
    "high": [],
    "medium": [],
    "low": []
  },
  "recommendations": []
}
```

## Batch Output

When validating multiple skills:

```json
{
  "summary": {
    "total": 7,
    "production": 3,
    "review": 2,
    "draft": 1,
    "blocked": 1
  },
  "skills": [
    {"name": "skill-a", "rating": "PRODUCTION", "score": 92.0},
    {"name": "skill-b", "rating": "REVIEW", "score": 78.5}
  ]
}
```

## Iron Law

```
ALWAYS return valid JSON
NEVER include interactive elements
```
