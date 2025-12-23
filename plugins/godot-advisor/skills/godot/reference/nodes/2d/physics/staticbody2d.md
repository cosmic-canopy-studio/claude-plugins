---
class: StaticBody2D
godot_version: "4.3"
sources:
  - local: repos/godot-docs/classes/class_staticbody2d.rst
status: extracted
---

# StaticBody2D

## Inheritance
PhysicsBody2D < CollisionObject2D < Node2D < CanvasItem < Node < Object

## Description
A 2D physics body that can't be moved by external forces. When moved manually, it doesn't affect other bodies in its path.

A static 2D physics body. It can't be moved by external forces or contacts, but can be moved manually by other means such as code, AnimationMixers (with callback_mode_process set to ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS), and RemoteTransform2D.

When StaticBody2D is moved, it is teleported to its new position without affecting other physics bodies in its path. If this is not desired, use AnimatableBody2D instead.

StaticBody2D is useful for completely static objects like floors and walls, as well as moving surfaces like conveyor belts and circular revolving platforms (by using constant_linear_velocity and constant_angular_velocity).

## Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| constant_angular_velocity | float | 0.0 | Body's constant angular velocity (affects touching bodies) |
| constant_linear_velocity | Vector2 | Vector2(0, 0) | Body's constant linear velocity (affects touching bodies) |
| physics_material_override | PhysicsMaterial | null | Physics material override for the body |

## Common Patterns

### Pattern 1: Basic Platform/Wall

```gdscript
extends StaticBody2D

# No special code needed - just attach CollisionShape2D children
# with appropriate shapes (RectangleShape2D, etc.)

func _ready() -> void:
	# Optional: Customize physics material for specific friction/bounce
	if physics_material_override == null:
		var material := PhysicsMaterial.new()
		material.friction = 0.8
		material.bounce = 0.0
		physics_material_override = material
```

### Pattern 2: Conveyor Belt

```gdscript
extends StaticBody2D

@export var belt_speed: float = 100.0
@export var belt_direction: Vector2 = Vector2.RIGHT

func _ready() -> void:
	# Set constant velocity to move objects on the belt
	constant_linear_velocity = belt_direction.normalized() * belt_speed

	# Optional: Low friction material for smoother movement
	var material := PhysicsMaterial.new()
	material.friction = 0.1
	physics_material_override = material
```

### Pattern 3: Rotating Platform

```gdscript
extends StaticBody2D

@export var rotation_speed: float = 1.0  # Radians per second

func _ready() -> void:
	# Set constant angular velocity for continuous rotation
	constant_angular_velocity = rotation_speed

	# Optional: Prevent objects from sliding off
	var material := PhysicsMaterial.new()
	material.friction = 1.5
	physics_material_override = material
```

## See Also
- [Official Docs](https://docs.godotengine.org/en/stable/classes/class_staticbody2d.html)
- [Physics Introduction Tutorial](repos/godot-docs/tutorials/physics/physics_introduction.rst)
