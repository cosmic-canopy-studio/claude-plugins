---
name: knowledge-pipeline
description: Orchestrates the full analysis-to-synthesis workflow with quality gates (project) - when ingesting YouTube videos, analyzing repos, synthesizing guides, auditing content quality, or asking "what's next" in knowledge work
when_to_use: when ingesting YouTube videos, analyzing repos, synthesizing guides, auditing content quality, or asking "what's next" in knowledge work
version: 1.1.0
---

# Knowledge Pipeline

End-to-end workflow for transforming sources into validated guides.

## Pipeline Overview

```
INTAKE → ANALYZE → VALIDATE → EXTRACT DOMAINS → VALIDATE → SYNTHESIZE → VALIDATE → ARCHIVE
```

## Quick Commands

| Phase | Command | What It Does |
|-------|---------|--------------|
| Intake | Manual | Add to `references/INTAKE.md` |
| Download | `/yt-transcribe` | Get YouTube transcript |
| Analyze | `/batch-analyze` | Process all pending sources |
| Validate | (auto) | `quality-gate` skill triggers |
| Extract | `/batch-extract-domains` | Populate `knowledge/` from analyses |
| Validate | `/validate-domains` | Check domain document quality |
| Synthesize | `/batch-synthesize` | Create use-case guides from domains |
| Audit | `/audit-pipeline` | Full quality report |
| Archive | `/complete` | Clean up and document |

## What's Next?

When you ask "what should I do next?" in knowledge pipeline work:

1. **Check INTAKE.md** - Any sources pending download or analysis?
2. **Check analysis docs** - Any without validation status footer?
3. **Check domains** - Run `/validate-domains` to check domain coverage
4. **Check guides** - Any use cases needing synthesis from domains?
5. **Run audit** - `/audit-pipeline` for overall health

## Iron Law

```
Every phase boundary requires quality-gate validation
No proceeding without validation pass
```

## Context Budget Checkpoints

**⚠️ Pipeline work is context-heavy. Monitor usage at phase boundaries.**

### Phase Checkpoints

| After Phase | Check | If Exceeded |
|-------------|-------|-------------|
| ANALYZE (batch) | ~40% context | Compact before next batch |
| VALIDATE | N/A (quick) | Continue |
| EXTRACT | ~50% context | Start fresh session for synthesis |
| SYNTHESIZE | ~60% context | Complete one guide, then new session |

### Warning Signs

Watch for these during pipeline work:
- Analysis quality declining in later batches
- Repeated validation failures on same criteria
- Synthesis missing patterns you know exist

**If you notice degradation → Compact and continue in fresh session**

### Compaction at Phase Boundaries

When crossing a checkpoint with high context:

1. **Document current state**: Which sources analyzed, which pending
2. **Save working artifacts**: Ensure files are written, not just in context
3. **Fresh session prompt**: "Continue from [last completed phase], analyses archived at [location]"

### Context-Efficient Pipeline

For large batch work (10+ sources):
- Analyze 3-4 sources per session
- Write results immediately (don't batch in context)
- Use domain docs as compression layer (not raw analyses)
- Synthesize from domains, not analyses directly

See patterns.md for detailed phase workflows.
See reference.md for status indicators and workflow shortcuts.
