# Two-Phase Extraction Methodology

## The Problem

Single-pass extraction tries to do both **extract** and **filter** in one step:

```
Section → Extract with quality judgment → Final items
```

This is hard to calibrate:
- Too permissive: 889 concepts (noise)
- Too strict: 2 concepts (missed items)

The fundamental issue: **you can't apply good judgment without full context**.

---

## The Solution: Extract → Review

Separate extraction from quality judgment:

```
Phase 1: Extract (permissive, parallel)
         ↓
    _candidates/
         ↓
Phase 2: Review (holistic, quality tests)
         ↓
    _analysis/
```

### Why This Works

| Aspect | Single-Pass | Two-Phase |
|--------|-------------|-----------|
| Extraction | Must be precise | Can be permissive |
| Context | One section at a time | All sections visible |
| Deduplication | String matching | Semantic understanding |
| Synthesis | Not possible | Finds emergent patterns |
| Calibration | Hard to tune | Adjust review phase only |

---

## Phase 1: Candidate Extraction

**Agent:** `candidate-extractor`
**Skill:** `extract-candidates`

### Philosophy

> **Be inclusive, not selective.** It's better to extract 20 candidates and have 15 filtered out than to miss 5 genuine items.

### Behavior

- Read ONE markdown section file
- Extract ANYTHING that might be a concept, pattern, rule, anti-pattern, or example
- Record source location and raw context
- Note uncertainty ("might also be an anti-pattern")
- Write to `_candidates/{section}.json`

### Parallelization

Run up to 10 candidate-extractor agents simultaneously. Each processes one file independently.

### Output Format

```json
{
  "source": "03_3_shatter_long_functions/01_31_five_lines.md",
  "extracted_at": "2025-12-21T15:30:00",
  "candidates": [
    {
      "category": "rule",
      "name": "Five Lines",
      "raw_context": "### 3.1 Rule: Five Lines...",
      "source_location": {
        "line_start": 1,
        "line_end": 15,
        "heading": "3.1 Rule: Five Lines"
      },
      "notes": "Core rule of the book. Very explicit."
    }
  ]
}
```

---

## Phase 2: Curation & Synthesis

**Agents:** `candidate-validator` → `item-curator` → `theme-synthesizer` → `output-formatter`
**Skill:** `curate-knowledge`

### Philosophy

> With full context, apply **quality judgment** to filter, merge, and synthesize.

### Behavior

1. **Load** all candidate JSON files
2. **Group** similar candidates across sections
3. **Apply quality tests** (see below)
4. **Merge** duplicates, keeping best definition
5. **Identify themes** that span multiple sections
6. **Write** curated output to `_analysis/`

### Quality Tests

#### 1. Glossary Test (Concepts)

> Would this term and definition make sense in the book's glossary?

**YES:** "Refactoring - changing code to make it more readable without changing behavior"
**NO:** "Figure 3.2" (navigation), "The code" (too generic)

#### 2. Cookbook Test (Patterns)

> Would this be a clear recipe a developer could follow?

**YES:** "Extract Method - 1. Select code, 2. Create new method, 3. Replace with call"
**NO:** Vague descriptions without steps

#### 3. Common Mistakes Appendix Test (Anti-Patterns)

> Would a developer recognize this as a named bad practice with clear symptoms?

**YES:** "Long Methods - methods over 5 lines are hard to understand"
**NO:** Section headers, sentence fragments

### Output Structure

```
_analysis/
├── _index.json        # Level 1: Cards for search
├── _themes.md         # Cross-cutting themes
├── _summary.json      # Counts and metadata
├── rules.md           # Level 2: Structured reference
├── patterns.md
├── concepts.md
├── anti_patterns.md
├── examples.md
└── items/             # Level 3: Full detail
    └── {id}/_full.md
```

---

## Progressive Disclosure (3 Levels)

Output is formatted in 3 levels for different use cases:

### Level 1: Card (Search/Scanning)

**Location:** `_index.json`

```json
{
  "id": "rule-five-lines",
  "name": "Five Lines",
  "type": "rule",
  "summary": "Methods should have no more than 5 lines.",
  "tags": ["method-length", "readability"]
}
```

**Use case:** Quick search, filtering by tag, scanning available knowledge.

### Level 2: Structured (~100-200 words)

**Location:** `{type}.md`

```markdown
## Five Lines
**Type:** Rule | **Sources:** Chapter 3
**Statement:** A method should not contain more than 5 lines.
**When to Apply:** Any method exceeding 5 lines.
**Related:** Prevents "Long Methods" smell.
```

**Use case:** Quick reference during development.

### Level 3: Rich (Full Context)

**Location:** `items/{id}/_full.md`

- Full explanation with quotes from source
- All code examples
- Cross-references to related items
- Source attribution with line numbers

**Use case:** Deep understanding, learning new concepts.

---

## Test Results

Tested on "Five Lines of Code" by Christian Clausen:

### Phase 1 Results

| Category | Candidates |
|----------|------------|
| Patterns | 15 |
| Rules | 20 |
| Concepts | 40 |
| Anti-Patterns | 15 |
| Examples | 46 |
| **Total** | **116** |

### Phase 2 Results

| Category | Candidates | Kept | Merged | Discarded |
|----------|------------|------|--------|-----------|
| Patterns | 15 | 15 | 3 | 0 |
| Rules | 20 | 13 | 7 | 4 |
| Concepts | 40 | 35 | 5 | 5 |
| Anti-Patterns | 15 | 13 | 2 | 2 |
| Examples | 46 | 20 | 8 | 26 |

**Pass rate:** 82.8%
**Themes identified:** 13

### Key Themes Discovered

1. **Mechanical Refactoring Over Intuition** - Follow rules, not judgment
2. **Composition as Central Principle** - Favor composition over inheritance
3. **Compiler as Refactoring Assistant** - Use type system for safety
4. **Architecture Emerges from Local Rules** - Apply simple rules consistently

### Key Relationships Found

- **Rule: Five Lines** → prevents → **Anti-Pattern: Long Methods**
- **Rule: Never use if with else** → prevents → **Anti-Pattern: Hardcoded Decisions**
- **Pattern: Replace Type Code** → implements → **Concept: Late Binding**

---

## Best Practices

### Phase 1 Best Practices

1. **Extract generously** - False positives are OK
2. **Preserve context** - Include surrounding text (50-200 words)
3. **Note uncertainty** - "Might also be an anti-pattern"
4. **Record source location** - Line numbers, heading
5. **Don't filter** - That's Phase 2's job

### Phase 2 Best Practices

1. **Read all candidates first** - Full context before judging
2. **Group before filtering** - Similar items across sections
3. **Apply quality tests consistently** - Glossary, Cookbook, Mistakes
4. **Merge semantically** - Same concept, different words
5. **Look for themes** - Patterns that span the book
6. **Document relationships** - Rule X prevents Anti-pattern Y

### Calibration Tips

- If too few items: Loosen Phase 1 extraction criteria
- If too many low-quality items: Tighten Phase 2 quality tests
- If duplicates slip through: Improve Phase 2 grouping
- If themes are missed: Add explicit theme identification step

---

## When to Use Each Phase

### Phase 1 Only

Use for quick exploration:
- "What might be in this book?"
- "How many patterns does this book have?"

### Full Two-Phase

Use for production extraction:
- Building the knowledge base
- Creating book summaries
- Extracting actionable patterns

---

## Current Architecture

### Agents (5 minimal, single-purpose)

| Agent | Purpose | Lines |
|-------|---------|-------|
| `candidate-extractor` | Extract candidates from ONE section | ~60 |
| `candidate-validator` | Apply actionability tests | ~50 |
| `item-curator` | Merge duplicates, format output | ~70 |
| `theme-synthesizer` | Find cross-cutting themes | ~60 |
| `output-formatter` | Generate 3-level output | ~50 |

### Skills (3 minimal)

| Skill | Purpose |
|-------|---------|
| `extract-candidates` | Phase 1: spawn extractors in parallel |
| `curate-knowledge` | Phase 2: validate → curate → synthesize → format |
| `analyze-book` | Full pipeline: Phase 1 + Phase 2 |

### Deprecated (Removed)

- `section-analyzer` - Single-pass extraction (too complex)
- `book-aggregator` - Heuristic deduplication (replaced by semantic)
- `section-extractor` - Replaced by candidate-extractor
- `book-reviewer` - Split into 4 focused agents
