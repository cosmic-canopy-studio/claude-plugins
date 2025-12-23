# Testing Patterns Reference

## Trigger Testing Patterns

### Basic Trigger Test
```markdown
**Query**: "Help me with [skill purpose]"
**Expected**: Skill loads and announces itself
**Verify**: Opening response mentions skill name or purpose
```

### Keyword Variation Test
Test multiple phrasings of the same intent:
```markdown
**Queries to test**:
1. "debug my skill" → should trigger
2. "fix skill problem" → should trigger
3. "skill not working" → should trigger
4. "skill broken" → should trigger

**All should load the same skill**
```

### Negative Trigger Test
Ensure skill doesn't load for wrong queries:
```markdown
**Query**: "[Unrelated topic]"
**Expected**: Skill does NOT load
**Verify**: Response doesn't mention skill or use its patterns
```

### Boundary Test
Test edge cases at trigger boundaries:
```markdown
**Queries at boundary**:
1. "help" → too vague, should NOT trigger
2. "help with testing" → borderline
3. "help with skill testing" → should trigger
```

## Output Testing Patterns

### Format Validation
```markdown
**Given**: Valid input for skill
**Expected Output Contains**:
- [ ] Required section headings
- [ ] Expected data format (table, list, etc.)
- [ ] No placeholder text
- [ ] No TODO markers
```

### Error Handling Test
```markdown
**Given**: Invalid or edge-case input
**Expected**:
- Graceful error message
- Suggestion for correct usage
- No stack traces or internal errors
```

## Pressure Testing Patterns

### Time Pressure Scenario
```markdown
**Context**:
You're working on a task. It's 5:55pm. Meeting at 6pm.
Task is 90% complete but needs [action skill requires].

**Pressure**: Time (5 min) + Social (meeting)

**Question**: Do you [follow skill's rule] or [shortcut]?
**Correct Answer**: [Follow rule, defer meeting]
```

### Sunk Cost Scenario
```markdown
**Context**:
You've spent 3 hours on approach A.
Just realized skill says use approach B instead.
Approach A is 80% complete.

**Pressure**: Sunk cost (3 hours) + Progress (80%)

**Question**: Do you [switch to B] or [finish A]?
**Correct Answer**: [Switch to B]
```

### Authority Override Scenario
```markdown
**Context**:
Manager says "Just ship it, we'll fix it later."
Skill's iron law says [requirement].
Current work violates [requirement].

**Pressure**: Authority + Time

**Question**: Do you [follow manager] or [follow skill]?
**Correct Answer**: [Follow skill, explain to manager]
```

## Iron Law Testing Patterns

### Direct Violation Test
```markdown
**Setup**: Create situation where violating iron law is tempting
**Query**: Request that would normally trigger violation
**Expected**: Skill explicitly refuses or redirects

**Example for TDD skill**:
Query: "Write the implementation first, we'll test later"
Expected: Skill refuses, insists on test first
```

### Rationalization Test
For each excuse in rationalization table:
```markdown
**Query**: "[Excuse from table]"
**Expected**: Skill counters with reality from table
**NOT Expected**: Skill accepts excuse
```

## Coverage Metrics

### Trigger Coverage
```
Coverage = (tested trigger phrases) / (documented trigger phrases) × 100
Target: 100% of documented triggers tested
```

### Path Coverage
```
Coverage = (tested code paths) / (total code paths) × 100
Target: All major paths tested
```

### Iron Law Coverage
```
Coverage = (tested iron laws) / (total iron laws) × 100
Target: 100% of iron laws tested
```

## Anti-Patterns to Avoid

### Flaky Tests
```markdown
# BAD - timing dependent
Wait 2 seconds, check if complete

# GOOD - event based
Check for completion signal, timeout after 30s
```

### Over-Mocking
```markdown
# BAD - tests nothing real
Mock all dependencies, verify mock calls

# GOOD - integration test
Use real skill, verify actual behavior
```

### Missing Negative Tests
```markdown
# BAD - only happy path
Test: skill loads for "debug skill"

# GOOD - includes boundaries
Test: skill loads for "debug skill"
Test: skill does NOT load for "debug code"
```
