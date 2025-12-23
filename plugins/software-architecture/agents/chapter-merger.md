# Chapter Merger Agent

Merge curated items from multiple chapters, handling cross-chapter duplicates.

## Input

- `chapter_dirs`: List of paths to `_chapters/{ch}/` directories containing `_curated.json`
- `output_dir`: Path to `_analysis/` directory

## Output

Write `{output_dir}/_merged.json`:

```json
{
  "items": [
    {
      "id": "rule-dont-mix-changes",
      "name": "Don't Mix Functional Changes and Refactorings",
      "type": "rule",
      "level_1": {
        "summary": "Either make a functional change or refactor, but not both at once.",
        "category": "Refactoring",
        "tags": ["refactoring", "code-changes", "discipline"]
      },
      "level_2": {
        "statement": "When making a change to the codebase...",
        "explanation": "A refactoring should not change behaviors...",
        "when_to_apply": "Any code modification",
        "related_pattern": null
      },
      "sources": ["10_102_good_unit_test.md:47-51"],
      "chapters": ["ch10"]
    }
  ],
  "stats": {
    "chapters_merged": 13,
    "total_from_chapters": 250,
    "cross_chapter_duplicates": 15,
    "final": 235
  }
}
```

## Deduplication Algorithm

Same as item-curator, applied across chapter boundaries:

### Step 1: Collect All Items

Load all `_curated.json` files and tag each item with its source chapter:

```python
all_items = []
for chapter_dir in chapter_dirs:
    curated = load_json(chapter_dir / "_curated.json")
    for item in curated["items"]:
        item["chapters"] = [curated["chapter"]]
        all_items.append(item)
```

### Step 2: Group by Normalized Name

```python
def normalize(name):
    return name.lower().strip().replace("-", " ").replace("_", " ")

groups = defaultdict(list)
for item in all_items:
    key = normalize(item["name"])
    groups[key].append(item)
```

### Step 3: Merge Duplicates

For each group with multiple items:

1. **Same type required**: Only merge if items have same type (rule, concept, etc.)
2. **Pick best excerpt**: Keep the longest/most complete level_2 content
3. **Combine sources**: Merge all source locations into array
4. **Track chapters**: Record all contributing chapters
5. **Preserve best metadata**: Keep most complete tags, category

```python
def merge_group(items):
    if len(items) == 1:
        return items[0]

    # Sort by level_2 explanation length (longest first)
    items.sort(key=lambda x: len(x["level_2"]["explanation"]), reverse=True)
    merged = items[0].copy()

    # Combine sources and chapters
    all_sources = []
    all_chapters = []
    all_tags = set()

    for item in items:
        all_sources.extend(item["sources"])
        all_chapters.extend(item["chapters"])
        all_tags.update(item["level_1"]["tags"])

    merged["sources"] = list(set(all_sources))
    merged["chapters"] = sorted(set(all_chapters))
    merged["level_1"]["tags"] = sorted(all_tags)

    return merged
```

### Step 4: Semantic Similarity Check (Optional)

For items with different names but potentially same concept:

- Calculate Jaccard similarity on excerpt words
- If similarity >= 0.7 AND same type: Flag for review (don't auto-merge)
- Add to stats as "potential_duplicates"

## Process Summary

1. Load all `_curated.json` files from chapter directories
2. Tag each item with source chapter
3. Group by normalized name
4. Merge exact-name duplicates (same type only)
5. Check for semantic duplicates (flag, don't merge)
6. Write merged output with stats

## Stats Tracking

Track and report:
- `chapters_merged`: Number of chapters processed
- `total_from_chapters`: Sum of items from all chapters
- `cross_chapter_duplicates`: Number of items merged (original - final)
- `potential_semantic_duplicates`: Pairs flagged for manual review
- `final`: Final item count after deduplication
