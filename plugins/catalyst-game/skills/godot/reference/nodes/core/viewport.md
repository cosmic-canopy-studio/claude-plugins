---
class: Viewport
category: nodes/core
complexity: advanced
tags: [viewport, rendering, multiview, camera]
---

# Viewport

**Inherits:** Node < Object
**Inherited By:** SubViewport, Window

Abstract base class for viewports. Encapsulates drawing and interaction with a game world.

## Description

A Viewport creates a different view into the screen, or a sub-view inside another viewport. Child 2D nodes will display on it, and child Camera3D 3D nodes will render on it too.

Optionally, a viewport can have its own 2D or 3D world, so it doesn't share what it draws with other viewports.

Viewports can also choose to be audio listeners, so they generate positional audio depending on a 2D or 3D camera child of it.

Also, viewports can be assigned to different screens in case the devices have multiple screens.

Finally, viewports can also behave as render targets, in which case they will not be visible unless the associated texture is used to draw.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `world_2d` | `World2D` | | World2D resource used by this viewport |
| `world_3d` | `World3D` | | World3D resource used by this viewport |
| `own_world_3d` | `bool` | `false` | If true, viewport has its own separate World3D |
| `transparent_bg` | `bool` | `false` | If true, viewport background is transparent |
| `audio_listener_enable_2d` | `bool` | `false` | If true, viewport is a 2D audio listener |
| `audio_listener_enable_3d` | `bool` | `false` | If true, viewport is a 3D audio listener |
| `canvas_transform` | `Transform2D` | | The canvas transform for 2D rendering |
| `global_canvas_transform` | `Transform2D` | | The global canvas transform |
| `canvas_cull_mask` | `int` | `4294967295` | Which canvas layers are rendered |
| `disable_3d` | `bool` | `false` | If true, 3D rendering is disabled |
| `snap_2d_transforms_to_pixel` | `bool` | `false` | If true, 2D transforms snap to pixels |
| `snap_2d_vertices_to_pixel` | `bool` | `false` | If true, 2D vertices snap to pixels |
| `msaa_2d` | `MSAA` | `0` | MSAA mode for 2D rendering |
| `msaa_3d` | `MSAA` | `0` | MSAA mode for 3D rendering |
| `screen_space_aa` | `ScreenSpaceAA` | `0` | Screen-space anti-aliasing mode |
| `use_debanding` | `bool` | `false` | If true, uses debanding |
| `use_hdr_2d` | `bool` | `false` | If true, enables HDR for 2D |
| `use_taa` | `bool` | `false` | If true, enables TAA |
| `scaling_3d_mode` | `Scaling3DMode` | `0` | 3D scaling mode for resolution scaling |
| `scaling_3d_scale` | `float` | `1.0` | 3D scaling factor |
| `physics_object_picking` | `bool` | `false` | If true, enables physics object picking |

## Key Methods

| Return | Method |
|--------|--------|
| `Camera2D` | `get_camera_2d()` |
| `Camera3D` | `get_camera_3d()` |
| `World2D` | `find_world_2d()` |
| `World3D` | `find_world_3d()` |
| `ViewportTexture` | `get_texture()` |
| `Vector2` | `get_mouse_position()` |
| `Transform2D` | `get_final_transform()` |
| `Transform2D` | `get_screen_transform()` |
| `Rect2` | `get_visible_rect()` |
| `void` | `warp_mouse(position: Vector2)` |
| `void` | `push_input(event: InputEvent, in_local_coords: bool = false)` |
| `void` | `set_input_as_handled()` |
| `bool` | `is_input_handled()` |

## Signals

- **gui_focus_changed(node: Control)**: Emitted when a Control node grabs keyboard focus
- **size_changed()**: Emitted when the size of the viewport is changed

## Quick Examples

### Basic render target viewport

```gdscript
@onready var viewport: SubViewport = $SubViewport

func _ready() -> void:
    viewport.size = Vector2i(512, 512)
    viewport.transparent_bg = true
    var texture := viewport.get_texture()
    $Sprite2D.texture = texture
```

### Split-screen setup

```gdscript
# Player 1 viewport
@onready var viewport1: SubViewport = $SplitContainer/Viewport1
# Player 2 viewport
@onready var viewport2: SubViewport = $SplitContainer/Viewport2

func _ready() -> void:
    # Each viewport needs its own camera
    viewport1.get_camera_3d().make_current()
    viewport2.get_camera_3d().make_current()
```

### Custom 2D world viewport

```gdscript
@onready var viewport: SubViewport = $SubViewport

func _ready() -> void:
    # Create separate 2D world
    viewport.world_2d = World2D.new()
```

## Common Patterns

### Minimap viewport

```gdscript
@onready var minimap_viewport: SubViewport = $MinimapViewport
@onready var minimap_camera: Camera2D = $MinimapViewport/Camera2D

func _ready() -> void:
    minimap_viewport.size = Vector2i(200, 200)
    var texture := minimap_viewport.get_texture()
    $UI/Minimap.texture = texture
```

### Get mouse position in viewport

```gdscript
func _input(event: InputEvent) -> void:
    if event is InputEventMouseButton:
        var mouse_pos := get_viewport().get_mouse_position()
        print("Mouse at: ", mouse_pos)
```

## Best Practices

- **World Separation**: Use separate worlds for independent physics/rendering
- **Render Targets**: Use SubViewport for render-to-texture effects
- **Performance**: Consider resolution scaling with `scaling_3d_mode` and `scaling_3d_scale`
- **Input Handling**: Use `set_input_as_handled()` to prevent input propagation
- **Canvas Layers**: Each CanvasLayer is specific to one viewport

## Anti-Patterns

- Don't share CanvasLayers between viewports (not supported)
- Don't forget to set size for SubViewport
- Don't enable unnecessary features (MSAA, HDR) if not needed

## See Also

- [SubViewport](subviewport.md) - For render targets and multi-viewport setups
- [Camera2D](../2d/rendering/camera2d.md) - For 2D viewport cameras
- [Camera3D](../3d/rendering/camera3d.md) - For 3D viewport cameras
- [CanvasLayer](canvaslayer.md) - For layered 2D rendering
