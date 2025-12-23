---
name: issue-analyze
description: Analyze GitHub issues to extract implicit requirements, identify technical challenges, suggest acceptance criteria, and assess complexity. Use when discussing issues, asking about requirements, or needing issue recommendations.
when_to_use:
  triggers:
    - "analyze issue"
    - "review issue"
    - "what does issue #"
    - "analyze #"
    - "issue needs"
    - "requirements for #"
    - "acceptance criteria for"
    - "run issue analyzer"
    - "analyze all issues"
    - "issues needing"
  symptoms:
    - "Issue mentioned by number"
    - "Discussing requirements or criteria"
    - "Asking about issue complexity"
    - "Need to understand an issue"
  context:
    - "Working with GitHub issues"
    - "Planning implementation"
    - "Reviewing incomplete issues"
  auto_invoke: always
version: 1.0.0
---

# Skill: Issue Analysis

Analyze GitHub issues from the lacrosse-bosse project to generate recommendations.

## Quick Reference

**Trigger:** User asks about issues, mentions issue numbers, or requests analysis
**Output:** Analysis files at `docs/recommendations/issues/XXX-title-analysis.md`
**Agent:** Uses `issue-analyzer` agent for deep analysis

## Modes

### Single Issue Mode

When user mentions a specific issue (e.g., "analyze issue #60"):

1. Read issue from `docs/issues/[category]/XXX-title.md`
2. Launch `issue-analyzer` agent with issue context
3. Generate analysis file
4. Report key findings

### Batch Mode

When user asks to analyze multiple issues (e.g., "analyze all issues needing criteria"):

1. Run `/issue-catalog` to identify issues needing analysis
2. Group issues into batches of 3
3. Launch parallel `issue-analyzer` agents per batch
4. Collect results and summarize

### Catalog Mode

When user runs `/issue-catalog --analyze`:

1. Identify issues with placeholder/missing criteria
2. Generate analysis for each
3. Update `docs/recommendations/issue-catalog.md`

## Process

### Step 1: Identify Target Issues

**Single issue:**
```
User: "analyze issue #60"
→ Target: #60
```

**Multiple issues:**
```
User: "analyze the CI/CD issues"
→ Targets: #54, #55, #56, #60, #62, #63
```

**All needing analysis:**
```
User: "analyze issues needing criteria"
→ Run issue-catalog, filter by placeholder/missing criteria
```

### Step 2: Gather Context

For each issue:
1. Read local issue file from `docs/issues/`
2. Optionally fetch fresh data from GitHub
3. Search lacrosse-bosse codebase for related files

### Step 3: Generate Analysis

Launch `issue-analyzer` agent(s) with:
- Issue content and context
- Related codebase findings
- Analysis template

### Step 4: Write Output

Create file at `docs/recommendations/issues/XXX-title-analysis.md`

Format:
```markdown
# Analysis: [Title] (#XX)

> Generated: YYYY-MM-DD
> Issue: docs/issues/[category]/XXX-title.md

## Summary
[2-3 sentences]

## Implicit Requirements
...

## Technical Challenges
...

## Suggested Acceptance Criteria
...

## Complexity Assessment
**Size:** Small/Medium/Large/XL
...

## Recommendations
...
```

### Step 5: Report Results

Summarize:
- Issues analyzed
- Complexity breakdown
- Key recommendations
- Any issues requiring follow-up

## Integration

- **Issue Catalog:** Provides list of issues needing analysis
- **PR Review:** Can analyze linked issues
- **Workflow Prepare:** Can inform implementation planning

## Guidelines

1. **Use local files first** - `docs/issues/` is source of truth
2. **Batch for efficiency** - Max 3 parallel agents
3. **Be specific** - Reference actual file paths
4. **Output locally** - Don't auto-post to GitHub
5. **Track progress** - Use TodoWrite for batch jobs
