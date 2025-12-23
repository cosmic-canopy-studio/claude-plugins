# Image Asset Analyzer Agent

Analyze, validate, and troubleshoot game image assets including sprites, tilesets, and textures. Combines Claude's visual understanding with ImageMagick for pixel-precise analysis.

## Agent Configuration

```yaml
name: image-asset-analyzer
model: sonnet
tools:
  - Read      # Visual analysis via Claude's multimodal capabilities
  - Bash      # ImageMagick commands for precise measurements
  - Glob      # Find image files
  - Grep      # Search import files
  - Write     # Generate reports
```

## When to Use This Agent

Use when you need to:
- **Validate sprites**: Check dimensions, transparency, edge content
- **Extract from tilesets**: Pull individual sprites with validation
- **Diagnose visual issues**: Analyze why sprites look wrong in-game
- **Audit asset consistency**: Verify all sprites in a set match expected properties
- **Compare sprites**: Check if extracted sprites match originals

## Capabilities

### 1. Visual Analysis (Claude Vision)
- Describe sprite content and visual style
- Identify obvious issues (missing parts, wrong orientation)
- Compare multiple sprites for consistency
- Analyze color palettes and art style

### 2. Precise Measurement (ImageMagick)
- Exact pixel dimensions
- Color count and palette extraction
- Alpha channel analysis
- Edge content detection
- Row-by-row pixel inspection

### 3. Tileset Operations
- Calculate grid dimensions from tileset size
- Extract individual tiles by index
- Validate extraction accuracy
- Handle spacing/padding in tilesets

### 4. Godot Integration
- Check .import file settings
- Validate texture filter modes
- Verify compression settings for pixel art

## Tool Scripts

The agent uses these shell scripts from `tools/image/`:

| Script | Purpose |
|--------|---------|
| `sprite-validator.sh` | Validate sprite dimensions and properties |
| `tileset-extractor.sh` | Extract tiles from tilesets with validation |
| `sprite-edge-checker.sh` | Analyze sprite edges for content/transparency |

## Example Workflows

### Validate a Sprite
```
Task image-asset-analyzer "Validate knight.png is 16x16 with proper transparency"
```

Agent will:
1. Run `sprite-validator.sh` for dimensions
2. Run `sprite-edge-checker.sh` for transparency
3. Use Read tool to visually verify content
4. Report findings

### Extract from Tileset
```
Task image-asset-analyzer "Extract tile 96 from roguelikeSheet.png as 16x16 to knight.png"
```

Agent will:
1. Analyze tileset dimensions
2. Calculate grid layout
3. Run `tileset-extractor.sh`
4. Validate extracted sprite
5. Report success with validation

### Diagnose Visual Issue
```
Task image-asset-analyzer "Investigate why the player sprite looks cut off at the bottom"
```

Agent will:
1. Read the sprite file visually
2. Run pixel-level edge analysis
3. Check Godot import settings
4. Compare with original tileset if available
5. Identify root cause

### Audit Sprite Set
```
Task image-asset-analyzer "Audit all sprites in assets/sprites/player/ for 16x16 consistency"
```

Agent will:
1. Glob for all PNG files
2. Run validator on each
3. Generate summary report
4. Flag any inconsistencies

## Input Requirements

When invoking, provide:
- **File paths**: Absolute paths to images
- **Expected dimensions**: If validating size
- **Tileset info**: Tile size, spacing, index for extraction
- **Issue description**: What looks wrong if diagnosing

## Output Format

The agent produces structured reports:

```
========================================
IMAGE ANALYSIS REPORT
========================================
File:       sprite.png
Dimensions: 16x16
Format:     PNG with alpha
Colors:     6
----------------------------------------
VISUAL ANALYSIS:
[Claude's description of sprite content]
----------------------------------------
VALIDATION:
✓ Dimensions match expected 16x16
✓ Has transparency (alpha channel)
✓ Bottom edge has content (feet visible)
----------------------------------------
RESULT: PASS
========================================
```

## Limitations

- **Cannot generate images**: Analysis only, no creation/editing
- **Limited spatial precision**: Claude can describe but not measure exact pixels
- **Requires ImageMagick**: For precise measurements
- **16x16 sprites are tiny**: Claude works better with larger images

## Best Practices

1. **Start with visual check**: Use Read tool first for quick assessment
2. **Use scripts for precision**: When exact measurements matter
3. **Check import settings**: Godot import can modify pixel art
4. **Compare to source**: Keep original tilesets for reference
5. **Validate after extraction**: Always verify extracted sprites

## Related Skills

- `godot-animated-sprite-2d`: AnimatedSprite2D patterns
- `godot-asset-selection`: Choosing appropriate assets
- `godot-tile-map-layer`: Tileset usage in Godot
