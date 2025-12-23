# Common Failure Patterns

## Trigger Failures

### Pattern: Vague Description
**Symptom**: Skill never loads for any query
**Cause**: Description uses abstract terms Claude doesn't match

```yaml
# BAD
description: Helps with development tasks

# GOOD
description: Debug skill trigger failures. USE WHEN skill not loading, skill broken, debugging skills.
```

**Fix**: Add concrete trigger keywords, use "USE WHEN" pattern

### Pattern: Buried Intent
**Symptom**: Skill loads inconsistently
**Cause**: Trigger conditions aren't in first paragraph

```markdown
# BAD - trigger buried
## Overview
This skill helps with various development workflows...

When to use: [trigger conditions here]

# GOOD - trigger first
USE WHEN you need to debug skills that won't load.
Takes: skill name and problem description.
Produces: diagnosis and fix recommendation.
```

**Fix**: Move trigger conditions to very first sentences

### Pattern: Abstract Symptoms
**Symptom**: Skill doesn't match user's actual phrasing
**Cause**: when_to_use uses abstract concepts

```yaml
# BAD
when_to_use: for testing purposes

# GOOD
when_to_use: when tests fail randomly, tests pass/fail inconsistently, debugging flaky tests
```

**Fix**: Use exact phrases users would type

## Output Failures

### Pattern: Incomplete Output
**Symptom**: Skill starts but doesn't complete workflow
**Cause**: Missing step definitions or unclear transitions

**Fix**: Add explicit step numbers, verification at each step

### Pattern: Wrong Format
**Symptom**: Output doesn't match expected structure
**Cause**: Template not in SKILL.md or too complex

**Fix**: Add explicit output template, simplify structure

## Context Failures

### Pattern: Token Overflow
**Symptom**: Skill loads but session degrades quickly
**Cause**: Skill content too large

```markdown
# Check sizes
SKILL.md: should be <300 words
patterns.md: should be <500 words per pattern
reference.md: unlimited (loaded on demand)
```

**Fix**: Move content to reference files, use progressive disclosure

### Pattern: Force-Load Abuse
**Symptom**: Too much context loaded immediately
**Cause**: Using @ syntax to force-load files

```markdown
# BAD
See @patterns.md for details

# GOOD
See patterns.md for details (loaded when needed)
```

**Fix**: Remove @ prefixes, let Claude load on demand

## Iron Law Failures

### Pattern: Rule Ignored Under Pressure
**Symptom**: Skill's iron law violated in complex scenarios
**Cause**: No rationalization table

**Fix**: Add Red Flags section with excuse → reality mapping

### Pattern: Loophole Exploitation
**Symptom**: Rule technically followed but spirit violated
**Cause**: Rule stated positively without explicit negations

```markdown
# BAD
Always write tests first.

# GOOD
Always write tests first.
No exceptions:
- Don't keep code "as reference"
- Don't "adapt" existing code
- Violating the letter IS violating the spirit
```

**Fix**: Add explicit "No exceptions" section

## Conflict Failures

### Pattern: Wrong Skill Loads
**Symptom**: Different skill activates for your query
**Cause**: Keyword overlap between skills

**Fix**:
1. Add negative triggers to SKILL.md ("Don't use for...")
2. Make trigger keywords more specific
3. Check for conflicting when_to_use fields

### Pattern: Multiple Skills Compete
**Symptom**: Skill selection seems random
**Cause**: Multiple skills have similar descriptions

**Fix**: Differentiate descriptions, add explicit scope limits

## Platform Failures

### Pattern: Works in Claude Code, Not Web
**Symptom**: Skill works locally but not when uploaded
**Cause**: Path differences or packaging issues

**Fix**:
1. Check file structure matches expected format
2. Zip correctly (skill folder, not parent)
3. Verify YAML valid after extraction

### Pattern: 20-Skill Limit Hit
**Symptom**: Can't upload new skill
**Cause**: Web/desktop limit of 20 skills

**Fix**: Remove low-value skills, consolidate related skills
