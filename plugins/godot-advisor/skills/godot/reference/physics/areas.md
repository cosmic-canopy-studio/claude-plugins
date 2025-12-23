---
topic: area-triggers
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-area-2d
  - godot-area-3d
---

# Area Triggers

Area2D and Area3D for detection zones, triggers, and overlaps.

## Basic Area Detection {#body-entered}

Detect when bodies enter/exit:

```gdscript
extends Area2D

signal collected

func _ready() -> void:
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
    if body.is_in_group("player"):
        collected.emit()
        queue_free()
```

### Connection in Inspector

1. Select Area2D
2. Node dock > Signals tab
3. Double-click `body_entered` or `body_exited`
4. Select target node and method

### Available Signals

| Signal | Triggered When |
|--------|----------------|
| `body_entered(body)` | PhysicsBody enters |
| `body_exited(body)` | PhysicsBody exits |
| `area_entered(area)` | Another Area enters |
| `area_exited(area)` | Another Area exits |

## Pickup/Collectible

```gdscript
extends Area2D

@export var item_id: String = "coin"
@export var value: int = 10

func _ready() -> void:
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
    if body.has_method("collect_item"):
        body.collect_item(item_id, value)
        queue_free()
```

## Damage Zone

```gdscript
extends Area2D

@export var damage: int = 10
@export var damage_interval: float = 1.0
@export var one_shot: bool = false

var _bodies_in_zone: Array[Node2D] = []
var _damage_timer: Timer

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)

    if not one_shot:
        _damage_timer = Timer.new()
        _damage_timer.wait_time = damage_interval
        _damage_timer.timeout.connect(_deal_damage)
        add_child(_damage_timer)
        _damage_timer.start()

func _on_body_entered(body: Node2D) -> void:
    if body.has_method("take_damage"):
        _bodies_in_zone.append(body)
        if one_shot:
            body.take_damage(damage)

func _on_body_exited(body: Node2D) -> void:
    _bodies_in_zone.erase(body)

func _deal_damage() -> void:
    for body in _bodies_in_zone:
        if is_instance_valid(body) and body.has_method("take_damage"):
            body.take_damage(damage)
```

## Interaction Zone

Detect when player can interact:

```gdscript
extends Area2D

signal interaction_available(interactable: Node2D)
signal interaction_unavailable

var _interactable_in_range: Node2D = null

func _ready() -> void:
    area_entered.connect(_on_area_entered)
    area_exited.connect(_on_area_exited)

func _on_area_entered(area: Area2D) -> void:
    if area.is_in_group("interactable"):
        _interactable_in_range = area.get_parent()
        interaction_available.emit(_interactable_in_range)

func _on_area_exited(area: Area2D) -> void:
    if area.is_in_group("interactable"):
        _interactable_in_range = null
        interaction_unavailable.emit()

func try_interact() -> bool:
    if _interactable_in_range and _interactable_in_range.has_method("interact"):
        _interactable_in_range.interact()
        return true
    return false
```

## Physics Overrides

Areas can modify physics for bodies inside:

```gdscript
extends Area2D

func _ready() -> void:
    # Gravity modification
    gravity_space_override = Area2D.SPACE_OVERRIDE_REPLACE
    gravity_direction = Vector2.UP  # Reverse gravity
    gravity = 980.0

    # Or for water/slow zone
    gravity_space_override = Area2D.SPACE_OVERRIDE_COMBINE
    gravity = 100.0  # Reduced gravity
    linear_damp_space_override = Area2D.SPACE_OVERRIDE_REPLACE
    linear_damp = 5.0  # Slow movement
```

### Space Override Modes

| Mode | Effect |
|------|--------|
| `SPACE_OVERRIDE_DISABLED` | No effect |
| `SPACE_OVERRIDE_COMBINE` | Add to default physics |
| `SPACE_OVERRIDE_REPLACE` | Replace default physics |
| `SPACE_OVERRIDE_COMBINE_REPLACE` | Add, then replace children |
| `SPACE_OVERRIDE_REPLACE_COMBINE` | Replace, then add children |

## 3D Area Example

```gdscript
extends Area3D

@export var force_strength: float = 10.0

func _ready() -> void:
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node3D) -> void:
    if body is RigidBody3D:
        var direction := (body.global_position - global_position).normalized()
        body.apply_impulse(direction * force_strength)
```

## Query Overlapping Bodies

Check what's currently inside:

```gdscript
extends Area2D

func get_enemies_in_range() -> Array[Node2D]:
    var enemies: Array[Node2D] = []
    for body in get_overlapping_bodies():
        if body.is_in_group("enemy"):
            enemies.append(body)
    return enemies

func get_areas_in_range() -> Array[Area2D]:
    return get_overlapping_areas()
```

## Monitoring vs Monitorable

| Property | What It Does |
|----------|-------------|
| `monitoring` | This area DETECTS others (fires signals) |
| `monitorable` | This area CAN BE DETECTED by others |

```gdscript
# Invisible sensor (detects but isn't detected)
monitoring = true
monitorable = false

# Detectable zone (is detected but doesn't detect)
monitoring = false
monitorable = true
```

## Scene Setup

### 2D Trigger Zone
```
Area2D (root)
├── CollisionShape2D
│   └── RectangleShape2D or CircleShape2D
└── Sprite2D (optional visual)
```

### 3D Trigger Zone
```
Area3D (root)
├── CollisionShape3D
│   └── BoxShape3D or SphereShape3D
└── MeshInstance3D (optional visual)
```

**Collision Settings:**
- `collision_layer`: What layer this area occupies
- `collision_mask`: What layers this area detects
