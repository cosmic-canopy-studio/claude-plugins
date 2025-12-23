---
topic: animation-player
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/stable/classes/class_animationplayer.html
  - repos/godot_node_essentials/screens/animation_player/
  - https://forum.godotengine.org/t/blend-time-in-animationplayer/8235
---

# AnimationPlayer

AnimationPlayer is the primary node for playing back animations. It manages animation libraries, controls playback, queues animations, and handles blending between transitions.

## Basic Playback

### Playing an Animation

```gdscript
@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
    animation_player.play("idle")
```

### Play with Parameters

```gdscript
# Play with custom blend time (0.5 seconds)
animation_player.play("run", -1, 1.0, false)

# Play at 2x speed
animation_player.play("attack", -1, 2.0)

# Play backwards
animation_player.play("fade_out", -1, -1.0, true)
# Or use convenience method:
animation_player.play_backwards("fade_out")
```

**Method signature:** `play(name: String = "", custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false)`

- **name**: Animation to play (empty resumes current)
- **custom_blend**: Blend time in seconds (-1 uses default)
- **custom_speed**: Playback speed multiplier (negative = reverse)
- **from_end**: Start from end if true (useful for reverse playback)

## Stopping Animations

```gdscript
# Stop and keep at current position
animation_player.stop()

# Stop and reset to beginning
animation_player.stop(true)

# Check if playing
if animation_player.is_playing():
    animation_player.stop()
```

## Queuing Animations {#queue}

Queue animations to play sequentially:

```gdscript
# Example: Gun reload sequence
func shoot() -> void:
    if animation_player.is_playing():
        return

    animation_player.queue("fire")
    if _current_ammo < 1:
        animation_player.queue("reload")
    animation_player.queue("pump")
```

### Queue with Await

```gdscript
# Play multiple animations in sequence
func death_sequence() -> void:
    animation_player.play("fade_out")
    await animation_player.animation_finished

    # Reset after fade completes
    player.global_position = spawn_point
    animation_player.play("fade_in")
```

### Pickup Respawn Pattern

```gdscript
# Example: Health pickup with respawn delay
func _on_body_entered(body: Node2D) -> void:
    if not body.is_in_group("player"):
        return

    animation_player.stop()
    animation_player.queue("collected")
    animation_player.queue("delay")      # Invisible pause
    animation_player.queue("respawn")
```

## Animation Signals {#signals}

### animation_finished

Emitted when an animation completes (not emitted for looping animations):

```gdscript
func _ready() -> void:
    animation_player.animation_finished.connect(_on_animation_finished)

func _on_animation_finished(anim_name: String) -> void:
    match anim_name:
        "attack":
            return_to_idle()
        "die":
            queue_free()
        "spawn":
            enable_input()
```

### Using Await

```gdscript
func fade_transition() -> void:
    animation_player.play("fade_out")
    await animation_player.animation_finished

    # Change scene
    get_tree().change_scene_to_file("res://levels/next_level.tscn")
```

### animation_started

```gdscript
animation_player.animation_started.connect(_on_animation_started)

func _on_animation_started(anim_name: String) -> void:
    if anim_name == "attack":
        hitbox.monitoring = true
```

### animation_changed

Emitted when the playing animation changes (not emitted by `play()` calls):

```gdscript
animation_player.animation_changed.connect(_on_animation_changed)

func _on_animation_changed(old_name: String, new_name: String) -> void:
    print("Switched from %s to %s" % [old_name, new_name])
```

## Playback Control

### Speed Control

```gdscript
# Set speed via property (affects all animations)
animation_player.speed_scale = 2.0  # 2x speed

# Or per-animation via play()
animation_player.play("run", -1, 1.5)  # 1.5x speed
```

**Scene property:** Set `speed_scale` in the Inspector for permanent speed changes.

### Seeking

Jump to specific time in animation:

```gdscript
# Seek to 2 seconds into animation
animation_player.seek(2.0)

# Seek and update immediately
animation_player.seek(0.0, true)  # Reset to start

# Random start time (for particle sync)
animation_player.play("idle")
animation_player.seek(randf_range(0.0, 2.0))
```

### Assigned Animation

Track the current/last played animation:

```gdscript
# Check current animation
if animation_player.assigned_animation == "turn_off":
    animation_player.play("turn_on")
else:
    animation_player.play("turn_off")

# Check before interrupting
if animation_player.assigned_animation == "push":
    return  # Don't interrupt
```

## Blend Times {#blend}

Smooth transitions between animations:

### Default Blend Time

Set in Inspector or code:

```gdscript
# Set default blend for all transitions
animation_player.playback_default_blend_time = 0.2
```

### Custom Blend Times

Set blend time between specific animations:

```gdscript
func _ready() -> void:
    # 0.3 second blend from "idle" to "run"
    animation_player.set_blend_time("idle", "run", 0.3)

    # 0.5 second blend from "run" to "jump"
    animation_player.set_blend_time("run", "jump", 0.5)

    # Instant transition from "jump" to "fall"
    animation_player.set_blend_time("jump", "fall", 0.0)

# Get blend time
var blend: float = animation_player.get_blend_time("idle", "run")
```

### Per-Play Blend

Override blend for a single play call:

```gdscript
# Blend over 0.5 seconds to "attack"
animation_player.play("attack", 0.5)
```

## Common Patterns

### State-Based Animation

```gdscript
extends CharacterBody2D

@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        if velocity.y < 0:
            animation_player.play("jump")
        else:
            animation_player.play("fall")
    elif velocity.x != 0:
        animation_player.play("run")
    else:
        animation_player.play("idle")

    move_and_slide()
```

### Damage/Death Sequence

```gdscript
func take_damage(amount: int) -> void:
    health -= amount

    if health <= 0:
        die()
    else:
        flash_damage()

func flash_damage() -> void:
    animation_player.play("hurt")

func die() -> void:
    set_physics_process(false)
    animation_player.play("die")
    await animation_player.animation_finished
    queue_free()
```

### Highlight Effect

```gdscript
func highlight() -> void:
    if animation_player != null:
        animation_player.play("highlight")
        animation_player.seek(0.0, true)  # Reset to start
```

### Animation-Triggered Actions

Connect button presses to animations with bound parameters:

```gdscript
func _ready() -> void:
    # Each button plays its corresponding attack animation
    for button: Button in attack_buttons:
        var attack_name: String = button.name.to_lower()
        button.pressed.connect(animation_player.play.bind(attack_name))
```

### Visibility-Based Playback

```gdscript
func _ready() -> void:
    var notifier: VisibleOnScreenNotifier2D = $VisibleOnScreenNotifier2D
    notifier.screen_entered.connect(animation_player.play.bind("show"))
    notifier.screen_exited.connect(animation_player.play.bind("hide"))
```

### Randomized Speed

```gdscript
func _ready() -> void:
    # Randomize speed for variation
    animation_player.speed_scale = randf_range(0.5, 1.5)
```

## Animation Callbacks

Use animation tracks to call methods at specific times:

### Call Method Track

In the Animation editor:
1. Add a "Call Method Track"
2. Target the node with the method
3. Insert keyframes where method should be called
4. Select method and parameters

**Example uses:**
- Play sound effects mid-animation
- Spawn particles on hit frame
- Enable/disable collision shapes
- Emit signals at specific moments

```gdscript
# Methods called from animation tracks
func play_footstep_sound() -> void:
    audio_player.play()

func spawn_explosion() -> void:
    var explosion := explosion_scene.instantiate()
    get_parent().add_child(explosion)
    explosion.global_position = global_position

func enable_hitbox() -> void:
    hitbox.monitoring = true
```

## Best Practices

### Check Before Playing

```gdscript
# Prevent interrupting critical animations
func attack() -> void:
    if animation_player.is_playing():
        return  # Already animating

    animation_player.play("attack")
```

### Pause with Physics

```gdscript
# Disable input during cutscene
func play_cutscene() -> void:
    player.set_physics_process(false)
    animation_player.play("cutscene")
    await animation_player.animation_finished
    player.set_physics_process(true)
```

### Reset After Stop

```gdscript
# Stop and reset to avoid mid-animation states
func reset_animation() -> void:
    animation_player.stop()
    animation_player.seek(0, true)
```

### Cleanup Connections

When connecting to autoloads or long-lived nodes:

```gdscript
var _callback: Callable

func _ready() -> void:
    _callback = _on_animation_finished
    animation_player.animation_finished.connect(_callback)

func _exit_tree() -> void:
    if animation_player.animation_finished.is_connected(_callback):
        animation_player.animation_finished.disconnect(_callback)
```

## Common Pitfalls

### Resuming vs. Restarting

```gdscript
# Calling play() with same animation RESUMES if paused
animation_player.play("idle")  # Starts from beginning
animation_player.pause()
animation_player.play("idle")  # Resumes from paused position

# Force restart
animation_player.stop()
animation_player.play("idle")  # Starts from beginning
```

### Queue Only Works Sequential

```gdscript
# WRONG: Queuing without initial play
animation_player.queue("attack")  # Won't play!

# CORRECT: Start with play(), then queue
animation_player.play("attack")
animation_player.queue("return_to_idle")
```

### Looping Blocks Queue

```gdscript
# Looping animations never emit animation_finished
# Queued animations won't play after looping animations
animation_player.play("idle_loop")  # Loops forever
animation_player.queue("attack")    # Never plays!
```

### Update Timing

```gdscript
# Animation updates next frame, not immediately
animation_player.play("spawn")
print(sprite.modulate)  # Still old value!

# Force immediate update
animation_player.play("spawn")
animation_player.advance(0)  # Update now
print(sprite.modulate)  # New value
```

## Performance Tips

- **Use AnimationTree** for complex state machines (blending, transitions)
- **Batch animations** in same AnimationLibrary for faster loading
- **Avoid seeking every frame** - expensive operation
- **Disable autoplay** for animations controlled by code
- **Use call method tracks** instead of polling in `_process()`

## Related Topics

- [AnimationTree](animation-tree.md) - Advanced state machines and blending
- [State Machines](state-machines.md) - Controlling animations via states
- [Tweens](tween.md) - Code-driven procedural animations
- [Signals](../patterns/signals.md) - Using animation signals effectively

## See Also

- **Official Docs:** [AnimationPlayer Class Reference](https://docs.godotengine.org/en/stable/classes/class_animationplayer.html)
- **Tutorial:** 2D sprite animation with AnimationPlayer
- **Tutorial:** Using call method tracks for complex sequences
