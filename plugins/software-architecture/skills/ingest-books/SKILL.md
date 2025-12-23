---
name: ingest-books
description: |
  Full pipeline: extract → analyze → build knowledge base. Runs the complete book ingestion workflow.
  TRIGGERS: "ingest books", "full pipeline", "process everything", "build complete knowledge base", "run full workflow", "ingest all".
  PROACTIVE: Use when user wants complete end-to-end processing of books into searchable knowledge.
---

# Ingest Books

Run the full knowledge extraction pipeline from raw books to searchable knowledge base.

## Pipeline Stages

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  extract-books  │ ──▶ │  analyze-books  │ ──▶ │ build-knowledge │
│   (parallel)    │     │   (parallel)    │     │  (sequential)   │
└─────────────────┘     └─────────────────┘     └─────────────────┘
        │                       │                       │
        ▼                       ▼                       ▼
   PDF/EPUB → MD          MD → Analysis          Analyses → Index
```

## Behavior

### Stage 1: Extract Books (Parallel)

1. Invoke `extract-books` skill
2. Processes all unextracted books in `references/books/`
3. Runs up to 3 books in parallel
4. Wait for all extractions to complete
5. Report extraction statistics

### Stage 2: Analyze Books (Parallel)

1. Invoke `analyze-books` skill
2. Processes all extracted but unanalyzed books
3. Runs up to 3 books in parallel
4. Each book spawns multiple section-analyzer agents (up to 10 parallel)
5. Wait for all analyses to complete
6. Report analysis statistics with quality metrics

### Stage 3: Build Knowledge Base (Sequential)

1. Invoke `build-knowledge` skill
2. Spawns 5 category-merger agents in parallel (one per category)
3. Wait for mergers to complete
4. Spawns knowledge-indexer agent (sequential)
5. Report final knowledge base statistics

## Examples

- "ingest all books"
- "run the full pipeline"
- "process everything and build knowledge base"
- "ingest books into knowledge base"

## Output Summary

```markdown
## Ingestion Complete

### Stage 1: Extraction
- Books extracted: 8
- Total chapters: 142
- Total sections: 1,247
- Images processed: 523
- Code snippets: 2,891

### Stage 2: Analysis
- Books analyzed: 8
- Patterns extracted: 156
- Rules extracted: 89
- Concepts extracted: 412
- Code examples: 892
- Anti-patterns: 134
- Average confidence: 0.78

### Stage 3: Knowledge Base
- Categories merged: 5
- Cross-book duplicates resolved: 47
- Search index entries: 1,683
- Cross-references created: 234

**Knowledge base ready at:** references/knowledge/
**Search with:** search-knowledge skill
```

## Error Handling

- If extraction fails for a book, continue with others
- If analysis fails for a book, continue with others
- If build-knowledge fails, report partial results
- Always report which stage failed and why

## Resumption

If pipeline is interrupted:
- Stage 1: Re-run will skip already-extracted books
- Stage 2: Re-run will skip already-analyzed books
- Stage 3: Always rebuilds from scratch (idempotent)

## Prerequisites

- Books must exist in `references/books/` as PDF or EPUB files
- Sufficient disk space for extracted content (~10x original size)
