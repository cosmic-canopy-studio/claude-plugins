---
topic: 2d-character-movement
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-character-body-2d
  - godot-8-way-movement
  - godot-platformer-mechanics
---

# 2D Character Movement

CharacterBody2D patterns for player and NPC movement in 2D games.

## 8-Way Movement (Top-Down) {#8-way}

Basic WASD/arrow key movement for top-down games:

```gdscript
extends CharacterBody2D

@export var speed: float = 300.0

func _physics_process(delta: float) -> void:
    var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    velocity = direction * speed
    move_and_slide()
```

**Input Actions Required:** `move_left`, `move_right`, `move_up`, `move_down`

### With Acceleration

Smoother movement with acceleration/deceleration:

```gdscript
@export var speed: float = 300.0
@export var acceleration: float = 1500.0
@export var friction: float = 1200.0

func _physics_process(delta: float) -> void:
    var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")

    if direction != Vector2.ZERO:
        velocity = velocity.move_toward(direction * speed, acceleration * delta)
    else:
        velocity = velocity.move_toward(Vector2.ZERO, friction * delta)

    move_and_slide()
```

## Platformer Movement {#platformer}

Side-scrolling with gravity and jump:

```gdscript
extends CharacterBody2D

@export var speed: float = 300.0
@export var jump_strength: float = 500.0
@export var gravity: float = 1200.0

func _physics_process(delta: float) -> void:
    velocity.x = Input.get_axis("move_left", "move_right") * speed
    velocity.y += gravity * delta

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = -jump_strength

    move_and_slide()
```

**Input Actions Required:** `move_left`, `move_right`, `jump`

### Variable Jump Height

Allow short hops and full jumps:

```gdscript
@export var jump_strength: float = 500.0
@export var jump_release_multiplier: float = 0.5

func _physics_process(delta: float) -> void:
    # ... movement code ...

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = -jump_strength

    # Release early for short jump
    if Input.is_action_just_released("jump") and velocity.y < 0:
        velocity.y *= jump_release_multiplier

    move_and_slide()
```

## Coyote Time {#coyote-time}

Allow jumping briefly after leaving a platform:

```gdscript
@export var coyote_time: float = 0.1

var _coyote_timer: float = 0.0
var _was_on_floor: bool = false

func _physics_process(delta: float) -> void:
    # Update coyote timer
    if is_on_floor():
        _coyote_timer = coyote_time
        _was_on_floor = true
    elif _was_on_floor:
        _coyote_timer -= delta
        if _coyote_timer <= 0:
            _was_on_floor = false

    # Jump with coyote time
    if Input.is_action_just_pressed("jump") and (_coyote_timer > 0 or is_on_floor()):
        velocity.y = -jump_strength
        _coyote_timer = 0  # Consume coyote time

    velocity.y += gravity * delta
    move_and_slide()
```

## Wall Sliding {#wall-slide}

Slow descent when touching walls:

```gdscript
@export var wall_slide_gravity: float = 200.0

func _physics_process(delta: float) -> void:
    # Normal gravity
    velocity.y += gravity * delta

    # Reduced gravity on walls
    if is_on_wall() and velocity.y > 0:
        velocity.y = min(velocity.y, wall_slide_gravity)

    move_and_slide()
```

### Wall Jump

Jump off walls:

```gdscript
@export var wall_jump_strength: Vector2 = Vector2(400, 500)

func _physics_process(delta: float) -> void:
    if Input.is_action_just_pressed("jump"):
        if is_on_floor():
            velocity.y = -jump_strength
        elif is_on_wall():
            var wall_normal := get_wall_normal()
            velocity.x = wall_normal.x * wall_jump_strength.x
            velocity.y = -wall_jump_strength.y

    move_and_slide()
```

## Dash Mechanic {#dash}

Quick burst of speed with cooldown:

```gdscript
@export var dash_speed: float = 800.0
@export var dash_duration: float = 0.15
@export var dash_cooldown: float = 0.5

var _is_dashing: bool = false
var _can_dash: bool = true
var _dash_direction: Vector2 = Vector2.RIGHT

func _physics_process(delta: float) -> void:
    var input_dir := Input.get_vector("move_left", "move_right", "move_up", "move_down")

    if input_dir != Vector2.ZERO:
        _dash_direction = input_dir.normalized()

    if Input.is_action_just_pressed("dash") and _can_dash:
        _start_dash()

    if _is_dashing:
        velocity = _dash_direction * dash_speed
    else:
        velocity = input_dir * speed

    move_and_slide()

func _start_dash() -> void:
    _is_dashing = true
    _can_dash = false
    await get_tree().create_timer(dash_duration).timeout
    _is_dashing = false
    await get_tree().create_timer(dash_cooldown).timeout
    _can_dash = true
```

## Smooth Movement {#smooth-movement}

Delta-independent lerp for smooth acceleration:

```gdscript
@export var speed: float = 300.0
@export var smoothing: float = 10.0  # Higher = snappier

func _physics_process(delta: float) -> void:
    var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    var target_velocity := direction * speed

    velocity = velocity.lerp(target_velocity, 1.0 - exp(-smoothing * delta))
    move_and_slide()
```

## Sprite Flipping

Flip sprite based on movement direction:

```gdscript
@onready var sprite: Sprite2D = $Sprite2D

func _physics_process(delta: float) -> void:
    var direction := Input.get_axis("move_left", "move_right")

    if direction != 0:
        sprite.flip_h = direction < 0

    # ... rest of movement
```

## Pixel Art Note

For pixel art games, round position after movement to prevent pixel jittering:

```gdscript
func _physics_process(delta: float) -> void:
    # ... movement code ...
    move_and_slide()

    # Round position for pixel-perfect rendering
    global_position = global_position.round()
```

## Scene Setup

```
CharacterBody2D (root)
├── CollisionShape2D
│   └── CapsuleShape2D or RectangleShape2D
├── Sprite2D or AnimatedSprite2D
└── (optional) Camera2D
```

**Collision Settings:**
- `collision_layer`: What this body IS (e.g., player = layer 1)
- `collision_mask`: What this body COLLIDES WITH (e.g., walls = layer 2)
