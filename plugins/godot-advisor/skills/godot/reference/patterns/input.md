---
topic: input
version: 2025.12.21
godot_version: "4.3"
sources:
  - official: https://docs.godotengine.org/en/4.3/classes/class_input.html
  - official: https://docs.godotengine.org/en/stable/tutorials/inputs/inputevent.html
  - official: https://docs.godotengine.org/en/stable/classes/class_inputmap.html
  - examples: repos/godot_node_essentials/common/2d/astronaut_player_2d/
  - examples: repos/godot_node_essentials/common/3d/fps_player_3d/
  - community: https://gamedevartisan.com/tutorials/godot-fundamentals/input-remapping
---

# Input Handling

Handle keyboard, mouse, gamepad, and touch input for responsive player control.

## Input Polling vs Events

### Polling in _physics_process()

Best for continuous movement and frequent checks:

```gdscript
func _physics_process(delta: float) -> void:
    # Action-based input (maps to multiple devices)
    var direction := Input.get_axis("move_left", "move_right")
    velocity.x = direction * speed

    # Check if action is currently held
    if Input.is_action_pressed("jump") and is_on_floor():
        velocity.y = -jump_strength
```

### Event Callbacks

Best for discrete actions (button presses, UI interactions):

```gdscript
# _input() - receives ALL input events (runs before UI)
func _input(event: InputEvent) -> void:
    if event.is_action_pressed("pause"):
        get_tree().paused = not get_tree().paused
        get_viewport().set_input_as_handled()

# _unhandled_input() - receives events NOT consumed by UI
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("interact"):
        attempt_interaction()
```

**When to use which:**
- `_input()` - UI, pausing, global shortcuts (runs first)
- `_unhandled_input()` - gameplay interactions (runs after UI)
- Polling - continuous movement, held buttons

## Action-Based Input

### Basic Actions

```gdscript
# Check state
Input.is_action_pressed("jump")        # Held this frame
Input.is_action_just_pressed("jump")   # Pressed this frame (edge trigger)
Input.is_action_just_released("jump")  # Released this frame (edge trigger)

# Get strength (0.0 to 1.0, useful for triggers)
var brake_amount := Input.get_action_strength("brake")
```

### Directional Input

```gdscript
# Single axis (-1.0 to 1.0)
var horizontal := Input.get_axis("move_left", "move_right")
velocity.x = horizontal * speed

# 2D vector (automatically normalized)
var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
velocity = direction * speed

# 3D movement with camera basis
var input := Input.get_vector("move_left", "move_right", "move_up", "move_down")
var direction_3d := Vector3(input.x, 0.0, input.y)
direction_3d = camera.global_basis * direction_3d
```

## Mouse Input

### Mouse Motion

```gdscript
@export var mouse_sensitivity := 0.25

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseMotion and Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
        # Use relative motion for smooth camera control
        rotate_y(-event.relative.x * mouse_sensitivity * 0.01)
        camera.rotate_x(-event.relative.y * mouse_sensitivity * 0.01)
```

### Mouse Modes

```gdscript
func _ready() -> void:
    # Capture mouse for FPS controls
    Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("ui_cancel"):
        # Release mouse for menus
        Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
```

**Mouse modes:**
- `MOUSE_MODE_VISIBLE` - Normal cursor
- `MOUSE_MODE_HIDDEN` - Invisible but not locked
- `MOUSE_MODE_CAPTURED` - Locked to center, invisible (FPS)
- `MOUSE_MODE_CONFINED` - Cannot leave window

### Mouse Position

```gdscript
func _process(_delta: float) -> void:
    # World position (2D)
    var world_pos := get_global_mouse_position()

    # Screen position
    var screen_pos := get_viewport().get_mouse_position()

    # Follow mouse
    global_position = world_pos
```

## Keyboard Input

### Direct Key Checks

```gdscript
func _input(event: InputEvent) -> void:
    if event is InputEventKey:
        if event.pressed and event.keycode == KEY_F11:
            toggle_fullscreen()

        # Check for modifiers
        if event.ctrl_pressed and event.keycode == KEY_S:
            save_game()
```

**Prefer actions over direct key checks** for player-configurable controls.

## Gamepad Input

### Setup in project.godot

```ini
[input]
jump={
"deadzone": 0.5,
"events": [
    Object(InputEventKey, "keycode": KEY_SPACE),
    Object(InputEventJoypadButton, "device": -1, "button_index": JOY_BUTTON_A)
]
}

move_left={
"deadzone": 0.2,
"events": [
    Object(InputEventKey, "keycode": KEY_A),
    Object(InputEventJoypadButton, "device": -1, "button_index": JOY_BUTTON_DPAD_LEFT),
    Object(InputEventJoypadMotion, "device": -1, "axis": JOY_AXIS_LEFT_X, "axis_value": -1.0)
]
}
```

**Note:** `device: -1` means any controller. Use specific device IDs for local multiplayer.

### Analog Stick Handling

```gdscript
# Input.get_axis() automatically handles deadzones
var input_right_left := Input.get_axis("move_left", "move_right")
var input_back_forward := Input.get_axis("move_up", "move_down")

# Manual deadzone (if needed)
var raw_x := Input.get_joy_axis(0, JOY_AXIS_LEFT_X)
var deadzone := 0.2
var stick_x := 0.0 if abs(raw_x) < deadzone else raw_x
```

### Vibration

```gdscript
func take_damage(amount: int) -> void:
    health -= amount

    # Rumble for 0.3 seconds (weak_magnitude, strong_magnitude)
    Input.start_joy_vibration(0, 0.5, 0.8, 0.3)
```

## Input Buffering

Store inputs for a short time to make controls more forgiving:

```gdscript
class_name Player extends CharacterBody2D

const JUMP_BUFFER_TIME := 0.1  # 100ms buffer

var _jump_buffer_timer := 0.0

func _physics_process(delta: float) -> void:
    # Update buffer timer
    if _jump_buffer_timer > 0.0:
        _jump_buffer_timer -= delta

    # Store jump input
    if Input.is_action_just_pressed("jump"):
        _jump_buffer_timer = JUMP_BUFFER_TIME

    # Consume buffered input
    if _jump_buffer_timer > 0.0 and is_on_floor():
        velocity.y = -jump_strength
        _jump_buffer_timer = 0.0  # Clear buffer

    move_and_slide()
```

### Coyote Time Pattern

Allow jumping shortly after leaving a ledge:

```gdscript
const COYOTE_TIME := 0.15

var _coyote_timer := 0.0
var _was_on_floor := false

func _physics_process(delta: float) -> void:
    var on_floor := is_on_floor()

    # Start coyote timer when leaving floor
    if _was_on_floor and not on_floor:
        _coyote_timer = COYOTE_TIME

    # Decrease timer
    if _coyote_timer > 0.0:
        _coyote_timer -= delta

    # Allow jump during coyote time
    if Input.is_action_just_pressed("jump") and (_coyote_timer > 0.0 or on_floor):
        velocity.y = -jump_strength
        _coyote_timer = 0.0

    _was_on_floor = on_floor
    move_and_slide()
```

## Input Remapping

### Runtime Key Rebinding

```gdscript
# Display current binding
func get_action_key_name(action: String) -> String:
    var events := InputMap.action_get_events(action)
    for event in events:
        if event is InputEventKey:
            return OS.get_keycode_string(event.keycode)
    return "Unbound"

# Wait for new key input
func remap_action(action: String, new_event: InputEvent) -> void:
    # Remove existing events
    InputMap.action_erase_events(action)

    # Add new event
    InputMap.action_add_event(action, new_event)

# UI example
var _remapping_action := ""

func start_remapping(action: String) -> void:
    _remapping_action = action
    status_label.text = "Press any key..."

func _input(event: InputEvent) -> void:
    if _remapping_action == "":
        return

    if event is InputEventKey and event.pressed:
        remap_action(_remapping_action, event)
        status_label.text = "Bound to: %s" % OS.get_keycode_string(event.keycode)
        _remapping_action = ""
        get_viewport().set_input_as_handled()
```

### Creating Actions at Runtime

```gdscript
func create_custom_action(action_name: String, key: Key) -> void:
    # Check if action already exists
    if InputMap.has_action(action_name):
        return

    # Add new action
    InputMap.add_action(action_name)

    # Create and add event
    var event := InputEventKey.new()
    event.keycode = key
    InputMap.action_add_event(action_name, event)

# Usage
func _ready() -> void:
    create_custom_action("toggle_debug", KEY_F3)
```

## Input Cooldowns

Prevent spam and enforce ability timing:

```gdscript
class_name AbilityController extends Node2D

var _boost_cooldown := 0.0
@export var boost_cooldown_time := 2.0

func _process(delta: float) -> void:
    # Decrease cooldown
    if _boost_cooldown > 0.0:
        _boost_cooldown -= delta

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("boost"):
        attempt_boost()

func attempt_boost() -> void:
    if _boost_cooldown > 0.0:
        return  # Still on cooldown

    # Activate ability
    execute_boost()

    # Start cooldown
    _boost_cooldown = boost_cooldown_time

func is_boost_ready() -> bool:
    return _boost_cooldown <= 0.0

func get_cooldown_percent() -> float:
    return 1.0 - (_boost_cooldown / boost_cooldown_time)
```

## Input Sequences

Detect combo inputs (e.g., fighting game moves):

```gdscript
class_name ComboDetector extends Node

const SEQUENCE_TIMEOUT := 0.5
var _sequence: Array[String] = []
var _sequence_timer := 0.0

func _process(delta: float) -> void:
    if _sequence_timer > 0.0:
        _sequence_timer -= delta
        if _sequence_timer <= 0.0:
            _sequence.clear()

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("punch"):
        add_to_sequence("punch")
    elif event.is_action_pressed("kick"):
        add_to_sequence("kick")

func add_to_sequence(action: String) -> void:
    _sequence.append(action)
    _sequence_timer = SEQUENCE_TIMEOUT

    check_combos()

func check_combos() -> void:
    # Check for specific sequences
    if _sequence == ["punch", "punch", "kick"]:
        execute_combo("triple_strike")
        _sequence.clear()
    elif _sequence == ["kick", "punch"]:
        execute_combo("uppercut")
        _sequence.clear()

func execute_combo(combo_name: String) -> void:
    print("Executed combo: ", combo_name)
```

## Input Validation

Prevent invalid states and handle edge cases:

```gdscript
func _physics_process(delta: float) -> void:
    # Prevent contradictory inputs
    var direction := Input.get_axis("move_left", "move_right")

    # Dead zone for analog inputs
    if abs(direction) < 0.1:
        direction = 0.0

    # Only allow jump from valid states
    if Input.is_action_just_pressed("jump"):
        if is_on_floor() and not is_stunned and not is_dead:
            jump()

    # Prevent action during animation
    if Input.is_action_just_pressed("attack"):
        if not animation_player.is_playing():
            attack()
```

## Best Practices

### Use Actions, Not Raw Keys

```gdscript
# Bad - hardcoded to Space key
if Input.is_key_pressed(KEY_SPACE):
    jump()

# Good - player can rebind "jump" action
if Input.is_action_just_pressed("jump"):
    jump()
```

### Handle Input in Appropriate Callbacks

```gdscript
# Continuous movement - use _physics_process()
func _physics_process(delta: float) -> void:
    var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
    velocity = direction * speed
    move_and_slide()

# Discrete actions - use _unhandled_input()
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("interact"):
        interact_with_object()
```

### Consume Input Events

```gdscript
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("special_move"):
        perform_special_move()
        # Prevent other nodes from processing this event
        get_viewport().set_input_as_handled()
```

### Separate Input from Logic

```gdscript
# Good - separate input reading from action execution
class_name Player extends CharacterBody2D

var _wants_to_jump := false

func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("jump"):
        _wants_to_jump = true

func _physics_process(delta: float) -> void:
    if _wants_to_jump and can_jump():
        jump()
    _wants_to_jump = false  # Clear flag

    move_and_slide()

func can_jump() -> bool:
    return is_on_floor() and not is_stunned
```

### Handle Multiple Input Devices

```gdscript
# Accept input from any source
var direction := Input.get_vector("move_left", "move_right", "move_up", "move_down")
# Works with: WASD, arrow keys, D-pad, left stick

# Local multiplayer - device-specific
func _input(event: InputEvent) -> void:
    if event.device == player_device_id:
        # Only process input from this player's controller
        process_player_input(event)
```

## Common Patterns

### Jump with Variable Height

```gdscript
func _physics_process(delta: float) -> void:
    velocity.y += gravity * delta

    # Start jump
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = -jump_strength

    # Cut jump short if button released
    if Input.is_action_just_released("jump") and velocity.y < 0.0:
        velocity.y *= 0.5  # Reduce upward velocity

    move_and_slide()
```

### Charge Attack

```gdscript
var _charge_time := 0.0
const MAX_CHARGE_TIME := 2.0

func _process(delta: float) -> void:
    # Charge while held
    if Input.is_action_pressed("attack"):
        _charge_time = min(_charge_time + delta, MAX_CHARGE_TIME)

    # Release to attack
    if Input.is_action_just_released("attack"):
        var charge_percent := _charge_time / MAX_CHARGE_TIME
        attack(charge_percent)
        _charge_time = 0.0
```

### Aim Assist (Stick Drift Correction)

```gdscript
func get_aim_direction() -> Vector2:
    var aim := Input.get_vector("aim_left", "aim_right", "aim_up", "aim_down")

    # Ignore very small values (stick drift)
    if aim.length() < 0.15:
        return Vector2.ZERO

    return aim.normalized()
```

## Performance Tips

- Use `is_action_just_pressed()` instead of manual frame tracking
- Cache input values when using multiple times per frame
- Avoid polling in `_process()` - use `_physics_process()` for consistency
- Use action deadzones in Project Settings instead of manual checks

## See Also

- [Signals](signals.md) - Decouple input handling from game logic
- [State Machines](../patterns/state-machine.md) - Manage context-sensitive controls
- [CharacterBody2D/3D](../nodes/character-body.md) - Physics-based movement
