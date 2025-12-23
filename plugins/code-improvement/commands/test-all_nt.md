---
name: test-all_nt
description: Run artifact tests in background with JSON output for CI integration
---

# Non-Terminal Artifact Testing

Run tests without terminal interaction, outputting JSON for programmatic use.

## Arguments

- `(empty)` - Test all artifact types
- `skills|hooks|agents|commands` - Test specific type

## Process

1. Run test runner with JSON output in background:
   ```bash
   python .claude/testing/test_runner.py --json $ARGUMENTS
   ```

2. Results are saved to:
   - `.claude/data/test_results/latest.json` - Most recent run
   - `.claude/data/test_results/history.jsonl` - Append-only trend data

3. Exit code indicates status:
   - `0` - All artifacts passed (PRODUCTION or REVIEW rating)
   - `1` - One or more artifacts BLOCKED

## JSON Output Format

```json
{
  "timestamp": "2025-12-21T12:00:00",
  "results": {
    "skills": [
      {
        "name": "token-budget-advisor",
        "score": 95.0,
        "rating": "PRODUCTION",
        "dimensions": {
          "structure": 100,
          "triggers": 90,
          "security": 100,
          "performance": 85,
          "dependencies": 100
        },
        "issues": []
      }
    ],
    "hooks": [...],
    "agents": [...],
    "commands": [...]
  }
}
```

## CI Integration

Use in pre-commit or CI pipeline:
```bash
python .claude/testing/test_runner.py --json --type skills || exit 1
```
