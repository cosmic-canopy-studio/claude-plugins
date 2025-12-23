---
class: Node2D
source: repos/godot-docs/classes/class_node2d.rst
generated: 2025-12-21
---

# Node2D

**Inherits:** CanvasItem < Node < Object

**Inherited By:** AnimatedSprite2D, AudioListener2D, AudioStreamPlayer2D, BackBufferCopy, Bone2D, Camera2D, CanvasGroup, CanvasModulate, CollisionObject2D, CollisionPolygon2D, CollisionShape2D, CPUParticles2D, GPUParticles2D, Joint2D, Light2D, LightOccluder2D, Line2D, Marker2D, MeshInstance2D, MultiMeshInstance2D, NavigationLink2D, NavigationObstacle2D, NavigationRegion2D, Parallax2D, ParallaxLayer, Path2D, PathFollow2D, Polygon2D, RayCast2D, RemoteTransform2D, ShapeCast2D, Skeleton2D, Sprite2D, TileMap, TileMapLayer, TouchScreenButton, VisibleOnScreenNotifier2D

A 2D game object, inherited by all 2D-related nodes. Has a position, rotation, scale, and skew.

## Description

A 2D game object, with a transform (position, rotation, and scale). All 2D nodes, including physics objects and sprites, inherit from Node2D. Use Node2D as a parent node to move, scale and rotate children in a 2D project. Also gives control of the node's render order.

Note: Since both Node2D and Control inherit from CanvasItem, they share several concepts from the class such as the z_index and visible properties.

## Properties

| Type | Property | Default |
|------|----------|---------|
| Vector2 | global_position | |
| float | global_rotation | |
| float | global_rotation_degrees | |
| Vector2 | global_scale | |
| float | global_skew | |
| Transform2D | global_transform | |
| Vector2 | position | Vector2(0, 0) |
| float | rotation | 0.0 |
| float | rotation_degrees | |
| Vector2 | scale | Vector2(1, 1) |
| float | skew | 0.0 |
| Transform2D | transform | |

## Methods

| Return Type | Method |
|-------------|--------|
| void | `apply_scale(ratio: Vector2)` |
| float | `get_angle_to(point: Vector2)` const |
| Transform2D | `get_relative_transform_to_parent(parent: Node)` const |
| void | `global_translate(offset: Vector2)` |
| void | `look_at(point: Vector2)` |
| void | `move_local_x(delta: float, scaled: bool = false)` |
| void | `move_local_y(delta: float, scaled: bool = false)` |
| void | `rotate(radians: float)` |
| Vector2 | `to_global(local_point: Vector2)` const |
| Vector2 | `to_local(global_point: Vector2)` const |
| void | `translate(offset: Vector2)` |

## Key Properties

- **position**: Position, relative to the node's parent. See also global_position.
- **rotation**: Rotation in radians, relative to the node's parent. Note: This property is edited in the inspector in degrees.
- **scale**: The node's scale, relative to the node's parent. Unscaled value: (1, 1).
- **skew**: If set to a non-zero value, slants the node in one direction or another. This can be used for pseudo-3D effects.
- **global_transform**: Global Transform2D. See also transform.

## Common Methods

- **look_at(point)**: Rotates the node so that its local +X axis points towards the point, which is expected to use global coordinates.
- **to_global(local_point)**: Transforms the provided local position into a position in global coordinate space.
- **to_local(global_point)**: Transforms the provided global position into a position in local coordinate space.
- **rotate(radians)**: Applies a rotation to the node, in radians, starting from its current rotation.

## Key Concepts

### Transform Hierarchy

Node2D provides transform properties (position, rotation, scale, skew) that are relative to the parent node:
- Local transforms combine with parent transforms
- Modify local properties for relative movement
- Use global properties when you need world-space positioning

### Coordinate Space Conversion

- `to_global()`: Local → Global (world space)
- `to_local()`: Global → Local (node space)

This is essential for things like projectiles (spawn in local space, move in global space) or mouse input (convert screen to local coordinates).

### Rotation

- `rotation`: In radians (use `deg_to_rad()` to convert from degrees)
- `rotation_degrees`: Convenience property in degrees (editor uses this)
- `look_at()`: Automatically rotates to face a point (uses +X as forward)

### Scale and Skew

- `scale`: Non-uniform scaling (x and y can differ)
- Default: `Vector2(1, 1)` (no scaling)
- `skew`: Pseudo-3D slant effect (in radians)

## Best Practices

- Use `position` for relative movement, `global_position` when you need world coordinates
- Convert coordinates with `to_global()`/`to_local()` rather than manual math
- Use `look_at()` for aiming/facing rather than manual rotation calculation
- Remember rotation is in radians - use `rotation_degrees` in editor/debugging
- Prefer `move_local_x()`/`move_local_y()` for direction-relative movement
- Keep transforms simple - excessive skewing can cause visual artifacts

## Anti-Patterns

- Don't mix local and global property modifications in the same frame - choose one space
- Don't manually calculate rotations when `look_at()` exists
- Don't forget to convert degrees to radians when setting `rotation` from constants
- Don't modify `transform` directly unless you understand Transform2D math
- Don't use skew for actual 3D rotation - use Node3D instead

## Common Patterns

```gdscript
# Following a target
extends Node2D

@export var target: Node2D

func _process(delta: float) -> void:
    if target:
        # Look at target (rotates to face it)
        look_at(target.global_position)

        # Move toward target
        var direction: Vector2 = global_position.direction_to(target.global_position)
        position += direction * 100.0 * delta
```

```gdscript
# Local movement (direction relative to rotation)
extends Node2D

func _process(delta: float) -> void:
    # Move forward in local +X direction (accounts for rotation)
    move_local_x(100.0 * delta)

    # Strafe in local Y direction
    if Input.is_action_pressed("strafe_right"):
        move_local_y(50.0 * delta)
```

```gdscript
# Coordinate space conversion
extends Node2D

func shoot_at_mouse() -> void:
    # Convert mouse position from screen to local coordinates
    var local_mouse: Vector2 = to_local(get_global_mouse_position())

    # Spawn projectile in local space, moving in global direction
    var projectile: Node2D = preload("res://projectile.tscn").instantiate()
    projectile.position = $Weapon.position  # Local spawn point
    add_child(projectile)

    # Set velocity in global space
    var global_target: Vector2 = get_global_mouse_position()
    var direction: Vector2 = global_position.direction_to(global_target)
    projectile.velocity = direction * 500.0
```

```gdscript
# Smooth rotation to face direction
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    if velocity.length() > 0:
        # Smoothly rotate to face movement direction
        var target_rotation: float = velocity.angle()
        rotation = lerp_angle(rotation, target_rotation, 10.0 * delta)
```

```gdscript
# Relative positioning
extends Node2D

func orbit_around_parent(radius: float, speed: float, delta: float) -> void:
    # Orbit in local space (relative to parent)
    rotation += speed * delta
    position = Vector2(radius, 0).rotated(rotation)
```

## Performance Considerations

- Transform updates propagate to all children - keep hierarchies shallow when possible
- Frequent `to_global()`/`to_local()` calls have matrix multiplication cost
- Cache global positions if used multiple times per frame
- Avoid setting position every frame if node is stationary
