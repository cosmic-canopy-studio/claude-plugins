---
topic: progress-bars
version: 2025.12.21
godot_version: "4.3"
sources:
  - "Official: Godot Engine ProgressBar Documentation - https://docs.godotengine.org/en/stable/classes/class_progressbar.html"
  - "Official: Godot Engine TextureProgressBar Documentation - https://docs.godotengine.org/en/stable/classes/class_textureprogressbar.html"
  - "Official: Godot Engine Range Class Documentation - https://docs.godotengine.org/en/stable/classes/class_range.html"
  - "Examples: godot_node_essentials/screens/progress_bar/"
  - "Examples: godot_node_essentials/screens/sub_viewport/health_bar_3d/"
  - "Community: KidsCanCode - 3D Unit Healthbars - https://kidscancode.org/godot_recipes/4.x/3d/healthbars/"
  - "Community: GameDev Academy - ProgressBar Complete Guide - https://gamedevacademy.org/progressbar-in-godot-complete-guide/"
status: complete
---

# Progress Bars & Health Bars

Progress bars for health, loading, resource meters, and cooldowns.

## ProgressBar (Basic) {#progressbar}

Simple bar using theme styling:

```gdscript
extends ProgressBar

func _ready() -> void:
    min_value = 0
    max_value = 100
    value = 100
    show_percentage = false

func set_health(current: int, maximum: int) -> void:
    max_value = maximum
    value = current
```

### ProgressBar Properties

| Property | Type | Description |
|----------|------|-------------|
| `min_value` | `float` | Minimum value (default: 0) |
| `max_value` | `float` | Maximum value (default: 100) |
| `value` | `float` | Current value between min and max |
| `show_percentage` | `bool` | Display percentage text |
| `fill_mode` | `int` | Fill direction (0=left-to-right, 1=right-to-left, 2=top-to-bottom, 3=bottom-to-top) |

### Animated Value Change

```gdscript
func set_health_smooth(new_value: float, duration: float = 0.3) -> void:
    var tween := create_tween()
    tween.set_trans(Tween.TRANS_CUBIC)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(self, "value", new_value, duration)
```

### Normalized Range (0.0 to 1.0)

```gdscript
func _ready() -> void:
    min_value = 0.0
    max_value = 1.0
    value = 1.0

func set_as_ratio(ratio: float) -> void:
    value = clampf(ratio, 0.0, 1.0)
```

### Level Progress Tracking

```gdscript
extends Node2D

@export var level_start: Marker2D
@export var level_end: Marker2D

@onready var _player: CharacterBody2D = %Player
@onready var _progress_bar: ProgressBar = %ProgressBar

func _process(_delta: float) -> void:
    # Calculate player progress from start to end
    var ratio := inverse_lerp(
        level_start.position.x,
        level_end.position.x,
        _player.position.x
    )
    _progress_bar.set_as_ratio(ratio)
```

## TextureProgressBar {#texture-progress-bar}

Custom textures for stylized bars:

```gdscript
extends TextureProgressBar

func _ready() -> void:
    # Assign textures
    texture_under = preload("res://ui/bar_background.png")
    texture_progress = preload("res://ui/bar_fill.png")
    texture_over = preload("res://ui/bar_border.png")

    min_value = 0
    max_value = 100
    value = 100
```

### Fill Modes

```gdscript
# Horizontal (left to right)
fill_mode = TextureProgressBar.FILL_LEFT_TO_RIGHT

# Horizontal (right to left)
fill_mode = TextureProgressBar.FILL_RIGHT_TO_LEFT

# Vertical (top to bottom)
fill_mode = TextureProgressBar.FILL_TOP_TO_BOTTOM

# Vertical (bottom to top)
fill_mode = TextureProgressBar.FILL_BOTTOM_TO_TOP

# Radial (clockwise)
fill_mode = TextureProgressBar.FILL_CLOCKWISE

# Radial (counter-clockwise)
fill_mode = TextureProgressBar.FILL_COUNTER_CLOCKWISE
```

### Radial Progress (Circular Fill)

```gdscript
func _ready() -> void:
    fill_mode = TextureProgressBar.FILL_CLOCKWISE
    radial_initial_angle = 0.0  # Start at top (12 o'clock)
    radial_fill_degrees = 360.0  # Full circle

    texture_progress = preload("res://ui/circle_fill.png")
```

### TextureProgressBar Properties

| Property | Type | Description |
|----------|------|-------------|
| `texture_under` | `Texture2D` | Background texture (empty bar) |
| `texture_progress` | `Texture2D` | Fill texture (changes with value) |
| `texture_over` | `Texture2D` | Foreground overlay (border, frame) |
| `fill_mode` | `int` | Direction of fill (see Fill Modes above) |
| `nine_patch_stretch` | `bool` | Use 9-slice scaling for textures |
| `tint_under` | `Color` | Modulate color for background |
| `tint_progress` | `Color` | Modulate color for fill |
| `tint_over` | `Color` | Modulate color for overlay |
| `radial_initial_angle` | `float` | Starting angle for radial fill (degrees) |
| `radial_fill_degrees` | `float` | How many degrees to fill (0-360) |

## Health Bar Patterns {#health-bar}

### Basic Health Bar

```gdscript
extends TextureProgressBar

const MAX_HEALTH := 100

@export var color_health_low := Color(0.69, 0.19, 0.36)  # Red
@export var color_health_high := Color(0.56, 0.87, 0.36)  # Green

var health: int = MAX_HEALTH:
    set(new_health):
        health = clampi(new_health, 0, MAX_HEALTH)
        _update_bar()

func _ready() -> void:
    max_value = MAX_HEALTH
    _update_bar()

func _update_bar() -> void:
    value = float(health)
    var ratio := float(health) / MAX_HEALTH
    tint_progress = color_health_low.lerp(color_health_high, ratio)
```

### Animated Health Bar with Color Transition

```gdscript
extends TextureProgressBar

const MAX_HEALTH := 100

@export var color_health_low := Color(0.69, 0.19, 0.36)
@export var color_health_high := Color(0.56, 0.87, 0.36)

@export_range(0, 100) var health: int = 50:
    set(new_health):
        if not is_inside_tree():
            await ready

        var previous_health := health
        health = clampi(new_health, 0, MAX_HEALTH)

        # Animate value change with color transition
        var tween := create_tween()
        tween.tween_method(
            _update_health_bar,
            float(previous_health),
            float(health),
            0.33
        )

func _update_health_bar(health_value: float) -> void:
    value = health_value
    var ratio := health_value / MAX_HEALTH
    tint_progress = color_health_low.lerp(color_health_high, ratio)
```

### Damage and Healing

```gdscript
extends CharacterBody2D

@onready var _health_bar: ProgressBar = %HealthBar

func take_damage(amount: int) -> void:
    var tween := create_tween()
    tween.set_trans(Tween.TRANS_CUBIC)
    tween.set_ease(Tween.EASE_IN_OUT)
    tween.tween_property(
        _health_bar,
        "value",
        _health_bar.value - amount,
        0.5
    )
    await tween.finished

    if _health_bar.value == 0:
        _die()

func heal(amount: int) -> void:
    # Don't overheal
    if _health_bar.value == _health_bar.max_value:
        return

    var tween := create_tween()
    tween.set_trans(Tween.TRANS_CUBIC)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(
        _health_bar,
        "value",
        _health_bar.value + amount,
        0.5
    )

func _die() -> void:
    queue_free()
```

### Dynamic Max Health

```gdscript
extends CharacterBody2D

const MAX_HEALTH: float = 300.0

@onready var _health_bar: ProgressBar = %HealthBar

func increase_max_health(amount: int) -> void:
    # Prevent exceeding absolute maximum
    if _health_bar.max_value >= MAX_HEALTH:
        return

    var tween := create_tween()
    tween.set_trans(Tween.TRANS_CUBIC)
    tween.set_ease(Tween.EASE_OUT)
    tween.set_parallel(true)

    # Increase max value and visual width
    tween.tween_property(
        _health_bar,
        "max_value",
        _health_bar.max_value + amount,
        0.5
    )
    tween.tween_property(
        _health_bar,
        "custom_minimum_size:x",
        (_health_bar.max_value + amount) * 5,
        0.5
    )
```

## Ability Cooldown Bar {#cooldown}

```gdscript
extends TextureProgressBar

@export var time_to_recharge: float = 3.0
@export var action_to_activate: Shortcut

@onready var _animation_player: AnimationPlayer = %AnimationPlayer

func _ready() -> void:
    value = max_value
    if _animation_player:
        _animation_player.play("ready")

func _unhandled_input(event: InputEvent) -> void:
    if action_to_activate.matches_event(event):
        if value == max_value:
            _use_ability()

func _use_ability() -> void:
    # Empty the bar immediately
    value = min_value

    # Refill over time
    var tween := create_tween()
    tween.tween_property(self, "value", max_value, time_to_recharge)

    # Visual effects
    _animation_player.play("use")
    tween.tween_callback(_animation_player.play.bind("ready"))
```

## Loading Bar {#loading}

```gdscript
extends ProgressBar

signal loading_complete

var _loading_thread: Thread

func start_loading(resource_path: String) -> void:
    value = 0.0
    _loading_thread = Thread.new()
    _loading_thread.start(_load_resource.bind(resource_path))

func _load_resource(path: String) -> void:
    var progress: Array[float] = []

    ResourceLoader.load_threaded_request(path)

    while true:
        var status := ResourceLoader.load_threaded_get_status(path, progress)

        # Update progress bar on main thread
        call_deferred("_update_progress", progress[0])

        if status == ResourceLoader.THREAD_LOAD_LOADED:
            call_deferred("_on_loading_complete")
            break
        elif status == ResourceLoader.THREAD_LOAD_FAILED:
            call_deferred("_on_loading_failed")
            break

        OS.delay_msec(100)

func _update_progress(progress_value: float) -> void:
    value = progress_value * 100.0

func _on_loading_complete() -> void:
    _loading_thread.wait_to_finish()
    loading_complete.emit()

func _on_loading_failed() -> void:
    _loading_thread.wait_to_finish()
    push_error("Failed to load resource")
```

## 3D Billboard Health Bar {#billboard-3d}

Use SubViewport to render 2D UI in 3D space:

### Scene Structure
```
CharacterBody3D
├── Sprite3D (billboard)
│   └── SubViewport
│       └── ProgressBar
```

### Scene Setup (in .tscn)

```gdscript
# Sprite3D configuration
[node name="Sprite3D" type="Sprite3D" parent="."]
transform = Transform3D(1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1.5, 0)
billboard = 1  # Always face camera
texture = SubResource("ViewportTexture_health")

# SubViewport configuration
[node name="SubViewport" type="SubViewport" parent="Sprite3D"]
transparent_bg = true
size = Vector2i(200, 48)

# ProgressBar inside viewport
[node name="ProgressBar" type="ProgressBar" parent="Sprite3D/SubViewport"]
offset_right = 200.0
offset_bottom = 48.0
value = 100.0
show_percentage = false
```

### Script for 3D Health Bar

```gdscript
extends CharacterBody3D

@onready var _progress_bar: ProgressBar = %ProgressBar

func take_damage() -> void:
    var tween := create_tween()
    tween.tween_property(_progress_bar, "value", 0.0, 1.0)
    tween.parallel().tween_property(
        _progress_bar,
        "modulate",
        Color.ROSY_BROWN,
        1.0
    )
    await tween.finished
    await get_tree().create_timer(1.0).timeout
    queue_free()
```

### Alternative: Pure Shader 3D Progress Bar

For better performance without SubViewport:

```gdscript
# Use a QuadMesh with custom shader
# See community addon: "Progress Bar 3D" on Godot Asset Library
# https://godotengine.org/asset-library/asset/2842
```

## Resource Meters (Mana, Stamina) {#resource-meters}

```gdscript
extends Control

@export var max_mana: float = 100.0
@export var mana_regen_rate: float = 5.0  # per second

@onready var _mana_bar: ProgressBar = %ManaBar

var current_mana: float:
    set(value):
        current_mana = clampf(value, 0.0, max_mana)
        _mana_bar.value = current_mana

func _ready() -> void:
    _mana_bar.max_value = max_mana
    current_mana = max_mana

func _process(delta: float) -> void:
    # Auto-regenerate mana
    if current_mana < max_mana:
        current_mana += mana_regen_rate * delta

func cast_spell(mana_cost: float) -> bool:
    if current_mana >= mana_cost:
        current_mana -= mana_cost
        return true
    return false
```

## Multiple Bars (Health + Shield) {#multiple-bars}

```gdscript
extends Control

@onready var _health_bar: ProgressBar = %HealthBar
@onready var _shield_bar: ProgressBar = %ShieldBar

var max_health: float = 100.0
var max_shield: float = 50.0
var current_health: float = 100.0
var current_shield: float = 50.0

func _ready() -> void:
    _health_bar.max_value = max_health
    _health_bar.value = current_health

    _shield_bar.max_value = max_shield
    _shield_bar.value = current_shield

func take_damage(amount: float) -> void:
    # Shield absorbs damage first
    if current_shield > 0:
        var shield_damage := minf(amount, current_shield)
        current_shield -= shield_damage
        _update_shield_bar()
        amount -= shield_damage

    # Remaining damage hits health
    if amount > 0:
        current_health -= amount
        _update_health_bar()

func _update_health_bar() -> void:
    var tween := create_tween()
    tween.tween_property(_health_bar, "value", current_health, 0.3)

func _update_shield_bar() -> void:
    var tween := create_tween()
    tween.tween_property(_shield_bar, "value", current_shield, 0.3)
```

## Best Practices & Pitfalls

### Performance
- Use ProgressBar for simple themed bars (lighter weight)
- Use TextureProgressBar when custom visuals are needed
- For many 3D health bars, consider shader-based approach instead of SubViewport
- Cache tween references to avoid creating too many simultaneous tweens

### Visual Design
- Always clamp values between min_value and max_value
- Use color transitions to indicate health status (green → yellow → red)
- Add smooth animations (0.2-0.5s) for better visual feedback
- Consider adding delayed "damage ghost" effect (show previous value briefly)

### Common Mistakes
- **Not waiting for ready**: Setters may run before nodes are in tree
  ```gdscript
  # CORRECT
  func set_health(value: int) -> void:
      if not is_inside_tree():
          await ready
      # Now safe to use
  ```
- **Inverse ranges**: For "faster = better" stats, invert display:
  ```gdscript
  # Fire rate: 0.05 (fast) to 0.5 (slow)
  # Display as: 100% (fast) to 0% (slow)
  var display_value := 1.0 - (fire_rate / max_fire_rate)
  bar.value = display_value * 100.0
  ```
- **Not clamping values**: Always use `clamp()` or `clampi()` to prevent overflow
- **Forgetting to set max_value**: Default is 100, update if using different range

### Accessibility
- Set `show_percentage = true` for important bars (screen readers)
- Use high-contrast colors for visibility
- Consider adding numerical text labels alongside bars
- Test bars at different screen resolutions

## Related Patterns

- [Tween](/home/sam/code/godot_advisor/.claude/skills/godot/reference/animation/tween.md) - Smooth value animations
- [Health System](/home/sam/code/godot_advisor/.claude/skills/godot/reference/patterns/health-system.md) - Complete health management
- [UI Controls](/home/sam/code/godot_advisor/.claude/skills/godot/reference/ui/controls.md) - Other UI elements
- [Themes](/home/sam/code/godot_advisor/.claude/skills/godot/reference/ui/themes.md) - Styling progress bars
