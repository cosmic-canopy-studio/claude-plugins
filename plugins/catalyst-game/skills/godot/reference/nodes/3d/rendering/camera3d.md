---
class: Camera3D
category: nodes/3d/rendering
complexity: intermediate
tags: [3d, camera, viewport, rendering, projection]
---

# Camera3D

**Inherits:** Node3D < Node < Object
**Inherited By:** XRCamera3D

Camera node, displays from a point of view.

## Description

Camera3D is a special node that displays what is visible from its current location. Cameras register themselves in the nearest Viewport node (when ascending the tree). Only one camera can be active per viewport. If no viewport is available ascending the tree, the camera will register in the global viewport. In other words, a camera just provides 3D display capabilities to a Viewport, and, without one, a scene registered in that Viewport (or higher viewports) can't be displayed.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `projection` | `ProjectionType` | `0` | Camera's projection mode (perspective/orthogonal/frustum) |
| `fov` | `float` | `75.0` | Field of view angle in degrees (perspective only) |
| `size` | `float` | `1.0` | Camera size in meters (orthogonal/frustum only) |
| `near` | `float` | `0.05` | Distance to near culling boundary |
| `far` | `float` | `4000.0` | Distance to far culling boundary |
| `current` | `bool` | `false` | If true, this camera is the active camera |
| `cull_mask` | `int` | `1048575` | Which layers are rendered by this camera |
| `keep_aspect` | `KeepAspect` | `1` | Axis to lock during FOV adjustments |
| `h_offset` | `float` | `0.0` | Horizontal offset of camera viewport |
| `v_offset` | `float` | `0.0` | Vertical offset of camera viewport |
| `frustum_offset` | `Vector2` | `Vector2(0, 0)` | Camera's frustum offset (FRUSTUM mode only) |
| `environment` | `Environment` | | Environment to use for this camera |
| `attributes` | `CameraAttributes` | | Camera attributes to use |
| `doppler_tracking` | `DopplerTracking` | `0` | Doppler effect simulation mode |

## Key Methods

| Return | Method |
|--------|--------|
| `void` | `make_current()` |
| `bool` | `is_position_in_frustum(world_point: Vector3)` |
| `bool` | `is_position_behind(world_point: Vector3)` |
| `Vector3` | `project_ray_origin(screen_point: Vector2)` |
| `Vector3` | `project_ray_normal(screen_point: Vector2)` |
| `Vector2` | `unproject_position(world_point: Vector3)` |
| `Array[Plane]` | `get_frustum()` |
| `void` | `set_perspective(fov: float, z_near: float, z_far: float)` |
| `void` | `set_orthogonal(size: float, z_near: float, z_far: float)` |

## Enumerations

### ProjectionType
- **PROJECTION_PERSPECTIVE** (0): Perspective projection (objects get smaller with distance)
- **PROJECTION_ORTHOGONAL** (1): Orthogonal projection (objects stay same size)
- **PROJECTION_FRUSTUM** (2): Frustum projection (allows tilted frustum effects)

### KeepAspect
- **KEEP_WIDTH** (0): Preserves horizontal aspect (Vert- scaling, best for portrait)
- **KEEP_HEIGHT** (1): Preserves vertical aspect (Hor+ scaling, best for landscape)

### DopplerTracking
- **DOPPLER_TRACKING_DISABLED** (0): Disables Doppler effect simulation
- **DOPPLER_TRACKING_IDLE_STEP** (1): Track objects changed in `_process`
- **DOPPLER_TRACKING_PHYSICS_STEP** (2): Track objects changed in `_physics_process`

## Property Details

### fov

The camera's field of view angle (in degrees). Only applicable in perspective mode. Since `keep_aspect` locks one axis, `fov` sets the other axis' field of view angle.

For reference, the default vertical FOV (75.0°) equals these horizontal FOVs:
- ~91.31° in 4:3 viewport
- ~101.67° in 16:10 viewport
- ~107.51° in 16:9 viewport
- ~121.63° in 21:9 viewport

### near / far

Distance to the near/far culling boundary relative to camera's local Z axis. Lower `near` values allow seeing objects closer, at the cost of precision. Values lower than default can lead to Z-fighting. Higher `far` values allow seeing further, but may reduce performance.

### cull_mask

The culling mask describing which VisualInstance3D layers are rendered. By default, all 20 user-visible layers are rendered.

**Note:** The cull_mask allows for 32 layers total. There are 12 additional layers used internally by the engine and not exposed in the editor. Setting cull_mask via script allows toggling these reserved layers, useful for editor plugins.

**Note:** VoxelGI, SDFGI and LightmapGI always consider all layers for global illumination. Set `GeometryInstance3D.gi_mode` to `GI_MODE_DISABLED` to exclude meshes.

Use `get_cull_mask_value()` and `set_cull_mask_value()` to adjust the mask easily.

### doppler_tracking

If not `DOPPLER_TRACKING_DISABLED`, simulates the Doppler effect for objects changed in particular `_process` methods.

**Note:** The Doppler effect will only be heard on AudioStreamPlayer3D nodes if their `doppler_tracking` is not set to `DOPPLER_TRACKING_DISABLED`.

### frustum_offset

The camera's frustum offset. This can create "tilted frustum" effects such as Y-shearing.

**Note:** Only effective if `projection` is `PROJECTION_FRUSTUM`.

## Method Details

### unproject_position()

Returns the 2D coordinate in the Viewport rectangle that maps to the given 3D point in world space.

**Note:** When using this to position GUI elements over a 3D viewport, use `is_position_behind()` to prevent them from appearing if the 3D point is behind the camera:

```gdscript
# This code block is part of a script that inherits from Node3D
# `control` is a reference to a node inheriting from Control
control.visible = not get_viewport().get_camera_3d().is_position_behind(global_transform.origin)
control.position = get_viewport().get_camera_3d().unproject_position(global_transform.origin)
```

### is_position_behind() / is_position_in_frustum()

Returns `true` if the given position is behind the camera / inside the camera's frustum respectively.

**Note:** A position which returns `false` from `is_position_behind()` may still be outside the camera's field of view.

## Quick Examples

### Basic 3D camera

```gdscript
@onready var camera: Camera3D = $Camera3D

func _ready() -> void:
    camera.make_current()
    camera.fov = 75.0
```

### Orthogonal camera for 2.5D games

```gdscript
@onready var camera: Camera3D = $Camera3D

func _ready() -> void:
    camera.set_orthogonal(10.0, 0.1, 100.0)
    camera.make_current()
```

### Third-person camera following

```gdscript
extends Camera3D

@export var target: Node3D
@export var follow_distance: float = 5.0
@export var follow_height: float = 2.0
@export var smoothness: float = 10.0

func _physics_process(delta: float) -> void:
    if target:
        var target_pos := target.global_position + Vector3(0, follow_height, follow_distance)
        global_position = global_position.lerp(target_pos, smoothness * delta)
        look_at(target.global_position, Vector3.UP)
```

## Common Patterns

### Mouse to 3D ray casting

```gdscript
@onready var camera: Camera3D = $Camera3D

func _input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        var mouse_pos := event.position
        var ray_origin := camera.project_ray_origin(mouse_pos)
        var ray_normal := camera.project_ray_normal(mouse_pos)
        # Use ray_origin and ray_normal for raycasting
```

### Check if object is visible

```gdscript
func is_object_visible(object_pos: Vector3) -> bool:
    var camera := get_viewport().get_camera_3d()
    if not camera:
        return false
    if camera.is_position_behind(object_pos):
        return false
    return camera.is_position_in_frustum(object_pos)
```

### Zoom with FOV

```gdscript
func zoom_camera(zoom_amount: float) -> void:
    $Camera3D.fov = clamp($Camera3D.fov - zoom_amount, 20.0, 120.0)
```

## Best Practices

- **Single Active Camera**: Only one camera should be current per viewport
- **Near Plane**: Keep `near` as high as possible to avoid Z-fighting
- **Far Plane**: Set `far` to the minimum needed to avoid unnecessary rendering
- **Culling Masks**: Use cull masks to control which layers are visible
- **Position Checking**: Use `is_position_behind()` when positioning 2D UI over 3D objects
- **FOV**: Default 75° works well for most games; lower for zoom, higher for wide-angle
- **Keep Aspect**: Use `KEEP_HEIGHT` for landscape games, `KEEP_WIDTH` for portrait

## Anti-Patterns

- Don't set `near` too low (causes Z-fighting)
- Don't set `far` unnecessarily high (performance cost)
- Don't forget to check `is_position_behind()` for UI positioning
- Don't enable multiple cameras in the same viewport
- Don't use extreme FOV values (< 20° or > 120°) unless intentional

## See Also

- [Camera2D](../../2d/rendering/camera2d.md) - For 2D camera systems
- [Viewport](../../core/viewport.md) - For multi-viewport setups
- [Environment](../../3d/environment.md) - For camera environment settings
- [SpringArm3D](springarm3d.md) - For collision-aware third-person cameras
