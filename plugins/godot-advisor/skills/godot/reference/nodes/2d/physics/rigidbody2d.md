---
class: RigidBody2D
godot_version: "4.3"
sources:
  - local: repos/godot-docs/classes/class_rigidbody2d.rst
status: extracted
---

# RigidBody2D

## Inheritance
PhysicsBody2D < CollisionObject2D < Node2D < CanvasItem < Node < Object

## Description
A 2D physics body that is moved by a physics simulation.

RigidBody2D implements full 2D physics. It cannot be controlled directly, instead, you must apply forces to it (gravity, impulses, etc.), and the physics simulation will calculate the resulting movement, rotation, react to collisions, and affect other physics bodies in its path.

The body's behavior can be adjusted via lock_rotation, freeze, and freeze_mode. By changing various properties of the object, such as mass, you can control how the physics simulation acts on it.

A rigid body will always maintain its shape and size, even when forces are applied to it. It is useful for objects that can be interacted with in an environment, such as a tree that can be knocked over or a stack of crates that can be pushed around.

**Note:** Changing the 2D transform or linear_velocity of a RigidBody2D very often may lead to some unpredictable behaviors.

## Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| angular_damp | float | 0.0 | Damps the body's rotation |
| angular_damp_mode | DampMode | 0 | How angular_damp is applied |
| angular_velocity | float | 0.0 | Body's rotational velocity in radians per second |
| can_sleep | bool | true | If true, body can enter sleep mode when no movement |
| center_of_mass | Vector2 | Vector2(0, 0) | Custom center of mass when mode is CUSTOM |
| center_of_mass_mode | CenterOfMassMode | 0 | How center of mass is determined |
| constant_force | Vector2 | Vector2(0, 0) | Total constant positional forces applied each frame |
| constant_torque | float | 0.0 | Total constant rotational forces applied each frame |
| contact_monitor | bool | false | If true, body emits signals when colliding |
| continuous_cd | CCDMode | 0 | Continuous collision detection mode |
| custom_integrator | bool | false | If true, disables standard force integration |
| freeze | bool | false | If true, body is frozen (no gravity/forces) |
| freeze_mode | FreezeMode | 0 | Body's behavior when frozen |
| gravity_scale | float | 1.0 | Multiplies the gravity applied to the body |
| inertia | float | 0.0 | Body's moment of inertia (0 = auto-computed) |
| linear_damp | float | 0.0 | Damps the body's movement |
| linear_damp_mode | DampMode | 0 | How linear_damp is applied |
| linear_velocity | Vector2 | Vector2(0, 0) | Body's linear velocity in pixels per second |
| lock_rotation | bool | false | If true, body cannot rotate |
| mass | float | 1.0 | Body's mass |
| max_contacts_reported | int | 0 | Maximum number of contacts recorded |
| physics_material_override | PhysicsMaterial | null | Physics material override |
| sleeping | bool | false | If true, body won't move until woken |

## Methods
| Method | Return | Description |
|--------|--------|-------------|
| _integrate_forces(state: PhysicsDirectBodyState2D) | void | Called during physics processing for custom force integration |
| add_constant_central_force(force: Vector2) | void | Adds constant directional force at center of mass |
| add_constant_force(force: Vector2, position: Vector2 = Vector2(0, 0)) | void | Adds constant positioned force |
| add_constant_torque(torque: float) | void | Adds constant rotational force |
| apply_central_force(force: Vector2) | void | Applies directional force at center of mass |
| apply_central_impulse(impulse: Vector2 = Vector2(0, 0)) | void | Applies directional impulse at center of mass |
| apply_force(force: Vector2, position: Vector2 = Vector2(0, 0)) | void | Applies positioned force |
| apply_impulse(impulse: Vector2, position: Vector2 = Vector2(0, 0)) | void | Applies positioned impulse |
| apply_torque(torque: float) | void | Applies rotational force |
| apply_torque_impulse(torque: float) | void | Applies rotational impulse |
| get_colliding_bodies() | Array[Node2D] | Returns list of bodies colliding with this one |
| get_contact_count() | int | Returns number of contacts with other bodies |
| set_axis_velocity(axis_velocity: Vector2) | void | Sets velocity on given axis |

## Signals
| Signal | Parameters | Description |
|--------|------------|-------------|
| body_entered | body: Node | Emitted when collision with another body occurs |
| body_exited | body: Node | Emitted when collision with another body ends |
| body_shape_entered | body_rid: RID, body: Node, body_shape_index: int, local_shape_index: int | Emitted when shape collision begins |
| body_shape_exited | body_rid: RID, body: Node, body_shape_index: int, local_shape_index: int | Emitted when shape collision ends |
| sleeping_state_changed | | Emitted when physics engine changes sleeping state |

## Enums

### FreezeMode
| Value | Name | Description |
|-------|------|-------------|
| 0 | FREEZE_MODE_STATIC | Body not affected by gravity/forces, doesn't collide |
| 1 | FREEZE_MODE_KINEMATIC | Similar to STATIC but collides along its path |

### CenterOfMassMode
| Value | Name | Description |
|-------|------|-------------|
| 0 | CENTER_OF_MASS_MODE_AUTO | Center of mass calculated from shapes |
| 1 | CENTER_OF_MASS_MODE_CUSTOM | Center of mass set via center_of_mass property |

### DampMode
| Value | Name | Description |
|-------|------|-------------|
| 0 | DAMP_MODE_COMBINE | Damping value added to area/default value |
| 1 | DAMP_MODE_REPLACE | Damping value replaces area/default value |

### CCDMode
| Value | Name | Description |
|-------|------|-------------|
| 0 | CCD_MODE_DISABLED | CCD disabled (fastest, may miss small/fast objects) |
| 1 | CCD_MODE_CAST_RAY | CCD using raycasting (faster but less precise) |
| 2 | CCD_MODE_CAST_SHAPE | CCD using shapecasting (slowest, most precise) |

## See Also
- [Official Docs](https://docs.godotengine.org/en/stable/classes/class_rigidbody2d.html)
- [Physics Introduction Tutorial](repos/godot-docs/tutorials/physics/physics_introduction.rst)
