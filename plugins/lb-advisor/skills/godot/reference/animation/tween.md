---
topic: tween
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-tween
---

# Tweening

Tween patterns for smooth animations and transitions.

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
    # Kill any existing tween
    if _current_tween:
        _current_tween.kill()

    _current_tween = create_tween()
    _current_tween.tween_property(self, "position", target, 1.0)
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
