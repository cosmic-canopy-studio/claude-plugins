---
topic: 3d-character-movement
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-character-body-3d
  - godot-fps-controller
---

# 3D Character Movement

CharacterBody3D patterns for player and NPC movement in 3D games.

## First-Person Movement {#fps}

Classic FPS controller with mouse look:

```gdscript
extends CharacterBody3D

@export var speed: float = 5.0
@export var jump_strength: float = 4.5
@export var mouse_sensitivity: float = 0.002

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")

@onready var camera: Camera3D = $Camera3D

func _ready() -> void:
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        rotate_y(-event.relative.x * mouse_sensitivity)
        camera.rotate_x(-event.relative.y * mouse_sensitivity)
        camera.rotation.x = clamp(camera.rotation.x, -PI/2, PI/2)

    if event.is_action_pressed("ui_cancel"):
        Input.mouse_mode = Input.MOUSE_MODE_VISIBLE

func _physics_process(delta: float) -> void:
    # Gravity
    if not is_on_floor():
        velocity.y -= gravity * delta

    # Jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_strength

    # Movement relative to camera direction
    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    velocity.x = direction.x * speed
    velocity.z = direction.z * speed

    move_and_slide()
```

**Input Actions Required:** `move_left`, `move_right`, `move_forward`, `move_back`, `jump`

## Third-Person Movement {#tps}

Movement relative to camera with separate camera node:

```gdscript
extends CharacterBody3D

@export var speed: float = 5.0
@export var rotation_speed: float = 10.0

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")

@onready var camera_pivot: Node3D = $CameraPivot
@onready var model: Node3D = $Model

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity.y -= gravity * delta

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = 4.5

    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")

    # Get camera's forward and right vectors (flattened to XZ plane)
    var cam_basis := camera_pivot.global_transform.basis
    var forward := -cam_basis.z
    forward.y = 0
    forward = forward.normalized()
    var right := cam_basis.x
    right.y = 0
    right = right.normalized()

    var direction := (forward * -input_dir.y + right * input_dir.x).normalized()

    if direction:
        velocity.x = direction.x * speed
        velocity.z = direction.z * speed

        # Rotate model to face movement direction
        var target_rotation := atan2(direction.x, direction.z)
        model.rotation.y = lerp_angle(model.rotation.y, target_rotation, rotation_speed * delta)
    else:
        velocity.x = move_toward(velocity.x, 0, speed)
        velocity.z = move_toward(velocity.z, 0, speed)

    move_and_slide()
```

## Jump and Gravity {#jump}

Standard jump with configurable gravity:

```gdscript
@export var jump_strength: float = 4.5
@export var fall_multiplier: float = 2.0  # Fall faster than rise

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        # Apply extra gravity when falling
        var gravity_mult := fall_multiplier if velocity.y < 0 else 1.0
        velocity.y -= gravity * gravity_mult * delta

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_strength

    move_and_slide()
```

## Slopes and Stairs {#slopes}

Handle slopes with floor settings:

```gdscript
func _ready() -> void:
    # In the inspector or code:
    floor_max_angle = deg_to_rad(45)  # Max walkable slope angle
    floor_snap_length = 0.5  # Snap to floor when walking down slopes
    floor_stop_on_slope = true  # Don't slide down slopes when standing still

func _physics_process(delta: float) -> void:
    # Disable snap when jumping
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_strength
        floor_snap_length = 0.0  # Disable snap during jump
    elif is_on_floor():
        floor_snap_length = 0.5  # Re-enable snap

    move_and_slide()
```

## Sprint {#sprint}

Hold to run faster:

```gdscript
@export var walk_speed: float = 5.0
@export var sprint_speed: float = 10.0
@export var sprint_fov_change: float = 10.0

@onready var camera: Camera3D = $Camera3D
var _base_fov: float

func _ready() -> void:
    _base_fov = camera.fov

func _physics_process(delta: float) -> void:
    var is_sprinting := Input.is_action_pressed("sprint") and is_on_floor()
    var current_speed := sprint_speed if is_sprinting else walk_speed

    # FOV effect when sprinting
    var target_fov := _base_fov + sprint_fov_change if is_sprinting else _base_fov
    camera.fov = lerp(camera.fov, target_fov, 10.0 * delta)

    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    velocity.x = direction.x * current_speed
    velocity.z = direction.z * current_speed

    move_and_slide()
```

## Crouch {#crouch}

Crouch with collision shape adjustment:

```gdscript
@export var stand_height: float = 2.0
@export var crouch_height: float = 1.0
@export var crouch_speed: float = 2.5

@onready var collision: CollisionShape3D = $CollisionShape3D
var _is_crouching: bool = false

func _physics_process(delta: float) -> void:
    var wants_crouch := Input.is_action_pressed("crouch")

    if wants_crouch and not _is_crouching:
        _start_crouch()
    elif not wants_crouch and _is_crouching:
        _try_stand()

    var current_speed := crouch_speed if _is_crouching else speed
    # ... rest of movement with current_speed

func _start_crouch() -> void:
    _is_crouching = true
    var shape := collision.shape as CapsuleShape3D
    shape.height = crouch_height
    collision.position.y = crouch_height / 2.0

func _try_stand() -> void:
    # Check if there's room to stand
    var space := get_world_3d().direct_space_state
    var query := PhysicsShapeQueryParameters3D.new()
    query.shape = CapsuleShape3D.new()
    (query.shape as CapsuleShape3D).height = stand_height
    query.transform = global_transform
    query.transform.origin.y += stand_height / 2.0

    if space.intersect_shape(query).is_empty():
        _is_crouching = false
        var shape := collision.shape as CapsuleShape3D
        shape.height = stand_height
        collision.position.y = stand_height / 2.0
```

## Scene Setup

### FPS Setup
```
CharacterBody3D (root)
├── CollisionShape3D (CapsuleShape3D, height ~2m)
└── Camera3D (at eye height, y ~1.6)
```

### TPS Setup
```
CharacterBody3D (root)
├── CollisionShape3D
├── Model (Node3D with mesh)
└── CameraPivot (Node3D)
    └── SpringArm3D
        └── Camera3D
```

**Collision Settings:**
- `collision_layer`: What this body IS
- `collision_mask`: What this body COLLIDES WITH
- `floor_max_angle`: Maximum walkable slope (default: 45 degrees)
