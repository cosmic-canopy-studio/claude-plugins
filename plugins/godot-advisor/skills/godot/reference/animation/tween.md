---
topic: tween
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/stable/classes/class_tween.html
  - godot-tween
---

# Tweening

Tween patterns for smooth animations and transitions. Tweens interpolate properties over time using Tweeners for lightweight, code-driven animations.

## Core Concepts

**Tween Lifecycle**: Tweens are created via `create_tween()` or `get_tree().create_tween()` and start automatically on the next process/physics frame. They are NOT reusable - create a new Tween for each animation sequence.

**Tweeners**: Building blocks of Tweens - PropertyTweener, IntervalTweener, CallbackTweener, MethodTweener. Chained together to form animation sequences.

**Fire-and-Forget**: Tweens don't require manual memory management. They auto-cleanup when finished unless bound to a freed node.

**IMPORTANT**: Never create Tweens with `Tween.new()` - they won't work. Always use `create_tween()` or `get_tree().create_tween()`.

## Basic Tween

```gdscript
func animate_position() -> void:
    var tween := create_tween()
    tween.tween_property(self, "position", Vector2(500, 300), 1.0)
```

## Property Tweening

```gdscript
# Move
tween.tween_property(node, "position", target_pos, duration)

# Rotate
tween.tween_property(node, "rotation", PI, duration)

# Scale
tween.tween_property(node, "scale", Vector2(2, 2), duration)

# Modulate (color/alpha)
tween.tween_property(sprite, "modulate", Color.RED, duration)

# Custom property
tween.tween_property(self, "health", 0, duration)
```

## Fade Effects {#fade}

### Fade In

```gdscript
func fade_in(duration: float = 0.5) -> void:
    modulate.a = 0.0
    var tween := create_tween()
    tween.tween_property(self, "modulate:a", 1.0, duration)
```

### Fade Out and Remove

```gdscript
func fade_out_and_remove(duration: float = 0.5) -> void:
    var tween := create_tween()
    tween.tween_property(self, "modulate:a", 0.0, duration)
    tween.tween_callback(queue_free)
```

## Slide Animation {#slide}

```gdscript
func slide_in_from_left(duration: float = 0.3) -> void:
    var target_x := position.x
    position.x = -size.x  # Start off-screen

    var tween := create_tween()
    tween.tween_property(self, "position:x", target_x, duration)
    tween.set_ease(Tween.EASE_OUT)
    tween.set_trans(Tween.TRANS_BACK)

func slide_out_to_right(duration: float = 0.3) -> void:
    var tween := create_tween()
    tween.tween_property(self, "position:x", get_viewport_rect().size.x, duration)
    tween.set_ease(Tween.EASE_IN)
```

## Easing Types

```gdscript
var tween := create_tween()
tween.set_ease(Tween.EASE_OUT)  # Start fast, end slow
tween.set_trans(Tween.TRANS_BOUNCE)  # Bounce effect
```

### Common Combinations

| Effect | Ease | Trans |
|--------|------|-------|
| Smooth deceleration | EASE_OUT | TRANS_QUAD |
| Bouncy | EASE_OUT | TRANS_BOUNCE |
| Elastic | EASE_OUT | TRANS_ELASTIC |
| Overshoot | EASE_OUT | TRANS_BACK |
| Snappy | EASE_OUT | TRANS_EXPO |
| Linear | (default) | TRANS_LINEAR |

## Chaining Tweens

Sequential animations:

```gdscript
func complex_animation() -> void:
    var tween := create_tween()

    # First: move right
    tween.tween_property(self, "position:x", 500, 0.5)

    # Then: scale up
    tween.tween_property(self, "scale", Vector2(2, 2), 0.3)

    # Then: fade out
    tween.tween_property(self, "modulate:a", 0.0, 0.2)

    # Finally: cleanup
    tween.tween_callback(queue_free)
```

## Parallel Tweens

Simultaneous animations:

```gdscript
func parallel_animation() -> void:
    var tween := create_tween()
    tween.set_parallel(true)  # All tweens run together

    tween.tween_property(self, "position", target_pos, 0.5)
    tween.tween_property(self, "rotation", PI, 0.5)
    tween.tween_property(self, "scale", Vector2(0.5, 0.5), 0.5)
```

### Mixed Sequential and Parallel

```gdscript
func mixed_animation() -> void:
    var tween := create_tween()

    # First group (parallel)
    tween.set_parallel(true)
    tween.tween_property(self, "position:x", 500, 0.5)
    tween.tween_property(self, "position:y", 300, 0.5)

    # Switch to sequential
    tween.set_parallel(false)
    tween.tween_property(self, "scale", Vector2(2, 2), 0.3)
```

## Callbacks

```gdscript
func with_callbacks() -> void:
    var tween := create_tween()

    tween.tween_callback(func(): print("Starting"))
    tween.tween_property(self, "position", target, 1.0)
    tween.tween_callback(func(): print("Finished"))
    tween.tween_callback(queue_free)
```

## Delays

```gdscript
func with_delay() -> void:
    var tween := create_tween()

    tween.tween_interval(0.5)  # Wait 0.5 seconds
    tween.tween_property(self, "position", target, 1.0)
```

## Looping

```gdscript
func looping_animation() -> void:
    var tween := create_tween()
    tween.set_loops()  # Infinite loops
    # Or: tween.set_loops(3) for 3 loops

    tween.tween_property(self, "scale", Vector2(1.2, 1.2), 0.5)
    tween.tween_property(self, "scale", Vector2.ONE, 0.5)
```

### Ping-Pong (Yoyo)

```gdscript
func ping_pong() -> void:
    var tween := create_tween()
    tween.set_loops()

    tween.tween_property(self, "position:y", position.y - 20, 0.5)
    tween.tween_property(self, "position:y", position.y, 0.5)
```

## Awaiting Tweens

```gdscript
func animated_sequence() -> void:
    var tween := create_tween()
    tween.tween_property(self, "position", target, 1.0)
    await tween.finished
    print("Animation complete!")
```

## Killing Tweens

```gdscript
var _current_tween: Tween

func start_animation() -> void:
    # Kill any existing tween to prevent conflicts
    if _current_tween and _current_tween.is_valid():
        _current_tween.kill()

    _current_tween = create_tween()
    _current_tween.tween_property(self, "position", target, 1.0)

# IMPORTANT: Only one tween per property at a time
# Multiple tweens on same property = last one wins
```

## Tween Control Methods

```gdscript
var tween := create_tween()
tween.tween_property(sprite, "position", target, 1.0)

# Pause/Resume
tween.pause()  # Pause animation
tween.play()   # Resume from paused position

# Stop and reset
tween.stop()  # Resets to initial state, keeps Tweeners

# Query state
if tween.is_running():
    print("Tween active")

if tween.is_valid():
    print("Tween exists in SceneTree")

# Check progress
var time_elapsed: float = tween.get_total_elapsed_time()
var loops_left: int = tween.get_loops_left()  # -1 = infinite
```

## Binding and Lifecycle

```gdscript
# Bind to node (auto-kill when node freed)
var tween := create_tween().bind_node(self)
# Or use Node.create_tween() which auto-binds
var tween2 := self.create_tween()

# Unbindable tween (continues even if creator freed)
var global_tween := get_tree().create_tween()

# WARNING: Unbound paused Tweens exist indefinitely
# Retrieve lost tweens:
var all_tweens: Array[Tween] = get_tree().get_processed_tweens()
```

## Common Patterns

### Damage Flash

```gdscript
func flash_damage() -> void:
    var tween := create_tween()
    tween.tween_property(sprite, "modulate", Color.RED, 0.05)
    tween.tween_property(sprite, "modulate", Color.WHITE, 0.1)
```

### Pop In

```gdscript
func pop_in() -> void:
    scale = Vector2.ZERO
    var tween := create_tween()
    tween.set_ease(Tween.EASE_OUT)
    tween.set_trans(Tween.TRANS_BACK)
    tween.tween_property(self, "scale", Vector2.ONE, 0.3)
```

### Shake

```gdscript
func shake(intensity: float = 10.0, duration: float = 0.2) -> void:
    var original_pos := position
    var tween := create_tween()

    for i in 5:
        var offset := Vector2(randf_range(-1, 1), randf_range(-1, 1)) * intensity
        tween.tween_property(self, "position", original_pos + offset, duration / 10.0)

    tween.tween_property(self, "position", original_pos, duration / 10.0)
```

### Smooth Value Change

```gdscript
var _displayed_score: float = 0.0

func update_score(new_score: int) -> void:
    var tween := create_tween()
    tween.tween_property(self, "_displayed_score", float(new_score), 0.5)
    tween.tween_callback(_update_label)

func _update_label() -> void:
    label.text = str(int(_displayed_score))

func _process(_delta: float) -> void:
    label.text = str(int(_displayed_score))  # For continuous updates
```

## Best Practices & Pitfalls

### Do

```gdscript
# Always create new Tweens (not reusable)
func animate() -> void:
    var tween := create_tween()
    tween.tween_property(self, "scale", Vector2(2, 2), 0.5)

# Kill previous Tween before creating new one on same property
if _tween and _tween.is_valid():
    _tween.kill()
_tween = create_tween()

# Use method chaining for cleaner code
var tween := create_tween().set_trans(Tween.TRANS_SINE).set_ease(Tween.EASE_OUT)
tween.tween_property(self, "position", target, 1.0)

# Bind Tweens to nodes for automatic cleanup
var tween := create_tween().bind_node(self)

# Use EASE_IN_OUT as default when unsure
tween.set_ease(Tween.EASE_IN_OUT)
```

### Don't

```gdscript
# Don't create with Tween.new() - won't work!
var tween := Tween.new()  # INVALID - never do this

# Don't reuse Tweens
_tween.stop()
_tween.tween_property(...)  # Bad - undefined behavior

# Don't create 0-duration infinite loops
var tween := create_tween().set_loops()
tween.tween_callback(shoot)  # Bad - will freeze game
# Must have duration/delay in loops

# Don't forget to check is_valid() before killing
_tween.kill()  # Bad - might crash if tween finished
if _tween and _tween.is_valid():
    _tween.kill()  # Good

# Don't animate same property with multiple Tweens
var tween1 := create_tween()
tween1.tween_property(sprite, "position:x", 100, 1.0)
var tween2 := create_tween()
tween2.tween_property(sprite, "position:x", 200, 1.0)  # Overrides tween1
```

## Timing and Processing

```gdscript
# Tween processing modes
var tween := create_tween()
tween.set_process_mode(Tween.TWEEN_PROCESS_PHYSICS)  # Update in _physics_process
# Or: TWEEN_PROCESS_IDLE (default, updates in _process)

# Pause behavior
tween.set_pause_mode(Tween.TWEEN_PAUSE_STOP)  # Pauses with SceneTree
# Or: TWEEN_PAUSE_PROCESS (ignores tree pausing)
# Or: TWEEN_PAUSE_BOUND (uses bound node's process_mode)

# Ignore time scale
tween.set_ignore_time_scale(true)  # Unaffected by Engine.time_scale

# Speed control
tween.set_speed_scale(2.0)  # 2x speed

# Custom stepping (for manual control)
tween.pause()
func _process(delta: float) -> void:
    tween.custom_step(delta)
```

## Advanced: Static Interpolation

Use `Tween.interpolate_value()` for manual interpolation without creating Tween instances:

```gdscript
# Manual lerp with easing
var start_pos := Vector2.ZERO
var end_pos := Vector2(100, 100)
var elapsed_time: float = 0.0
var duration: float = 1.0

func _process(delta: float) -> void:
    elapsed_time += delta
    var current_pos: Variant = Tween.interpolate_value(
        start_pos,              # initial_value
        end_pos - start_pos,    # delta_value (end - start)
        elapsed_time,           # elapsed_time
        duration,               # duration
        Tween.TRANS_SINE,       # transition type
        Tween.EASE_IN_OUT       # ease type
    )
    sprite.position = current_pos
```
