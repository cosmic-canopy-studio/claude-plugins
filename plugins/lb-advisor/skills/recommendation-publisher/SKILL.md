---
name: recommendation-publisher
description: Convert approved recommendations into GitHub issue updates. Extracts "Proposed GitHub Updates" sections and stages them for publishing.
allowed-tools: Read, Glob, Grep, Write, Bash
version: 1.0.0
---

# Recommendation Publisher

## Overview

Stage approved recommendations from `docs/recommendations/` for publishing to GitHub issues. This skill extracts the "Proposed GitHub Updates" section from analysis files and creates formatted files ready for `gh issue comment`.

**Announce at start:** "I'm using the recommendation-publisher skill to stage recommendations for GitHub."

## Process

### Phase 1: Find Recommendations

1. List files in `docs/recommendations/issues/`
2. Identify files with "Proposed GitHub Updates" sections
3. Present list to user for selection (or accept specific file/issue number)

### Phase 2: Extract Update Content

1. Read the selected analysis file
2. Extract the "Proposed GitHub Updates" section
3. Parse the issue number from the filename (XXX-title-analysis.md)

### Phase 3: Format for GitHub

1. Clean up the content (remove template markers)
2. Format as GitHub-flavored markdown
3. Add metadata header with source reference

### Phase 4: Stage for Publishing

Write to `docs/recommendations/github-updates/issue-XXX-update.md`:

```markdown
<!--
Source: docs/recommendations/issues/XXX-title-analysis.md
Issue: #XXX
Generated: YYYY-MM-DD
Status: STAGED (not yet published)
-->

[Extracted update content]
```

### Phase 5: Provide Publishing Command

Output the command to publish:

```bash
cd repos/lacrosse-bosse && gh issue comment XXX --body-file ../../docs/recommendations/github-updates/issue-XXX-update.md
```

## Usage

### Stage a specific recommendation:

```
Stage recommendation for issue #69
```

### Stage all pending recommendations:

```
Stage all pending recommendations
```

### Publish a staged update (manual step):

```bash
cd repos/lacrosse-bosse
gh issue comment 69 --body-file ../../docs/recommendations/github-updates/issue-069-update.md
```

## Output Format

### Staged Update File

```markdown
<!--
Source: docs/recommendations/issues/069-play-animation-preview-analysis.md
Issue: #69
Generated: 2025-12-20
Status: STAGED
-->

## Analysis Summary

Play Animation Preview requires a multi-view animation system with playback controls and step indicators. The implementation should leverage existing PlayManager3D while adding camera controls and UI overlays.

### Suggested Acceptance Criteria

- [ ] Play animation runs in overhead view with visible player paths
- [ ] First-person view shows player perspective during animation
- [ ] Step indicators display current/total steps
- [ ] Play/pause/seek controls available in all views
- [ ] Animation speed adjustable (0.5x, 1x, 2x)

### Technical Notes

- Coordinate with existing camera system in CameraManager3D
- Consider using AnimationPlayer for synchronized multi-fielder movement
- Step transitions should emit signals for UI synchronization
```

## File Naming

- Input: `docs/recommendations/issues/XXX-title-analysis.md`
- Output: `docs/recommendations/github-updates/issue-XXX-update.md`

## Status Tracking

After publishing, update the staged file:

```markdown
<!--
Source: docs/recommendations/issues/069-play-animation-preview-analysis.md
Issue: #69
Generated: 2025-12-20
Status: PUBLISHED on 2025-12-21
-->
```

## Notes

- Never auto-publish to GitHub - always stage first
- User must explicitly run the `gh issue comment` command
- Keep source analysis file after publishing
- Update status in staged file after publishing
