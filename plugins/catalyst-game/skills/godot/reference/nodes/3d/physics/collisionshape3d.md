---
class: CollisionShape3D
version: 2025.12.21
godot_version: "4.3"
sources:
  - repos/godot-docs/classes/class_collisionshape3d.rst
---

# CollisionShape3D

**Inherits:** Node3D < Node < Object

A node that provides a Shape3D to a CollisionObject3D parent.

## Description

A node that provides a Shape3D to a CollisionObject3D parent and allows to edit it. This can give a detection shape to an Area3D or turn a PhysicsBody3D into a solid object.

**Warning:** A non-uniformly scaled CollisionShape3D will likely not behave as expected. Make sure to keep its scale the same on all axes and adjust its shape resource instead.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `shape` | Shape3D | null | The actual shape owned by this collision shape |
| `disabled` | bool | `false` | If true, collision shape has no effect |
| `debug_color` | Color | `Color(0, 0, 0, 0)` | Color displayed in editor/debug mode |
| `debug_fill` | bool | `true` | Show solid fill color in addition to wireframe |

## Key Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `make_convex_from_siblings()` | void | Creates convex shape from sibling MeshInstance3D geometry |
| `resource_changed(resource)` | void | **Deprecated** - Does nothing (use Resource.changed instead) |

## Properties Detail

### shape

The actual shape owned by this collision shape. Can be any Shape3D type:
- BoxShape3D
- SphereShape3D
- CapsuleShape3D
- CylinderShape3D
- ConvexPolygonShape3D
- ConcavePolygonShape3D
- HeightMapShape3D
- WorldBoundaryShape3D
- SeparationRayShape3D

### disabled

A disabled collision shape has no effect in the world. This property should be changed with `Object.set_deferred()`.

```gdscript
# Correct way to disable
collision_shape.set_deferred("disabled", true)

# Incorrect (may cause physics errors)
collision_shape.disabled = true
```

### debug_color

The collision shape color displayed in the editor, or in the running project if **Debug > Visible Collision Shapes** is checked.

Default value is from `ProjectSettings.debug/shapes/collision/shape_color`.

### debug_fill

If `true`, when the shape is displayed, it will show a solid fill color in addition to its wireframe.

## Basic Setup

```gdscript
extends CollisionObject3D

func _ready() -> void:
    # Create collision shape
    var collision_shape := CollisionShape3D.new()

    # Create box shape
    var shape := BoxShape3D.new()
    shape.size = Vector3(2, 2, 2)

    collision_shape.shape = shape
    add_child(collision_shape)
```

## Common Shape Types

### BoxShape3D

```gdscript
var shape := BoxShape3D.new()
shape.size = Vector3(2.0, 1.0, 2.0)  # Width, height, depth
```

### SphereShape3D

```gdscript
var shape := SphereShape3D.new()
shape.radius = 1.0
```

### CapsuleShape3D

```gdscript
var shape := CapsuleShape3D.new()
shape.radius = 0.5
shape.height = 2.0  # Total height including caps
```

### CylinderShape3D

```gdscript
var shape := CylinderShape3D.new()
shape.radius = 1.0
shape.height = 2.0
```

## Dynamic Shape Modification

```gdscript
extends CharacterBody3D

@onready var collision_shape: CollisionShape3D = $CollisionShape3D

func crouch() -> void:
    if collision_shape.shape is CapsuleShape3D:
        var shape := collision_shape.shape as CapsuleShape3D
        shape.height = 1.0  # Make shorter

func stand() -> void:
    if collision_shape.shape is CapsuleShape3D:
        var shape := collision_shape.shape as CapsuleShape3D
        shape.height = 2.0  # Return to normal height
```

## Enable/Disable Collision

```gdscript
extends Area3D

@onready var collision_shape: CollisionShape3D = $CollisionShape3D

func disable_collision() -> void:
    # Use set_deferred to avoid physics errors
    collision_shape.set_deferred("disabled", true)

func enable_collision() -> void:
    collision_shape.set_deferred("disabled", false)
```

## Create Convex Shape from Mesh

```gdscript
extends StaticBody3D

@onready var mesh_instance: MeshInstance3D = $MeshInstance3D
@onready var collision_shape: CollisionShape3D = $CollisionShape3D

func _ready() -> void:
    # Automatically create convex shape from mesh
    collision_shape.make_convex_from_siblings()
```

## Multiple Collision Shapes

```gdscript
extends CharacterBody3D

func _ready() -> void:
    # Body collision
    var body_shape := CollisionShape3D.new()
    body_shape.shape = CapsuleShape3D.new()
    body_shape.shape.height = 1.8
    body_shape.shape.radius = 0.4
    add_child(body_shape)

    # Head collision (on top)
    var head_shape := CollisionShape3D.new()
    head_shape.shape = SphereShape3D.new()
    head_shape.shape.radius = 0.3
    head_shape.position = Vector3.UP * 1.0
    add_child(head_shape)
```

## Debug Visualization

```gdscript
extends CollisionShape3D

func _ready() -> void:
    # Set custom debug color
    debug_color = Color.RED
    debug_fill = true  # Show solid fill

    # Enable debug shapes at runtime
    get_tree().debug_collisions_hint = true
```

## Shape Selection Guide

| Use Case | Recommended Shape | Reason |
|----------|------------------|--------|
| Character/NPC | CapsuleShape3D | Smooth movement, doesn't catch on edges |
| Projectile | SphereShape3D | Fast collision checks, omnidirectional |
| Box/Crate | BoxShape3D | Matches visual, stable stacking |
| Floor/Wall | BoxShape3D or WorldBoundaryShape3D | Simple and performant |
| Vehicle | ConvexPolygonShape3D | Better approximation of shape |
| Terrain | ConcavePolygonShape3D or HeightMapShape3D | Exact collision (static only) |
| Trigger zone | BoxShape3D or SphereShape3D | Simple detection volume |

## Notes

- **Scale warning:** Non-uniform scale (e.g., `Vector3(2, 1, 1)`) can cause unexpected physics behavior. Scale the shape resource instead.
- **Performance:** Simpler shapes (Box, Sphere, Capsule) are faster than complex shapes (Convex, Concave)
- **Concave shapes:** ConcavePolygonShape3D only works with StaticBody3D and Area3D, not dynamic bodies
- **Disabled changes:** Always use `set_deferred("disabled", value)` to avoid physics errors
- **Multiple shapes:** One CollisionObject3D can have multiple CollisionShape3D children
- **Position/rotation:** CollisionShape3D can be positioned/rotated relative to parent
- **Debug color:** Default is from project settings, transparent black `Color(0,0,0,0)` means use default

## Common Patterns

### Basic Shape Setup (Most Common)

Creating collision shapes at runtime:

```gdscript
extends CharacterBody3D

func _ready() -> void:
    # Create collision shape node
    var collision_shape := CollisionShape3D.new()

    # Create and configure capsule shape (best for characters)
    var shape := CapsuleShape3D.new()
    shape.radius = 0.4
    shape.height = 1.8

    collision_shape.shape = shape
    add_child(collision_shape)
```

### Enable/Disable Collision

Toggle collision at runtime (use `set_deferred` to avoid physics errors):

```gdscript
extends Area3D

@onready var collision_shape: CollisionShape3D = $CollisionShape3D

func disable_collision() -> void:
    # ALWAYS use set_deferred when changing disabled property
    collision_shape.set_deferred("disabled", true)

func enable_collision() -> void:
    collision_shape.set_deferred("disabled", false)
```

### Dynamic Shape Modification (Crouching)

Modify collision shape properties at runtime:

```gdscript
extends CharacterBody3D

@onready var collision: CollisionShape3D = $CollisionShape3D
const STAND_HEIGHT: float = 1.8
const CROUCH_HEIGHT: float = 1.0

func crouch() -> void:
    var shape := collision.shape as CapsuleShape3D
    shape.height = CROUCH_HEIGHT
    collision.position.y = CROUCH_HEIGHT / 2.0

func stand() -> void:
    var shape := collision.shape as CapsuleShape3D
    shape.height = STAND_HEIGHT
    collision.position.y = STAND_HEIGHT / 2.0
```

### Debug Visualization

Enable runtime collision visualization:

```gdscript
extends CollisionShape3D

func _ready() -> void:
    # Set custom debug color for this shape
    debug_color = Color.RED
    debug_fill = true

    # Enable collision shapes globally (for all CollisionShape3D nodes)
    get_tree().debug_collisions_hint = true
```
