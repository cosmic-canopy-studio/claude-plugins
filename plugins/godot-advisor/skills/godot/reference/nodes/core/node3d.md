---
class: Node3D
source: repos/godot-docs/classes/class_node3d.rst
generated: 2025-12-21
---

# Node3D

**Inherits:** Node < Object

**Inherited By:** AudioListener3D, AudioStreamPlayer3D, BoneAttachment3D, Camera3D, CollisionObject3D, CollisionPolygon3D, CollisionShape3D, GridMap, ImporterMeshInstance3D, Joint3D, LightmapProbe, Marker3D, NavigationLink3D, NavigationObstacle3D, NavigationRegion3D, OpenXRCompositionLayer, OpenXRHand, OpenXRRenderModel, OpenXRRenderModelManager, Path3D, PathFollow3D, RayCast3D, RemoteTransform3D, ShapeCast3D, Skeleton3D, SkeletonModifier3D, SpringArm3D, SpringBoneCollision3D, VehicleWheel3D, VisualInstance3D, XRFaceModifier3D, XRNode3D, XROrigin3D

Base object in 3D space, inherited by all 3D nodes.

## Description

The Node3D node is the base representation of a node in 3D space. All other 3D nodes inherit from this class.

Affine operations (translation, rotation, scale) are calculated in the coordinate system relative to the parent, unless the Node3D's top_level is true. In this coordinate system, affine operations correspond to direct affine operations on the Node3D's transform. The term parent space refers to this coordinate system. The coordinate system that is attached to the Node3D itself is referred to as object-local coordinate system, or local space.

Note: Unless otherwise specified, all methods that need angle parameters must receive angles in radians. To convert degrees to radians, use `deg_to_rad()`.

Note: In Godot 3 and older, Node3D was named Spatial.

## Properties

| Type | Property | Default |
|------|----------|---------|
| Basis | basis | |
| Basis | global_basis | |
| Vector3 | global_position | |
| Vector3 | global_rotation | |
| Vector3 | global_rotation_degrees | |
| Transform3D | global_transform | |
| Vector3 | position | Vector3(0, 0, 0) |
| Quaternion | quaternion | |
| Vector3 | rotation | Vector3(0, 0, 0) |
| Vector3 | rotation_degrees | |
| RotationEditMode | rotation_edit_mode | 0 |
| EulerOrder | rotation_order | 2 |
| Vector3 | scale | Vector3(1, 1, 1) |
| bool | top_level | false |
| Transform3D | transform | Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0) |
| NodePath | visibility_parent | NodePath("") |
| bool | visible | true |

## Methods

| Return Type | Method |
|-------------|--------|
| void | `global_rotate(axis: Vector3, angle: float)` |
| void | `global_scale(scale: Vector3)` |
| void | `global_translate(offset: Vector3)` |
| void | `hide()` |
| void | `look_at(target: Vector3, up: Vector3 = Vector3(0, 1, 0), use_model_front: bool = false)` |
| void | `look_at_from_position(position: Vector3, target: Vector3, up: Vector3 = Vector3(0, 1, 0), use_model_front: bool = false)` |
| void | `orthonormalize()` |
| void | `rotate(axis: Vector3, angle: float)` |
| void | `rotate_object_local(axis: Vector3, angle: float)` |
| void | `rotate_x(angle: float)` |
| void | `rotate_y(angle: float)` |
| void | `rotate_z(angle: float)` |
| void | `scale_object_local(scale: Vector3)` |
| void | `show()` |
| Vector3 | `to_global(local_point: Vector3)` const |
| Vector3 | `to_local(global_point: Vector3)` const |
| void | `translate(offset: Vector3)` |
| void | `translate_object_local(offset: Vector3)` |
| Node3D | `get_parent_node_3d()` const |
| World3D | `get_world_3d()` const |
| Transform3D | `get_global_transform_interpolated()` |
| bool | `is_visible_in_tree()` const |
| void | `force_update_transform()` |
| void | `set_identity()` |
| void | `set_disable_scale(disable: bool)` |
| bool | `is_scale_disabled()` const |

## Signals

- **visibility_changed**()
  - Emitted when this node's visibility changes (see visible and is_visible_in_tree())

## Key Properties

- **position**: Position (translation) of this node in parent space (relative to the parent node).
- **rotation**: Rotation of this node as Euler angles, in radians and in parent space.
- **scale**: Scale of this node in local space (relative to this node).
- **global_transform**: The transformation of this node, in global space (relative to the world).
- **top_level**: If true, the node does not inherit its transformations from its parent.
- **visible**: If true, this node can be visible.

## Common Methods

- **look_at(target, up)**: Rotates the node so that the local forward axis (-Z) points toward the target position.
- **to_global(local_point)**: Returns the local_point converted from this node's local space to global space.
- **to_local(global_point)**: Returns the global_point converted from global space to this node's local space.
- **rotate(axis, angle)**: Rotates this node's basis around the axis by the given angle, in radians.
- **translate_object_local(offset)**: Adds the given translation offset to the node's position, in local space.

## Key Concepts

### 3D Coordinate System

Godot uses a right-handed coordinate system:
- **+X**: Right
- **+Y**: Up
- **+Z**: Toward camera (backward)
- **-Z**: Away from camera (forward)

This is why `look_at()` rotates -Z to face the target.

### Transform Hierarchy

Node3D provides transform properties relative to the parent node:
- Local transforms: `position`, `rotation`, `scale`, `basis`
- Global transforms: `global_position`, `global_rotation`, `global_transform`
- `top_level`: If true, node ignores parent transforms

### Rotation Representations

Node3D supports multiple rotation formats:
- **Euler angles** (`rotation`, `rotation_degrees`): Intuitive but has gimbal lock
- **Quaternion** (`quaternion`): Smooth interpolation, no gimbal lock
- **Basis**: Full rotation matrix, most powerful

The `rotation_order` property controls Euler angle calculation (XYZ, YXZ, etc.).

### Coordinate Space Conversion

- `to_global()`: Local → World space
- `to_local()`: World → Local space
- Essential for spawning objects, raycasting, and positioning

### Visibility

- `visible`: Can this node be seen?
- `is_visible_in_tree()`: Is node actually visible (considers parent visibility)?
- `visibility_parent`: Use another node's visibility state

## Best Practices

- Use radians for all rotation values (Godot's native unit)
- Use `look_at()` for orienting objects rather than manual rotation
- Use `translate_object_local()` for forward/backward movement
- Use `rotate_object_local()` for rotations in local space
- Use quaternions for smooth rotation interpolation (slerp)
- Remember: -Z is forward, not +Z
- Call `orthonormalize()` if basis becomes denormalized from repeated transformations
- Use `top_level` for world-space nodes that shouldn't inherit parent transforms

## Anti-Patterns

- Don't use Euler angles for interpolation - use quaternions (gimbal lock issues)
- Don't forget Godot uses -Z as forward, not +Z like some engines
- Don't manually build rotation matrices - use the provided methods
- Don't mix rotation representations (Euler + Quaternion) in same code
- Don't accumulate rotations with Euler angles - drift and gimbal lock occur
- Don't modify `basis` directly unless you understand 3D math
- Don't forget to check `is_visible_in_tree()` instead of just `visible`

## Common Patterns

```gdscript
# Looking at a target
extends Node3D

@export var target: Node3D

func _process(delta: float) -> void:
    if target:
        # Make -Z axis point at target, Y axis stays up
        look_at(target.global_position, Vector3.UP)
```

```gdscript
# Local movement (forward/backward)
extends Node3D

@export var speed: float = 5.0

func _process(delta: float) -> void:
    # Move forward (in -Z direction)
    if Input.is_action_pressed("forward"):
        translate_object_local(Vector3(0, 0, -speed * delta))

    # Move backward (in +Z direction)
    if Input.is_action_pressed("backward"):
        translate_object_local(Vector3(0, 0, speed * delta))
```

```gdscript
# Smooth rotation with quaternions (no gimbal lock)
extends Node3D

@export var target_rotation: Vector3  # Target rotation in degrees

func _process(delta: float) -> void:
    # Convert target to quaternion
    var target_quat: Quaternion = Quaternion.from_euler(
        deg_to_rad(target_rotation)
    )

    # Smoothly interpolate current rotation to target
    quaternion = quaternion.slerp(target_quat, 5.0 * delta)
```

```gdscript
# Rotating around axes
extends Node3D

func _process(delta: float) -> void:
    # Rotate around local Y axis (yaw)
    rotate_y(deg_to_rad(45.0) * delta)

    # Rotate around local X axis (pitch)
    rotate_x(deg_to_rad(30.0) * delta)

    # Or use a custom axis
    rotate(Vector3(1, 1, 0).normalized(), deg_to_rad(20.0) * delta)
```

```gdscript
# Coordinate space conversion for spawning
extends Node3D

func spawn_projectile() -> void:
    var projectile: Node3D = preload("res://projectile.tscn").instantiate()

    # Spawn at weapon mount point (local position)
    var spawn_point: Vector3 = $WeaponMount.position

    # Convert to global position
    var spawn_global: Vector3 = to_global(spawn_point)

    # Add to scene root
    get_tree().root.add_child(projectile)
    projectile.global_position = spawn_global

    # Set velocity in -Z (forward) direction in global space
    projectile.velocity = -global_transform.basis.z * 20.0
```

```gdscript
# Top-level node (ignores parent transform)
extends Node3D

func _ready() -> void:
    # This node's transform is now independent of parent
    top_level = true

    # Useful for:
    # - Floating damage numbers
    # - World-space UI
    # - Detached visual effects
```

```gdscript
# Fix denormalized basis (after many transformations)
extends Node3D

func _process(delta: float) -> void:
    # Do lots of rotations...
    rotate_x(delta)
    rotate_y(delta * 0.5)

    # Periodically fix accumulated floating-point errors
    if Engine.get_frames_drawn() % 100 == 0:
        orthonormalize()
```

## Performance Considerations

- Transform updates propagate to all children - avoid deep hierarchies
- `to_global()`/`to_local()` involve matrix multiplications - cache if used often
- Visibility culling depends on `visible` and camera frustum
- Use `visibility_parent` to group visibility updates for many objects
- Quaternion interpolation (slerp) is faster than Euler angle math
