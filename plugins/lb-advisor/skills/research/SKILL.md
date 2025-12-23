---
name: research
description: Research best practices with multi-pattern discovery and scoring. Discovers ALL patterns from diverse sources before making reasoned recommendations. Auto-triggers on "how do I", "what's the best way", and similar questions.
---

# Research Skill

Discovers multiple implementation patterns from diverse sources, scores them against relevant factors, and makes reasoned recommendations.

## Core Principle

**Never short-circuit pattern discovery.** Always gather patterns from at least 3 sources before recommending. Codebase consistency is ONE factor, not an automatic winner.

## Auto-Trigger Patterns

This skill triggers automatically when detecting:
- "how do I..." + Godot/implementation context
- "how can I..." + implementation context
- "what's the way to...", "best practice for..."
- Any implementation question in Godot project context

**Default assumption:** Best practice / Godot idiomatic is ALWAYS implied.

## Workflow

### Step 1: Pattern Discovery (Parallel, Never Short-Circuit)

Search ALL sources before recommending:

1. **Internal References** (`godot` skill dispatchers + reference files)
   - Source tag: `internal`
   - May be incomplete - never stop here

2. **Codebase Patterns** (grep project for similar functionality)
   - Source tag: `codebase`
   - Consistency is a scoring factor, not automatic recommendation

3. **Official Documentation** (godot-docs-researcher agent)
   - Source tag: `official-docs`
   - High authority

4. **Official Demo Projects** (github.com/godotengine/godot-demo-projects)
   - Source tag: `official-demo`
   - Very high authority - real working examples

5. **Community Examples** (GDQuest, tutorials, forums)
   - Source tag: `community`
   - Lower priority but may reveal alternatives

**Minimum requirement:** At least 3 sources searched before synthesis.

### Step 2: Pattern Catalog

For EACH discovered pattern, document:
- **Name**: Descriptive identifier
- **Source**: Where discovered (with link/file:line)
- **Approach**: Brief description
- **Code Example**: Minimal working example (static typed)
- **Best For**: When this pattern excels

### Step 3: Scoring Matrix

Score each pattern (1-5) using best judgement. Always show the matrix.

**Core Factors** (always consider):
| Factor | Description |
|--------|-------------|
| Simplicity | Lines of code, concepts required |
| Maintainability | Long-term code health |
| Performance | Runtime efficiency |
| Official Support | Documented, endorsed approach |
| Codebase Fit | Matches existing patterns |

**Context-Specific Factors** (add when relevant):
| Factor | When to Include |
|--------|-----------------|
| State Preservation | Scene transitions, mode switching |
| Responsiveness | Input handling |
| Extensibility | State machines, plugin systems |
| Memory Efficiency | Resource-constrained contexts |

**Scoring approach:**
- Use best judgement, not scripted formulas
- Weight factors based on the specific question context
- Consider user's stated requirements when scoring
- Be transparent about reasoning

### Step 4: Reasoned Recommendation

Present:
1. **Pattern Comparison Table** - all patterns with scores
2. **Recommended Pattern** - with rationale tied to scores
3. **Alternative Guidance** - "Choose X if..." for other patterns

## Output Format

### Inline Response

```
**Patterns Found:** [N patterns from M sources]

**Comparison:**
| Pattern | Score | Best For |
|---------|-------|----------|
| ... | ... | ... |

**Recommended:** [Pattern name] - [1-sentence rationale]

**Choose [Alt] if:** [alternative context]

**Full analysis:** See `docs/research/YYYY-MM-DD-topic.md`
```

### Document Format (`docs/research/YYYY-MM-DD-topic.md`)

```markdown
# Research: [Topic]

## Question
[Original question restated]

## Patterns Discovered

### Pattern 1: [Name]
**Source:** [official-demo/codebase/internal/community]
**Link:** [URL or file:line]

**Approach:** [Description]

**Code Example:**
```gdscript
# Full example with static typing
```

**Best For:** [Use case]

### Pattern 2: [Name]
...

## Scoring Matrix

| Factor | Pattern 1 | Pattern 2 | Pattern 3 | Notes |
|--------|-----------|-----------|-----------|-------|
| Simplicity | 4 | 3 | 5 | [reasoning] |
| Maintainability | 4 | 5 | 3 | [reasoning] |
| ... | ... | ... | ... | ... |
| **Total** | **3.8** | **4.1** | **3.5** | |

## Recommendation

**Recommended:** Pattern 2

**Rationale:**
- [Reason tied to scoring]
- [Context consideration]

**Choose Pattern 1 if:** [Alternative context]
**Choose Pattern 3 if:** [Alternative context]

## Sources
- [All sources with links]
```

## Example: Scene Loading

**User:** "How do I handle scene loading from main menu?"

### Step 1: Pattern Discovery (4 sources)

1. `internal` - reference/patterns/scenes.md
2. `codebase` - core/main_menu.gd uses change_scene_to_packed
3. `official-docs` - SceneTree documentation
4. `official-demo` - 2d/role_playing_game uses remove_child/add_child

### Step 2: Pattern Catalog

| Pattern | Source | Approach |
|---------|--------|----------|
| change_scene_to_file() | official-docs | Full scene swap, path-based |
| change_scene_to_packed() | codebase | Full scene swap, preloaded |
| remove_child/add_child | official-demo | Scene persistence, swap visibility |
| SceneManager autoload | internal | Centralized with transitions |

### Step 3: Scoring Matrix

| Factor | file() | packed() | child_swap | SceneManager |
|--------|--------|----------|------------|--------------|
| Simplicity | 5 | 4 | 3 | 2 |
| Maintainability | 4 | 4 | 4 | 5 |
| Performance | 3 | 4 | 5 | 4 |
| Flexibility | 3 | 3 | 5 | 5 |
| Official Support | 5 | 5 | 5 | 4 |
| Codebase Fit | 2 | 5 | 2 | 3 |
| State Preservation | 1 | 1 | 5 | 3 |
| **Total** | 3.3 | 3.7 | 4.1 | 3.7 |

### Step 4: Recommendation

**For lacrosse-bosse main menu:** `change_scene_to_packed()`
- Highest codebase fit (existing pattern)
- No state preservation needed for menu→game transitions
- Editor validation via @export

**Choose child_swap if:**
- Need to preserve scene state (returning to exploration after combat)
- Scenes swap frequently back and forth

**Choose SceneManager if:**
- Need fade transitions, loading screens, or scene history
