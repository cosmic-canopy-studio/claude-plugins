---
name: search-knowledge
description: |
  Search the knowledge base for patterns, rules, concepts, examples, and anti-patterns.
  TRIGGERS: "search for [pattern]", "find [concept]", "what patterns", "how do I refactor", "best practices for", "code smells", "what rules apply to", "show me examples of".
  PROACTIVE: Use for any programming question that could be answered by extracted book knowledge.
  PREREQUISITE: Knowledge base must be built (references/knowledge/ exists with _search_index.json).
---

# Search Knowledge

Search the knowledge base for specific items.

## Arguments

- `query`: Search terms (e.g., "extract method", "five lines", "refactoring")
- `--category`: Optional filter (patterns, rules, concepts, examples, anti_patterns)
- `--book`: Optional filter by source book

## Examples

- "search for extract method"
- "find patterns about refactoring"
- "what rules do we have about function length"
- "show me anti-patterns related to if-else"

## Behavior

1. **Load Search Index**
   - Read `references/knowledge/_search_index.json`
   - If not found, suggest running build-knowledge skill first

2. **Search Items**
   - Match query against:
     - Item names (weighted highest)
     - Item aliases
     - Keywords
     - Descriptions
   - Apply category filter if specified
   - Apply book filter if specified

3. **Rank Results**
   - Sort by relevance score
   - Name matches rank highest
   - Keyword matches rank lower
   - Description matches rank lowest

4. **Return Top Results**
   - Show top 10 matches
   - Include category, source books, brief description
   - Provide links to full entries

## Output

```markdown
## Search Results: "extract method"

Found 5 results:

### 1. Extract Method (Pattern)
**Sources:** Five Lines of Code, Good Code Bad Code
**Relevance:** 100%

Takes part of one method and extracts it into its own method.

[View full entry](references/knowledge/patterns/extract_method.md)

---

### 2. Extract Common Subexpression (Pattern)
**Sources:** Five Lines of Code
**Relevance:** 75%

Extracts repeated expressions into a named variable.

[View full entry](references/knowledge/patterns/extract_common_subexpression.md)

---

### 3. Five Lines Rule (Rule)
**Sources:** Five Lines of Code
**Relevance:** 60%

Mentions Extract Method as the primary technique...

[View full entry](references/knowledge/rules/five_lines.md)
```

## Error Handling

- If knowledge base not found, suggest building it first
- If no results found, suggest related searches
- Handle empty queries gracefully
