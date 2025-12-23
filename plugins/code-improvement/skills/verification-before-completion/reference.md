# Reference: Verification Before Completion

## Why This Matters

From 24 failure memories:
- Your human partner said "I don't believe you" - trust broken
- Undefined functions shipped - would crash
- Missing requirements shipped - incomplete features
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## The Spirit of the Rule

**Violating the letter of this rule IS violating the spirit of this rule.**

This includes:
- Finding loopholes ("technically I said...")
- Rewording to avoid triggers
- Partial compliance
- Different phrasing with same meaning

## Full Example

**Wrong approach:**
```
I've fixed the bug by updating the regex. The tests should pass now.
```

**Correct approach:**
```
I've updated the regex. Let me run the tests to verify:

$ npm test
...
Tests: 34 passed, 34 total

All 34 tests pass. The fix is verified.
```

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
