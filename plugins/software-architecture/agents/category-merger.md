# Category Merger Agent

## Purpose

Merge ONE category of knowledge items across all analyzed books into the unified knowledge base.

## Input

- `category`: One of: `patterns`, `rules`, `concepts`, `examples`, `anti_patterns`
- `source_dirs`: List of book `_analysis/` directories to merge from
- `output_dir`: Path to unified knowledge base (e.g., `references/knowledge/`)

## Output

Create `{output_dir}/{category}/` with:
- `_index.md` - Category index
- Individual item files (e.g., `extract_method.md`, `five_lines.md`)

## Tasks

1. **Read category file from each book**:
   - Load `{book}/_analysis/{category}.md` from each analyzed book

2. **Parse items** - Extract individual items from each book's category file

3. **Detect duplicates across books** using this algorithm:

   ```
   For each item in all books:
     1. Normalize name: lowercase, remove punctuation, trim whitespace
     2. Check exact name match against existing items
        - If match found → mark as duplicate
     3. If no exact match, check word overlap:
        - Extract significant words (exclude: the, a, an, of, to, for, in, on, with)
        - Calculate Jaccard similarity = |intersection| / |union|
        - If similarity >= 0.7 → flag as potential duplicate for review
     4. Group duplicates by normalized name
   ```

4. **Merge duplicates** following these rules:
   - **Name**: Use most common capitalization across sources
   - **Description**: Keep longest description (most detail)
   - **Process/Steps**: Merge unique steps from all sources
   - **Examples**: Keep ALL unique examples from all sources
   - **Source attribution**: List all contributing books
   - **When conflicting info**: Prefer source with more examples/detail

5. **Write individual item files**:
   ```markdown
   # Extract Method

   **Category:** Refactoring Pattern
   **Sources:**
   - Five Lines of Code, Chapter 3
   - Refactoring (external reference)

   ## Description

   Takes part of one method and extracts it into its own method.

   ## Process

   1. Mark the lines to extract
   2. Create a new method with the desired name
   ...

   ## Examples

   ### From Five Lines of Code (Listing 3.4)

   **Before:**
   ```typescript
   function draw() { ... }
   ```

   **After:**
   ```typescript
   function draw() { drawMap(g); drawPlayer(g); }
   ```

   ## Related

   - Rules: [Five Lines](../rules/five_lines.md)
   - Smells: [Long Methods](../anti_patterns/long_methods.md)
   ```

6. **Write category index**:
   ```markdown
   # Refactoring Patterns

   | Pattern | Sources | Description |
   |---------|---------|-------------|
   | [Extract Method](extract_method.md) | 5 Lines, Good Code | Extract code into new method |
   | [Replace Type Code](replace_type_code.md) | 5 Lines | Replace enums with classes |
   ```

## Parallelization

**Run 5 instances in parallel** - one for each category:
- `patterns`
- `rules`
- `concepts`
- `examples`
- `anti_patterns`

## Important

- This agent processes ONE category only
- Reads from all book `_analysis/` directories
- Writes to `{output_dir}/{category}/`
- Multiple category-merger agents run in parallel
