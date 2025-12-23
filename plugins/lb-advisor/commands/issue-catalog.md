# Sync and analyze GitHub issues to local catalog

Fetches all issues from lacrosse-bosse and syncs them to the local `docs/issues/` catalog.

## Usage

/issue-catalog [--sync] [--analyze] [--category <name>]

## Options

- `--sync`: Create/update local issue files from GitHub (default: report only)
- `--analyze`: Run deep analysis on issues with incomplete criteria
- `--category`: Filter to specific category (gameplay, ci-cd, team-features, ui-ux, platforms, audio-visual, design, technical)

## Workflow

### Phase 1: Fetch GitHub Data

```bash
cd repos/lacrosse-bosse && gh issue list --state all --json number,title,body,labels,state,createdAt,closedAt,milestone,author --limit 200
```

### Phase 2: Sync to Local Catalog (if --sync)

For each GitHub issue:

1. **Determine category** from labels/content:
   | Label/Content Pattern | Category |
   |----------------------|----------|
   | Field, play, practice, objective | gameplay |
   | GitHub Actions, CI, build, pipeline | ci-cd |
   | Auth, subscription, team, coach | team-features |
   | Menu, button, UI, indicator | ui-ux |
   | iOS, Android, mobile, export | platforms |
   | Audio, sound, VFX, splash | audio-visual |
   | Figma, design, roster | design |
   | Refactor, bug, logging, technical | technical |

2. **Check if local file exists**: `docs/issues/<category>/<number>-<slug>.md`

3. **If missing, create from template**:
   ```markdown
   # <Title>

   | Field | Value |
   |-------|-------|
   | **Number** | #<number> |
   | **State** | <Open/Closed> |
   | **Milestone** | <milestone or N/A> |
   | **Labels** | <labels> |
   | **Created** | <date> |
   | **Closed** | <date or N/A> |
   | **URL** | <url> |

   ## User Story

   <Extracted from body or placeholder>

   ## Acceptance Criteria

   <Extracted from body>

   ## Technical Notes

   <Empty - for local notes>

   ## Related Issues

   <Extracted references>
   ```

4. **If exists, update metadata only** (preserve Technical Notes)

5. **Detect orphans**: Local files with no matching GitHub issue

### Phase 3: Validate Acceptance Criteria

Scan for issues with incomplete criteria:

| Pattern | Status |
|---------|--------|
| `**Given** [initial state]` | ⚠️ Placeholder |
| `**Given** \[.*\] **When**` | ⚠️ Incomplete brackets |
| No "Acceptance Criteria" section | ⚠️ Missing |
| All criteria have `- [ ]` only | ⚠️ No content |

### Phase 4: Build Dependency Graph

Extract issue references from bodies:
- `#<number>` pattern
- "depends on", "blocked by", "after" keywords
- "deferred from", "split from" keywords

Build adjacency list and detect:
- Circular dependencies
- Orphan issues (no connections)
- Blocked chains (open issue depends on open issue)

### Phase 5: Generate Report

Update `docs/issues/README.md` with:
- Updated counts and milestone progress
- Category tables with current state
- Dependency tree visualization
- Warnings section for incomplete criteria
- Last updated timestamp

## Output Files

| File | Purpose |
|------|---------|
| `docs/issues/README.md` | Main catalog (regenerated) |
| `docs/issues/<category>/*.md` | Individual issue files |
| `docs/issues/dependencies.md` | Dependency graph |
| `docs/issues/tech-debt.md` | Technical debt tracking |

## Examples

```bash
# Report current state (no changes)
/issue-catalog

# Sync from GitHub and update local files
/issue-catalog --sync

# Analyze specific category
/issue-catalog --category gameplay

# Full sync with deep analysis
/issue-catalog --sync --analyze
```

## Integration

This command works with:
- `issue-analyzer` agent: For deep analysis of individual issues
- `issue-analyze` skill: Auto-triggers analysis workflow
- `/pr-review` command: Links PR changes to issues

---

## Execution

When invoked, perform these steps:

### Basic Mode (no flags)
1. Navigate to lacrosse-bosse repo
2. Fetch all issues via `gh issue list`
3. Compare with local `docs/issues/` files
4. Report differences
5. Validate acceptance criteria
6. Generate dependency analysis
7. List warnings and recommendations

### With --sync Flag
1. All basic mode steps
2. Create missing issue files from template
3. Update metadata in existing files
4. Regenerate `docs/issues/README.md`

### With --analyze Flag
1. All basic mode steps
2. Identify issues needing analysis:
   - Placeholder criteria (`**Given** [initial state]`)
   - Missing criteria section
3. Group issues into batches of 3
4. For each batch, launch parallel `issue-analyzer` agents:
   ```
   Task(subagent_type="issue-analyzer", prompt="Analyze issue #XX...")
   ```
5. Wait for batch completion before starting next
6. Collect all analysis files
7. Update `docs/recommendations/issue-catalog.md` with summary
8. Report completion:
   - Issues analyzed
   - Complexity breakdown
   - Key recommendations

### Progress Reporting

For batch analysis, report:
```
Analyzing batch 1/6: #54, #55, #56
  ✓ #54 - Mobile Build Pipelines (Small)
  ✓ #55 - iOS/Testflight Release (Large)
  ✓ #56 - Android Play Console (Medium)

Analyzing batch 2/6: #60, #62, #63
  ...
```
