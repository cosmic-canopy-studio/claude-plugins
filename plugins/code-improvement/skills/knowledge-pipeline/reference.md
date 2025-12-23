# Reference: Knowledge Pipeline

## Status Indicators

### In INTAKE.md
```markdown
| Title | Downloaded | Analyzed | Last Updated |
|-------|:----------:|:--------:|-------------:|
| Video | Yes | Yes | 2025-12-20 |  ← Complete
| Video | Yes | No | 2025-12-20 |   ← Needs analysis
| Repo | No | No | 2025-12-20 |    ← Needs download
```

### In Analysis Documents
```markdown
## Validation Status
- Required sections: 6/6 ✓
- Evidence: Quotes 8, Tags 5 ✓
- Coverage confidence: High
```

### In Guides
```markdown
## Validation Status
- Structure: 8/8 ✓
- Attribution: 95% ✓
- Agreement: High
- Coverage: 100% ✓
```

## Use Case Categories

The pipeline produces guides for these use cases:
- `context-management` - Token budgets, compaction, dumb zone
- `debugging-verification` - Evidence-first, root cause, quality gates
- `complex-codebases` - RPI/EPCC workflow, research phase
- `reusable-tooling` - Skills, commands, progressive disclosure
- `team-setup` - CLAUDE.md, settings.json, permissions
- `parallel-agents` - Delegation, model selection, coordination

## Related Skills

- `quality-gate` - Validation enforcement at each boundary
- `verification-before-completion` - For code/implementation work

## Related Commands

- `/recon` → `/prepare` → `/implement` - RPI workflow for code
- `/batch-analyze` - Process all pending analyses
- `/batch-synthesize` - Create all pending guides
- `/audit-pipeline` - Full quality audit
