# Performance Profiling Patterns

## Analysis Process

### Step 1: Measure Current State
```markdown
## Skill: [name]

| File | Words | Tokens (est) | Status |
|------|-------|--------------|--------|
| SKILL.md | 245 | ~327 | WARNING |
| patterns.md | 890 | ~1187 | CRITICAL |
| Total | 1135 | ~1514 | CRITICAL |
```

### Step 2: Identify Issues
- [ ] SKILL.md over 300 words
- [ ] Patterns.md over 500 words per pattern
- [ ] Force-load (@) syntax used
- [ ] Redundant content across files
- [ ] Content that could be reference

### Step 3: Recommend Optimizations

| Issue | Current | Target | Action |
|-------|---------|--------|--------|
| SKILL.md too large | 245 words | <200 | Move examples to patterns.md |
| Patterns too dense | 890 words | <500/pattern | Split into multiple files |

---

## Optimization Techniques

### Progressive Disclosure
```markdown
# Before - all in SKILL.md
[Full pattern with all examples and edge cases]

# After - layered
SKILL.md: Core pattern, 2-3 line example
patterns.md: Extended examples (loaded on demand)
reference.md: Full edge case documentation
```

### Content Compression
```markdown
# Before - verbose
When you encounter a situation where you need to debug
a skill that is not loading correctly, you should first
check the YAML frontmatter for syntax errors.

# After - concise
Check YAML syntax first when skill won't load.
```

### File Organization
```
skill/
├── SKILL.md         # Core only (<200 words)
├── patterns.md      # Common patterns (on-demand)
├── reference.md     # Heavy docs (on-demand)
└── examples/        # Code examples (on-demand)
```

---

## Output Report Format

```markdown
## Performance Profile: [skill-name]

### Current State
| Metric | Value | Status |
|--------|-------|--------|
| SKILL.md | 245 words | WARNING |
| Total tokens | ~1514 | CRITICAL |
| Force-loads | 2 | WARNING |

### Issues Found
1. **SKILL.md too large** (245 words, target <200)
2. **Force-load abuse** (2 @ references)
3. **Dense patterns** (890 words in patterns.md)

### Optimization Plan
| Priority | Action | Impact |
|----------|--------|--------|
| 1 | Move examples to patterns.md | -100 tokens |
| 2 | Remove @ references | -500 tokens |
| 3 | Split patterns into 2 files | Better on-demand loading |

### Projected After Optimization
| Metric | Before | After | Change |
|--------|--------|-------|--------|
| SKILL.md | 245 | 180 | -27% |
| Total load | ~1514 | ~300 | -80% |
```

---

## Integration

- Run before deploying new skills
- Use with skill-debugging-assistant for context issues
- Feed results to /skill-validate for comprehensive check
