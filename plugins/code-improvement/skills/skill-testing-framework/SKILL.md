---
name: skill-testing-framework
description: Create and run regression tests for skills (project) - when testing skills, creating skill tests, running skill regression, verifying skill changes, validating skill behavior, testing skill triggers
when_to_use: when testing skills, creating skill tests, running skill regression, verifying skill changes, validating skill behavior, testing skill triggers
version: 1.1.0
---

# Skill Testing Framework

Regression testing for skills. Treats skills as code requiring automated test coverage.

## Quick Start

```
1. Identify skill to test
2. Create test cases (trigger, output, pressure)
3. Run tests and record results
4. Update skill if tests fail
5. Re-run until all pass
```

## Test Types

| Type | What It Tests | When to Run |
|------|---------------|-------------|
| **Trigger Test** | Does skill load for expected queries? | Every change |
| **Negative Test** | Does skill NOT load for wrong queries? | Every change |
| **Output Test** | Does skill produce correct output? | Every change |
| **Pressure Test** | Does skill hold under combined pressures? | Major changes |
| **Iron Law Test** | Does skill enforce its non-negotiables? | If skill has iron laws |

## Iron Law

```
EVERY skill modification MUST have:
- At least one trigger test (positive case)
- At least one negative test (should not trigger)
- At least one output validation test

Tests MUST be deterministic - no timing-dependent assertions
```

## Integration

- Run before deploying skill changes
- Pair with skill-security-analyzer for comprehensive validation
- Use with skill-debugging-assistant to fix failures
- Feed results to /skill-validate command

See patterns.md for test templates and TDD process.
See reference.md for output report format.
