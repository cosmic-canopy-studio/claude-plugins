---
class: CharacterBody3D
version: 2025.12.21
godot_version: "4.3"
sources:
  - repos/godot-docs/classes/class_characterbody3d.rst
---

# CharacterBody3D

**Inherits:** PhysicsBody3D < CollisionObject3D < Node3D < Node < Object

A 3D physics body specialized for characters moved by script.

## Description

CharacterBody3D is a specialized class for physics bodies that are meant to be user-controlled. They are not affected by physics at all, but they affect other physics bodies in their path. They are mainly used to provide high-level API to move objects with wall and slope detection (`move_and_slide()` method) in addition to the general collision detection provided by `PhysicsBody3D.move_and_collide()`. This makes it useful for highly configurable physics bodies that must move in specific ways and collide with the world, as is often the case with user-controlled characters.

For game objects that don't require complex movement or collision detection, such as moving platforms, AnimatableBody3D is simpler to configure.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `velocity` | Vector3 | `Vector3(0, 0, 0)` | Current velocity vector (meters per second) |
| `motion_mode` | MotionMode | `MOTION_MODE_GROUNDED` | Defines behavior for floor/ceiling/wall detection |
| `up_direction` | Vector3 | `Vector3(0, 1, 0)` | Vector pointing upwards for floor detection |
| `floor_max_angle` | float | `0.7853982` (45°) | Maximum angle where slope is considered floor |
| `floor_snap_length` | float | `0.1` | Snapping distance to keep attached to slopes |
| `floor_stop_on_slope` | bool | `true` | Prevent sliding on slopes when standing still |
| `floor_constant_speed` | bool | `false` | Maintain constant speed regardless of slope |
| `floor_block_on_wall` | bool | `true` | Prevent moving on walls (only floor) |
| `slide_on_ceiling` | bool | `true` | Slide along ceiling during jump or stop |
| `max_slides` | int | `6` | Maximum direction changes before stopping |
| `wall_min_slide_angle` | float | `0.2617994` (15°) | Minimum angle to slide along walls |
| `safe_margin` | float | `0.001` | Extra margin for collision recovery |
| `platform_floor_layers` | int | `4294967295` | Collision layers for floor platforms |
| `platform_wall_layers` | int | `0` | Collision layers for wall platforms |
| `platform_on_leave` | PlatformOnLeave | `PLATFORM_ON_LEAVE_ADD_VELOCITY` | Behavior when leaving moving platforms |

## Key Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `move_and_slide()` | bool | Moves the body based on velocity, returns true if collision occurred |
| `is_on_floor()` | bool | Returns true if on floor after move_and_slide() |
| `is_on_ceiling()` | bool | Returns true if on ceiling after move_and_slide() |
| `is_on_wall()` | bool | Returns true if on wall after move_and_slide() |
| `is_on_floor_only()` | bool | Returns true if only on floor |
| `is_on_ceiling_only()` | bool | Returns true if only on ceiling |
| `is_on_wall_only()` | bool | Returns true if only on wall |
| `get_floor_normal()` | Vector3 | Returns collision normal of floor |
| `get_wall_normal()` | Vector3 | Returns collision normal of wall |
| `get_floor_angle(up_direction)` | float | Returns floor collision angle |
| `get_last_motion()` | Vector3 | Returns last motion applied during move_and_slide() |
| `get_position_delta()` | Vector3 | Returns travel (position delta) during last move_and_slide() |
| `get_real_velocity()` | Vector3 | Returns actual velocity (diagonal movement on slopes) |
| `get_platform_velocity()` | Vector3 | Returns linear velocity of platform at last collision |
| `get_platform_angular_velocity()` | Vector3 | Returns angular velocity of platform |
| `get_slide_collision(index)` | KinematicCollision3D | Returns collision info for specific slide |
| `get_slide_collision_count()` | int | Returns number of collisions during last move_and_slide() |
| `get_last_slide_collision()` | KinematicCollision3D | Returns latest collision info |
| `apply_floor_snap()` | void | Manually apply snap to floor regardless of velocity |

## Enums

### MotionMode

| Constant | Value | Description |
|----------|-------|-------------|
| `MOTION_MODE_GROUNDED` | 0 | Notions of walls, ceiling, and floor are relevant. Body reacts to slopes. For platformers. |
| `MOTION_MODE_FLOATING` | 1 | No notion of floor or ceiling. All collisions reported as wall. For space games. |

### PlatformOnLeave

| Constant | Value | Description |
|----------|-------|-------------|
| `PLATFORM_ON_LEAVE_ADD_VELOCITY` | 0 | Add last platform velocity to velocity when leaving |
| `PLATFORM_ON_LEAVE_ADD_UPWARD_VELOCITY` | 1 | Add platform velocity but ignore downward motion (preserves jump height) |
| `PLATFORM_ON_LEAVE_DO_NOTHING` | 2 | Do nothing when leaving platform |

## Basic Movement Pattern

```gdscript
extends CharacterBody3D

const SPEED: float = 5.0
const JUMP_VELOCITY: float = 4.5

func _physics_process(delta: float) -> void:
    # Add gravity
    if not is_on_floor():
        velocity += get_gravity() * delta

    # Handle jump
    if Input.is_action_just_pressed("ui_accept") and is_on_floor():
        velocity.y = JUMP_VELOCITY

    # Get input direction
    var input_dir := Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    if direction:
        velocity.x = direction.x * SPEED
        velocity.z = direction.z * SPEED
    else:
        velocity.x = move_toward(velocity.x, 0, SPEED)
        velocity.z = move_toward(velocity.z, 0, SPEED)

    move_and_slide()
```

## Notes

- **Warning:** The collision normal is not always the same as the surface normal.
- `velocity` is used and modified during `move_and_slide()` calls.
- When on moving platforms, platform velocity is automatically added to body motion.
- Floor snapping requires `floor_snap_length` > 0 and downward velocity to attach to surfaces.
- Set `up_direction` cannot be `Vector3.ZERO`. For omnidirectional movement, use `MOTION_MODE_FLOATING`.
