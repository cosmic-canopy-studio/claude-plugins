---
name: batch-extract-domains
description: Extract patterns from all analysis documents and consolidate into knowledge domain documents. Run after /batch-analyze or when initializing/updating the knowledge/ directory.
model: opus
---

# Batch Extract Domains

You are orchestrating domain extraction from analysis documents into the `knowledge/` directory.

## Process Overview

```
Survey Analyses → Extract per Domain → Validate → Report
```

## Step 1: Survey Analysis Documents

Read the current state:

1. List all `references/analysis_*.md` files
2. Check each for domain-relevant content:
   - Look for `@domain-name` tags (explicit)
   - Look for `#category` tags (legacy)
   - Check section headers for domain topics
3. Categorize patterns found by domain

```markdown
## Source Survey

| Source | CTX | WFL | AGT | SKL | DBG | TMS | CQA |
|--------|-----|-----|-----|-----|-----|-----|-----|
| analysis_dex_horthy.md | 4 | 3 | 2 | 0 | 1 | 0 | 0 |
| analysis_humanlayer_repo.md | 2 | 4 | 5 | 3 | 2 | 3 | 1 |
...
```

## Step 2: Extract for Each Domain

For each of the 7 domains, spawn a `domain-extractor` agent:

```
Use the Task tool with subagent_type: "domain-extractor"

Prompt: "Extract all patterns from references/analysis_*.md for the {domain} domain.

Domain: {domain-name}
Prefix: {prefix}
Key topics: {topic list}

Sources with relevant content:
- {list from survey}

Write to:
- knowledge/{domain}/domain.md (patterns)
- knowledge/{domain}/provenance.md (source tracking)

Follow the domain extraction protocol exactly."
```

**Domains to process**:
1. context-management (CTX) - dumb zone, progressive disclosure, compaction
2. workflow-patterns (WFL) - RPI, EPCC, phased development
3. agent-architecture (AGT) - subagent design, tool limits, delegation
4. skills-design (SKL) - triggers, meta skills, progressive loading
5. debugging-verification (DBG) - quality gates, root cause, proof-first
6. team-setup (TMS) - CLAUDE.md, settings, permissions
7. code-quality (CQA) - types, testing, entropy

## Step 3: Validate Extraction

After all extractions complete:

1. Invoke the `validate-domains` skill
2. Check each domain's score
3. Flag domains needing remediation

## Step 4: Report Results

```markdown
## Domain Extraction Complete

### Extraction Summary
| Domain | Patterns | Sources | Score | Status |
|--------|----------|---------|-------|--------|
| context-management | 8 | 6 | 92 | ✓ Production |
| workflow-patterns | 6 | 5 | 88 | ✓ Production |
| agent-architecture | 7 | 5 | 85 | ✓ Production |
| skills-design | 9 | 7 | 90 | ✓ Production |
| debugging-verification | 5 | 4 | 78 | ⚠ Review |
| team-setup | 4 | 3 | 65 | ⚠ Draft |
| code-quality | 3 | 3 | 58 | ⚠ Draft |

### Issues Requiring Review
1. [debugging-verification] Pattern DBG-003 missing provenance
2. [team-setup] Below minimum pattern threshold (4 < 5)
3. [code-quality] Below minimum pattern threshold (3 < 5)

### Cross-Domain Links Created
- CTX-001 → WFL-003 (compaction in workflow)
- AGT-002 → CTX-005 (subagent isolation)
- SKL-004 → CTX-002 (progressive disclosure)

### Next Steps
1. Review flagged domains for additional sources
2. Run `/validate-domains` for full audit
3. Run `/batch-synthesize` to update guides from domains

### Knowledge Pipeline Status
- ANALYZE: Complete (17 sources)
- EXTRACT DOMAINS: Complete
- Ready for: SYNTHESIZE phase
```

## Seeding from CROSS_ANALYSIS.md

For initial extraction, use `references/CROSS_ANALYSIS.md` as a guide:
- It contains 25+ patterns already categorized
- Use as extraction seed with source references
- Verify against original analysis documents

## Quality Gates

Before reporting success:
- [ ] All 7 domains have domain.md files
- [ ] Each domain has at least 3 patterns (warn if < 5)
- [ ] All patterns have provenance entries
- [ ] Cross-domain links validated
- [ ] Frontmatter updated with counts and dates

## Error Handling

If extraction fails for a domain:
1. Log the error
2. Continue with other domains
3. Report partial success with failed domains listed
4. Suggest remediation steps
