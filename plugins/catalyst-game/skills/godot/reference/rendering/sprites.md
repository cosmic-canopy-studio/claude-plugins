---
topic: sprites
version: 2025.12.21
godot_version: "4.3"
sources:
  - official: https://docs.godotengine.org/en/stable/classes/class_sprite2d.html
  - official: https://docs.godotengine.org/en/stable/classes/class_animatedsprite2d.html
  - official: https://docs.godotengine.org/en/stable/tutorials/2d/2d_sprite_animation.html
  - examples: repos/godot_node_essentials
---

# Sprites

2D graphics rendering with static and animated sprites.

## Static Sprites (Sprite2D) {#static}

Display a single texture:

```gdscript
extends Sprite2D

func _ready() -> void:
    texture = preload("res://assets/player.png")
    centered = true  # Center on position (default)
    offset = Vector2.ZERO  # Additional offset
```

### Texture Properties

```gdscript
extends Sprite2D

func _ready() -> void:
    # Basic texture assignment
    texture = load("res://assets/sprite.png")

    # Flipping
    flip_h = false  # Horizontal flip
    flip_v = false  # Vertical flip

    # Positioning
    centered = true  # Pivot at center
    offset = Vector2(0, -8)  # Additional offset from center

    # Sprite sheet region (if using atlas)
    region_enabled = false
    region_rect = Rect2(0, 0, 32, 32)  # Sub-region of texture
```

### Dynamic Texture Loading

```gdscript
extends Sprite2D

@export var texture_path: String = "res://assets/icons/sword.png"

func _ready() -> void:
    texture = load(texture_path)

func set_sprite_texture(new_texture: Texture2D) -> void:
    texture = new_texture
```

**Example from godot_node_essentials:**
```gdscript
# Level editor cursor
@onready var _mouse_cursor: Sprite2D = %MouseCursor

func set_paint_mode() -> void:
    _mouse_cursor.texture = PaintCursorTexture
    _mouse_cursor.scale = 2.0 * Vector2.ONE

func set_erase_mode() -> void:
    _mouse_cursor.texture = EraseCursorTexture
    _mouse_cursor.scale = Vector2.ONE
```

## Animated Sprites (AnimatedSprite2D) {#animated}

Play frame-based animations:

```gdscript
extends AnimatedSprite2D

func _ready() -> void:
    # Sprite frames must be set up in editor or via code
    sprite_frames = preload("res://assets/player_animations.tres")
    animation = "idle"  # Default animation
    autoplay = "idle"  # Auto-start this animation
    play()

func start_running() -> void:
    play("run")

func stop_animation() -> void:
    stop()
```

### Animation Control

```gdscript
extends AnimatedSprite2D

func _ready() -> void:
    animation_finished.connect(_on_animation_finished)

func play_animation(anim_name: String, from_start: bool = true) -> void:
    if from_start:
        frame = 0
    play(anim_name)

func _on_animation_finished() -> void:
    # Called when non-looping animation completes
    if animation == "attack":
        play("idle")
```

**Example from godot_node_essentials:**
```gdscript
# Character name UI with animated portrait
@onready var _animated_sprite: AnimatedSprite2D = $AnimatedSprite2D

func _on_button_button_down(button: Button) -> void:
    _animated_sprite.frame = button.get_index()
```

### Isometric Character Animations

```gdscript
extends CharacterBody2D

const ANIMATION_FPS := 16.0

var _input_direction_to_cardinal_direction: Dictionary[Vector2, String] = {
    (Vector2.RIGHT + Vector2.UP).normalized(): "north",
    Vector2.RIGHT: "north_east",
    (Vector2.RIGHT + Vector2.DOWN).normalized(): "east",
    Vector2.DOWN: "south_east",
    (Vector2.LEFT + Vector2.DOWN).normalized(): "south",
    Vector2.LEFT: "south_west",
    (Vector2.LEFT + Vector2.UP).normalized(): "west",
    Vector2.UP: "north_west",
}

@onready var animated_sprite: AnimatedSprite2D = %AnimatedSprite2D

func _physics_process(_delta: float) -> void:
    var input_direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")

    if input_direction.is_zero_approx():
        var idle_animation := animated_sprite.animation.replace("run", "idle")
        animated_sprite.play(idle_animation)
        return

    var orientation := _input_direction_to_cardinal_direction[input_direction]
    animated_sprite.play("run_%s" % orientation)
    move_and_slide()

func _adjust_animation_fps() -> void:
    var isometric_factor := Vector2(1.0, 0.5)  # Example ratio

    for animation in animated_sprite.sprite_frames.get_animation_names():
        if animation.begins_with("idle"):
            continue

        var animation_fps := ANIMATION_FPS
        match animation:
            "run_north_west", "run_south_east":
                animation_fps *= isometric_factor.y
            "run_north", "run_east", "run_south", "run_west":
                animation_fps *= (isometric_factor.x + isometric_factor.y) / 2.0

        animated_sprite.sprite_frames.set_animation_speed(animation, animation_fps)
```

## Sprite Flipping {#flipping}

Flip sprites to face different directions:

```gdscript
extends Sprite2D

func face_direction(direction: Vector2) -> void:
    if direction.x < 0:
        flip_h = true
    elif direction.x > 0:
        flip_h = false

# Alternative: use scale for flipping with preserved starting scale
var _skin_start_scale: Vector2

func _ready() -> void:
    _skin_start_scale = scale

func face_horizontal_direction(horizontal_direction: float) -> void:
    scale.x = -sign(horizontal_direction) * _skin_start_scale.x
```

**Example from godot_node_essentials:**
```gdscript
# Robot enemy that faces player
@onready var _skin: Sprite2D = %Skin

var _horizontal_direction: float = 1.0

func update_facing() -> void:
    _skin.scale.x = _horizontal_direction
```

## Dynamic Scaling {#scaling}

Scale sprites based on game state:

```gdscript
extends Sprite2D

# Pulse effect
func pulse(duration: float = 0.5) -> void:
    var tween := create_tween().set_trans(Tween.TRANS_ELASTIC)
    tween.tween_property(self, "scale", Vector2.ONE * 1.2, duration / 2.0)
    tween.tween_property(self, "scale", Vector2.ONE, duration / 2.0)

# Grow/shrink over time
func grow(delta: float, growth_rate: float = 1.0) -> void:
    scale *= (1.0 + delta * growth_rate)
```

**Example from godot_node_essentials:**
```gdscript
# Ship flames scale with velocity
@onready var _flame_main: Sprite2D = %FlameMain
@onready var _flame_left: Sprite2D = %FlameLeft
@onready var _flame_right: Sprite2D = %FlameRight

const MAX_SPEED := 1000.0

func _update_flames() -> void:
    var speed_rate := velocity.length() / MAX_SPEED

    _flame_main.scale = Vector2.ONE * speed_rate
    _flame_left.scale = Vector2.ONE * speed_rate * 0.35
    _flame_right.scale = Vector2.ONE * speed_rate * 0.35
```

## Sprite Sheets & Regions {#sprite-sheets}

Use texture atlases for better performance:

```gdscript
extends Sprite2D

func _ready() -> void:
    texture = preload("res://assets/sprite_sheet.png")
    region_enabled = true

    # Show top-left 32x32 tile
    region_rect = Rect2(0, 0, 32, 32)

func set_frame(frame_x: int, frame_y: int, frame_size: int = 32) -> void:
    region_rect = Rect2(
        frame_x * frame_size,
        frame_y * frame_size,
        frame_size,
        frame_size
    )
```

### Texture Atlas Coordinates

```gdscript
# Accessing tiles by atlas coordinates
const TILE_COORDS := {
    "door_closed": Vector2i(5, 0),
    "door_open": Vector2i(1, 1),
    "switch_off": Vector2i(4, 3),
    "switch_on": Vector2i(0, 3),
}

func show_sprite(sprite_name: String, tile_size: int = 32) -> void:
    var coords: Vector2i = TILE_COORDS[sprite_name]
    region_enabled = true
    region_rect = Rect2(coords.x * tile_size, coords.y * tile_size, tile_size, tile_size)
```

## State-Based Sprites {#state-based}

Change sprites based on game state:

```gdscript
extends Node2D

@export var texture_normal: Texture2D
@export var texture_pressed: Texture2D

@onready var _sprite: Sprite2D = %Sprite2D

var is_activated := false

func activate() -> void:
    is_activated = not is_activated
    _sprite.texture = texture_pressed if is_activated else texture_normal
```

**Example from godot_node_essentials:**
```gdscript
# Pressure plate
@export var texture_pressed: Texture2D

@onready var _sprite: Sprite2D = %Sprite2D

func _on_body_entered(body: Node2D) -> void:
    _sprite.texture = texture_pressed
```

## Frame-Based Animations (AnimatedSprite2D) {#frames}

Control individual frames:

```gdscript
extends AnimatedSprite2D

func _ready() -> void:
    sprite_frames = preload("res://assets/turret_frames.tres")
    animation = "default"
    frame = 0  # Start frame
    speed_scale = 1.0  # Animation speed multiplier

func set_turret_state(is_active: bool) -> void:
    frame = 1 if is_active else 0
```

**Example from godot_node_essentials:**
```gdscript
# Turret with line of sight
@onready var _turret: AnimatedSprite2D = %Turret

var _has_target := false

func _set_has_target(is_found: bool) -> void:
    _has_target = is_found
    _turret.frame = 1 if _has_target else 0
```

## Choosing Sprite vs AnimatedSprite2D {#choosing}

**Use Sprite2D when:**
- Displaying static images (UI icons, background objects)
- Manual texture swapping for simple state changes
- Using sprite sheets with manual region control
- Performance is critical (Sprite2D is lighter)

**Use AnimatedSprite2D when:**
- Playing frame-based animations (walk cycles, explosions)
- Need automatic frame timing and looping
- Working with SpriteFrames resources
- Multiple animation states (idle, run, attack, etc.)

**Example decision flow:**
```gdscript
# Static icon → Sprite2D
var icon: Sprite2D = Sprite2D.new()
icon.texture = load("res://icon.png")

# 2-3 states with manual control → Sprite2D
var door: Sprite2D = Sprite2D.new()
door.texture = door_closed_texture if is_closed else door_open_texture

# Multiple frames, automatic playback → AnimatedSprite2D
var character: AnimatedSprite2D = AnimatedSprite2D.new()
character.sprite_frames = load("res://character_anims.tres")
character.play("walk")
```

## Common Patterns

### Character Facing Direction

```gdscript
extends CharacterBody2D

@onready var _sprite: Sprite2D = %Sprite2D

func _physics_process(delta: float) -> void:
    var direction := Input.get_axis("move_left", "move_right")

    if not is_zero_approx(direction):
        _sprite.flip_h = direction < 0
        velocity.x = direction * 300.0

    move_and_slide()
```

### Blinking Effect

```gdscript
extends Sprite2D

@onready var _animation_player: AnimationPlayer = $AnimationPlayer

func take_damage() -> void:
    start_blink()

func start_blink(loop_mode: Animation.LoopMode = Animation.LOOP_NONE) -> void:
    _animation_player.get_animation("blink").loop_mode = loop_mode
    _animation_player.play("blink")

func stop_blink() -> void:
    _animation_player.stop()
    _animation_player.seek(0, true)
```

### UI Cursor Following Mouse

```gdscript
extends Sprite2D

func _process(_delta: float) -> void:
    global_position = get_global_mouse_position()
```

## Performance Tips

1. **Use sprite sheets** instead of individual files
2. **Disable `process`** when sprite is static
3. **Use Sprite2D** for non-animated graphics
4. **Pool sprites** for frequently spawned objects
5. **Limit region updates** to state changes only

## Scene Structure Examples

### Static Sprite
```
Node2D
└── Sprite2D
    - texture = icon.png
```

### Animated Character
```
CharacterBody2D
└── AnimatedSprite2D
    - sprite_frames = player_anims.tres
    - animation = "idle"
    - autoplay = "idle"
```

### Multi-Sprite Object
```
Node2D (Ship)
├── Sprite2D (Hull)
├── Sprite2D (FlameMain)
├── Sprite2D (FlameLeft)
└── Sprite2D (FlameRight)
```

### State-Based Sprite
```
StaticBody2D (Door)
├── Sprite2D
│   - texture = set via code
└── CollisionShape2D
```
