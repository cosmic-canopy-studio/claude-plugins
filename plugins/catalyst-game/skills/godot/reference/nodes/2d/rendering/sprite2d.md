---
class: Sprite2D
category: nodes/2d/rendering
complexity: beginner
tags: [2d, sprite, texture, rendering]
---

# Sprite2D

**Inherits:** Node2D < CanvasItem < Node < Object

General-purpose sprite node.

## Description

A node that displays a 2D texture. The texture displayed can be a region from a larger atlas texture, or a frame from a sprite sheet animation.

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `centered` | `bool` | `true` | If `true`, texture is centered |
| `flip_h` | `bool` | `false` | If `true`, texture is flipped horizontally |
| `flip_v` | `bool` | `false` | If `true`, texture is flipped vertically |
| `frame` | `int` | `0` | Current frame to display from sprite sheet |
| `frame_coords` | `Vector2i` | `Vector2i(0, 0)` | Coordinates of the frame to display from sprite sheet |
| `hframes` | `int` | `1` | The number of columns in the sprite sheet |
| `offset` | `Vector2` | `Vector2(0, 0)` | The texture's drawing offset |
| `region_enabled` | `bool` | `false` | If `true`, texture is cut from a larger atlas texture |
| `region_filter_clip_enabled` | `bool` | `false` | If `true`, the area outside of region_rect is clipped |
| `region_rect` | `Rect2` | `Rect2(0, 0, 0, 0)` | The region of the atlas texture to display |
| `texture` | `Texture2D` | | Texture2D object to draw |
| `vframes` | `int` | `1` | The number of rows in the sprite sheet |

## Methods

| Return | Method |
|--------|--------|
| `Rect2` | `get_rect()` |
| `bool` | `is_pixel_opaque(pos: Vector2)` |

## Signals

- **frame_changed()**: Emitted when the frame changes
- **texture_changed()**: Emitted when the texture changes

## Property Details

### centered

If `true`, texture is centered.

**Note:** For games with a pixel art aesthetic, textures may appear deformed when centered. This is caused by their position being between pixels. To prevent this, set this property to `false`, or consider enabling `ProjectSettings.rendering/2d/snap/snap_2d_vertices_to_pixel` and `ProjectSettings.rendering/2d/snap/snap_2d_transforms_to_pixel`.

### offset

The texture's drawing offset.

**Note:** When you increase `offset.y` in Sprite2D, the sprite moves downward on screen (i.e., +Y is down).

### frame

Current frame to display from sprite sheet. `hframes` or `vframes` must be greater than 1. This property is automatically adjusted when `hframes` or `vframes` are changed to keep pointing to the same visual frame (same column and row). If that's impossible, this value is reset to `0`.

### frame_coords

Coordinates of the frame to display from sprite sheet. This is an alias for the `frame` property. `hframes` or `vframes` must be greater than 1.

### region_enabled

If `true`, texture is cut from a larger atlas texture. See `region_rect`.

**Note:** When using a custom Shader on a Sprite2D, the `UV` shader built-in will refer to the entire texture space. Use the `REGION_RECT` built-in to get the currently visible region defined in `region_rect` instead.

### region_filter_clip_enabled

If `true`, the area outside of the `region_rect` is clipped to avoid bleeding of the surrounding texture pixels. `region_enabled` must be `true`.

## Quick Examples

### Basic sprite display

```gdscript
@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
    sprite.texture = preload("res://assets/player.png")
    sprite.centered = true
```

### Sprite sheet animation

```gdscript
@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
    sprite.texture = preload("res://assets/player_sheet.png")
    sprite.hframes = 4
    sprite.vframes = 2

func animate_frame() -> void:
    sprite.frame = (sprite.frame + 1) % (sprite.hframes * sprite.vframes)
```

### Atlas region sprite

```gdscript
@onready var sprite: Sprite2D = $Sprite2D

func _ready() -> void:
    sprite.texture = preload("res://assets/atlas.png")
    sprite.region_enabled = true
    sprite.region_rect = Rect2(0, 0, 32, 32)
```

## Common Patterns

### Flip sprite based on movement direction

```gdscript
func update_sprite_direction(velocity: Vector2) -> void:
    if velocity.x != 0:
        $Sprite2D.flip_h = velocity.x < 0
```

### Check if mouse clicked on sprite

```gdscript
func _input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        if event.button_index == MOUSE_BUTTON_LEFT:
            var sprite: Sprite2D = $Sprite2D
            if sprite.get_rect().has_point(sprite.to_local(event.position)):
                print("Sprite clicked!")
```

### Check pixel opacity

```gdscript
func is_pixel_solid(local_pos: Vector2) -> bool:
    return $Sprite2D.is_pixel_opaque(local_pos)
```

**Note:** `is_pixel_opaque()` returns `false` if the sprite's texture is `null` or if the given position is invalid.

## Best Practices

- **Pixel Art**: For pixel art games, set `centered` to `false` to avoid texture deformation between pixels
- **Atlas Textures**: Use `region_enabled` with `region_rect` for atlas textures to save memory
- **Sprite Sheets**: Use `hframes` and `vframes` for simple sprite sheet animations
- **Complex Animations**: For complex animations, consider using AnimatedSprite2D instead
- **Frame Access**: Use `frame_coords` for coordinate-based frame access (alternative to `frame`)
- **Shader UV**: When using custom shaders, use `REGION_RECT` built-in instead of `UV` for region-enabled sprites

## Anti-Patterns

- Don't center sprites in pixel-art games without enabling pixel snapping
- Don't use Sprite2D for complex animations with many frames (use AnimatedSprite2D)
- Don't forget to check texture is not null before calling `is_pixel_opaque()`

## See Also

- [AnimatedSprite2D](animatedsprite2d.md) - For animation-focused sprites
- [Sprite3D](../../3d/rendering/sprite3d.md) - For 2D sprites in 3D space
- [TextureRect](../../../ui/texturerect.md) - For UI textures
