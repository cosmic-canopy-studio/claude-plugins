---
class: CollisionShape2D
godot_version: "4.3"
sources:
  - local: repos/godot-docs/classes/class_collisionshape2d.rst
status: extracted
---

# CollisionShape2D

## Inheritance
Node2D < CanvasItem < Node < Object

## Description
A node that provides a Shape2D to a CollisionObject2D parent.

A node that provides a Shape2D to a CollisionObject2D parent and allows to edit it. This can give a detection shape to an Area2D or turn a PhysicsBody2D into a solid object.

## Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| debug_color | Color | Color(0, 0, 0, 0) | Collision shape color displayed in editor/debug |
| disabled | bool | false | If true, collision shape has no effect (use set_deferred) |
| one_way_collision | bool | false | If true, shape only detects collision on one side |
| one_way_collision_margin | float | 1.0 | Margin for one-way collision in pixels |
| shape | Shape2D | null | The actual shape owned by this collision shape |

## Common Patterns

### Pattern 1: Shape Setup in Code

```gdscript
extends CharacterBody2D

@onready var collision_shape: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	# Create and assign a shape programmatically
	var shape := CircleShape2D.new()
	shape.radius = 20.0
	collision_shape.shape = shape

	# Optional: Set debug visualization color
	collision_shape.debug_color = Color.GREEN
```

### Pattern 2: Dynamic Enable/Disable (Crouching)

```gdscript
extends CharacterBody2D

@onready var standing_collision: CollisionShape2D = $StandingCollision
@onready var crouching_collision: CollisionShape2D = $CrouchingCollision

var is_crouching: bool = false

func _ready() -> void:
	# Start in standing state
	crouching_collision.disabled = true

func toggle_crouch() -> void:
	is_crouching = not is_crouching

	# Use set_deferred to safely change collision during physics step
	standing_collision.set_deferred("disabled", is_crouching)
	crouching_collision.set_deferred("disabled", not is_crouching)
```

### Pattern 3: One-Way Platform

```gdscript
extends StaticBody2D

@onready var platform_collision: CollisionShape2D = $CollisionShape2D

func _ready() -> void:
	# Configure as one-way platform (player can jump through from below)
	platform_collision.one_way_collision = true
	platform_collision.one_way_collision_margin = 2.0

	# Create platform shape
	var shape := RectangleShape2D.new()
	shape.size = Vector2(128, 16)
	platform_collision.shape = shape
```

## See Also
- [Official Docs](https://docs.godotengine.org/en/stable/classes/class_collisionshape2d.html)
- [Physics Introduction Tutorial](repos/godot-docs/tutorials/physics/physics_introduction.rst)
- [Collision Shapes 2D Tutorial](repos/godot-docs/tutorials/physics/collision_shapes_2d.rst)
