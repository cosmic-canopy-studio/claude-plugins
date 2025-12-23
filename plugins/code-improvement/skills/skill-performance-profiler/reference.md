# Token Estimation Reference

## Word to Token Conversion

Approximate ratios for English text:

| Content Type | Words per Token |
|--------------|-----------------|
| Plain prose | 0.75 |
| Technical docs | 0.65 |
| Code | 0.50 |
| YAML/JSON | 0.45 |

**Quick estimation**: tokens ≈ words × 1.33

## Context Window Usage

Claude's context window and skill impact:

| Skill Size | Est. Tokens | Context Impact |
|------------|-------------|----------------|
| Minimal (<150 words) | ~200 | Negligible |
| Small (<300 words) | ~400 | Low |
| Medium (<500 words) | ~700 | Moderate |
| Large (>500 words) | >700 | Significant |

## Progressive Disclosure Tiers

### Tier 1: Always Loaded (Metadata)
```yaml
name: skill-name
description: Brief description with triggers
when_to_use: trigger conditions
```
**Target**: ~50 tokens

### Tier 2: On Activation (SKILL.md)
```markdown
# Skill Name
## Overview (1-2 sentences)
## Quick Start (3-5 steps)
## Key Patterns (summary only)
```
**Target**: ~200-400 tokens

### Tier 3: On Demand (reference files)
```markdown
# Full documentation
# Examples with edge cases
# API references
# Troubleshooting guides
```
**Target**: Unlimited (only loaded when needed)

## File Organization Patterns

### Minimal Skill (1 file)
```
skill/
└── SKILL.md         # Everything inline, <200 words
```
Use for: Simple, focused skills

### Standard Skill (2-3 files)
```
skill/
├── SKILL.md         # Core workflow
├── patterns.md      # Common patterns
└── reference.md     # Heavy docs
```
Use for: Most skills

### Complex Skill (4+ files)
```
skill/
├── SKILL.md         # Minimal core
├── patterns/
│   ├── pattern-a.md
│   └── pattern-b.md
├── reference.md
└── examples/
    └── example.md
```
Use for: Skills with multiple distinct patterns

## Anti-Patterns

### Force-Load Abuse
```markdown
# BAD - forces immediate load
See @patterns.md for details
Use the patterns from @reference.md

# GOOD - deferred load
See patterns.md for details
(Claude loads when actually needed)
```

### Monolithic SKILL.md
```markdown
# BAD - everything in one file
[500+ words of patterns, examples, edge cases]

# GOOD - split by loading priority
SKILL.md: Core only
patterns.md: Common patterns
reference.md: Edge cases, full examples
```

### Redundant Content
```markdown
# BAD - repeated across files
SKILL.md: "Check YAML syntax..."
patterns.md: "Always check YAML syntax..."
reference.md: "First, verify YAML syntax..."

# GOOD - single source
SKILL.md: "Check YAML syntax (see patterns.md for details)"
```

## Optimization Checklist

Before deploying a skill:

- [ ] SKILL.md is <300 words (ideally <200)
- [ ] No @ force-load syntax
- [ ] Heavy content in reference files
- [ ] Patterns are <500 words each
- [ ] No redundant content across files
- [ ] File structure matches complexity
- [ ] Examples are minimal but complete
