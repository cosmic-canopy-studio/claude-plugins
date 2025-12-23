---
class: CanvasItem
source: repos/godot-docs/classes/class_canvasitem.rst
generated: 2025-12-21
---

# CanvasItem

**Inherits:** Node < Object

**Inherited By:** Control, Node2D

Abstract base class for everything in 2D space.

## Description

Abstract base class for everything in 2D space. Canvas items are laid out in a tree; children inherit and extend their parent's transform. CanvasItem is extended by Control for GUI-related nodes, and by Node2D for 2D game objects.

Any CanvasItem can draw. For this, `queue_redraw()` is called by the engine, then NOTIFICATION_DRAW will be received on idle time to request a redraw. Because of this, canvas items don't need to be redrawn on every frame, improving the performance significantly. Several functions for drawing on the CanvasItem are provided (see `draw_*` functions). However, they can only be used inside `_draw()`, its corresponding `Object._notification()` or methods connected to the `draw` signal.

Canvas items are drawn in tree order on their canvas layer. By default, children are on top of their parents, so a root CanvasItem will be drawn behind everything. This behavior can be changed on a per-item basis.

A CanvasItem can be hidden, which will also hide its children. By adjusting various other properties of a CanvasItem, you can also modulate its color (via `modulate` or `self_modulate`), change its Z-index, blend mode, and more.

**Important:** Properties like transform, modulation, and visibility are only propagated to *direct* CanvasItem child nodes. If there is a non-CanvasItem node in between, like Node or AnimationPlayer, the CanvasItem nodes below will have an independent position and modulate chain. See also `top_level`.

## Properties

| Type | Property | Default |
|------|----------|---------|
| ClipChildrenMode | clip_children | 0 |
| int | light_mask | 1 |
| Material | material | |
| Color | modulate | Color(1, 1, 1, 1) |
| Color | self_modulate | Color(1, 1, 1, 1) |
| bool | show_behind_parent | false |
| TextureFilter | texture_filter | 0 |
| TextureRepeat | texture_repeat | 0 |
| bool | top_level | false |
| bool | use_parent_material | false |
| int | visibility_layer | 1 |
| bool | visible | true |
| bool | y_sort_enabled | false |
| bool | z_as_relative | true |
| int | z_index | 0 |

## Methods

| Return Type | Method |
|-------------|--------|
| void | `_draw()` virtual |
| void | `draw_arc(center: Vector2, radius: float, start_angle: float, end_angle: float, point_count: int, color: Color, width: float = -1.0, antialiased: bool = false)` |
| void | `draw_char(font: Font, pos: Vector2, char: String, font_size: int = 16, modulate: Color = Color(1, 1, 1, 1))` const |
| void | `draw_circle(position: Vector2, radius: float, color: Color, filled: bool = true, width: float = -1.0, antialiased: bool = false)` |
| void | `draw_colored_polygon(points: PackedVector2Array, color: Color, uvs: PackedVector2Array = PackedVector2Array(), texture: Texture2D = null)` |
| void | `draw_line(from: Vector2, to: Vector2, color: Color, width: float = -1.0, antialiased: bool = false)` |
| void | `draw_multiline(points: PackedVector2Array, color: Color, width: float = -1.0, antialiased: bool = false)` |
| void | `draw_polygon(points: PackedVector2Array, colors: PackedColorArray, uvs: PackedVector2Array = PackedVector2Array(), texture: Texture2D = null)` |
| void | `draw_polyline(points: PackedVector2Array, color: Color, width: float = -1.0, antialiased: bool = false)` |
| void | `draw_rect(rect: Rect2, color: Color, filled: bool = true, width: float = -1.0)` |
| void | `draw_string(font: Font, pos: Vector2, text: String, alignment: HorizontalAlignment = 0, width: float = -1, font_size: int = 16, modulate: Color = Color(1, 1, 1, 1), justification_flags: BitField[JustificationFlag] = 3, direction: TextDirection = 0, orientation: TextOrientation = 0)` const |
| void | `draw_texture(texture: Texture2D, position: Vector2, modulate: Color = Color(1, 1, 1, 1))` |
| void | `draw_texture_rect(texture: Texture2D, rect: Rect2, tile: bool, modulate: Color = Color(1, 1, 1, 1), transpose: bool = false)` |
| RID | `get_canvas()` const |
| RID | `get_canvas_item()` const |
| Transform2D | `get_canvas_transform()` const |
| Vector2 | `get_global_mouse_position()` const |
| Transform2D | `get_global_transform()` const |
| Vector2 | `get_local_mouse_position()` const |
| Transform2D | `get_screen_transform()` const |
| Transform2D | `get_transform()` const |
| Rect2 | `get_viewport_rect()` const |
| Transform2D | `get_viewport_transform()` const |
| void | `hide()` |
| bool | `is_local_transform_notification_enabled()` const |
| bool | `is_transform_notification_enabled()` const |
| bool | `is_visible_in_tree()` const |
| Vector2 | `make_canvas_position_local(screen_point: Vector2)` const |
| InputEvent | `make_input_local(event: InputEvent)` const |
| void | `move_to_front()` |
| void | `queue_redraw()` |
| void | `set_notify_local_transform(enable: bool)` |
| void | `set_notify_transform(enable: bool)` |
| void | `show()` |

## Signals

- **draw**()
  - Emitted when the CanvasItem must redraw, after the related NOTIFICATION_DRAW notification, and before `_draw()` is called

- **hidden**()
  - Emitted when the CanvasItem becomes hidden

- **item_rect_changed**()
  - Emitted when the item's Rect2 boundaries (position or size) have changed, or when an action has taken place that may have affected these boundaries

- **visibility_changed**()
  - Emitted when the visibility (hidden/visible) changes

## Key Concepts

### Custom Drawing

- All drawing functions (`draw_*`) can only be called inside `_draw()`, `_notification()`, or methods connected to the `draw` signal
- Call `queue_redraw()` to request a redraw - the engine will call `_draw()` on idle time
- Canvas items don't redraw every frame for performance - only when requested

### Draw Order

- Children are drawn on top of parents by default
- Use `z_index` to control draw order
- `z_as_relative` determines if z_index is relative to parent or absolute
- `show_behind_parent` reverses the child/parent draw order

### Transform Propagation

- Transform, modulation, and visibility only propagate to direct CanvasItem children
- Non-CanvasItem nodes (like Node, AnimationPlayer) break the propagation chain
- Use `top_level` to make a node ignore its parent's transform

### Visibility

- Setting `visible = false` hides the node and all its children
- `is_visible_in_tree()` checks if node is actually visible (considers parent visibility)
- Signals: `visibility_changed`, `hidden`

### Modulation

- `modulate`: Affects this node and all children
- `self_modulate`: Only affects this node, not children
- Colors are multiplied down the tree

## Best Practices

- Use `queue_redraw()` instead of forcing redraws every frame for better performance
- Keep drawing code in `_draw()` - don't scatter it across multiple methods
- Use z_index strategically to control layering without restructuring the scene tree
- Remember that visibility and modulation propagate only through CanvasItem chains
- Use `top_level` when you need a child to ignore parent transforms (e.g., UI overlays)

## Common Patterns

```gdscript
# Basic custom drawing
extends Node2D

func _draw() -> void:
    # Draw a circle
    draw_circle(Vector2.ZERO, 50.0, Color.RED)

    # Draw a line
    draw_line(Vector2.ZERO, Vector2(100, 0), Color.BLUE, 2.0)

func _on_something_changed() -> void:
    queue_redraw()  # Request redraw on next idle frame
```

```gdscript
# Modulation for damage flash
extends Sprite2D

func take_damage() -> void:
    # Flash red using self_modulate (doesn't affect children)
    self_modulate = Color.RED
    await get_tree().create_timer(0.1).timeout
    self_modulate = Color.WHITE
```

```gdscript
# Z-index for layering
extends Node2D

func _ready() -> void:
    # Background layer
    $Background.z_index = -10

    # Player on default layer (0)
    $Player.z_index = 0

    # UI elements on top
    $UI.z_index = 10
```
