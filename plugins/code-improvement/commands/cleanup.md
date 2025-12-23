---
name: cleanup
description: Archive completed plans and organize project documentation
---

# Clean up project documentation

Archives completed plans and consolidates scattered documentation.

## Usage

/cleanup [--execute] [--dry-run]

## Options

- `--execute`: Perform cleanup (default shows preview and asks for confirmation)
- `--dry-run`: Show preview without making changes

## What it does

1. **Analyzes** project structure to identify:
   - Completed plans (those moved to archive/)
   - Scattered documentation files
   - Files ready for archival

2. **Archives** completed work to `docs/plans/archive/` directory:
   - Already archived plans stay in place
   - Plans older than 30 days move to archive

3. **Consolidates** scattered documentation:
   - `plan/` → `docs/plans/` (if exists)
   - `implementation/` → `docs/plans/` (if exists)

4. **Updates** cross-references in moved files

## Process Flow

1. Runs analyzer to classify files
2. Shows preview of changes
3. Asks for confirmation (unless --dry-run)
4. Executes changes (if confirmed)
5. Updates references
6. Reports results

## Safety Features

- Always runs in preview mode by default
- Requires explicit --execute flag to make changes
- Preserves all active work and drafts
- Creates archive directory mirroring original structure

## Output Format

```markdown
## Cleanup Report

### Files Analyzed
- Plans: [N] (completed: [N], active: [N])
- Documentation: [N] files scanned

### Actions Taken
- Archived: [list of archived files]
- Consolidated: [list of moved files]
- References updated: [N] files

### Summary
[Brief description of cleanup results]
```

---

cd /home/sam/code/code_improvement && python tools/cleanup.py $*