# Token Budget Reference

## Context Window Sizes

| Model | Context Window | Smart Zone (35%) | Warning (50%) | Critical (60%) |
|-------|----------------|------------------|---------------|----------------|
| Claude Opus | 200K | 70K | 100K | 120K |
| Claude Sonnet | 200K | 70K | 100K | 120K |
| Claude Haiku | 200K | 70K | 100K | 120K |

## Detailed Token Estimation

### By Content Type

| Content | Tokens/Word | Tokens/100 Lines |
|---------|-------------|------------------|
| English prose | 1.33 | ~500 |
| Technical documentation | 1.54 | ~600 |
| Source code (Python) | 2.0 | ~800 |
| Source code (TypeScript) | 2.2 | ~900 |
| JSON/YAML config | 2.5 | ~1000 |
| Markdown with code | 1.8 | ~700 |

### Quick Estimates

| Element | Typical Tokens |
|---------|---------------|
| User message (short) | 50-100 |
| User message (detailed) | 200-500 |
| Claude response (brief) | 100-300 |
| Claude response (detailed) | 500-2000 |
| File read (small) | 200-500 |
| File read (medium) | 500-2000 |
| File read (large) | 2000-10000 |
| Skill load | 200-700 |
| System prompt | 2000-5000 |

## Conversation Token Accumulation

### Typical Session Pattern

```
Turn 1:  ~1K tokens (system + first exchange)
Turn 5:  ~5K tokens
Turn 10: ~10K tokens
Turn 20: ~25K tokens (tool outputs accumulating)
Turn 30: ~40K tokens (approaching caution zone)
Turn 40: ~60K tokens (in warning zone)
```

### Compaction Points

| Tokens | Recommended Action |
|--------|-------------------|
| 25K | Consider task batching |
| 40K | Evaluate need for compaction |
| 60K | Execute compaction strategy |
| 80K | Strong recommendation to reset |
| 100K | Critical - handoff immediately |

## Degradation Patterns

### The "Dumb Zone" Explained

> "Performance degrades around 40% context usage. The model starts making worse decisions, forgetting earlier context, and requiring more corrections."
> — Dex Horthy

**Observable symptoms at each threshold:**

| Threshold | Symptoms |
|-----------|----------|
| 35% | Subtle quality decrease, more verbose responses |
| 50% | Noticeable forgetting, repeating suggestions |
| 60% | Significant errors, losing conversation thread |
| 70%+ | Major degradation, contradicting itself |

### Death Valley Pattern

From Stanford study: ~10M tokens/month is a "Death Valley" where more AI usage correlates with worse outcomes.

**Session-level analog**: Around 50-60% context usage, more interaction often makes things worse rather than better.

## Compaction Strategies (Detailed)

### 1. Handoff Document

Create a compressed summary for new session:

```markdown
# Handoff: [Task Name]

## Completed
- [What was accomplished]

## Current State
- [Where things stand now]

## Next Steps
- [What needs to happen]

## Key Decisions
- [Important choices made and why]

## Avoid
- [Approaches that didn't work]
```

### 2. Sub-Agent Delegation

Fork context for isolated work:

```
Main context: 60K tokens (warning zone)
↓
Spawn sub-agent: 5K tokens (fresh context)
↓
Return summary: +500 tokens to main
```

**Best for**: Research, exploration, isolated fixes

### 3. Selective Reset

Keep only essential context:

1. Export key decisions to file
2. Note current working state
3. Start new session with targeted context
4. Import only what's needed

### 4. On-Demand Research

Replace cached context with fresh queries:

**Instead of**: Keeping large documentation in context
**Do this**: Read specific sections when needed

## Integration with Hooks

### Status Line Display

```
🟢 Tokens: 23% (46K/200K) | Tools: 15
```

Color coding:
- 🟢 Green: 0-35%
- 🟡 Yellow: 35-50%
- 🟠 Orange: 50-60%
- 🔴 Red: 60%+

### Hook Triggers

```json
{
  "PostToolUse": [
    {
      "matcher": "*",
      "hooks": [
        {
          "type": "command",
          "command": "python3 context-monitor.py"
        }
      ]
    }
  ]
}
```

## Calculation Formula

```python
def estimate_tokens(messages, tool_outputs, skills_loaded):
    """Estimate current context usage."""
    base = 3000  # System prompt

    message_tokens = sum(
        len(m.content.split()) * 1.5  # User messages
        for m in messages if m.role == "user"
    )

    response_tokens = sum(
        len(m.content.split()) * 1.5  # Claude responses
        for m in messages if m.role == "assistant"
    )

    tool_tokens = sum(
        len(str(o).split()) * 2  # Tool outputs (code-heavy)
        for o in tool_outputs
    )

    skill_tokens = skills_loaded * 400  # Avg skill size

    total = base + message_tokens + response_tokens + tool_tokens + skill_tokens

    return {
        "total": total,
        "percentage": total / 200_000 * 100,
        "zone": get_zone(total / 200_000 * 100)
    }

def get_zone(percentage):
    if percentage < 35:
        return "green"
    elif percentage < 50:
        return "yellow"
    elif percentage < 60:
        return "orange"
    else:
        return "red"
```
