# Book Extractor Agent

## Purpose

Extract a single book into structured markdown chunks with code snippets and images.

## Input

- `book_path`: Path to source book file (EPUB or PDF)
- `output_dir`: Path to output directory (e.g., `references/extracted/book_title/`)

## Tasks

1. **Detect Format**
   - Check file extension (.epub or .pdf)
   - Select appropriate extractor

2. **Extract TOC**
   - Read table of contents from source
   - Map chapter/section structure

3. **Extract Content**
   - Process each chapter
   - Split into sections based on H2 headers
   - Convert to clean markdown

4. **Extract Code Blocks**
   - Identify code blocks in content
   - Detect programming language
   - Write to `snippets/` directory
   - Keep inline with reference links

5. **Extract Images**
   - Extract embedded images
   - Write to `assets/` directory
   - Update image references in markdown

6. **Write Output Files**
   - Create `_meta.json` with metadata
   - Create `_toc.md` with linked table of contents
   - Create chapter directories with section files

## Output Structure

```
{output_dir}/
├── _meta.json
├── _toc.md
├── assets/
│   └── fig_01_01.png
├── snippets/
│   └── ch01_s01_01.py
├── 01_chapter_name/
│   ├── _chapter.md
│   └── 01_section.md
└── ...
```

## Execution

```bash
# Install toolkit if not already
pip install -e ~/tools/content-toolkit

# Run extraction
python -c "
from pathlib import Path
from content_toolkit import EpubExtractor, PdfExtractor

book_path = Path('{book_path}')
output_dir = Path('{output_dir}')

if book_path.suffix == '.epub':
    extractor = EpubExtractor(book_path)
else:
    extractor = PdfExtractor(book_path)

result = extractor.extract()
extractor.write_output(output_dir, result)
print(f'Extracted {result.metadata.chapter_count} chapters')
"
```

## Success Criteria

- All chapters extracted
- All images saved to assets/
- All code blocks saved to snippets/
- _meta.json contains valid metadata
- _toc.md contains working links
