# Knowledge Indexer Agent

## Purpose

Build search index and cross-references for the unified knowledge base after category-merger agents complete.

## Input

- `knowledge_dir`: Path to unified knowledge base (e.g., `references/knowledge/`)

## Output

Create in `{knowledge_dir}/`:
- `_index.md` - Main navigation page
- `_search_index.json` - Machine-readable search index
- `_sources.md` - List of all source books

## Tasks

1. **Scan all category directories**:
   - Read all `.md` files in `patterns/`, `rules/`, `concepts/`, `examples/`, `anti_patterns/`

2. **Build search index** (`_search_index.json`):
   ```json
   {
     "version": "1.0",
     "generated": "2025-12-20T14:00:00",
     "items": [
       {
         "id": "extract_method",
         "type": "pattern",
         "name": "Extract Method",
         "aliases": ["Extract function"],
         "keywords": ["extract", "method", "function", "refactoring"],
         "sources": ["five_lines_of_code", "good_code_bad_code"],
         "path": "patterns/extract_method.md"
       }
     ],
     "tags": {
       "refactoring": ["extract_method", "inline_method"],
       "readability": ["five_lines", "good_function_name"]
     }
   }
   ```

3. **Build cross-references**:
   - Scan item files for "Related" sections
   - Find patterns that address specific smells
   - Link rules to patterns that implement them
   - Update item files with bidirectional links

4. **Write `_index.md`**:
   ```markdown
   # Software Architecture Knowledge Base

   **Generated:** 2025-12-20
   **Sources:** 5 books analyzed

   ## Quick Stats

   | Category | Items |
   |----------|-------|
   | [Refactoring Patterns](patterns/) | 37 |
   | [Rules & Best Practices](rules/) | 27 |
   | [Concepts](concepts/) | 73 |
   | [Code Examples](examples/) | 245 |
   | [Anti-Patterns](anti_patterns/) | 15 |

   ## Browse by Category

   ### Refactoring Patterns
   - [Extract Method](patterns/extract_method.md) - Extract code into new method
   - [Replace Type Code](patterns/replace_type_code.md) - Replace enums with classes
   ...

   ### Rules & Best Practices
   - [Five Lines](rules/five_lines.md) - Methods should have ≤5 lines
   - [Never Use If With Else](rules/never_use_if_with_else.md) - Avoid if-else chains
   ...

   ## Browse by Tag

   - **refactoring**: [Extract Method](patterns/extract_method.md), [Inline Method](patterns/inline_method.md)
   - **readability**: [Five Lines](rules/five_lines.md), [Good Names](rules/good_names.md)
   ```

5. **Write `_sources.md`**:
   ```markdown
   # Source Books

   | Book | Items Extracted | Analysis Date |
   |------|-----------------|---------------|
   | Five Lines of Code | 151 | 2025-12-20 |
   | Good Code Bad Code | 87 | 2025-12-20 |
   | Grokking Simplicity | 64 | 2025-12-20 |

   ## External References

   Books referenced but not analyzed:
   - Refactoring (Martin Fowler)
   - Clean Code (Robert C. Martin)
   ```

## Important

- This agent runs AFTER all category-merger agents complete
- Reads from the unified knowledge base
- Builds navigation and search infrastructure
- Only ONE instance runs (not parallelized)
