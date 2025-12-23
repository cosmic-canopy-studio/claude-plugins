---
class: Area2D
godot_version: "4.3"
sources:
  - local: repos/godot-docs/classes/class_area2d.rst
status: extracted
---

# Area2D

## Inheritance
CollisionObject2D < Node2D < CanvasItem < Node < Object

## Description
A region of 2D space that detects other CollisionObject2Ds entering or exiting it.

Area2D is a region of 2D space defined by one or multiple CollisionShape2D or CollisionPolygon2D child nodes. It detects when other CollisionObject2Ds enter or exit it, and it also keeps track of which collision objects haven't exited it yet (i.e. which one are overlapping it).

This node can also locally alter or override physics parameters (gravity, damping) and route audio to custom audio buses.

**Note:** Areas and bodies created with PhysicsServer2D might not interact as expected with Area2Ds, and might not emit signals or track objects correctly.

## Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| angular_damp | float | 1.0 | Rate at which objects stop spinning in this area |
| angular_damp_space_override | SpaceOverride | 0 | Override mode for angular damping calculations |
| audio_bus_name | StringName | &"Master" | Name of the area's audio bus |
| audio_bus_override | bool | false | If true, area's audio bus overrides default |
| gravity | float | 980.0 | Area's gravity intensity in pixels per second squared |
| gravity_direction | Vector2 | Vector2(0, 1) | Area's gravity vector (not normalized) |
| gravity_point | bool | false | If true, gravity calculated from a point |
| gravity_point_center | Vector2 | Vector2(0, 1) | Point of attraction if gravity is a point |
| gravity_point_unit_distance | float | 0.0 | Distance where gravity strength equals gravity value |
| gravity_space_override | SpaceOverride | 0 | Override mode for gravity calculations |
| linear_damp | float | 0.1 | Rate at which objects stop moving in this area |
| linear_damp_space_override | SpaceOverride | 0 | Override mode for linear damping calculations |
| monitorable | bool | true | If true, other monitoring areas can detect this area |
| monitoring | bool | true | If true, area detects bodies/areas entering and exiting |
| priority | int | 0 | Area's priority (higher priority processed first) |

## Methods
| Method | Return | Description |
|--------|--------|-------------|
| get_overlapping_areas() | Array[Area2D] | Returns list of intersecting Area2Ds |
| get_overlapping_bodies() | Array[Node2D] | Returns list of intersecting PhysicsBody2Ds and TileMaps |
| has_overlapping_areas() | bool | Returns true if intersecting any Area2Ds |
| has_overlapping_bodies() | bool | Returns true if intersecting any bodies |
| overlaps_area(area: Node) | bool | Returns true if given Area2D intersects this area |
| overlaps_body(body: Node) | bool | Returns true if given body intersects this area |

## Signals
| Signal | Parameters | Description |
|--------|------------|-------------|
| area_entered | area: Area2D | Emitted when another area enters this area |
| area_exited | area: Area2D | Emitted when another area exits this area |
| area_shape_entered | area_rid: RID, area: Area2D, area_shape_index: int, local_shape_index: int | Emitted when a shape of another area enters |
| area_shape_exited | area_rid: RID, area: Area2D, area_shape_index: int, local_shape_index: int | Emitted when a shape of another area exits |
| body_entered | body: Node2D | Emitted when a body enters this area |
| body_exited | body: Node2D | Emitted when a body exits this area |
| body_shape_entered | body_rid: RID, body: Node2D, body_shape_index: int, local_shape_index: int | Emitted when a shape of a body enters |
| body_shape_exited | body_rid: RID, body: Node2D, body_shape_index: int, local_shape_index: int | Emitted when a shape of a body exits |

## Enums

### SpaceOverride
| Value | Name | Description |
|-------|------|-------------|
| 0 | SPACE_OVERRIDE_DISABLED | Area does not affect gravity/damping |
| 1 | SPACE_OVERRIDE_COMBINE | Area adds its values to calculated values |
| 2 | SPACE_OVERRIDE_COMBINE_REPLACE | Area adds values, ignoring lower priority areas |
| 3 | SPACE_OVERRIDE_REPLACE | Area replaces all gravity/damping values |
| 4 | SPACE_OVERRIDE_REPLACE_COMBINE | Area replaces values but continues calculating other areas |

## Common Patterns

### Pattern 1: Damage Zone

```gdscript
extends Area2D

@export var damage_per_second: float = 10.0

var bodies_inside: Array[Node2D] = []

func _ready() -> void:
	body_entered.connect(_on_body_entered)
	body_exited.connect(_on_body_exited)

func _on_body_entered(body: Node2D) -> void:
	if body.has_method("take_damage"):
		bodies_inside.append(body)

func _on_body_exited(body: Node2D) -> void:
	bodies_inside.erase(body)

func _process(delta: float) -> void:
	for body in bodies_inside:
		if body.has_method("take_damage"):
			body.take_damage(damage_per_second * delta)
```

### Pattern 2: Pickup/Collectible Detection

```gdscript
extends Area2D

@export var pickup_value: int = 10
@export var pickup_type: String = "coin"

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
	if body.has_method("collect_item"):
		body.collect_item(pickup_type, pickup_value)
		queue_free()  # Remove pickup after collection
```

### Pattern 3: Trigger Zone with Cooldown

```gdscript
extends Area2D

signal triggered(body: Node2D)

@export var cooldown_time: float = 2.0

var is_on_cooldown: bool = false
var cooldown_timer: Timer

func _ready() -> void:
	body_entered.connect(_on_body_entered)

	# Create cooldown timer
	cooldown_timer = Timer.new()
	cooldown_timer.one_shot = true
	cooldown_timer.timeout.connect(_on_cooldown_finished)
	add_child(cooldown_timer)

func _on_body_entered(body: Node2D) -> void:
	if not is_on_cooldown and body is CharacterBody2D:
		triggered.emit(body)
		is_on_cooldown = true
		cooldown_timer.start(cooldown_time)

func _on_cooldown_finished() -> void:
	is_on_cooldown = false
```

## See Also
- [Official Docs](https://docs.godotengine.org/en/stable/classes/class_area2d.html)
- [Using Area2D Tutorial](repos/godot-docs/tutorials/physics/using_area_2d.rst)
- [Physics Introduction Tutorial](repos/godot-docs/tutorials/physics/physics_introduction.rst)
