---
class: Camera2D
category: nodes/2d/rendering
complexity: intermediate
tags: [2d, camera, viewport, rendering]
---

# Camera2D

**Inherits:** Node2D < CanvasItem < Node < Object

Camera node for 2D scenes.

## Description

Camera node for 2D scenes. It forces the screen (current layer) to scroll following this node. This makes it easier (and faster) to program scrollable scenes than manually changing the position of CanvasItem-based nodes.

Cameras register themselves in the nearest Viewport node (when ascending the tree). Only one camera can be active per viewport. If no viewport is available ascending the tree, the camera will register in the global viewport.

This node is intended to be a simple helper to get things going quickly, but more functionality may be desired to change how the camera works. To make your own custom camera node, inherit it from Node2D and change the transform of the canvas by setting `Viewport.canvas_transform` in Viewport (you can obtain the current Viewport by using `Node.get_viewport()`).

## Key Concepts

**Note:** The Camera2D node's `global_position` doesn't represent the actual position of the screen, which may differ due to applied smoothing or limits. You can use `get_screen_center_position()` to get the real position. Same for the node's `global_rotation` which may be different due to applied rotation smoothing. You can use `get_screen_rotation()` to get the current rotation of the screen.

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `anchor_mode` | `AnchorMode` | `1` | The Camera2D's anchor point |
| `custom_viewport` | `Node` | | Custom Viewport node attached to the Camera2D |
| `drag_horizontal_enabled` | `bool` | `false` | If `true`, camera only moves when reaching horizontal drag margins |
| `drag_horizontal_offset` | `float` | `0.0` | Relative horizontal drag offset |
| `drag_left_margin` | `float` | `0.2` | Left margin needed to drag the camera |
| `drag_right_margin` | `float` | `0.2` | Right margin needed to drag the camera |
| `drag_top_margin` | `float` | `0.2` | Top margin needed to drag the camera |
| `drag_bottom_margin` | `float` | `0.2` | Bottom margin needed to drag the camera |
| `drag_vertical_enabled` | `bool` | `false` | If `true`, camera only moves when reaching vertical drag margins |
| `drag_vertical_offset` | `float` | `0.0` | Relative vertical drag offset |
| `enabled` | `bool` | `true` | Controls whether the camera can be active or not |
| `ignore_rotation` | `bool` | `true` | If `true`, camera's view is not affected by rotation |
| `limit_bottom` | `int` | `10000000` | Bottom scroll limit in pixels |
| `limit_enabled` | `bool` | `true` | If `true`, limits will be enabled |
| `limit_left` | `int` | `-10000000` | Left scroll limit in pixels |
| `limit_right` | `int` | `10000000` | Right scroll limit in pixels |
| `limit_smoothed` | `bool` | `false` | If `true`, camera smoothly stops when reaches limits |
| `limit_top` | `int` | `-10000000` | Top scroll limit in pixels |
| `offset` | `Vector2` | `Vector2(0, 0)` | Camera's relative offset (useful for shake effects) |
| `position_smoothing_enabled` | `bool` | `false` | If `true`, camera's view smoothly moves towards target position |
| `position_smoothing_speed` | `float` | `5.0` | Speed in pixels per second of camera smoothing |
| `process_callback` | `Camera2DProcessCallback` | `1` | Camera's process callback |
| `rotation_smoothing_enabled` | `bool` | `false` | If `true`, camera's view smoothly rotates to align with target rotation |
| `rotation_smoothing_speed` | `float` | `5.0` | Angular speed of camera's rotation smoothing |
| `zoom` | `Vector2` | `Vector2(1, 1)` | Camera's zoom (higher values = more zoomed in) |

## Methods

| Return | Method |
|--------|--------|
| `void` | `align()` |
| `void` | `force_update_scroll()` |
| `float` | `get_drag_margin(margin: Side)` |
| `int` | `get_limit(margin: Side)` |
| `Vector2` | `get_screen_center_position()` |
| `float` | `get_screen_rotation()` |
| `Vector2` | `get_target_position()` |
| `bool` | `is_current()` |
| `void` | `make_current()` |
| `void` | `reset_smoothing()` |
| `void` | `set_drag_margin(margin: Side, drag_margin: float)` |
| `void` | `set_limit(margin: Side, limit: int)` |

## Enumerations

### AnchorMode
- **ANCHOR_MODE_FIXED_TOP_LEFT** (0): Camera's position is fixed so that the top-left corner is always at the origin
- **ANCHOR_MODE_DRAG_CENTER** (1): Camera's position takes into account offsets and screen size

### Camera2DProcessCallback
- **CAMERA2D_PROCESS_PHYSICS** (0): Camera updates during physics frames
- **CAMERA2D_PROCESS_IDLE** (1): Camera updates during process frames

## Property Details

### drag_horizontal_offset / drag_vertical_offset

The relative horizontal/vertical drag offset of the camera between the margins.

**Note:** Used to set the initial drag offset; determine the current offset; or force the current offset. It's not automatically updated when drag is enabled or the drag margins are changed.

### limit_smoothed

If `true`, the camera smoothly stops when it reaches its limits.

This property has no effect if `position_smoothing_enabled` is `false`.

**Note:** To immediately update the camera's position to be within limits without smoothing, even with this setting enabled, invoke `reset_smoothing()`.

### rotation_smoothing_enabled

If `true`, the camera's view smoothly rotates, via asymptotic smoothing, to align with its target rotation at `rotation_smoothing_speed`.

**Note:** This property has no effect if `ignore_rotation` is `true`.

### zoom

The camera's zoom. Higher values are more zoomed in. For example, a zoom of `Vector2(2.0, 2.0)` will be twice as zoomed in on each axis (the view covers an area four times smaller). In contrast, a zoom of `Vector2(0.5, 0.5)` will be twice as zoomed out on each axis (the view covers an area four times larger). The X and Y components should generally always be set to the same value, unless you wish to stretch the camera view.

**Note:** `FontFile.oversampling` does not take Camera2D zoom into account. This means that zooming in/out will cause bitmap fonts and rasterized (non-MSDF) dynamic fonts to appear blurry or pixelated unless the font is part of a CanvasLayer that makes it ignore camera zoom. To ensure text remains crisp regardless of zoom, you can enable MSDF font rendering.

## Method Details

### get_screen_center_position()

Returns the center of the screen from this camera's point of view, in global coordinates.

**Note:** The exact targeted position of the camera may be different. See `get_target_position()`.

### get_screen_rotation()

Returns the current screen rotation from this camera's point of view.

**Note:** The screen rotation can be different from `global_rotation` if the camera is rotating smoothly due to `rotation_smoothing_enabled`.

### get_target_position()

Returns this camera's target position, in global coordinates.

**Note:** The returned value is not the same as `global_position`, as it is affected by the drag properties. It is also not the same as the current position if `position_smoothing_enabled` is `true` (see `get_screen_center_position()`).

## Quick Examples

### Basic camera follow

```gdscript
extends CharacterBody2D

@onready var camera: Camera2D = $Camera2D

func _ready() -> void:
    camera.enabled = true
```

### Camera with limits

```gdscript
@onready var camera: Camera2D = $Camera2D

func _ready() -> void:
    camera.limit_left = 0
    camera.limit_top = 0
    camera.limit_right = 1920
    camera.limit_bottom = 1080
```

### Smooth camera follow

```gdscript
@onready var camera: Camera2D = $Camera2D

func _ready() -> void:
    camera.position_smoothing_enabled = true
    camera.position_smoothing_speed = 5.0
```

## Common Patterns

### Camera shake effect

```gdscript
@onready var camera: Camera2D = $Camera2D
var shake_amount: float = 0.0

func shake_camera(strength: float, duration: float) -> void:
    shake_amount = strength
    await get_tree().create_timer(duration).timeout
    shake_amount = 0.0
    camera.offset = Vector2.ZERO

func _process(delta: float) -> void:
    if shake_amount > 0:
        camera.offset = Vector2(
            randf_range(-shake_amount, shake_amount),
            randf_range(-shake_amount, shake_amount)
        )
```

### Drag margins for platformers

```gdscript
@onready var camera: Camera2D = $Camera2D

func _ready() -> void:
    camera.drag_horizontal_enabled = true
    camera.drag_vertical_enabled = true
    camera.drag_left_margin = 0.2
    camera.drag_right_margin = 0.2
    camera.drag_top_margin = 0.1
    camera.drag_bottom_margin = 0.3
```

### Zoom control

```gdscript
@onready var camera: Camera2D = $Camera2D

func zoom_in() -> void:
    camera.zoom = Vector2(2.0, 2.0)

func zoom_out() -> void:
    camera.zoom = Vector2(0.5, 0.5)

func smooth_zoom(target_zoom: Vector2, speed: float) -> void:
    var tween: Tween = create_tween()
    tween.tween_property(camera, "zoom", target_zoom, speed)
```

### Get camera world position

```gdscript
func get_camera_world_position() -> Vector2:
    return $Camera2D.get_screen_center_position()
```

## Best Practices

- **Real Position**: Use `get_screen_center_position()` to get the real camera position (not `global_position`)
- **Level Bounds**: Set limits to prevent camera from showing areas outside the level
- **Smooth Following**: Enable `position_smoothing_enabled` for smooth following behavior
- **Camera Shake**: Use `offset` for camera shake effects, not `position`
- **Single Camera**: Only one camera should be `enabled` per viewport
- **Pixel-Perfect**: For pixel-perfect camera, disable `position_smoothing_enabled`
- **Zoom Values**: Zoom values above 1.0 zoom in, below 1.0 zoom out
- **Uniform Zoom**: Keep X and Y zoom components equal unless intentionally stretching

## Anti-Patterns

- Don't use `global_position` for camera position (use `get_screen_center_position()`)
- Don't modify `position` for shake effects (use `offset`)
- Don't enable multiple cameras in the same viewport
- Don't use mismatched zoom X/Y values unless intentionally stretching
- Don't forget to call `reset_smoothing()` when teleporting the camera

## See Also

- [Viewport](../../core/viewport.md) - For multi-viewport setups
- [CanvasLayer](../../core/canvaslayer.md) - For UI that ignores camera
- [Camera3D](../../3d/rendering/camera3d.md) - For 3D camera systems
