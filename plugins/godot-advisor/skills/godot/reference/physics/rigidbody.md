---
topic: rigidbody
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/stable/classes/class_rigidbody2d.html
  - https://docs.godotengine.org/en/stable/classes/class_rigidbody3d.html
  - https://docs.godotengine.org/en/stable/tutorials/physics/rigid_body.html
  - repos/godot_node_essentials/common/2d/astronaut_player_2d/astronaut_rigid_player_2d.gd
  - repos/godot_node_essentials/common/3d/astronaut_player_3d/astronaut_rigid_player_3d.gd
  - repos/godot_node_essentials/common/2d/ship_player_2d/ship_rigid_player_2d.gd
  - repos/godot_node_essentials/screens/rigid_body_2d/ragdoll_rigid_body_2d/ragdoll_rigid_body_2d.gd
  - repos/godot_node_essentials/common/2d/weapons_2d/rocket_weapon_2d/rocket_rigid_body_2d.gd
---

# RigidBody Physics

Physics-driven objects that respond to forces, impulses, and gravity in 2D and 3D.

## Overview

RigidBody2D/3D implements full physics simulation. Unlike CharacterBody, you cannot control a RigidBody directly. Instead, you must:

- Apply forces (continuous over time)
- Apply impulses (instant velocity changes)
- Override physics behavior with `_integrate_forces()`

**Key principle:** A rigid body maintains its shape and size even when forces are applied.

## Basic Setup {#setup}

### 2D Scene Structure

```
RigidBody2D (root)
├── CollisionShape2D
│   └── CapsuleShape2D or CircleShape2D
└── Sprite2D or AnimatedSprite2D
```

### 3D Scene Structure

```
RigidBody3D (root)
├── CollisionShape3D
│   └── CapsuleShape3D or SphereShape3D
└── MeshInstance3D
```

## Forces vs Impulses {#forces-impulses}

### Continuous Forces

Use `apply_central_force()` for continuous acceleration (call every frame):

```gdscript
extends RigidBody2D

@export var move_force_magnitude: float = 6000.0

func _physics_process(_delta: float) -> void:
    var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")

    if not direction.is_zero_approx():
        # Continuous force - safe to call every frame
        apply_central_force(direction * move_force_magnitude)
```

**Key:** Forces are time-dependent. They accelerate the body over time.

### Instant Impulses

Use `apply_central_impulse()` for instant velocity changes (one-time events):

```gdscript
extends RigidBody2D

@export var jump_impulse: float = 2000.0

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    if is_on_floor(state) and Input.is_action_just_pressed("jump"):
        # Impulse - only call once per event
        apply_central_impulse(Vector2.UP * jump_impulse)
```

**Key:** Impulses are time-independent. Applying them every frame creates framerate-dependent behavior (bad!).

### Positioned Forces/Impulses

Apply forces at specific points to create rotation:

```gdscript
# 2D: Apply force at position (creates torque)
apply_force(force: Vector2, position: Vector2)
apply_impulse(impulse: Vector2, position: Vector2)

# 3D: Apply torque directly
apply_torque(torque: Vector3)
apply_torque_impulse(torque: Vector3)
```

### Force Summary

| Method | When to Use | Frame Rate Dependent |
|--------|-------------|---------------------|
| `apply_central_force()` | Continuous acceleration (thrusters, movement) | No (delta-based) |
| `apply_central_impulse()` | One-time events (jumps, explosions) | No (instant) |
| `apply_force()` | Positioned force with rotation | No |
| `apply_impulse()` | Positioned instant change | No |

## Custom Physics Integration {#integrate-forces}

Override `_integrate_forces()` for direct physics state access:

```gdscript
extends RigidBody2D

@export var horizontal_speed: float = 800.0
@export var jump_impulse: float = 2000.0

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    # Direct velocity modification
    var direction := Input.get_axis("move_left", "move_right")
    state.linear_velocity.x = direction * horizontal_speed

    # Apply jump impulse
    if is_on_floor(state) and Input.is_action_pressed("jump"):
        state.linear_velocity.y = -jump_impulse
```

**When to use:**
- Player controllers requiring precise movement
- Overriding default gravity or damping
- Complex physics interactions

**Warning:** Setting `custom_integrator = true` disables internal forces (gravity, damping). You must handle everything manually.

### PhysicsDirectBodyState Access

The state parameter provides:

```gdscript
# Velocity
state.linear_velocity  # Current velocity
state.angular_velocity # Rotation speed

# Transform
state.transform        # Current position/rotation

# Forces (read-only)
state.total_gravity    # Current gravity vector
state.total_linear_damp
state.total_angular_damp

# Contact information
state.get_contact_count()
state.get_contact_local_normal(index: int)
state.get_contact_collider(index: int)
state.get_contact_impulse(index: int)

# Time
state.step  # Physics delta time
```

## Floor Detection {#floor-detection}

RigidBody doesn't have `is_on_floor()` built-in. Check contacts manually:

```gdscript
func is_on_floor(state: PhysicsDirectBodyState2D) -> bool:
    for contact_index in state.get_contact_count():
        var contact_normal := state.get_contact_local_normal(contact_index)
        # Check if contact normal points upward
        if contact_normal.dot(Vector2.UP) > 0.5:
            return true
    return false
```

**Important:** Set `max_contacts_reported` high enough (e.g., 4) to detect all contacts.

### 3D Floor Detection

```gdscript
func is_on_floor(state: PhysicsDirectBodyState3D) -> bool:
    for contact in state.get_contact_count():
        var contact_normal := state.get_contact_local_normal(contact)
        if contact_normal.dot(Vector3.UP) > 0.5:
            return true
    return false
```

### Custom Gravity Detection

For planet gravity or varying gravity directions:

```gdscript
@export var move_force: float = 40.0
@export var jump_initial_impulse: float = 18.0

var _gravity_direction := Vector3.DOWN

func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
    # Store gravity direction from physics state
    _gravity_direction = state.total_gravity.normalized()

    # Jump against gravity
    if Input.is_action_just_pressed("jump") and _is_on_floor(state):
        apply_central_impulse(-_gravity_direction * jump_initial_impulse)

func _is_on_floor(state: PhysicsDirectBodyState3D) -> bool:
    for contact in range(state.get_contact_count()):
        var contact_normal := state.get_contact_local_normal(contact)
        # Check if contact is "below" us relative to gravity
        if contact_normal.dot(-_gravity_direction) > 0.5:
            return true
    return false
```

## Freeze Modes {#freeze}

Control whether physics affects the body:

```gdscript
# Stop physics simulation
freeze = true

# Resume physics
freeze = false
```

### Freeze Mode Enum

```gdscript
enum FreezeMode {
    FREEZE_MODE_STATIC,    # No collision when moved (default)
    FREEZE_MODE_KINEMATIC  # Collides when moved
}

freeze_mode = RigidBody2D.FREEZE_MODE_KINEMATIC
```

**Key difference:**
- **STATIC:** Frozen body doesn't collide when you move it via code
- **KINEMATIC:** Frozen body collides with others when moved (useful for drag-and-drop)

### Selective Freezing

Lock specific axes:

```gdscript
# Lock rotation (prevents body from spinning)
lock_rotation = true

# 3D: Lock specific axes
axis_lock_linear_x = true   # Can't move on X
axis_lock_angular_y = true  # Can't rotate around Y
```

### Drag and Drop Pattern

```gdscript
extends RigidBody2D

var _dragging: bool = false

func _on_input_event(_viewport: Node, event: InputEvent, _shape_idx: int) -> void:
    if event is InputEventMouseButton and event.pressed:
        _dragging = true
        freeze = true
        freeze_mode = RigidBody2D.FREEZE_MODE_KINEMATIC

func _input(event: InputEvent) -> void:
    if event is InputEventMouseButton and not event.pressed and _dragging:
        _dragging = false
        freeze = false
        # Optional: throw the object
        var mouse_velocity := Input.get_last_mouse_velocity()
        apply_central_impulse(mouse_velocity * 0.5)

func _physics_process(_delta: float) -> void:
    if _dragging:
        global_position = get_global_mouse_position()
```

## Mass and Physics Properties {#properties}

```gdscript
# Mass (affects how forces move the body)
mass = 1.0

# Center of mass offset
center_of_mass_mode = RigidBody2D.CENTER_OF_MASS_MODE_CUSTOM
center_of_mass = Vector2(0, 10)  # Offset for top-heavy objects

# Damping (slows down over time)
linear_damp = 1.0   # Reduces linear velocity
angular_damp = 2.0  # Reduces rotation

# Gravity
gravity_scale = 1.0  # Multiplier for scene gravity (0 = no gravity)
```

### Physics Material

Add a PhysicsMaterial for friction and bounce:

```gdscript
# In editor: Create PhysicsMaterial resource
# Or in code:
var physics_material := PhysicsMaterial.new()
physics_material.friction = 0.8      # 0 = ice, 1 = sticky
physics_material.bounce = 0.5        # 0 = no bounce, 1 = perfect bounce
physics_material.absorbent = false   # If true, ignores bounce from other objects
physics_material.rough = false       # Affects friction calculation

physics_material_override = physics_material
```

## Contact Monitoring {#contacts}

Detect collisions via signals:

```gdscript
extends RigidBody2D

func _ready() -> void:
    # Enable contact monitoring
    contact_monitor = true
    max_contacts_reported = 4

    # Connect signals
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)

func _on_body_entered(body: Node) -> void:
    if body.is_in_group("enemy"):
        print("Hit enemy!")
```

**Important:** Set `max_contacts_reported` > 0 or no contacts will be recorded.

### Detailed Contact Info

Access contact details in `_integrate_forces()`:

```gdscript
func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    for i in state.get_contact_count():
        var collider := state.get_contact_collider(i)
        var normal := state.get_contact_local_normal(i)
        var position := state.get_contact_local_position(i)
        var impulse := state.get_contact_impulse(i)

        print("Hit %s at %v with impulse %v" % [collider, position, impulse])
```

**Note:** `get_contact_impulse()` may return `Vector3.ZERO` on the first frame of collision (known issue).

## Explosion Force Pattern {#explosion}

Apply outward impulses to nearby bodies:

```gdscript
extends RigidBody2D

const BLAST_IMPULSE: float = 1500.0

@onready var explosion_area: Area2D = $ExplosionArea2D

func explode() -> void:
    var bodies := explosion_area.get_overlapping_bodies()

    for body in bodies:
        if body is RigidBody2D:
            var direction := global_position.direction_to(body.global_position)
            body.apply_central_impulse(BLAST_IMPULSE * direction)
```

## Ship Controller Pattern {#ship}

Apply force in facing direction:

```gdscript
extends RigidBody2D

@export var move_force_magnitude: float = 6000.0

@onready var pivot: Node2D = $Pivot

func _physics_process(_delta: float) -> void:
    var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")

    if not direction.is_zero_approx():
        apply_central_force(direction * move_force_magnitude)
        pivot.rotation = direction.angle()
```

### With Linear Damping

Stop the ship when input stops:

```gdscript
# Set in editor or _ready():
linear_damp = 2.0  # Ship slows down when no input
```

## Ragdoll Pattern {#ragdoll}

Break an object into frozen RigidBody parts:

```gdscript
extends RigidBody2D

func explode() -> void:
    # Hide main sprite
    $Sprite2D.visible = false

    # Release all child RigidBody2D parts
    for child: RigidBody2D in find_children("", "RigidBody2D", false):
        child.visible = true
        child.freeze = false
        # Apply random impulse
        var random_impulse := Vector2(randf_range(-1, 1), randf_range(-1, 1))
        child.apply_central_impulse(1000 * random_impulse)

    # Freeze parent
    freeze = true
```

**Setup:** Create child RigidBody2D nodes for each part (arm, leg, head, etc.), initially frozen and invisible.

## Character Controller (3D) {#character-3d}

Full character with movement and rotation:

```gdscript
extends RigidBody3D

@export var move_force: float = 20.0
@export var jump_initial_impulse: float = 10.0
@export var jump_additional_force: float = 5.0
@export var rotation_speed: float = 12.0

var _move_direction := Vector3.ZERO
var _last_strong_direction := Vector3.FORWARD

func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
    # Get input relative to camera
    var input := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    _move_direction = camera.global_basis * Vector3(input.x, 0.0, input.y)

    if _move_direction.length() > 0.2:
        _last_strong_direction = _move_direction.normalized()

    # Jump
    if Input.is_action_just_pressed("jump") and _is_on_floor(state):
        apply_central_impulse(Vector3.UP * jump_initial_impulse)
    # Hold jump for higher jump
    elif Input.is_action_pressed("jump") and not _is_on_floor(state):
        if linear_velocity.y > 0:
            apply_central_force(Vector3.UP * jump_additional_force)

    # Apply movement force
    apply_central_force(_move_direction * move_force)

    # Rotate to face movement
    _orient_character_to_direction(state.step)

func _orient_character_to_direction(delta: float) -> void:
    if _last_strong_direction.is_zero_approx():
        return

    var left_axis := Vector3.UP.cross(_last_strong_direction)
    var rotation_basis := Basis(left_axis, Vector3.UP, _last_strong_direction)
    rotation_basis = rotation_basis.orthonormalized()

    # Smooth rotation
    basis = basis.slerp(rotation_basis, delta * rotation_speed)

func _is_on_floor(state: PhysicsDirectBodyState3D) -> bool:
    for contact in state.get_contact_count():
        if state.get_contact_local_normal(contact).dot(Vector3.UP) > 0.5:
            return true
    return false
```

## Continuous Collision Detection {#ccd}

Prevent fast-moving objects from tunneling through walls:

```gdscript
# 2D
continuous_cd = RigidBody2D.CCD_MODE_CAST_SHAPE

# 3D
continuous_cd = true
```

**CCD Modes (2D):**
- `CCD_MODE_DISABLED`: Fast but can tunnel
- `CCD_MODE_CAST_RAY`: Prevents tunneling with raycast
- `CCD_MODE_CAST_SHAPE`: Most accurate, uses shape casting

**When to use:** High-speed projectiles, fast-moving players.

## Common Patterns

### Initial Velocity

Set starting velocity for projectiles:

```gdscript
extends RigidBody2D

var direction := Vector2.ZERO

func _ready() -> void:
    # Set initial velocity immediately
    linear_velocity = 1500 * direction
```

### Despawn After Time

```gdscript
func _ready() -> void:
    # Fade out and despawn
    await get_tree().create_timer(5.0).timeout

    var tween := create_tween()
    tween.tween_property(self, "modulate", Color.TRANSPARENT, 1.0)
    await tween.finished
    queue_free()
```

### Collision Signal Setup

```gdscript
func _ready() -> void:
    body_entered.connect(_on_body_entered)
    contact_monitor = true
    max_contacts_reported = 1  # Only need first collision

func _on_body_entered(body: Node) -> void:
    explode()
```

## Best Practices

1. **Use impulses for one-time events**, forces for continuous
2. **Set `max_contacts_reported`** when using contact monitoring
3. **Override `_integrate_forces()`** for player controllers
4. **Enable CCD** for fast-moving objects (projectiles)
5. **Lock rotation** for objects that shouldn't spin
6. **Use linear_damp** to slow down without friction
7. **Set appropriate mass** - heavier objects harder to push
8. **PhysicsMaterial** controls surface properties (bounce, friction)

## Common Pitfalls

- Applying impulses every frame (creates framerate-dependent behavior)
- Not setting `max_contacts_reported` when using signals
- Setting position directly in `_physics_process()` (breaks physics)
- Forgetting to set `freeze_mode` for drag-and-drop
- Using RigidBody for precise platformer controls (use CharacterBody instead)

## When NOT to Use RigidBody

Use **CharacterBody2D/3D** instead when you need:
- Precise player control (platformers, top-down)
- No rotation or bouncing
- Predictable movement without physics quirks

Use **RigidBody** for:
- Physics-driven objects (balls, boxes, vehicles)
- Ragdolls and destructibles
- Objects affected by explosions
- Space/flight simulation with momentum
