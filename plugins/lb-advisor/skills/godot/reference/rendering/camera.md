---
topic: camera-systems
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-camera-2d
  - godot-camera-3d
  - godot-spring-arm-3d
---

# Camera Systems

Camera patterns for 2D and 3D games.

## Camera Follow (2D) {#follow}

Smooth camera following with built-in smoothing:

```gdscript
# Camera2D as child of player - uses built-in smoothing
extends Camera2D

func _ready() -> void:
    position_smoothing_enabled = true
    position_smoothing_speed = 5.0  # Lower = smoother, higher = snappier
```

### Manual Follow with Lerp

For more control, follow a separate target:

```gdscript
extends Camera2D

@export var target: Node2D
@export var follow_speed: float = 5.0

func _physics_process(delta: float) -> void:
    if target:
        global_position = global_position.lerp(target.global_position, 1.0 - exp(-follow_speed * delta))
```

## Camera Limits {#limits}

Constrain camera to level bounds:

```gdscript
extends Camera2D

func set_limits_from_tilemap(tilemap: TileMapLayer) -> void:
    var used_rect := tilemap.get_used_rect()
    var tile_size := tilemap.tile_set.tile_size

    limit_left = int(used_rect.position.x * tile_size.x)
    limit_top = int(used_rect.position.y * tile_size.y)
    limit_right = int(used_rect.end.x * tile_size.x)
    limit_bottom = int(used_rect.end.y * tile_size.y)

    limit_smoothed = true  # Smooth transitions at edges
```

### Static Room Limits

```gdscript
func _ready() -> void:
    limit_left = 0
    limit_top = 0
    limit_right = 1920
    limit_bottom = 1080
    limit_smoothed = true
```

## Screen Shake (2D) {#shake}

Perlin noise-based screen shake:

```gdscript
extends Camera2D

@export var max_shake_offset: float = 16.0
@export var shake_decay: float = 5.0

var _shake_intensity: float = 0.0
var _noise := FastNoiseLite.new()

func _ready() -> void:
    _noise.seed = randi()
    _noise.frequency = 4.0

func _physics_process(delta: float) -> void:
    _shake_intensity = max(_shake_intensity - shake_decay * delta, 0.0)

    if _shake_intensity > 0:
        var time := Time.get_ticks_msec() / 1000.0
        offset = Vector2(
            _noise.get_noise_2d(time * 100, 0),
            _noise.get_noise_2d(0, time * 100)
        ) * max_shake_offset * _shake_intensity
    else:
        offset = Vector2.ZERO

func shake(intensity: float = 1.0) -> void:
    _shake_intensity = clamp(intensity, 0.0, 1.0)
```

**Usage:**
```gdscript
# From anywhere
camera.shake(0.5)  # Medium shake
camera.shake(1.0)  # Full shake
```

## Camera Zoom (2D) {#zoom}

Smooth zoom in/out:

```gdscript
extends Camera2D

@export var min_zoom: float = 0.5
@export var max_zoom: float = 2.0
@export var zoom_speed: float = 5.0

var _target_zoom: float = 1.0

func _input(event: InputEvent) -> void:
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_WHEEL_UP:
            _target_zoom = min(_target_zoom * 1.1, max_zoom)
        elif event.button_index == MOUSE_BUTTON_WHEEL_DOWN:
            _target_zoom = max(_target_zoom / 1.1, min_zoom)

func _physics_process(delta: float) -> void:
    zoom = zoom.lerp(Vector2.ONE * _target_zoom, zoom_speed * delta)
```

## Multi-Target Camera {#multi-target}

Camera that frames multiple targets:

```gdscript
extends Camera2D

@export var targets: Array[Node2D] = []
@export var margin: float = 100.0
@export var min_zoom: float = 0.5
@export var max_zoom: float = 2.0

func _physics_process(delta: float) -> void:
    if targets.is_empty():
        return

    # Calculate bounding box of all targets
    var min_pos := targets[0].global_position
    var max_pos := targets[0].global_position

    for target in targets:
        min_pos = min_pos.min(target.global_position)
        max_pos = max_pos.max(target.global_position)

    # Center camera on midpoint
    var center := (min_pos + max_pos) / 2.0
    global_position = global_position.lerp(center, 5.0 * delta)

    # Zoom to fit all targets
    var size := max_pos - min_pos + Vector2.ONE * margin * 2
    var screen_size := get_viewport_rect().size
    var zoom_x := screen_size.x / size.x
    var zoom_y := screen_size.y / size.y
    var target_zoom := clamp(min(zoom_x, zoom_y), min_zoom, max_zoom)
    zoom = zoom.lerp(Vector2.ONE * target_zoom, 3.0 * delta)
```

## FPS Camera (3D) {#fps-camera}

First-person mouse look:

```gdscript
extends Camera3D

@export var mouse_sensitivity: float = 0.002

func _ready() -> void:
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        # Rotate parent (character) horizontally
        get_parent().rotate_y(-event.relative.x * mouse_sensitivity)
        # Rotate camera vertically
        rotate_x(-event.relative.y * mouse_sensitivity)
        rotation.x = clamp(rotation.x, -PI/2, PI/2)
```

## Orbit Camera (3D) {#orbit}

Third-person orbit camera:

```gdscript
extends Node3D  # CameraPivot

@export var target: Node3D
@export var distance: float = 5.0
@export var mouse_sensitivity: float = 0.003
@export var min_pitch: float = -80.0
@export var max_pitch: float = 80.0

var _yaw: float = 0.0
var _pitch: float = 0.0

@onready var camera: Camera3D = $Camera3D

func _ready() -> void:
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED
    camera.position.z = distance

func _input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        _yaw -= event.relative.x * mouse_sensitivity
        _pitch -= event.relative.y * mouse_sensitivity
        _pitch = clamp(_pitch, deg_to_rad(min_pitch), deg_to_rad(max_pitch))

func _physics_process(delta: float) -> void:
    if target:
        global_position = target.global_position

    rotation = Vector3(_pitch, _yaw, 0)
```

## Spring Arm (3D) {#spring-arm}

Camera that avoids walls:

```gdscript
# Scene structure:
# CharacterBody3D
# └── CameraPivot (Node3D)
#     └── SpringArm3D
#         └── Camera3D

extends SpringArm3D

func _ready() -> void:
    spring_length = 5.0  # Default distance
    collision_mask = 1   # Layer to check for collision
    margin = 0.2         # Distance from collision point

    # SpringArm automatically shortens when obstructed
```

## Screen Shake (3D) {#shake-3d}

3D camera shake:

```gdscript
extends Camera3D

@export var max_shake_offset: float = 0.1
@export var max_shake_rotation: float = 0.05
@export var shake_decay: float = 5.0

var _shake_intensity: float = 0.0
var _noise := FastNoiseLite.new()

func _ready() -> void:
    _noise.seed = randi()

func _physics_process(delta: float) -> void:
    _shake_intensity = max(_shake_intensity - shake_decay * delta, 0.0)

    if _shake_intensity > 0:
        var time := Time.get_ticks_msec() / 1000.0
        h_offset = _noise.get_noise_2d(time * 100, 0) * max_shake_offset * _shake_intensity
        v_offset = _noise.get_noise_2d(0, time * 100) * max_shake_offset * _shake_intensity
        rotation.z = _noise.get_noise_2d(time * 50, time * 50) * max_shake_rotation * _shake_intensity

func shake(intensity: float = 1.0) -> void:
    _shake_intensity = clamp(intensity, 0.0, 1.0)
```

## Scene Setups

### 2D Platformer Camera
```
CharacterBody2D
└── Camera2D
    - position_smoothing_enabled = true
    - limit_left/right/top/bottom = room bounds
```

### 3D FPS Camera
```
CharacterBody3D
├── CollisionShape3D
└── Camera3D (at eye height)
```

### 3D TPS Camera
```
CharacterBody3D
├── CollisionShape3D
├── Model
└── CameraPivot (Node3D)
    └── SpringArm3D
        └── Camera3D
```
