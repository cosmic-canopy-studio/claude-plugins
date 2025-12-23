---
name: docs-howto
description: Create task-oriented how-to guides
---

# Create How-To Guide

Creates practical guides for solving specific problems or completing specific tasks.

## Usage

/docs-howto --task=STRING [--context=STRING] [--framework=STRING]

## Options

- `--task`: Specific problem to solve (required)
- `--context`: Additional context (optional)
- `--framework`: Technology framework (optional)

## Output Format

How-to guides follow this structure:
```markdown
# How-to: [Specific Task]

## Problem
- Brief problem statement
- When this task is needed

## Solution
- Step-by-step instructions
- Code examples
- Configuration notes
- Expected results

## Variations
- Alternative approaches
- Common pitfalls
- Troubleshooting tips
```

## Best Practices

- Focus on single, specific task
- Assume reader has basic familiarity
- Include complete code examples
- Provide expected outcomes
- Mention common mistakes and fixes

---

cd /home/sam/code/code_improvement && python tools/create_docs.py howto "$*"