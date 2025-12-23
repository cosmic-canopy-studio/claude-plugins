---
name: batch-synthesize
description: Synthesize analysis documents into consolidated use-case guides with quality-gate validation.
model: opus
---

# Batch Synthesize Guides

You are orchestrating the synthesis of analysis documents into consolidated use-case guides.

## Process

### 1. Gather Analysis Documents

Read all analysis documents:
- `references/analysis_*.md` - all analysis files
- `references/SYNTHESIS.md` - existing synthesis for context

Create an inventory:
```
## Analysis Documents Found

### Transcript Analyses
- analysis_transcript_abc.md - [Key topics]
- analysis_transcript_def.md - [Key topics]

### Repo Analyses
- analysis_repo_name.md - [Key topics]
- analysis_humanlayer_repo.md - [Key topics]

### Existing Syntheses
- SYNTHESIS.md - [Coverage]

Total: X analysis documents
```

### 2. Categorize by Use Case

Scan each analysis document and categorize insights by use case:

**Use Case Categories:**
- `complex-codebases` - RPI workflow, research agents, codebase exploration
- `reusable-tooling` - Skills, commands, agents design patterns
- `context-management` - Smart zone, compaction, progressive disclosure
- `debugging-verification` - Verification, quality gates, systematic debugging
- `team-setup` - CLAUDE.md, shared commands, project conventions
- `parallel-agents` - Delegation patterns, model selection, coordination

Display coverage:
```
## Use Case Coverage

| Use Case | Sources | Insights |
|----------|---------|----------|
| complex-codebases | 5 | ~12 |
| reusable-tooling | 8 | ~20 |
| context-management | 4 | ~8 |
| debugging-verification | 3 | ~6 |
| team-setup | 4 | ~10 |
| parallel-agents | 3 | ~5 |
```

### 3. Confirm Synthesis Plan

Use `AskUserQuestion` to confirm:
- Which use cases to synthesize?
- Any priority ordering?
- Minimum insight threshold? (default: 3+ insights)

### 4. Create Guide Structure

First, ensure the guide directory structure exists:

```
guides/
├── index.md
└── use-cases/
    ├── complex-codebases/
    ├── reusable-tooling/
    ├── context-management/
    ├── debugging-verification/
    ├── team-setup/
    └── parallel-agents/
```

### 5. Synthesize Guides

For each use case with sufficient insights, spawn a `guide-synthesizer` agent:

```
Use the Task tool with subagent_type: "guide-synthesizer"

Prompt: "Synthesize a guide for the '[use-case]' use case.

Read these analysis documents:
- references/analysis_transcript_abc.md
- references/analysis_repo_xyz.md
- [list all relevant sources]

Extract all insights tagged with '[use-case]' and related patterns.

Output the guide to: guides/use-cases/[use-case]/index.md

Follow the guide-synthesizer output format exactly."
```

Process sequentially (synthesis requires careful consolidation).

### 6. Validate Each Guide (MANDATORY)

**⚠️ DO NOT claim synthesis complete until validation passes.**

After each guide is written, validate it:

1. **Check Structure** - All 8 required sections present?
   - Quick Answer, Problem/Signs, Solution, Principles, Steps, Templates, Mistakes, Sources

2. **Check Attribution** - Sample 5 major claims:
   - Find cited source in `references/analysis_*.md`
   - Verify claim accurately represents source
   - Flag any misrepresentations

3. **Check Agreement** - For "best practice" claims:
   - Verify 3+ sources support the claim (or mark as single-source)
   - Flag any false agreement claims

4. **Check Coverage** - Match against expected topics:
   - context-management: dumb zone, compaction, progressive disclosure, subagent isolation
   - debugging-verification: evidence-first, root cause, quality gates
   - complex-codebases: RPI/EPCC workflow, research phase, planning
   - reusable-tooling: skills structure, progressive disclosure, trigger words
   - team-setup: CLAUDE.md patterns, settings.json, permissions
   - parallel-agents: delegation patterns, model selection, coordination

**If validation PASSES:**
- Score ≥70%: Include in index
- Score ≥85%: Mark as "production-ready"

**If validation FAILS:**
- DO NOT include in main index
- Log specific issues with line numbers
- Include in "Needs Remediation" section

### 7. Create Main Index

After all guides are created, create or update `guides/index.md`:

```markdown
# Claude Code Best Practices

> Consolidated insights from [N] sources

## What Are You Trying To Do?

### I need to tackle a complex feature
→ [Working with Complex Codebases](./use-cases/complex-codebases/)

### I want to create reusable automation
→ [Creating Reusable Tooling](./use-cases/reusable-tooling/)

### My conversations are getting confused
→ [Context Management](./use-cases/context-management/)

[Continue for each use case...]

## Sources

This guide synthesizes insights from:
- [N] YouTube transcripts
- [M] reference repositories
- Official Claude Code documentation

See [Source Index](./reference/source-index.md) for full list.

**Last Generated**: [Date]
```

### 7. Update SYNTHESIS.md

Add links to new guides in `references/SYNTHESIS.md`:

```markdown
## Generated Guides

- [Complex Codebases Guide](../guides/use-cases/complex-codebases/)
- [Reusable Tooling Guide](../guides/use-cases/reusable-tooling/)
[etc.]
```

### 9. Report Results

```
## Synthesis Complete

### Guides Validated and Created
- [✓] complex-codebases/index.md (Score: 88, 12 patterns from 5 sources)
- [✓] reusable-tooling/index.md (Score: 92, 20 patterns from 8 sources)
- [✓] context-management/index.md (Score: 85, 8 patterns from 4 sources)

### Failed Validation (Needs Remediation)
- [✗] debugging-verification/index.md → Missing 2 sections, 1 false agreement
- [✗] parallel-agents/index.md → Coverage only 50% (needs: coordination topic)

### Validation Summary
| Guide | Structure | Attribution | Agreement | Coverage | Score |
|-------|-----------|-------------|-----------|----------|-------|
| complex-codebases | 8/8 | 100% | ✓ | 100% | 88 |
| reusable-tooling | 8/8 | 95% | ✓ | 100% | 92 |
| context-management | 8/8 | 100% | ✓ | 100% | 85 |

### Index Updated
- guides/index.md (only validated guides included)
- references/SYNTHESIS.md

### Summary
- Guides attempted: X
- Passed validation: Y
- Failed validation: Z
- Average score: [N]/100

### Next Steps
1. Fix failed guides (see remediation issues above)
2. Re-run synthesis for failed use cases
3. Run `/audit-pipeline` for full quality assessment
```

## Error Handling

**If synthesis fails for a use case:**
- Log the error with details
- Continue with remaining use cases
- Report failures at the end
- Suggest manual synthesis for failed cases

**If insufficient insights:**
- Skip use case (don't create empty guide)
- Note in report which use cases need more sources

## Guidelines

- **Quality over quantity** - Better to have fewer, richer guides
- **Preserve attribution** - Every pattern must cite its source
- **Handle conflicts** - Document when sources disagree
- **Cross-reference** - Link related guides to each other
- **Be complete** - Include all relevant patterns, don't cherry-pick
