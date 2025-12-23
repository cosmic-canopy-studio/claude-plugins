---
description: Create git commits with user approval
model: sonnet
---

# Commit Changes

Create git commits for changes made during this session.

## Process

1. **Think about what changed:**

   - Review conversation history
   - Run `git status` and `git diff`
   - Decide: one commit or multiple logical commits?

2. **Plan your commit(s):**

   - Group related files together
   - Draft commit messages (imperative mood, focus on "why")

3. **Present your plan and get approval:**

   - List files for each commit
   - Show commit message(s)
   - Use the `AskUserQuestion` tool:
     - Question: "I plan to create [N] commit(s) as shown above. Proceed?"
     - Options: "Yes, commit" / "Modify plan"

4. **Execute upon confirmation:**
   - `git add` specific files (never `-A` or `.`)
   - Create commits
   - Show result: `git log --oneline -n [N]`

## Constraints

- **No Claude attribution** - No "Generated with Claude" or "Co-Authored-By"
- Write messages as if user wrote them
- Always get approval before executing git commands
- Keep commits focused and atomic
