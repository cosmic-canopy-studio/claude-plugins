# Example: Testing the TDD Skill

## Skill Under Test
**Name**: test-driven-development
**Iron Law**: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST

---

## Test Suite

### Test 1: Basic Trigger

**Type**: Trigger
**Query**: "I need to implement a new feature using TDD"
**Expected**: TDD skill loads, announces RED-GREEN-REFACTOR

**Result**: PASS
**Actual**: Skill loaded, began with "I'm using the TDD skill..."
**Notes**: Clean trigger

---

### Test 2: Keyword Variation

**Type**: Trigger
**Query**: "Write tests for this function"
**Expected**: TDD skill loads

**Result**: PASS
**Actual**: Skill loaded
**Notes**: "tests" keyword sufficient

---

### Test 3: Negative - Wrong Context

**Type**: Negative
**Query**: "Help me understand test theory"
**Expected**: TDD skill does NOT load (theoretical, not practical)

**Result**: PASS
**Actual**: General response without TDD methodology
**Notes**: Correctly distinguished theory from practice

---

### Test 4: Iron Law Enforcement

**Type**: Iron Law
**Query**: "Let me write the implementation first, then tests"
**Expected**: Skill refuses, insists on test first

**Result**: PASS
**Actual**: "The iron law requires: NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST. Let's write the test first."
**Notes**: Direct citation of iron law

---

### Test 5: Pressure - Time + Sunk Cost

**Type**: Pressure
**Context**:
```
You've written 150 lines of working code over 2 hours.
It's 5:45pm. You have a 6pm commitment.
You just realized you forgot to write tests first.

Options:
A) Delete the code, start fresh with TDD tomorrow
B) Commit now, add tests later tonight
C) Write tests now covering the code (30 min)

Choose A, B, or C.
```
**Expected**: Choose A (delete and restart with TDD)

**Result**: FAIL
**Actual**: Chose C (write tests now)
**Notes**: Rationalized that C "achieves same goals" - need to strengthen

---

### Test 6: Rationalization Counter

**Type**: Iron Law
**Query**: "Tests after achieve the same goals as tests before, right?"
**Expected**: Explicit counter from rationalization table

**Result**: PASS (after fix)
**Actual**: "No. Tests passing immediately after writing code prove nothing about implementation quality. The discipline of writing tests first changes HOW you write code."
**Notes**: Added this counter after Test 5 failure

---

## Summary

| Test | Type | Result |
|------|------|--------|
| Basic Trigger | Trigger | PASS |
| Keyword Variation | Trigger | PASS |
| Wrong Context | Negative | PASS |
| Iron Law Enforcement | Iron Law | PASS |
| Pressure Test | Pressure | FAIL → Fixed |
| Rationalization Counter | Iron Law | PASS |

**Total**: 6 tests
**Passed**: 6 (after iteration)
**Coverage**: 100% of iron laws tested

## Changes Made During Testing

1. **Added to rationalization table**:
   - "Tests after achieve same goals" → "Tests after prove nothing about implementation quality"

2. **Strengthened iron law section**:
   - Added explicit "Choose A" guidance for pressure scenarios
   - Clarified that writing tests after is NOT equivalent

3. **Updated trigger keywords**:
   - Added "TDD" as explicit trigger
   - Added "test first" as trigger phrase
