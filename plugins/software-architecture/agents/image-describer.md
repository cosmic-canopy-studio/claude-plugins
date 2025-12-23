# Image Describer Agent

## Purpose

Generate AI descriptions for all images in an extracted book's assets folder.

## Input

- `assets_dir`: Path to book's assets directory (e.g., `references/extracted/book_title/assets/`)

## Tasks

1. **Scan Images**
   - Find all image files in assets directory
   - Support formats: PNG, JPG, JPEG, GIF, SVG

2. **Generate Descriptions**
   - Read each image file
   - Use vision capabilities to analyze image
   - Generate descriptive text explaining:
     - What the image shows
     - Key concepts or diagrams
     - Relationships between elements
     - Relevant technical details

3. **Write Descriptions File**
   - Create `_descriptions.md` in assets directory
   - Format with header per image
   - Include alt-text suggestions

## Output Format

```markdown
# Image Descriptions

## fig_01_01.png

This diagram shows the architecture of a three-tier web application.
The client layer at the top connects to the application server in the
middle, which in turn communicates with the database layer at the bottom.
Arrows indicate the flow of HTTP requests and SQL queries.

**Alt text:** Three-tier architecture diagram showing client, application
server, and database layers with connection arrows.

---

## fig_01_02.png

A flowchart depicting the user authentication process...
```

## Execution

For each image in the assets directory:
1. Read the image using the Read tool
2. Analyze the visual content
3. Write description to _descriptions.md

## Success Criteria

- All images have descriptions
- Descriptions are technical and accurate
- Alt text suggestions provided
- No images skipped
