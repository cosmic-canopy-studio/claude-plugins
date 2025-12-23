---
name: asset-research
description: Research asset creation techniques across all tools (Blender, Aseprite, Krita, Tiled). Searches knowledge base and web in parallel, returns quick summary with detailed guide written to file.
---

# Asset Research

Primary skill for researching game asset creation techniques.

## Triggers

Invoke this skill when user asks:
- "how to [action]" or "how do I [action]"
- "best way to [action]"
- "compare [approaches/tools] for [action]"
- "what's the workflow for [action]"
- "can I use [tool] for [action]"

## Workflow

### 1. Parse Intent

Extract from user query:
- **Action**: What they want to achieve
- **Input**: What they're starting with (photo, model, sketch, etc.)
- **Output**: What format/style they want
- **Constraints**: Any mentioned requirements (16-bit, retro, specific tool)

### 2. Dispatch Parallel Searches

Use `research-router` to determine which KB locators are relevant, then invoke in parallel:

**Always search:**
- `web-researcher` - Get up-to-date tutorials and docs

**Conditionally search based on relevance:**
- `kb-locator-aseprite` - pixel art, sprites, animation, retro
- `kb-locator-krita` - painting, concept art, filters, photo editing
- `kb-locator-blender` - 3D, modeling, textures, rendering
- `kb-locator-tiled` - tilemaps, level design, autotiling

### 3. Synthesize Results

Use `research-synthesizer` to:
- Combine all findings
- Rank approaches by fit
- Generate quick summary
- Write detailed guide to file

### 4. Respond

Return:
1. **Quick summary** in chat (best approach + alternatives table)
2. **Path to detailed guide** written to `guides/` directory

## Example Interaction

**User Query:**
> I have a photo of a lacrosse field that I want to pixelize to fit the retro 16-bit art theme

**Parse:**
```yaml
action: pixelize/convert to pixel art
input: photo (lacrosse field)
output: 16-bit retro pixel art
constraints: must look retro/authentic
```

**Relevant Tools:** aseprite, krita (photo + pixel art keywords)

**Parallel Search:**
- kb-locator-aseprite: photo-to-pixel, indexed-color, color-reduction
- kb-locator-krita: pixelize-filter, posterize
- web-researcher: "photo to pixel art tutorial"

**Response:**
```markdown
## Best Approach: Aseprite - Indexed Color Reduction

**Why:** For a lacrosse field photo, you'll want precise control over
how grass textures and field markings are rendered. Aseprite's indexed
color mode lets you hand-pick which details survive pixelization.

**Quick Start:**
1. Resize photo to 320x180 (16:9 at retro resolution)
2. Image > Color Mode > Indexed (16 colors)
3. Manually clean up field lines and important details

## Alternatives Compared

| Tool | Technique | Pros | Cons | Difficulty |
|------|-----------|------|------|------------|
| Aseprite | Indexed Color | Full control | Manual work | Intermediate |
| Krita | Pixelize Filter | Very fast | Less control | Beginner |
| Hybrid | Krita → Aseprite | Best results | Two tools | Intermediate |

**Detailed guide:** `guides/cross-tool/retro_photo-to-pixel.md`
```

## See Also

- [research-router](../research-router/SKILL.md) - Tool relevance detection
