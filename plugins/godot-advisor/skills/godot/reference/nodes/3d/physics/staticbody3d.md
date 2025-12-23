---
class: StaticBody3D
version: 2025.12.21
godot_version: "4.3"
sources:
  - repos/godot-docs/classes/class_staticbody3d.rst
---

# StaticBody3D

**Inherits:** PhysicsBody3D < CollisionObject3D < Node3D < Node < Object

**Inherited By:** AnimatableBody3D

A 3D physics body that can't be moved by external forces. When moved manually, it doesn't affect other bodies in its path.

## Description

A static 3D physics body. It can't be moved by external forces or contacts, but can be moved manually by other means such as code, AnimationMixer's (with `callback_mode_process` set to `ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS`), and RemoteTransform3D.

When StaticBody3D is moved, it is teleported to its new position without affecting other physics bodies in its path. If this is not desired, use AnimatableBody3D instead.

StaticBody3D is useful for completely static objects like floors and walls, as well as moving surfaces like conveyor belts and circular revolving platforms (by using `constant_linear_velocity` and `constant_angular_velocity`).

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `physics_material_override` | PhysicsMaterial | null | Physics material for friction and bounce |
| `constant_linear_velocity` | Vector3 | `Vector3(0, 0, 0)` | Constant velocity affecting touching bodies |
| `constant_angular_velocity` | Vector3 | `Vector3(0, 0, 0)` | Constant angular velocity affecting touching bodies |

## Properties Detail

### physics_material_override

The physics material override for the body.

If a material is assigned to this property, it will be used instead of any other physics material, such as an inherited one.

### constant_linear_velocity

The body's constant linear velocity. This does not move the body, but affects touching bodies, as if it were moving.

**Use cases:**
- Conveyor belts
- Moving platforms (for simple constant movement)
- Water currents

### constant_angular_velocity

The body's constant angular velocity. This does not rotate the body, but affects touching bodies, as if it were rotating.

**Use cases:**
- Rotating platforms
- Fans or windmills
- Centrifuges

## Basic Static Floor

```gdscript
extends StaticBody3D

# StaticBody3D needs no code for basic static collision
# Just add CollisionShape3D child with appropriate shape

func _ready() -> void:
    # Optional: Set physics material
    var material := PhysicsMaterial.new()
    material.friction = 0.8
    material.bounce = 0.0
    physics_material_override = material
```

## Conveyor Belt

```gdscript
extends StaticBody3D

@export var belt_speed: float = 5.0
@export var belt_direction: Vector3 = Vector3.FORWARD

func _ready() -> void:
    # Move objects touching the belt
    constant_linear_velocity = belt_direction.normalized() * belt_speed
```

## Rotating Platform

```gdscript
extends StaticBody3D

@export var rotation_speed: float = 1.0  # Radians per second

func _ready() -> void:
    # Rotate objects on the platform
    constant_angular_velocity = Vector3.UP * rotation_speed
```

## Moving Platform (Animated)

```gdscript
extends StaticBody3D

@export var move_distance: float = 5.0
@export var move_speed: float = 2.0

var _start_position: Vector3
var _time: float = 0.0

func _ready() -> void:
    _start_position = global_position

func _physics_process(delta: float) -> void:
    _time += delta * move_speed

    # Move platform
    var offset := sin(_time) * move_distance
    global_position = _start_position + Vector3.RIGHT * offset

    # Update velocity for objects on platform
    constant_linear_velocity = Vector3.RIGHT * cos(_time) * move_distance * move_speed
```

## Physics Material Setup

```gdscript
extends StaticBody3D

func _ready() -> void:
    var material := PhysicsMaterial.new()

    # Ice surface (low friction, no bounce)
    material.friction = 0.1
    material.bounce = 0.0

    # OR Bouncy surface
    material.friction = 0.5
    material.bounce = 0.8

    # OR Sticky surface (high friction)
    material.friction = 1.0
    material.bounce = 0.0

    physics_material_override = material
```

## Common Patterns

### Basic Static Terrain/Wall

The most common use case - completely immovable collision:

```gdscript
extends StaticBody3D

# No code needed! StaticBody3D + CollisionShape3D child = working collision
# Add physics material in editor or code for friction/bounce customization

func _ready() -> void:
    # Optional: Customize physics material
    var material := PhysicsMaterial.new()
    material.friction = 0.8
    material.bounce = 0.0
    physics_material_override = material
```

### Conveyor Belt

Objects touching the belt move in a constant direction:

```gdscript
extends StaticBody3D

@export var belt_speed: float = 5.0
@export var belt_direction: Vector3 = Vector3.FORWARD

func _ready() -> void:
    # Objects on belt move at constant velocity
    constant_linear_velocity = belt_direction.normalized() * belt_speed
```

### Rotating Platform

Objects on the platform experience rotational force:

```gdscript
extends StaticBody3D

@export var rotation_speed: float = 1.0  # Radians per second

func _ready() -> void:
    # Objects on platform rotate with it
    constant_angular_velocity = Vector3.UP * rotation_speed
```

## Notes

- **Static vs Animatable:** Use StaticBody3D for objects that never move or move at constant velocity. Use AnimatableBody3D for animated platforms that should push bodies.
- **Teleportation:** Moving StaticBody3D via code teleports it (doesn't push other bodies). For pushing, use AnimatableBody3D.
- **Constant velocities:** Don't actually move the body, only affect touching RigidBody3D/CharacterBody3D
- **Performance:** StaticBody3D is the most performant physics body type (no physics simulation)
- **Movement:** Can be moved via:
  - Direct position/rotation assignment
  - Animations (with physics callback mode)
  - RemoteTransform3D
  - Code in `_process()` or `_physics_process()`

## When to Use StaticBody3D

Use **StaticBody3D** for:
- Floors, walls, ceilings
- Completely immovable obstacles
- Conveyor belts (constant velocity)
- Rotating platforms (constant angular velocity)
- Objects that teleport without pushing

Use **AnimatableBody3D** for:
- Moving platforms that push bodies
- Doors that slide open
- Elevators
- Any animated object that should affect physics bodies

Use **RigidBody3D** with `freeze = true` for:
- Objects that switch between static and dynamic
- Drag-and-drop objects
