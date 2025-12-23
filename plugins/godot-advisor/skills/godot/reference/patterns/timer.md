---
topic: timer
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/4.3/classes/class_timer.html
  - https://docs.godotengine.org/en/4.3/classes/class_scenetreetimer.html
  - repos/godot_node_essentials/screens/timer/*
  - repos/godot_node_essentials/common/2d/weapons_2d/*
---

# Timer

Time-based event patterns using Timer nodes and SceneTreeTimer.

## Timer Node Overview

Timer is a countdown timer that emits a `timeout` signal when finished. Use it for cooldowns, delays, repeating events, and time-based game logic.

### Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `wait_time` | float | 1.0 | Time in seconds before timeout. Min ~0.05s for stability |
| `one_shot` | bool | false | If true, timer stops after one timeout. False = auto-restart |
| `autostart` | bool | false | If true, starts automatically when entering scene tree |
| `paused` | bool | false | If true, timer is paused (still running, just frozen) |
| `process_callback` | TimerProcessCallback | TIMER_PROCESS_IDLE | Update in process (1) or physics (0) frames |
| `time_left` | float | (read-only) | Remaining time in seconds (0 if stopped) |
| `ignore_time_scale` | bool | false | If true, ignores Engine.time_scale |

### Key Methods

| Method | Description |
|--------|-------------|
| `start(time_sec: float = -1.0)` | Start or restart timer (optionally override wait_time) |
| `stop()` | Stop the timer |
| `is_stopped() -> bool` | Returns true if timer is not running |

### Signals

| Signal | Description |
|--------|-------------|
| `timeout` | Emitted when timer reaches zero |

## Common Patterns

### One-Shot Timer (Delays)

Use for single delayed actions. Set `one_shot = true` in the editor or code.

```gdscript
class_name DelayedAction
extends Node

@onready var delay_timer: Timer = %DelayTimer

func _ready() -> void:
    delay_timer.wait_time = 2.0
    delay_timer.one_shot = true
    delay_timer.timeout.connect(_on_delay_timeout)
    delay_timer.start()

func _on_delay_timeout() -> void:
    print("Action executed after delay")
```

### Repeating Timer (Cyclic Events)

Use for recurring actions. Leave `one_shot = false` (default).

```gdscript
class_name CyclicCounter
extends Control

var count: int = 0

@onready var timer: Timer = %Timer
@onready var label: Label = %Label

func _ready() -> void:
    timer.wait_time = 1.0
    timer.one_shot = false  # Repeats automatically
    timer.autostart = true  # Starts immediately
    timer.timeout.connect(_on_timer_timeout)
    label.text = str(count)

func _on_timer_timeout() -> void:
    count += 1
    label.text = str(count)
```

### Cooldown Timer

Use for ability cooldowns and rate limiting. Check `is_stopped()` before allowing actions.

```gdscript
class_name AbilityCooldown
extends Node2D

@onready var cooldown_timer: Timer = %CooldownTimer
@onready var player: CharacterBody2D = %Player

func _ready() -> void:
    cooldown_timer.wait_time = 2.0
    cooldown_timer.one_shot = true

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("dash"):
        attempt_dash()

func attempt_dash() -> void:
    # Only dash if cooldown finished
    if not cooldown_timer.is_stopped():
        return

    # Start cooldown
    cooldown_timer.start()

    # Execute ability
    var tween := create_tween()
    tween.tween_property(player, "position", player.position + Vector2.RIGHT * 100, 0.3)
```

### Weapon Fire Rate

Use timers to control weapon firing rates.

```gdscript
class_name RapidFireWeapon
extends Node2D

@onready var fire_timer: Timer = %Timer

func _ready() -> void:
    fire_timer.wait_time = 0.1  # 10 shots per second
    fire_timer.one_shot = true

func _physics_process(_delta: float) -> void:
    if Input.is_action_pressed("shoot") and fire_timer.is_stopped():
        shoot()

func shoot() -> void:
    fire_timer.start()
    # Spawn bullet, play sound, etc.
    var bullet := bullet_scene.instantiate()
    get_parent().add_child(bullet)
    bullet.global_position = global_position
```

### Pausable Timer

Use the `paused` property to pause/resume timers.

```gdscript
class_name PausableTimer
extends Control

var time_counter: int = 0

@onready var timer: Timer = %Timer
@onready var label: Label = %Label

func _ready() -> void:
    timer.wait_time = 0.05
    timer.autostart = true
    timer.timeout.connect(_on_timer_timeout)
    label.text = str(time_counter)

func _on_timer_timeout() -> void:
    time_counter += 1
    label.text = str(time_counter)

func _on_pause_button_toggled(toggled_on: bool) -> void:
    timer.paused = toggled_on
```

## SceneTreeTimer (Await Pattern)

For quick delays without creating Timer nodes, use `get_tree().create_timer()` with `await`.

### Basic Await Delay

```gdscript
class_name AwaitDelay
extends Node

func _ready() -> void:
    await_example()

func await_example() -> void:
    print("Starting...")
    await get_tree().create_timer(2.0).timeout
    print("2 seconds later!")
```

### Sequential Animation with Delays

```gdscript
class_name TrafficLight
extends Control

var light_sequence: Array[String] = ["red", "yellow", "green"]

@onready var animation_player: AnimationPlayer = %AnimationPlayer

func _ready() -> void:
    animate_lights()

func animate_lights() -> void:
    for animation in light_sequence:
        animation_player.play(animation)
        # Random delay between animations
        await get_tree().create_timer(randf_range(1.0, 2.0)).timeout

        # Safety check: ensure still in tree
        if not is_inside_tree():
            return

    # Loop back to start
    animate_lights()
```

### Delayed Cleanup

```gdscript
class_name TimedDestruction
extends Node2D

func _ready() -> void:
    destroy_after_delay()

func destroy_after_delay() -> void:
    await get_tree().create_timer(3.0).timeout
    queue_free()
```

### Combining Timer Node with Await

```gdscript
class_name HybridTimerPattern
extends Node3D

@onready var ledge_timer: Timer = $LedgeTimer

func attempt_ledge_grab() -> void:
    ledge_timer.start()

    # Wait for timer to finish
    await ledge_timer.timeout

    # Execute after timeout
    complete_ledge_grab()

func complete_ledge_grab() -> void:
    print("Ledge grab completed")
```

## Programmatic Timer Creation

Create timers dynamically when needed.

```gdscript
class_name DynamicTimer
extends Node

func create_custom_timer(duration: float, callback: Callable) -> Timer:
    var timer := Timer.new()
    timer.wait_time = duration
    timer.one_shot = true
    timer.timeout.connect(callback)
    add_child(timer)
    timer.start()
    return timer

func _ready() -> void:
    # Create timer that auto-deletes after use
    var temp_timer := create_custom_timer(2.0, _on_temp_timeout)

func _on_temp_timeout() -> void:
    print("Temporary timer finished")
```

## Advanced Patterns

### Timer with Progress Tracking

```gdscript
class_name ProgressTimer
extends Control

@onready var timer: Timer = %Timer
@onready var progress_bar: ProgressBar = %ProgressBar

func _ready() -> void:
    timer.wait_time = 10.0
    timer.one_shot = true
    timer.start()

    progress_bar.max_value = timer.wait_time
    progress_bar.value = 0.0

func _process(_delta: float) -> void:
    if not timer.is_stopped():
        progress_bar.value = timer.wait_time - timer.time_left
```

### Spawn Timer with Randomization

```gdscript
class_name EnemySpawner
extends Node2D

@export var enemy_scene: PackedScene
@export var min_spawn_time: float = 1.0
@export var max_spawn_time: float = 3.0

@onready var spawn_timer: Timer = %Timer

func _ready() -> void:
    spawn_timer.one_shot = true
    spawn_timer.timeout.connect(_on_spawn_timer_timeout)
    start_random_timer()

func _on_spawn_timer_timeout() -> void:
    spawn_enemy()
    start_random_timer()

func spawn_enemy() -> void:
    var enemy := enemy_scene.instantiate()
    add_child(enemy)
    enemy.global_position = global_position

func start_random_timer() -> void:
    spawn_timer.wait_time = randf_range(min_spawn_time, max_spawn_time)
    spawn_timer.start()
```

### Countdown Timer UI

```gdscript
class_name CountdownTimer
extends Control

@export var initial_count: int = 10
var count: int = 0

@onready var label: Label = %Label
@onready var timer: Timer = %Timer

func _ready() -> void:
    count = initial_count
    label.text = str(count)

    timer.wait_time = 1.0
    timer.autostart = true
    timer.timeout.connect(_on_timer_timeout)

func _on_timer_timeout() -> void:
    count -= 1
    count = wrapi(count, 0, initial_count + 1)
    label.text = str(count)

    if count == 0:
        game_over()

func game_over() -> void:
    timer.stop()
    print("Time's up!")
```

### Coyote Time Pattern

Grace period for jumping after leaving platform.

```gdscript
class_name CoyoteJump
extends CharacterBody2D

@onready var coyote_timer: Timer = $CoyoteTimer

func _ready() -> void:
    coyote_timer.wait_time = 0.15
    coyote_timer.one_shot = true

func _physics_process(_delta: float) -> void:
    var was_on_floor := is_on_floor()
    move_and_slide()
    var is_now_on_floor := is_on_floor()

    # Start coyote timer when leaving ground
    if was_on_floor and not is_now_on_floor:
        coyote_timer.start()

    # Can jump if on floor OR coyote time active
    if Input.is_action_just_pressed("jump"):
        if is_on_floor() or not coyote_timer.is_stopped():
            jump()
            coyote_timer.stop()

func jump() -> void:
    velocity.y = -500.0
```

## Best Practices & Pitfalls

### Do

```gdscript
# Use one_shot for delays and cooldowns
cooldown_timer.one_shot = true

# Check is_stopped() for cooldowns
if cooldown_timer.is_stopped():
    execute_ability()

# Use await for quick one-time delays
await get_tree().create_timer(1.0).timeout

# Check is_inside_tree() after await
await get_tree().create_timer(2.0).timeout
if not is_inside_tree():
    return

# Use Timer nodes for repeating events
spawn_timer.autostart = true  # Starts on _ready()

# Store timer references for later control
@onready var cooldown: Timer = %CooldownTimer
```

### Don't

```gdscript
# Don't use very short timers (< 0.05 seconds)
timer.wait_time = 0.01  # Bad - unstable with variable framerate
# Use _process() or _physics_process() instead
# NOTE: Timers process once per frame, affected by framerate

# Don't forget to connect timeout signal
timer.start()  # Bad - no signal connected, timer does nothing

# Don't access tree after await without checking
await get_tree().create_timer(5.0).timeout
label.text = "Done"  # Bad - node might be freed

# Don't create new timers every frame
func _process(_delta: float) -> void:
    var timer := Timer.new()  # Bad - memory leak

# Don't rely on exact timing
timer.wait_time = 1.0
# Timer might finish at 0.98 or 1.02 seconds due to frame timing
# Timers depend on physics_ticks_per_second or framerate

# Don't call stop() expecting timeout signal
timer.stop()
# NOTE: stop() does NOT emit timeout signal
# Use timer.timeout.emit() manually if needed
```

## Performance Considerations

### Timer Node vs SceneTreeTimer

| Use Case | Recommendation | Reason |
|----------|---------------|--------|
| Repeating events | Timer node | Reusable, no allocation per cycle |
| One-time delay | SceneTreeTimer | No node overhead, auto-cleanup |
| Cooldowns | Timer node | Need is_stopped() check |
| Animation sequencing | SceneTreeTimer | Clean await syntax |
| Many simultaneous timers | SceneTreeTimer | Less scene tree overhead |

### Memory Management

```gdscript
# SceneTreeTimer auto-cleans up
await get_tree().create_timer(1.0).timeout  # No cleanup needed

# Programmatic Timer nodes need cleanup
var temp_timer := Timer.new()
add_child(temp_timer)
temp_timer.timeout.connect(func():
    temp_timer.queue_free()  # Clean up after use
)
temp_timer.start()
```

### Frame Rate Independence

```gdscript
# Timers are frame-rate independent
timer.wait_time = 2.0  # Always 2 seconds, regardless of FPS

# For very precise timing < 0.05 seconds, use delta instead
var time_accumulator: float = 0.0

func _process(delta: float) -> void:
    time_accumulator += delta
    if time_accumulator >= 0.01:
        time_accumulator = 0.0
        precise_action()
```

## Timer States

```gdscript
# Timer is stopped (default state)
timer.is_stopped()  # true

# Start timer
timer.start()
timer.is_stopped()  # false

# Check remaining time
print(timer.time_left)  # Time until timeout

# Pause timer
timer.paused = true
timer.is_stopped()  # false (still running, just paused)

# Stop timer
timer.stop()
timer.is_stopped()  # true
```

## Common Use Cases

| Use Case | Pattern | Configuration |
|----------|---------|---------------|
| Ability cooldown | One-shot timer | `one_shot = true`, check `is_stopped()` |
| Enemy spawning | Repeating timer | `one_shot = false`, randomize `wait_time` |
| UI countdown | Repeating timer | `autostart = true`, update label on timeout |
| Delayed action | SceneTreeTimer | `await get_tree().create_timer().timeout` |
| Fire rate limiting | One-shot timer | Start on shoot, check `is_stopped()` before next shot |
| Grace period (coyote time) | One-shot timer | Start on leave platform, stop on jump |
| Animation sequencing | SceneTreeTimer | `await` in loop with delays |
| Temporary invincibility | One-shot timer | Start on hit, check `is_stopped()` before damage |
| Combo window | One-shot timer | Start on first hit, check `is_stopped()` for combo |
| Timed destruction | SceneTreeTimer | `await` then `queue_free()` |

## Related Patterns

- [Signals](signals.md) - Timers use timeout signal for event notification
- [Autoloads](autoloads.md) - Global timers for game-wide cooldowns
- [Input](input.md) - Combining input with cooldown timers
- [Health System](health-system.md) - Invincibility timers after damage

## See Also

- Official Timer documentation: https://docs.godotengine.org/en/4.3/classes/class_timer.html
- Official SceneTreeTimer documentation: https://docs.godotengine.org/en/4.3/classes/class_scenetreetimer.html
