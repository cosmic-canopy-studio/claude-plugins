---
class: TextureRect
category: nodes/ui
complexity: basic
tags: [ui, control, texture, image, display]
last_updated: 2025-12-21
---

# TextureRect

**Inherits:** Control < CanvasItem < Node < Object

A control that displays a texture with various scaling and positioning options.

## Description

TextureRect is a UI control that displays a Texture2D resource. It provides flexible placement and scaling options through `stretch_mode` and `expand_mode` properties. Commonly used for icons, images, backgrounds, and visual UI elements.

## Common Use Cases

- UI icons and images
- Background images
- Item inventory slots
- Character portraits
- Decorative UI elements
- Image galleries

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `texture` | Texture2D | null | The texture to display |
| `stretch_mode` | StretchMode | STRETCH_SCALE | How texture scales/positions |
| `expand_mode` | ExpandMode | EXPAND_KEEP_SIZE | How minimum size is determined |
| `flip_h` | bool | false | Flip texture horizontally |
| `flip_v` | bool | false | Flip texture vertically |

## StretchMode Enumeration

| Value | Description |
|-------|-------------|
| `STRETCH_SCALE` | Scale to fit bounding rectangle |
| `STRETCH_TILE` | Tile within bounding rectangle |
| `STRETCH_KEEP` | Original size, top-left corner |
| `STRETCH_KEEP_CENTERED` | Original size, centered |
| `STRETCH_KEEP_ASPECT` | Scale maintaining aspect ratio |
| `STRETCH_KEEP_ASPECT_CENTERED` | Scale maintaining aspect ratio, centered |
| `STRETCH_KEEP_ASPECT_COVERED` | Scale to cover area (may clip) |

## ExpandMode Enumeration

| Value | Description |
|-------|-------------|
| `EXPAND_KEEP_SIZE` | Min size equals texture size |
| `EXPAND_IGNORE_SIZE` | Can shrink below texture size |
| `EXPAND_FIT_WIDTH` | Min width matches height (experimental) |
| `EXPAND_FIT_WIDTH_PROPORTIONAL` | Fit width, keep aspect (experimental) |
| `EXPAND_FIT_HEIGHT` | Min height matches width (experimental) |
| `EXPAND_FIT_HEIGHT_PROPORTIONAL` | Fit height, keep aspect (experimental) |

## Basic Example

```gdscript
extends Control

@onready var icon: TextureRect = $Icon

func _ready() -> void:
    # Load and display a texture
    icon.texture = load("res://assets/icons/sword.png")
    icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
```

## Background Image Pattern

```gdscript
extends Control

func setup_background(texture_path: String) -> void:
    var background: TextureRect = $Background
    background.texture = load(texture_path)
    background.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
    background.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
```

## Tiled Texture Pattern

```gdscript
extends TextureRect

func _ready() -> void:
    stretch_mode = STRETCH_TILE
    texture = load("res://assets/patterns/tile.png")
    custom_minimum_size = Vector2(400, 300)
```

## Dynamic Icon Swapping

```gdscript
extends Node

@onready var item_icon: TextureRect = $ItemIcon

func display_item(item_data: Dictionary) -> void:
    if item_data.has("icon_path"):
        item_icon.texture = load(item_data.icon_path)
        item_icon.tooltip_text = item_data.get("name", "")

func clear_icon() -> void:
    item_icon.texture = null
```

## Aspect Ratio Preservation

```gdscript
extends Control

func setup_portrait(portrait_texture: Texture2D) -> void:
    var portrait: TextureRect = $Portrait
    portrait.texture = portrait_texture
    portrait.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
    portrait.expand_mode = TextureRect.EXPAND_KEEP_SIZE

    # Container will respect texture's aspect ratio
    portrait.custom_minimum_size = Vector2(100, 100)
```

## Flip Animation

```gdscript
extends TextureRect

var flip_timer: float = 0.0

func _process(delta: float) -> void:
    flip_timer += delta
    if flip_timer >= 0.5:
        flip_h = not flip_h
        flip_timer = 0.0
```

## Common Patterns

### Responsive Icon Sizing

```gdscript
func create_responsive_icon(parent: Control, icon_texture: Texture2D) -> TextureRect:
    var icon := TextureRect.new()
    icon.texture = icon_texture
    icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
    icon.expand_mode = TextureRect.EXPAND_IGNORE_SIZE
    icon.custom_minimum_size = Vector2(32, 32)
    parent.add_child(icon)
    return icon
```

### Loading Placeholder

```gdscript
var placeholder_texture: Texture2D = preload("res://assets/ui/placeholder.png")

func load_async_texture(path: String, target: TextureRect) -> void:
    target.texture = placeholder_texture

    # Simulate async loading
    await get_tree().create_timer(0.5).timeout

    if ResourceLoader.exists(path):
        target.texture = load(path)
```

### Image Gallery Cell

```gdscript
func create_gallery_item(image_path: String) -> TextureRect:
    var cell := TextureRect.new()
    cell.texture = load(image_path)
    cell.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_COVERED
    cell.custom_minimum_size = Vector2(128, 128)
    cell.mouse_filter = Control.MOUSE_FILTER_STOP

    cell.gui_input.connect(func(event: InputEvent) -> void:
        if event is InputEventMouseButton and event.pressed:
            print("Clicked image: ", image_path)
    )

    return cell
```

## Best Practices

1. **Choose appropriate stretch_mode**: Match mode to use case (icons vs backgrounds)
2. **Preload common textures**: Use `preload()` for assets loaded at startup
3. **Mind performance**: Large textures consume VRAM; use compressed formats
4. **Set minimum sizes**: Helps with layout predictability
5. **Use mouse_filter**: Set to PASS if TextureRect shouldn't block clicks

## Common Pitfalls

- Using STRETCH_SCALE for icons (causes distortion; use STRETCH_KEEP_ASPECT instead)
- Forgetting to set `texture` property (displays nothing)
- EXPAND_FIT_WIDTH/HEIGHT modes are experimental and may cause layout issues
- Large uncompressed textures causing performance problems
- Not setting `mouse_filter = PASS` when texture should be non-interactive

## Performance Considerations

- TextureRect is lightweight for rendering
- Texture size affects VRAM usage, not node count
- Use texture atlases for many small icons
- Consider using TextureButton for interactive elements
- Mipmaps improve quality when scaling down

## Related Nodes

- **Sprite2D**: For 2D game objects (not UI)
- **TextureButton**: Interactive texture-based button
- **NinePatchRect**: Scalable UI element with border preservation
- **TextureProgressBar**: Texture-based progress indicator
- **Panel**: Stylable UI background container

## Source

Official Godot Documentation: [TextureRect](https://docs.godotengine.org/en/stable/classes/class_texturerect.html)
