---
name: batch-analyze
description: Batch analyze all pending YouTube transcripts and GitHub repos for Claude Code patterns with quality-gate validation.
model: opus
---

# Batch Analyze Sources

You are orchestrating batch analysis of reference materials to extract Claude Code best practices.

## Process

### 1. Survey Pending Sources

Read `references/INTAKE.md` to identify unanalyzed sources:

**Find YouTube transcripts where Analyzed = No:**
- Look for `transcript_*.md` files in `references/`
- Match against INTAKE.md status

**Find repos where Analyzed = No:**
- Look for directories in `repos/`
- Match against INTAKE.md status

Display a summary:
```
## Pending Analysis

### YouTube Transcripts (N)
- transcript_abc123.md - "Video Title"
- transcript_def456.md - "Video Title"

### Repositories (M)
- repos/repo-name/ - "Purpose"
- repos/other-repo/ - "Purpose"

Total: X sources to analyze
```

### 2. Confirm with User

Use `AskUserQuestion` to confirm:
- Process all sources?
- Skip any specific sources?
- Any priority ordering?

### 3. Parallel Analysis

**For YouTube transcripts:**
Spawn `transcript-analyzer` agents using the Task tool:

```
Use the Task tool with subagent_type: "transcript-analyzer"

Prompt: "Analyze the transcript at references/transcript_XYZ.md for Claude Code best practices.
Output your analysis to references/analysis_transcript_XYZ.md"
```

- Process up to 4 transcripts in parallel
- Wait for batch to complete before next batch

**For repositories:**
Spawn `repo-analyzer` agents:

```
Use the Task tool with subagent_type: "repo-analyzer"

Prompt: "Analyze the repository at repos/REPO_NAME/ for Claude Code patterns.
Output your analysis to references/analysis_repo_REPO_NAME.md"
```

- Process up to 2 repos in parallel (larger context)
- Wait for batch to complete before next batch

### 4. Validate Each Analysis (MANDATORY)

**⚠️ DO NOT mark as Analyzed until validation passes.**

After each analysis is written, validate it:

1. **Read the analysis document** completely
2. **Check for Validation Status section** at the end
   - If missing: FAIL - return to analyzer for completion
3. **Verify all checkmarks are ✓**
   - If any ✗: FAIL - document specific gaps
4. **Check evidence thresholds**:
   - Transcripts: 5+ quotes, 3+ tags, 50%+ timestamp coverage
   - Repos: 10+ file refs, 2+ templates, 3+ transferability ratings

**If validation PASSES:**
- Proceed to update INTAKE.md status
- Include score in results summary

**If validation FAILS:**
- DO NOT update INTAKE.md status
- Log the specific failure reason
- Include in "Needs Remediation" section of report
- Suggest re-running analyzer or manual fixes

### 5. Update Status (Only After Validation)

After EACH source passes validation:

Edit `references/INTAKE.md` to update:
- Change `No` to `Yes` in the Analyzed column
- Update `Last Updated` to today's date (YYYY-MM-DD format)

### 6. Report Results

After all sources processed, display:

```
## Batch Analysis Complete

### Passed Validation
- [✓] transcript_abc123.md → analysis_transcript_abc123.md (Score: 92)
- [✓] transcript_def456.md → analysis_transcript_def456.md (Score: 88)
- [✓] repos/repo-name/ → analysis_repo_repo-name.md (Score: 85)

### Failed Validation (Needs Remediation)
- [✗] transcript_xyz.md → Missing Validation Status section
- [✗] repos/other-repo/ → Only 7 file refs (needs 10+)

### Summary
- Sources attempted: X
- Passed validation: Y
- Failed validation: Z
- Average score: [N]/100

### Next Steps
1. Fix failed analyses (see remediation list above)
2. Re-run `/batch-analyze` for failed sources
3. Run `/batch-synthesize` to consolidate into use-case guides
```

## Error Handling

**If an agent fails:**
- Log the error
- Continue with remaining sources
- Report failures at the end
- Suggest manual analysis for failed sources

**If INTAKE.md update fails:**
- Continue processing
- Report status update failures
- Provide manual update instructions

## Guidelines

- **Don't skip sources** unless user explicitly requests
- **Process in batches** to manage context
- **Update status immediately** after each completion
- **Be verbose** about progress - user should see each step
- **Parallelize wisely** - transcripts are lighter than repos
