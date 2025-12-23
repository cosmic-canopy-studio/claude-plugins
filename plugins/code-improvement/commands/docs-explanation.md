---
name: docs-explanation
description: Create conceptual explanations for deeper understanding
---

# Create Explanation

Creates in-depth explanations that help readers understand concepts and their "why".

## Usage

/docs-explanation --concept=STRING [--depth=basic|detailed] [--context=STRING]

## Options

- `--concept`: Concept to explain (required)
- `--depth`: Explanation depth (default: detailed)
- `--context`: Surrounding context (optional)

## Output Format

Explanations follow this structure:
```markdown
# Explanation: [Concept]

## Overview
- High-level description
- Why this concept matters

## How it works
- Internal mechanisms
- Design decisions
- Key principles

## When to use
- Appropriate scenarios
- Benefits provided
- Trade-offs involved

## Related concepts
- Connections to other topics
- Prerequisites
- Next steps

## Examples
- Concrete illustrations
- Real-world analogies
```

## Best Practices

- Focus on "why" not just "how"
- Use analogies and metaphors
- Provide historical context when helpful
- Connect to related concepts
- Answer anticipated questions
- Adapt to audience knowledge level

---

cd /home/sam/code/code_improvement && python tools/create_docs.py explanation "$*"