# Knowledge Pipeline Patterns

## Phase Details

### 1. INTAKE
**Trigger**: New YouTube video URL or repo to analyze
**Action**: Add entry to `references/INTAKE.md`
```markdown
| [Title](URL) | No | No | YYYY-MM-DD |
```

### 2. DOWNLOAD
**Trigger**: Entry with "Downloaded: No"
**For Videos**: `/yt-transcribe "VIDEO_URL"` → `references/transcript_VIDEOID.md`
**For Repos**: `git clone` → `repos/repo-name/`
**Update**: Set "Downloaded: Yes" in INTAKE.md

### 3. ANALYZE
**Trigger**: "Downloaded: Yes, Analyzed: No"
**Commands**:
- Videos: `transcript-analyzer` agent → `references/analysis_transcript_*.md`
- Repos: `repo-analyzer` agent → `references/analysis_repo_*.md`

### 4. VALIDATE (Analysis)
**Trigger**: Analysis document created
**Auto-Invokes**: `quality-gate` skill
**Checks**:
- Required sections present
- Evidence thresholds met (quotes ≥5, tags ≥3)
- References valid
**Update**: If passing, set "Analyzed: Yes" in INTAKE.md

### 5. SYNTHESIZE
**Trigger**: Multiple analyses ready for a use case
**Command**: `/batch-synthesize` or spawn `guide-synthesizer` agent
**Output**: `guides/use-cases/*/index.md`

### 6. VALIDATE (Synthesis)
**Trigger**: Guide created
**Checks**:
- Attribution accuracy (100% sourced)
- Agreement verification (claimed consensus is real)
- Coverage completeness (expected topics addressed)

### 7. ARCHIVE
**Trigger**: All validations pass
**Actions**:
- Update `references/SYNTHESIS.md` with results
- Update `guides/index.md` status
- Archive any plan files via `/complete`

## Workflow Shortcuts

**Process single video:**
```
1. Add to INTAKE.md
2. /yt-transcribe "URL"
3. Spawn transcript-analyzer
4. (quality-gate auto-validates)
5. Update INTAKE.md → Analyzed: Yes
```

**Process batch:**
```
1. Add all sources to INTAKE.md
2. /batch-analyze (processes all pending)
3. /batch-synthesize (creates guides)
4. /audit-pipeline (final check)
```
