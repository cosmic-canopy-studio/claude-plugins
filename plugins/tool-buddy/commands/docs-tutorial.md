---
description: Create learning-oriented tutorials for beginners
---

# Create Tutorial

Creates hands-on learning tutorials that guide beginners through concepts step-by-step.

## Usage

/docs-tutorial [--topic=STRING] [--level=beginner|intermediate] [--project=STRING]

## Options

- `--topic`: What the tutorial teaches (required)
- `--level`: Target audience level (default: beginner)
- `--project`: Project context (optional)

## Output Format

Tutorial documents follow this structure:
```markdown
# Tutorial: [Topic]

## What you'll learn
- Clear learning objectives
- Skills you'll gain

## Prerequisites
- Required knowledge
- Tools needed

## Step 1: [Action]
- Hands-on exercise
- Expected outcome
- Verification step

## Step 2: [Action]
- Continues learning
- Builds on previous step

## Summary
- Recap of learning
- Next steps
```

## Best Practices

- Start with concrete example, not abstract concepts
- Ensure each step succeeds before moving to next
- Include verification at each step
- Use simple, clear language
- Provide recovery steps for common mistakes

---

cd /home/sam/code/code_improvement && python tools/create_docs.py tutorial "$*"