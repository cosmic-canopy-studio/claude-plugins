---
class: AnimatedSprite2D
category: nodes/2d/rendering
complexity: beginner
tags: [2d, sprite, animation, rendering]
---

# AnimatedSprite2D

**Inherits:** Node2D < CanvasItem < Node < Object

Sprite node that contains multiple textures as frames to play for animation.

## Description

AnimatedSprite2D is similar to the Sprite2D node, except it carries multiple textures as animation frames. Animations are created using a SpriteFrames resource, which allows you to import image files (or a folder containing said files) to provide the animation frames for the sprite.

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `animation` | `StringName` | `&"default"` | The current animation from the sprite_frames resource |
| `autoplay` | `String` | `""` | The key of the animation to play when the scene loads |
| `centered` | `bool` | `true` | If `true`, texture will be centered |
| `flip_h` | `bool` | `false` | If `true`, texture is flipped horizontally |
| `flip_v` | `bool` | `false` | If `true`, texture is flipped vertically |
| `frame` | `int` | `0` | The displayed animation frame's index |
| `frame_progress` | `float` | `0.0` | The progress value between 0.0 and 1.0 until the current frame transitions to the next |
| `offset` | `Vector2` | `Vector2(0, 0)` | The texture's drawing offset |
| `speed_scale` | `float` | `1.0` | The speed scaling ratio (1.0 = normal speed, 0.5 = half speed, 2.0 = double speed) |
| `sprite_frames` | `SpriteFrames` | | The SpriteFrames resource containing the animation(s) |

## Methods

| Return | Method |
|--------|--------|
| `float` | `get_playing_speed()` |
| `bool` | `is_playing()` |
| `void` | `pause()` |
| `void` | `play(name: StringName = &"", custom_speed: float = 1.0, from_end: bool = false)` |
| `void` | `play_backwards(name: StringName = &"")` |
| `void` | `set_frame_and_progress(frame: int, progress: float)` |
| `void` | `stop()` |

## Signals

- **animation_changed()**: Emitted when animation changes
- **animation_finished()**: Emitted when the animation reaches the end (not emitted for looping animations)
- **animation_looped()**: Emitted when the animation loops
- **frame_changed()**: Emitted when frame changes
- **sprite_frames_changed()**: Emitted when sprite_frames changes

## Quick Examples

### Basic animation playback

```gdscript
@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D

func _ready() -> void:
    animated_sprite.play("walk")
```

### Control animation from code

```gdscript
@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D

func _ready() -> void:
    animated_sprite.animation_finished.connect(_on_animation_finished)

func start_attack() -> void:
    animated_sprite.play("attack")

func _on_animation_finished() -> void:
    animated_sprite.play("idle")
```

### Autoplay on scene load

```gdscript
# Set in editor or code
@onready var animated_sprite: AnimatedSprite2D = $AnimatedSprite2D

func _ready() -> void:
    animated_sprite.autoplay = "idle"
```

## Common Patterns

### State-based animation

```gdscript
enum State { IDLE, WALK, RUN, JUMP }
var current_state: State = State.IDLE

func update_animation() -> void:
    match current_state:
        State.IDLE:
            $AnimatedSprite2D.play("idle")
        State.WALK:
            $AnimatedSprite2D.play("walk")
        State.RUN:
            $AnimatedSprite2D.play("run")
        State.JUMP:
            $AnimatedSprite2D.play("jump")
```

### Speed control

```gdscript
func slow_motion() -> void:
    $AnimatedSprite2D.speed_scale = 0.5

func fast_forward() -> void:
    $AnimatedSprite2D.speed_scale = 2.0

func pause_animation() -> void:
    $AnimatedSprite2D.pause()

func resume_animation() -> void:
    $AnimatedSprite2D.play()  # Resumes from current frame
```

### Change animation while preserving frame

```gdscript
func change_animation_smoothly(new_animation: String) -> void:
    var sprite: AnimatedSprite2D = $AnimatedSprite2D
    var current_frame: int = sprite.frame
    var current_progress: float = sprite.frame_progress
    sprite.play(new_animation)
    sprite.set_frame_and_progress(current_frame, current_progress)
```

## Best Practices

- Use `animation_finished` signal for chaining animations or triggering events
- Set `autoplay` for idle/default animations
- Use `speed_scale` for slow-motion or fast-forward effects
- Pause with `pause()` to resume later; use `stop()` to reset to frame 0
- For pixel art, set `centered` to `false` to avoid deformation
- Negative `speed_scale` plays animation in reverse

## See Also

- [Sprite2D](sprite2d.md) - For static sprites
- [AnimationPlayer](../../core/animationplayer.md) - For complex multi-property animations
