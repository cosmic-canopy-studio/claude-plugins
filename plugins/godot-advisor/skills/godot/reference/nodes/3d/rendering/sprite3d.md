---
class: Sprite3D
category: nodes/3d/rendering
complexity: beginner
tags: [3d, sprite, texture, rendering, billboard]
---

# Sprite3D

**Inherits:** SpriteBase3D < GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

2D sprite node in a 3D world.

## Description

A node that displays a 2D texture in a 3D environment. The texture displayed can be a region from a larger atlas texture, or a frame from a sprite sheet animation. See also SpriteBase3D where properties such as the billboard mode are defined.

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `frame` | `int` | `0` | Current frame to display from sprite sheet |
| `frame_coords` | `Vector2i` | `Vector2i(0, 0)` | Coordinates of the frame to display from sprite sheet |
| `hframes` | `int` | `1` | The number of columns in the sprite sheet |
| `region_enabled` | `bool` | `false` | If `true`, sprite will use region_rect |
| `region_rect` | `Rect2` | `Rect2(0, 0, 0, 0)` | The region of the atlas texture to display |
| `texture` | `Texture2D` | | Texture2D object to draw |
| `vframes` | `int` | `1` | The number of rows in the sprite sheet |

## Signals

- **frame_changed()**: Emitted when the frame changes
- **texture_changed()**: Emitted when the texture changes

## Property Details

### texture

Texture2D object to draw. If `GeometryInstance3D.material_override` is used, this will be overridden. The size information is still used.

### frame

Current frame to display from sprite sheet. `hframes` or `vframes` must be greater than 1. This property is automatically adjusted when `hframes` or `vframes` are changed to keep pointing to the same visual frame (same column and row). If that's impossible, this value is reset to `0`.

### frame_coords

Coordinates of the frame to display from sprite sheet. This is an alias for the `frame` property. `hframes` or `vframes` must be greater than 1.

### hframes / vframes

The number of columns/rows in the sprite sheet. When this property is changed, `frame` is adjusted so that the same visual frame is maintained (same row and column). If that's impossible, `frame` is reset to `0`.

### region_enabled

If `true`, the sprite will use `region_rect` and display only the specified part of its texture.

### region_rect

The region of the atlas texture to display. `region_enabled` must be `true`.

## Quick Examples

### Basic 3D sprite

```gdscript
@onready var sprite: Sprite3D = $Sprite3D

func _ready() -> void:
    sprite.texture = preload("res://assets/tree.png")
    sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
```

### Sprite sheet in 3D

```gdscript
@onready var sprite: Sprite3D = $Sprite3D

func _ready() -> void:
    sprite.texture = preload("res://assets/explosion.png")
    sprite.hframes = 4
    sprite.vframes = 4

func animate_explosion() -> void:
    for i in range(16):
        sprite.frame = i
        await get_tree().create_timer(0.05).timeout
```

### Atlas region sprite

```gdscript
@onready var sprite: Sprite3D = $Sprite3D

func _ready() -> void:
    sprite.texture = preload("res://assets/atlas_3d.png")
    sprite.region_enabled = true
    sprite.region_rect = Rect2(0, 0, 64, 64)
```

## Common Patterns

### Billboard sprite for particles effect

```gdscript
@onready var sprite: Sprite3D = $Sprite3D

func _ready() -> void:
    sprite.billboard = BaseMaterial3D.BILLBOARD_ENABLED
    sprite.texture_filter = BaseMaterial3D.TEXTURE_FILTER_NEAREST
```

### Y-axis billboard (tree/grass)

```gdscript
@onready var sprite: Sprite3D = $TreeSprite

func _ready() -> void:
    sprite.billboard = BaseMaterial3D.BILLBOARD_FIXED_Y
    sprite.texture = preload("res://assets/tree.png")
```

## Best Practices

- **Billboard Mode**: Use `billboard` property from SpriteBase3D for sprites that should face the camera
- **Sprite Sheets**: Use `hframes` and `vframes` for simple sprite sheet animations
- **Material Override**: Be aware that `material_override` will override the texture
- **Performance**: Consider using GPU particles for many sprite instances

## Anti-Patterns

- Don't use Sprite3D for complex 3D models (use MeshInstance3D)
- Don't forget to set billboard mode for particle-like effects
- Don't use too many individual Sprite3D nodes (use MultiMeshInstance3D or particles)

## See Also

- [Sprite2D](../../2d/rendering/sprite2d.md) - For 2D sprites
- [AnimatedSprite3D](animatedsprite3d.md) - For animated 3D sprites
- [SpriteBase3D](spritebase3d.md) - Parent class with billboard properties
- [MeshInstance3D](meshinstance3d.md) - For proper 3D models
