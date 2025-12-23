# Systematic Debugging Patterns

## Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

### 1.1 Read Error Messages Carefully
- Don't skip past errors or warnings
- Read stack traces completely
- Note line numbers, file paths, error codes

### 1.2 Reproduce Consistently
- Can you trigger it reliably?
- What are the exact steps?
- If not reproducible → gather more data, don't guess

### 1.3 Check Recent Changes
- Git diff, recent commits
- New dependencies, config changes
- Environmental differences

### 1.4 Multi-Component Diagnostics

**WHEN system has multiple components:**

Add diagnostic instrumentation BEFORE proposing fixes:
```
For EACH component boundary:
  - Log what data enters/exits component
  - Verify environment/config propagation
  - Check state at each layer

Run once to gather evidence
THEN analyze WHERE it breaks
```

### 1.5 Trace Data Flow

**WHEN error is deep in call stack:**
- Where does bad value originate?
- What called this with bad value?
- Keep tracing up until you find the source
- Fix at source, not at symptom

---

## Phase 2: Pattern Analysis

**Find the pattern before fixing:**

### 2.1 Find Working Examples
- Locate similar working code in same codebase
- What works that's similar to what's broken?

### 2.2 Compare Against References
- If implementing pattern, read reference implementation COMPLETELY
- Don't skim - understand the pattern fully

### 2.3 Identify Differences
- What's different between working and broken?
- List every difference, however small
- Don't assume "that can't matter"

### 2.4 Understand Dependencies
- What other components does this need?
- What settings, config, environment?

---

## Phase 3: Hypothesis and Testing

**Scientific method:**

### 3.1 Form Single Hypothesis
- State clearly: "I think X is the root cause because Y"
- Write it down
- Be specific, not vague

### 3.2 Test Minimally
- Make the SMALLEST possible change
- One variable at a time
- Don't fix multiple things at once

### 3.3 Verify Before Continuing
- Worked? → Phase 4
- Didn't work? → Form NEW hypothesis (don't add more fixes)

### 3.4 When You Don't Know
- Say "I don't understand X"
- Don't pretend to know
- Research more

---

## Phase 4: Implementation

**Fix the root cause, not the symptom:**

### 4.1 Create Failing Test Case
- Simplest possible reproduction
- Automated test if possible
- MUST have before fixing

### 4.2 Implement Single Fix
- Address the root cause identified
- ONE change at a time
- No "while I'm here" improvements

### 4.3 Verify Fix
- Test passes now?
- No other tests broken?
- Issue actually resolved?

### 4.4 If 3+ Fixes Failed

**Pattern indicating architectural problem:**
- Each fix reveals new problem in different place
- Fixes require "massive refactoring"
- Fixes create new symptoms elsewhere

**STOP and question fundamentals:**
- Is this pattern fundamentally sound?
- Should we refactor architecture vs. continue fixing symptoms?
- Discuss with your human partner before attempting more fixes
