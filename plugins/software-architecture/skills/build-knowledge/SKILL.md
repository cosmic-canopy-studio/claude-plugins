---
name: build-knowledge
description: |
  Build the unified knowledge base from all analyzed books by merging patterns, rules, concepts, examples, and anti-patterns.
  TRIGGERS: "build knowledge base", "merge analyses", "create index", "unify patterns", "consolidate knowledge", "rebuild index".
  PROACTIVE: Use after analyze-books completes to create unified searchable index.
  PREREQUISITE: Requires at least one book with completed analysis (_analysis/ directory exists).
---

# Build Knowledge

Build the unified knowledge base from all analyzed books.

## Examples

- "build the knowledge base"
- "merge all the book analyses"
- "create the unified knowledge index"

## Behavior

1. **Find Analyzed Books**
   - Scan `references/extracted/` for books with `_analysis/` directories
   - Verify each has `_summary.json`
   - Build list of source directories

2. **Merge Categories in Parallel**
   - Spawn 5 `category-merger` agents in parallel:
     - `patterns` merger
     - `rules` merger
     - `concepts` merger
     - `examples` merger
     - `anti_patterns` merger
   - Each writes to `references/knowledge/{category}/`

3. **Build Indexes**
   - After all mergers complete, spawn `knowledge-indexer` agent
   - Wait for index generation

4. **Report Results**
   - Show counts per category
   - Report duplicates merged
   - Show cross-references created

## Output

```markdown
## Knowledge Base Built

**Location:** references/knowledge/

| Category | Items | Merged | Unique |
|----------|-------|--------|--------|
| Patterns | 45 | 8 | 37 |
| Rules | 32 | 5 | 27 |
| Concepts | 85 | 12 | 73 |
| Examples | 255 | 0 | 255 |
| Anti-Patterns | 18 | 3 | 15 |

**Cross-References Generated:**
- 156 pattern-to-rule links
- 89 pattern-to-smell links
- 234 concept-to-example links

**Files Created:**
- references/knowledge/_index.md
- references/knowledge/_search_index.json
- references/knowledge/_sources.md
- 407 individual knowledge item files
```

## Output Structure

```
references/knowledge/
├── _index.md
├── _search_index.json
├── _sources.md
├── patterns/
│   ├── _index.md
│   ├── extract_method.md
│   └── ...
├── rules/
│   ├── _index.md
│   ├── five_lines.md
│   └── ...
├── concepts/
├── examples/
│   ├── by_language/
│   └── by_topic/
└── anti_patterns/
```

## Error Handling

- If no analyzed books found, report and exit
- If a category merger fails, continue with others
- If indexer fails, still preserve merged content
- Always produce a report even with failures
