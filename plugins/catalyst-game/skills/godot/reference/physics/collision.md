---
topic: collision-detection
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-collision-shape-2d
  - godot-collision-shape-3d
  - godot-collision-layers
---

# Collision Detection

Collision shapes, layers, and detection in Godot.

## Collision Shapes {#shapes}

### 2D Shapes

```gdscript
# Rectangle
var rect := RectangleShape2D.new()
rect.size = Vector2(32, 64)

# Circle
var circle := CircleShape2D.new()
circle.radius = 16.0

# Capsule (good for characters)
var capsule := CapsuleShape2D.new()
capsule.radius = 16.0
capsule.height = 48.0

# Apply to CollisionShape2D
collision_shape.shape = capsule
```

### 3D Shapes

```gdscript
# Box
var box := BoxShape3D.new()
box.size = Vector3(1, 2, 1)

# Sphere
var sphere := SphereShape3D.new()
sphere.radius = 0.5

# Capsule (good for characters)
var capsule := CapsuleShape3D.new()
capsule.radius = 0.5
capsule.height = 2.0

# Apply to CollisionShape3D
collision_shape.shape = capsule
```

## Collision Layers {#layers}

Godot uses layers (what something IS) and masks (what it COLLIDES WITH).

### Common Layer Setup

| Layer | Name | Usage |
|-------|------|-------|
| 1 | World | Static geometry, walls, floors |
| 2 | Player | Player character |
| 3 | Enemy | Enemy characters |
| 4 | Projectile | Bullets, arrows |
| 5 | Pickup | Collectibles, items |
| 6 | Platform | One-way platforms |

### Setting Layers in Code

```gdscript
# Set what this body IS (appears on layer 2 = player)
collision_layer = 1 << 1  # Layer 2

# Set what this body COLLIDES WITH (world + enemies)
collision_mask = (1 << 0) | (1 << 2)  # Layers 1 and 3

# Helper functions
func set_layer(layer_num: int, enabled: bool) -> void:
    set_collision_layer_value(layer_num, enabled)

func set_mask(layer_num: int, enabled: bool) -> void:
    set_collision_mask_value(layer_num, enabled)
```

### Dynamic Layer Changes

```gdscript
# Temporarily disable collision with platforms (for pass-through)
const PLATFORM_LAYER := 6

func drop_through_platform() -> void:
    set_collision_mask_value(PLATFORM_LAYER, false)
    await get_tree().create_timer(0.3).timeout
    set_collision_mask_value(PLATFORM_LAYER, true)
```

## One-Way Platforms {#one-way}

Platforms you can jump through from below:

### Using CollisionShape2D

```gdscript
# On the platform's CollisionShape2D:
one_way_collision = true
one_way_collision_margin = 4.0  # Pixels of tolerance
```

### Drop-Through Functionality

```gdscript
extends CharacterBody2D

const PLATFORM_LAYER := 6

func _physics_process(delta: float) -> void:
    if Input.is_action_just_pressed("move_down") and is_on_floor():
        # Check if on a one-way platform
        for i in get_slide_collision_count():
            var collision := get_slide_collision(i)
            var collider := collision.get_collider()
            if collider.collision_layer & (1 << (PLATFORM_LAYER - 1)):
                set_collision_mask_value(PLATFORM_LAYER, false)
                await get_tree().create_timer(0.2).timeout
                set_collision_mask_value(PLATFORM_LAYER, true)
                break
```

## Moving Platforms {#moving-platforms}

Platforms that carry the player:

```gdscript
extends AnimatableBody2D  # NOT StaticBody2D

@export var travel: Vector2 = Vector2(200, 0)
@export var duration: float = 2.0

func _ready() -> void:
    # sync_to_physics must be true for smooth movement
    sync_to_physics = true

    var tween := create_tween()
    tween.set_loops()
    tween.tween_property(self, "position", position + travel, duration)
    tween.tween_property(self, "position", position, duration)
```

**Key:** Use `AnimatableBody2D` (not StaticBody2D) with `sync_to_physics = true` for moving platforms that carry characters.

## Checking Collisions

### Get Slide Collisions (CharacterBody)

```gdscript
func _physics_process(delta: float) -> void:
    move_and_slide()

    # Check what we collided with
    for i in get_slide_collision_count():
        var collision := get_slide_collision(i)
        var collider := collision.get_collider()

        if collider.is_in_group("enemy"):
            _handle_enemy_collision(collider)
        elif collider.is_in_group("hazard"):
            take_damage()
```

### Manual Shape Query

```gdscript
func check_overlap(shape: Shape2D, position: Vector2) -> Array[Node2D]:
    var query := PhysicsShapeQueryParameters2D.new()
    query.shape = shape
    query.transform = Transform2D(0, position)
    query.collision_mask = collision_mask

    var space := get_world_2d().direct_space_state
    var results := space.intersect_shape(query)

    var nodes: Array[Node2D] = []
    for result in results:
        nodes.append(result.collider)
    return nodes
```

## Collision Exceptions

Ignore specific objects:

```gdscript
# Add exception (won't collide with this object)
add_collision_exception_with(other_body)

# Remove exception
remove_collision_exception_with(other_body)

# Example: projectile ignores shooter
func _ready() -> void:
    add_collision_exception_with(owner)  # owner = who fired this
```

## Compound Colliders

Multiple shapes for complex collision:

```
CharacterBody2D
├── CollisionShape2D (body - capsule)
├── CollisionShape2D (head - circle, for headshots)
└── CollisionShape2D (feet - small box, for ground detection)
```

```gdscript
@onready var body_collision := $BodyCollision
@onready var crouch_collision := $CrouchCollision

func set_crouching(crouching: bool) -> void:
    body_collision.disabled = crouching
    crouch_collision.disabled = not crouching
```

## Debug Visualization

Enable collision shape visibility:
- **Editor:** Debug > Visible Collision Shapes
- **Runtime:** In Project Settings, enable Debug > Shapes

```gdscript
# Draw collision shape for debugging
func _draw() -> void:
    var shape := $CollisionShape2D.shape
    if shape is CircleShape2D:
        draw_circle(Vector2.ZERO, shape.radius, Color.RED)
    elif shape is RectangleShape2D:
        draw_rect(Rect2(-shape.size/2, shape.size), Color.RED, false)
```
