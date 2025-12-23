---
name: skill-test
description: Run skill tests to verify triggers and outputs
---

# Skill Test

Run regression tests on skills to verify they trigger correctly and produce expected outputs.

## Arguments

$ARGUMENTS should be:
- A skill name (e.g., `skill-debugging-assistant`)
- A path to a skill directory (e.g., `.claude/skills/my-skill/`)
- `all` to test all skills in `.claude/skills/`

## Process

1. **Locate Skill(s)**
   - Find skill(s) matching the argument
   - Verify SKILL.md exists and has valid YAML frontmatter

2. **Run Trigger Tests**
   - Extract `when_to_use` keywords from metadata
   - Verify description contains trigger keywords in first paragraph
   - Check for "USE WHEN" pattern in description
   - Score: % of keywords present in description

3. **Run Negative Trigger Tests**
   - Check for explicit exclusions ("Don't use for...")
   - Verify no keyword overlap with other skills in project
   - Flag potential conflicts

4. **Run Output Tests**
   - Verify Iron Law section exists (if applicable)
   - Check for Quick Start section
   - Verify patterns.md and reference.md exist if skill is >300 words

5. **Run Token Budget Tests**
   - Count words in SKILL.md (target: <300 words)
   - Check for @ force-load syntax (should be 0)
   - Estimate total token load

## Output Report

```markdown
## Skill Test Report: [skill-name]

### Trigger Tests
| Test | Status | Details |
|------|--------|---------|
| Keywords in description | PASS/FAIL | 4/5 keywords found |
| USE WHEN pattern | PASS/FAIL | Found at line 3 |
| First paragraph triggers | PASS/FAIL | 80% trigger density |

### Negative Trigger Tests
| Test | Status | Details |
|------|--------|---------|
| Explicit exclusions | PASS/WARN | No exclusions defined |
| Skill conflicts | PASS/FAIL | Overlaps with skill-X |

### Output Structure Tests
| Test | Status | Details |
|------|--------|---------|
| Iron Law section | PASS/FAIL | Present |
| Quick Start section | PASS/FAIL | Present |
| Progressive disclosure | PASS/FAIL | Reference files exist |

### Token Budget Tests
| Test | Status | Details |
|------|--------|---------|
| SKILL.md word count | PASS/WARN/FAIL | 245 words (target <300) |
| Force-load syntax | PASS/FAIL | 0 @ references |
| Total estimated tokens | INFO | ~327 tokens |

### Summary
- Tests passed: X/Y
- Coverage: Z%
- Status: PASS/WARN/FAIL
```

## Iron Law

```
NEVER report PASS without actually running the checks
ALWAYS report specific line numbers and counts
```
