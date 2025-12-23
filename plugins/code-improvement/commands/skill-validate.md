---
name: skill-validate
description: Validate skill comprehensively before deployment
---

# Skill Validate

Run comprehensive validation on a skill before deployment. Combines security analysis, performance profiling, and dependency mapping.

## Arguments

$ARGUMENTS should be:
- A skill name or path
- `all` to validate all skills in `.claude/skills/`

## Process

### Phase 1: Security Analysis

Use skill-security-analyzer to check:
- [ ] No unrestricted Bash access
- [ ] No embedded credentials
- [ ] No unauthorized network access
- [ ] No dangerous file system patterns
- [ ] No obfuscated code

### Phase 2: Performance Profiling

Use skill-performance-profiler to measure:
- [ ] SKILL.md word count (<300 target)
- [ ] Total token estimate (<500 ideal, <1000 max)
- [ ] Force-load references (0 target)
- [ ] File organization (appropriate for complexity)

### Phase 3: Trigger Validation

Use skill-testing-framework to verify:
- [ ] Keywords in description
- [ ] USE WHEN pattern present
- [ ] No conflicts with other skills
- [ ] Negative triggers defined

### Phase 4: Dependency Mapping

Check skill relationships:
- [ ] No circular dependencies
- [ ] Referenced files exist
- [ ] Integration points documented

## Output Report

```markdown
## Skill Validation Report: [skill-name]

### Scores
| Category | Score | Weight | Weighted |
|----------|-------|--------|----------|
| Security | 95/100 | 40% | 38.0 |
| Performance | 80/100 | 25% | 20.0 |
| Triggers | 90/100 | 25% | 22.5 |
| Dependencies | 100/100 | 10% | 10.0 |
| **Total** | | | **90.5** |

### Rating
| Score Range | Rating | Meaning |
|-------------|--------|---------|
| 90-100 | PRODUCTION | Deploy with confidence |
| 75-89 | REVIEW | Address noted issues |
| 60-74 | DRAFT | Significant work needed |
| <60 | BLOCKED | Critical issues found |

### Security Findings
| Severity | Issue | Location | Recommendation |
|----------|-------|----------|----------------|
| ... | ... | ... | ... |

### Performance Findings
| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| SKILL.md words | 245 | <300 | PASS |
| Total tokens | 890 | <1000 | WARN |
| Force-loads | 0 | 0 | PASS |

### Trigger Findings
| Test | Status | Details |
|------|--------|---------|
| ... | ... | ... |

### Dependency Findings
| Dependency | Status | Notes |
|------------|--------|-------|
| ... | ... | ... |

### Recommendations
1. [Priority 1 action]
2. [Priority 2 action]
3. [Priority 3 action]

### Deployment Status: [PRODUCTION/REVIEW/DRAFT/BLOCKED]
```

## Iron Law

```
NEVER approve PRODUCTION status with any CRITICAL security issues
ALWAYS run all 4 phases before issuing rating
NEVER skip security analysis for any reason
```
