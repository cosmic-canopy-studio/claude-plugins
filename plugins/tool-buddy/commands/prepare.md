---
description: Create implementation plan with phased steps and success criteria
model: opus
---

# Create Implementation Plan

You are creating a detailed implementation plan. This is an interactive process - get feedback before writing the full plan.

## Input

You may receive:

- Recon output from `/recon` command
- A question or task description
- A file path to read

If input is unclear, ask: "What would you like me to plan?"

## Process

### Step 1: Understand the Task

1. **Read any provided files** completely
2. **If no research provided**, do quick exploration:
   - Spawn 1-2 Explore agents to find relevant code
   - Read key files (max 3)
3. **Summarize your understanding** and confirm with `AskUserQuestion`:

   First, present your summary in text:

   ```
   I understand we need to [summary].

   Key files involved:
   - `path/to/file.ts` - [why relevant]
   ```

   Then use `AskUserQuestion` to confirm:

   - Question: "Does this match your intent?"
   - Options: "Yes, proceed" / "Continue to explore" / "Needs adjustment"

### Step 2: Outline the Approach

After confirmation, present a brief outline in text:

```
Here's my proposed approach:

## Phases
1. [Phase name] - [what it accomplishes]
2. [Phase name] - [what it accomplishes]

## Out of Scope
- [What we're NOT doing]
```

Then use `AskUserQuestion`:

- Question: "Does this phasing make sense?"
- Options: "Yes, write the plan" / "Adjust phases"

### Step 3: Write the Plan

After outline approval, write the full plan to `docs/plans/YYYY-MM-DD-description.md`:

```markdown
# [Task Name] Implementation Plan

## Overview

[1-2 sentence summary]

## Current State

[What exists now, key files involved]

## Out of Scope

[Explicitly list what we're NOT doing]

---

## Phase 1: [Name]

### Changes

- `path/to/file.ts` - [what to change]

### Success Criteria

**Automated:**

- [ ] `[command]` passes

**Manual:**

- [ ] [Human verification step]

---

## Phase 2: [Name]

[Same structure...]

---

## Testing Strategy

[How to verify the full implementation]
```

### Step 4: Present for Review

Present the summary in text:

```
I've written the plan to `docs/plans/YYYY-MM-DD-description.md`.

Summary:
- Phase 1: [name]
- Phase 2: [name]
```

Then use `AskUserQuestion`:

- Question: "Ready to review the plan?"
- Options: "Yes, write the plan to file" / "Double check your plan" / "I want to review and suggest changes"

## Guidelines

- **Be interactive** - Don't write full plan without confirmation
- **Be specific** - Include file paths, not vague descriptions
- **Split verification** - Automated (commands) vs Manual (human testing)
- **Scope control** - Always include "Out of Scope" section
- **Keep phases small** - Each phase should be independently testable
