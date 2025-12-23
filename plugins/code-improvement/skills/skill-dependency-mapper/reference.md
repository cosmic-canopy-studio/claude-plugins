# Skill Dependency Reference

## Dependency Type Details

### Direct Dependencies

A skill explicitly references another skill by name.

**Detection patterns:**
```
"Use with [skill-name]"
"See [skill-name] for..."
"Pair with [skill-name]"
"Integrates with [skill-name]"
"After using [skill-name]"
```

**Example:**
```markdown
## Integration

- Use after skill-testing-framework finds failures
- Pair with skill-performance-profiler for size issues
```

### Chained Dependencies

Skills form a workflow where A depends on B which depends on C.

**Healthy chain:**
```
skill-security-analyzer
    → skill-testing-framework
    → skill-debugging-assistant
```

**Warning signs:**
- Chains longer than 4 skills
- Multiple branches merging
- Unclear entry points

### Circular Dependencies

Skill A depends on B which depends on A (directly or transitively).

**Detection algorithm:**
```python
def detect_cycles(skill, visited=None, path=None):
    if visited is None:
        visited = set()
    if path is None:
        path = []

    if skill in path:
        cycle_start = path.index(skill)
        return path[cycle_start:] + [skill]

    path.append(skill)
    visited.add(skill)

    for dep in get_dependencies(skill):
        if dep not in visited or dep in path:
            cycle = detect_cycles(dep, visited, path.copy())
            if cycle:
                return cycle

    return None
```

**Resolution strategies:**
1. **Extract common functionality** into a new skill
2. **Merge skills** if they're too tightly coupled
3. **Add abstraction layer** between skills
4. **Remove bidirectional references** - pick one direction

### Orphaned Skills

Skills with no incoming or outgoing references.

**Indicators:**
- Never mentioned in other skills
- No integration section
- May be deprecated or experimental

**Actions:**
1. **Review usage**: Is it actually used?
2. **Add integration**: Connect to relevant skills
3. **Archive**: Move to deprecated if unused
4. **Delete**: Remove if truly orphaned

## Healthy Dependency Patterns

### Hub and Spoke

One central skill with many dependent skills.

```
         ┌─ skill-a
         │
skill-hub ─┼─ skill-b
         │
         └─ skill-c
```

**Healthy hub size:** 3-5 spokes
**Warning:** >5 spokes = overloaded

### Pipeline

Linear workflow through skills.

```
skill-1 → skill-2 → skill-3 → skill-4
```

**Healthy length:** 2-4 skills
**Warning:** >5 skills = consider consolidation

### Star

Multiple skills reference common utilities.

```
skill-a ──┐
skill-b ──┼── utility-skill
skill-c ──┘
```

**Best for:** Shared functionality
**Warning:** Utility becoming a bottleneck

## Anti-Patterns

### The God Skill

One skill referenced by everything.

```
skill-a ──┐
skill-b ──┤
skill-c ──┼── mega-skill
skill-d ──┤
skill-e ──┘
```

**Problem:** Changes affect everything
**Solution:** Break into smaller, focused skills

### The Island

Skill with no connections.

```
skill-connected-a ─── skill-connected-b

skill-island   (floating alone)
```

**Problem:** May be unused or misplaced
**Solution:** Connect or archive

### The Spaghetti

Everything depends on everything.

```
skill-a ←→ skill-b
  ↕         ↕
skill-c ←→ skill-d
```

**Problem:** Changes cascade unpredictably
**Solution:** Establish clear hierarchy, break cycles

## Dependency Graph Output

### ASCII Format

```
skill-security-analyzer
├── skill-testing-framework
│   ├── skill-debugging-assistant
│   └── skill-performance-profiler
└── skill-dependency-mapper

Legend:
├── direct dependency
└── final dependency
[!] circular reference
[*] overloaded (>5 refs)
[?] orphaned
```

### Metrics Summary

```
Dependency Health Report
========================

Total Skills: 7
Connected: 6 (86%)
Orphaned: 1 (14%)

Dependency Counts:
- skill-testing-framework: 4 incoming (hub)
- skill-debugging-assistant: 2 incoming
- skill-security-analyzer: 0 incoming (entry point)

Issues:
- CRITICAL: 0 circular dependencies
- WARNING: 0 overloaded skills
- INFO: 1 orphaned skill (skill-gap-analyzer)

Health Score: 92/100
```

## Resolution Guide

### Circular Dependency Resolution

1. **Identify the cycle**
   ```
   skill-a → skill-b → skill-c → skill-a
   ```

2. **Find the weakest link**
   - Which reference is least essential?
   - Which could be replaced with documentation?

3. **Break the cycle**
   - Remove reference
   - Extract shared code
   - Introduce interface skill

4. **Verify resolution**
   - Run dependency mapper again
   - Confirm no cycles

### Overloaded Skill Resolution

1. **Analyze usage patterns**
   - Why do so many skills reference this one?
   - What specific functionality do they need?

2. **Split by functionality**
   - Create focused sub-skills
   - Move functionality to appropriate homes

3. **Update references**
   - Point to specific sub-skills
   - Keep original as facade if needed

### Orphan Resolution

1. **Check for soft references**
   - Natural language mentions
   - Documentation references

2. **Verify utility**
   - Is this skill actually used?
   - Could it be useful?

3. **Decide fate**
   - Connect: Add to workflow
   - Archive: Move to deprecated/
   - Delete: Remove entirely
