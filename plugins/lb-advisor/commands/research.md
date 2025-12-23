---
name: research
description: Research best practices for a Godot development question
arguments:
  - name: question
    description: The question to research
    required: true
---

# /research Command

Explicitly invoke the research workflow for a development question.

## Usage

```
/research "How should I implement scene transitions?"
```

## Behavior

Invokes the `research` skill with the provided question. Same workflow as auto-trigger:

1. **Quick Lookup** - Check godot skill reference files
2. **Codebase Context** - Analyze existing project patterns
3. **External Research** - Search official docs if needed
4. **Synthesis** - Write document + provide inline summary

## Output

- Inline quick answer with code example
- Full document written to `docs/research/YYYY-MM-DD-topic.md`

## Examples

```
/research "scene loading from main menu"
/research "state machine for player controller"
/research "input handling for mobile"
```
