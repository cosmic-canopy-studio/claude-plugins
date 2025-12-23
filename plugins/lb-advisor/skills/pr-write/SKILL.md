---
name: pr-write
description: Write PR descriptions focused on user impact, not code details. Minimal QA steps, always includes a fun gif.
when_to_use:
  triggers:
    - "write pr"
    - "draft pr"
    - "create pr description"
    - "pr for"
  auto_invoke: always
version: 1.0.0
---

# Skill: PR Description Writing

Write PR descriptions that communicate value to reviewers without drowning them in implementation details.

## Philosophy

**Reviewers care about impact, not commits.** Lead with what changed for users, not what files you touched.

## The Template

```markdown
## Description

[2-3 sentences: what can users do now that they couldn't before?]

**Key features:**
- [User-facing capability 1]
- [User-facing capability 2]
- [User-facing capability 3]

## Related Tickets & Documents

Fixes #<issue>

## Screenshots/Recordings

<!-- Add visuals for UI changes -->

## Steps to QA

1. [Happy path: main feature works]
2. [Secondary: related functionality]
3. [Edge case: error handling or limits]

## What gif best describes this PR?

![alt](giphy-url)
```

## Process

### 1. Extract Context

```bash
# Get branch name for issue number
git branch --show-current

# Get linked issue
gh issue view <NUMBER> --json title,body

# Count commits by type
git log main..HEAD --oneline | wc -l
```

### 2. Summarize at the Right Level

**Too granular (avoid):**
> - Added StepDescriptionEdit LineEdit to scene
> - Connected signal to _on_step_description_changed
> - Updated _set_current_step to load description

**Just right:**
> - Play steps now have editable descriptions
> - Descriptions persist when saving/loading plays

### 3. Write Minimal QA Steps

**Maximum 3-5 steps.** Focus on verification, not exploration.

| Bad | Good |
|-----|------|
| "Click around and test things" | "Create a play with 3 steps, save it, reload it" |
| "Test all the buttons" | "Verify pause menu returns to main menu" |
| "Make sure it works" | "Confirm undo restores deleted markers" |

### 4. Find a Gif

Use WebSearch to find a relevant Giphy gif:

```
site:giphy.com [keyword related to the feature]
```

Good keywords by PR type:
- New feature: "celebration", "magic", "building"
- Bug fix: "relief", "fixed it", "success"
- Refactor: "cleaning", "organizing", "tidy"
- Performance: "speed", "fast", "zoom"

Pick something fun that matches the PR's energy.

## Style Principles

### Lead with User Value

**Instead of:**
> This PR adds the PlayManager scene with position markers, action shapes, and step management.

**Write:**
> Coaches can now create plays visually using a drag-and-drop editor with step-by-step progression.

### Group by Feature, Not File

**Instead of:**
> Modified: play_manager.gd, play_canvas.gd, position_marker.gd, action_shape.gd

**Write:**
> - Visual play editor with drag-and-drop markers
> - Action arrows showing player movements
> - Multi-step play creation

### Keep QA Actionable

Each step should be:
- **Specific**: What exactly to do
- **Verifiable**: What success looks like
- **Brief**: One line max

## Output

Save to `docs/pr-drafts/<branch-name>.md`

When ready to create the actual PR:
```bash
gh pr create --draft --title "..." --body "$(cat docs/pr-drafts/<branch>.md)"
```
