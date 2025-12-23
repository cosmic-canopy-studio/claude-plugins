# Reference: Skill Debugging

## Diagnostic Checklist

Quick troubleshooting reference for skill issues.

### Skill Won't Load

1. Check YAML syntax with validator
2. Verify description has trigger keywords
3. Confirm when_to_use has concrete phrases
4. Check for conflicting skill descriptions

### Skill Loads Wrong

1. Add negative triggers ("Don't use for...")
2. Check keyword overlap with other skills
3. Make description more specific

### Skill Output Wrong

1. Check template in SKILL.md
2. Verify all steps have clear transitions
3. Add explicit output format section

### Context Issues

1. Check SKILL.md word count (<300)
2. Check patterns.md word count (<500/pattern)
3. Remove @ force-load syntax

## Error Messages

| Error | Likely Cause | Fix |
|-------|--------------|-----|
| "Skill not found" | Wrong path or missing file | Check .claude/skills/[name]/SKILL.md exists |
| "Invalid YAML" | Frontmatter syntax error | Validate YAML, check quote escaping |
| "No matching skill" | Trigger mismatch | Add keywords to description |

## File Structure

```
.claude/skills/[skill-name]/
├── SKILL.md      # Required - core skill, <300 words
├── patterns.md   # Optional - common patterns
└── reference.md  # Optional - detailed reference
```

## Tool Requirements

| Skill Type | Required Tools | Optional Tools |
|------------|----------------|----------------|
| File analysis | Read, Glob, Grep | - |
| Code modification | Edit, Write | Bash |
| Research | WebSearch, WebFetch | Read |
