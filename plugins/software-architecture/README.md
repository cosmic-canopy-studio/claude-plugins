# Software Architecture Knowledge Extraction System

Extract knowledge items (patterns, rules, concepts, examples, anti-patterns) from programming books and build a unified, searchable knowledge base.

## Quick Start

| Goal | Command |
|------|---------|
| Extract one book | `/extract-book five_lines_of_code` |
| Analyze one book | `/analyze-book five_lines_of_code` |
| Full pipeline | `/ingest-books` |
| Search knowledge | `/search-knowledge "refactoring patterns"` |

## Architecture Overview

```
PDF/EPUB → extract-book → Markdown sections
                              ↓
         analyze-book (two-phase extraction)
              ↓                    ↓
      Phase 1: Extract      Phase 2: Review
      (permissive,          (holistic,
       parallel)             quality tests)
              ↓                    ↓
        _candidates/          _analysis/
                              ↓
         build-knowledge → Unified knowledge base
                              ↓
         search-knowledge → Query results
```

See [METHODOLOGY.md](./METHODOLOGY.md) for details on the two-phase extraction approach.

---

## Agents

| Agent | Purpose | Phase |
|-------|---------|-------|
| `section-extractor` | Extract candidates from ONE section (permissive) | Phase 1 |
| `book-reviewer` | Review ALL candidates, filter & synthesize | Phase 2 |
| `book-extractor` | Extract PDF/EPUB to structured markdown | Extraction |
| `content-validator` | Validate extraction quality | Validation |
| `image-describer` | Generate AI descriptions for images | Extraction |
| `category-merger` | Merge one category across all books | Knowledge Base |
| `knowledge-indexer` | Build search index and cross-references | Knowledge Base |

### Deprecated Agents

| Agent | Replaced By |
|-------|-------------|
| `section-analyzer` | `section-extractor` + `book-reviewer` |
| `book-aggregator` | `book-reviewer` |

---

## Skills

### Book Processing

| Skill | Purpose | Triggers |
|-------|---------|----------|
| `extract-book` | Extract single book to markdown | "extract [book]" |
| `extract-books` | Batch extract all books | "extract all books" |
| `analyze-book` | Analyze single book (two-phase) | "analyze [book]" |
| `analyze-books` | Batch analyze all books | "analyze all books" |
| `validate-extractions` | Re-validate all extractions | "validate extractions" |

### Knowledge Base

| Skill | Purpose | Triggers |
|-------|---------|----------|
| `build-knowledge` | Build unified knowledge base | "build knowledge" |
| `search-knowledge` | Query the knowledge base | "search for [query]" |
| `ingest-books` | Full pipeline: extract → analyze → build | "ingest books" |

### Two-Phase Extraction

| Skill | Purpose | Phase |
|-------|---------|-------|
| `extract-candidates` | Run extractors in parallel | Phase 1 |
| `review-candidates` | Review and synthesize candidates | Phase 2 |

---

## Directory Structure

```
references/
├── books/                    # Source PDF/EPUB files
├── extracted/{book}/         # Extracted markdown
│   ├── _meta.json           # Book metadata
│   ├── _toc.md              # Table of contents
│   ├── _candidates/         # Phase 1 output (JSON)
│   ├── _analysis/           # Phase 2 output (curated MD)
│   ├── assets/              # Images
│   ├── snippets/            # Code snippets
│   └── {chapter}/           # Chapter directories
└── knowledge/               # Unified knowledge base
    ├── patterns/
    ├── rules/
    ├── concepts/
    ├── examples/
    └── anti_patterns/
```

---

## Workflow

### Single Book

```bash
# 1. Extract book from PDF/EPUB
/extract-book five_lines_of_code

# 2. Analyze book (two-phase extraction)
/analyze-book five_lines_of_code

# 3. Build knowledge base (after all books analyzed)
/build-knowledge
```

### Full Pipeline

```bash
# Extract, analyze, and build in one command
/ingest-books
```

---

## Test Results

Tested on "Five Lines of Code" by Christian Clausen:

| Metric | Value |
|--------|-------|
| Sections processed | 5 |
| Candidates extracted | 116 |
| Items kept | 96 (82.8%) |
| Items merged | 25 |
| Items discarded | 37 |
| Themes identified | 13 |

**Final output:** 15 patterns, 13 rules, 35 concepts, 13 anti-patterns, 20 examples

---

## Related Documentation

- [METHODOLOGY.md](./METHODOLOGY.md) - Two-phase extraction approach details
