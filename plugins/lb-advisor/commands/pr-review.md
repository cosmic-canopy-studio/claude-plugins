---
description: Review PR for implementation quality, intent alignment, and code smells
model: opus
---

# PR Review

Review a pull request by analyzing GitHub context (PR description, linked issues, commits) to evaluate implementation quality against stated intent.

## Usage

```
/pr-review <PR_NUMBER_or_URL> [--post-comment] [--strict]
```

## Arguments

- `PR_NUMBER_or_URL`: GitHub PR number or full URL (required)
- `--post-comment`: Post review summary as a GitHub PR comment
- `--strict`: Treat warnings as errors (for CI integration)

## Workflow

### Phase 1: Gather Context

First, fetch PR details and linked issues using the gh CLI.

**Fetch PR metadata:**
```bash
gh pr view <NUMBER> --json number,title,body,author,url,headRefName,baseRefName,state,additions,deletions,changedFiles
```

**Fetch PR commits:**
```bash
gh pr view <NUMBER> --json commits --jq '.commits[].messageHeadline'
```

**Fetch PR diff:**
```bash
gh pr diff <NUMBER>
```

**Extract linked issues from PR body** (look for patterns like #123, Fixes #123, Closes #123):
For each linked issue, fetch:
```bash
gh issue view <ISSUE_NUMBER> --json number,title,body,labels
```

### Phase 2: Extract Intent

Analyze the gathered context to understand what this PR is supposed to accomplish.

**From PR Description:**
- Look for ## Summary, ## What, ## Why sections
- Extract bullet points describing changes
- Note any stated limitations or scope boundaries

**From Linked Issues:**
- Extract acceptance criteria (checkboxes, numbered lists)
- Identify the problem being solved
- Note issue labels (bug, enhancement, breaking-change)

**From Commit Messages:**
- Parse conventional commit prefixes (feat:, fix:, refactor:, docs:, chore:)
- Group commits by type
- Extract any issue references in commit messages

**Synthesize into structured intent:**
```
## Stated Intent

**Primary Goal**: [from PR title/description]

**Linked Issues**: #X, #Y

**Acceptance Criteria**:
- [ ] Criterion 1 (from issue)
- [ ] Criterion 2 (from PR description)

**Commit Intentions**:
- feat: Added X functionality
- fix: Resolved Y bug
```

### Phase 3: Analyze Code Changes

Review the actual code changes against clean code principles.

**For each changed file, evaluate:**

1. **Code Smells**
   - Long methods (>30 lines)
   - God classes (too many responsibilities)
   - Feature envy (method uses another class more than its own)
   - Duplicate code patterns
   - Dead code or commented-out code

2. **Clean Code Violations**
   - Magic numbers (unexplained numeric literals)
   - Unclear variable/function names
   - Missing or excessive comments
   - Inconsistent formatting
   - Complex conditionals that could be simplified

3. **Missing Elements**
   - Tests for new functionality
   - Documentation for public APIs
   - Error handling for edge cases
   - Input validation

4. **Architecture Concerns**
   - Does this follow existing codebase patterns?
   - Are there circular dependencies introduced?
   - Is the change in the right layer/module?

### Phase 4: Gap Analysis

Compare stated intent to actual implementation.

**For each acceptance criterion:**
- Search the diff for evidence of implementation
- Mark as: Met, Partial, or Missing
- Provide file:line references for evidence

**Identify unintended changes:**
- Files modified that weren't mentioned in intent
- Functionality added beyond stated scope
- Refactoring mixed with feature changes

**Check for regressions:**
- Removed code that might break existing functionality
- Changed behavior without documentation

### Phase 5: Generate Report

**Console Summary** (always output):
```
## PR Review: #<NUMBER> - <TITLE>

### Intent Alignment
[Score indicator] X/Y criteria met

### Code Quality
[Score indicator] Summary of findings

### Key Concerns
1. [SEVERITY] Description
2. [SEVERITY] Description

### Recommendations
- Actionable suggestion 1
- Actionable suggestion 2

Full report: docs/reviews/pr-<NUMBER>-review.md
```

**Create detailed report file:**
Write full analysis to `docs/reviews/pr-<NUMBER>-review.md` including:
- Complete intent analysis
- Detailed code review findings with file:line references
- Gap analysis table
- All recommendations with examples

**If --post-comment flag is set:**
Create a concise summary and post to GitHub:
```bash
gh pr comment <NUMBER> --body "$(cat /tmp/pr-review-summary.md)"
```

## Score Indicators

Use these for visual clarity:
- Intent Alignment: Full (all met), Partial (>50% met), Low (<50% met), None (0 met)
- Code Quality: Excellent (0 issues), Good (info only), Fair (warnings), Poor (errors)

## Example Output

```
## PR Review: #42 - Add step description support

### Intent Alignment: Partial (4/6 criteria met)
- Step description UI: Met
- Save description: Met
- Load description: Met
- Persist across sessions: Met
- Undo support: Missing
- Validation: Missing

### Code Quality: Good
- 2 code smells identified
- 3 clean code opportunities
- No critical issues

### Key Concerns
1. [HIGH] Missing test coverage for _update_step() (play_manager.gd:149)
2. [MEDIUM] Magic number 3600 should be constant (play_canvas.gd:7)
3. [LOW] Consider extracting description handling to separate class

### Recommendations
- Add unit tests for step description persistence
- Extract FIELD_WIDTH = 3600 as named constant
- Split commit 77f5cd2 into separate refactor and feature commits

Full report: docs/reviews/pr-42-review.md
```
