---
class: RigidBody3D
version: 2025.12.21
godot_version: "4.3"
sources:
  - repos/godot-docs/classes/class_rigidbody3d.rst
---

# RigidBody3D

**Inherits:** PhysicsBody3D < CollisionObject3D < Node3D < Node < Object

**Inherited By:** VehicleBody3D

A 3D physics body that is moved by a physics simulation.

## Description

RigidBody3D implements full 3D physics. It cannot be controlled directly, instead, you must apply forces to it (gravity, impulses, etc.), and the physics simulation will calculate the resulting movement, rotation, react to collisions, and affect other physics bodies in its path.

The body's behavior can be adjusted via `lock_rotation`, `freeze`, and `freeze_mode`. By changing various properties of the object, such as `mass`, you can control how the physics simulation acts on it.

A rigid body will always maintain its shape and size, even when forces are applied to it. It is useful for objects that can be interacted with in an environment, such as a tree that can be knocked over or a stack of crates that can be pushed around.

If you need to directly affect the body, prefer `_integrate_forces()` as it allows you to directly access the physics state.

If you need to override the default physics behavior, you can write a custom force integration function. See `custom_integrator`.

**Note:** Changing the 3D transform or `linear_velocity` of a RigidBody3D very often may lead to some unpredictable behaviors. This also happens when a RigidBody3D is the descendant of a constantly moving node, like another RigidBody3D, as that will cause its global transform to be set whenever its ancestor moves.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `mass` | float | `1.0` | The body's mass |
| `linear_velocity` | Vector3 | `Vector3(0, 0, 0)` | Body's linear velocity in units per second |
| `angular_velocity` | Vector3 | `Vector3(0, 0, 0)` | Body's rotational velocity in radians per second |
| `linear_damp` | float | `0.0` | Damps the body's movement |
| `angular_damp` | float | `0.0` | Damps the body's rotation |
| `linear_damp_mode` | DampMode | `DAMP_MODE_COMBINE` | How linear_damp is applied |
| `angular_damp_mode` | DampMode | `DAMP_MODE_COMBINE` | How angular_damp is applied |
| `gravity_scale` | float | `1.0` | Multiplier for gravity (0 = no gravity, 2 = double gravity) |
| `center_of_mass_mode` | CenterOfMassMode | `CENTER_OF_MASS_MODE_AUTO` | How center of mass is determined |
| `center_of_mass` | Vector3 | `Vector3(0, 0, 0)` | Custom center of mass (when mode is CUSTOM) |
| `inertia` | Vector3 | `Vector3(0, 0, 0)` | Moment of inertia (auto-computed if ZERO) |
| `physics_material_override` | PhysicsMaterial | null | Physics material for friction and bounce |
| `freeze` | bool | `false` | If true, body is frozen (no physics) |
| `freeze_mode` | FreezeMode | `FREEZE_MODE_STATIC` | Behavior when frozen |
| `lock_rotation` | bool | `false` | If true, body cannot rotate |
| `custom_integrator` | bool | `false` | Disable standard force integration |
| `continuous_cd` | bool | `false` | Use continuous collision detection |
| `contact_monitor` | bool | `false` | Enable collision signals |
| `max_contacts_reported` | int | `0` | Maximum contacts to record (requires contact_monitor) |
| `can_sleep` | bool | `true` | Can enter sleep mode when no movement |
| `sleeping` | bool | `false` | If true, body is sleeping |
| `constant_force` | Vector3 | `Vector3(0, 0, 0)` | Total constant positional forces |
| `constant_torque` | Vector3 | `Vector3(0, 0, 0)` | Total constant rotational forces |

## Key Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `apply_central_force(force)` | void | Apply directional force without rotation |
| `apply_force(force, position)` | void | Apply positioned force (creates rotation) |
| `apply_central_impulse(impulse)` | void | Apply instant directional velocity change |
| `apply_impulse(impulse, position)` | void | Apply positioned impulse |
| `apply_torque(torque)` | void | Apply rotational force |
| `apply_torque_impulse(impulse)` | void | Apply rotational impulse |
| `add_constant_central_force(force)` | void | Add constant directional force |
| `add_constant_force(force, position)` | void | Add constant positioned force |
| `add_constant_torque(torque)` | void | Add constant rotational force |
| `set_axis_velocity(axis_velocity)` | void | Set velocity in specific axis |
| `get_colliding_bodies()` | Array[Node3D] | Returns list of colliding bodies |
| `get_contact_count()` | int | Returns number of contacts |
| `get_inverse_inertia_tensor()` | Basis | Returns inverse inertia tensor basis |
| `_integrate_forces(state)` | void | Virtual method for custom physics integration |

## Signals

| Signal | Parameters | Description |
|--------|-----------|-------------|
| `body_entered` | body: Node | Emitted when collision with PhysicsBody3D/GridMap starts |
| `body_exited` | body: Node | Emitted when collision ends |
| `body_shape_entered` | body_rid, body, body_shape_index, local_shape_index | Emitted when shapes collide |
| `body_shape_exited` | body_rid, body, body_shape_index, local_shape_index | Emitted when shape collision ends |
| `sleeping_state_changed` | | Emitted when physics engine changes sleeping state |

## Enums

### FreezeMode

| Constant | Value | Description |
|----------|-------|-------------|
| `FREEZE_MODE_STATIC` | 0 | Not affected by gravity/forces, doesn't collide when moved |
| `FREEZE_MODE_KINEMATIC` | 1 | Similar to STATIC but collides when moved (for animation) |

### CenterOfMassMode

| Constant | Value | Description |
|----------|-------|-------------|
| `CENTER_OF_MASS_MODE_AUTO` | 0 | Center of mass calculated from shapes |
| `CENTER_OF_MASS_MODE_CUSTOM` | 1 | Use custom center_of_mass value |

### DampMode

| Constant | Value | Description |
|----------|-------|-------------|
| `DAMP_MODE_COMBINE` | 0 | Damping value added to area/default values |
| `DAMP_MODE_REPLACE` | 1 | Damping value replaces area/default values |

## Basic Force Application

```gdscript
extends RigidBody3D

const MOVE_FORCE: float = 1000.0

func _physics_process(_delta: float) -> void:
    var input := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    var direction := Vector3(input.x, 0, input.y)

    if direction:
        apply_central_force(direction * MOVE_FORCE)
```

## Custom Physics Integration

```gdscript
extends RigidBody3D

const SPEED: float = 5.0
const JUMP_IMPULSE: float = 10.0

func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
    # Direct velocity modification
    var input := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    state.linear_velocity.x = input.x * SPEED
    state.linear_velocity.z = input.y * SPEED

    # Jump
    if Input.is_action_just_pressed("jump") and is_on_floor(state):
        state.linear_velocity.y = JUMP_IMPULSE

func is_on_floor(state: PhysicsDirectBodyState3D) -> bool:
    for i in state.get_contact_count():
        if state.get_contact_local_normal(i).dot(Vector3.UP) > 0.5:
            return true
    return false
```

## Contact Monitoring

```gdscript
extends RigidBody3D

func _ready() -> void:
    contact_monitor = true
    max_contacts_reported = 4
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node) -> void:
    print("Collided with: ", body.name)
```

## Notes

- Forces are time-dependent (apply every frame), impulses are instant (one-time)
- Use `continuous_cd = true` for fast-moving objects to prevent tunneling
- `max_contacts_reported` must be > 0 for contact signals to work
- To get computed inertia, use PhysicsServer3D (property doesn't update automatically)
- Setting position directly breaks physics simulation
- Use `_integrate_forces()` for frame-perfect physics control
- Requires active CollisionShape3D child for inertia calculation (or set manually)
