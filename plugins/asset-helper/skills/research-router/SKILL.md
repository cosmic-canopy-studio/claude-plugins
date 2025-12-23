---
name: research-router
description: Route research queries to appropriate KB locators based on keyword detection. Determines which tools are relevant and dispatches parallel searches.
---

# Research Router

Determine which KB locators to invoke based on query keywords.

## Tool Relevance Detection

### Aseprite Keywords
Invoke `kb-locator-aseprite` when query contains:
- pixel, pixelize, pixelate, pixel art
- sprite, spritesheet, sprite sheet
- retro, 8-bit, 16-bit, nes, snes, gameboy
- animation, frame, tag, loop
- indexed, color reduction, palette, dither

### Krita Keywords
Invoke `kb-locator-krita` when query contains:
- paint, painting, brush, digital art
- concept art, game art, character art
- filter, effect, blur, sharpen
- photo, image, edit, manipulation
- layer, export, flatten

### Blender Keywords
Invoke `kb-locator-blender` when query contains:
- 3D, model, mesh, vertex, polygon
- texture, material, UV, bake
- render, eevee, cycles
- animation, rig, armature, keyframe
- glTF, FBX, export

### Tiled Keywords
Invoke `kb-locator-tiled` when query contains:
- tilemap, tile map, tileset
- level, level design, map
- autotile, wang, terrain
- collision, layer, object
- tmx, godot export

## Routing Rules

### Always Search
- `web-researcher` - Always include for up-to-date info

### Keyword-Based Search
For each matching keyword category, add that tool's locator.

### Default: Search All
If no specific keywords match, search all 4 KB locators.

## Routing Examples

| Query | Tools to Search |
|-------|-----------------|
| "pixelize a photo" | aseprite, krita, web |
| "export model to Godot" | blender, web |
| "create sprite animation" | aseprite, web |
| "set up autotiling" | tiled, web |
| "concept art workflow" | krita, web |
| "best way to create game assets" | all + web |

## Output

Return list of agents to invoke:

```yaml
agents:
  - kb-locator-aseprite
  - kb-locator-krita
  - web-researcher
parallel: true  # All can run simultaneously
```

## Integration

Called by `asset-research` skill to determine which agents to dispatch before parallel search.
