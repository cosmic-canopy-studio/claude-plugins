---
topic: signals
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-signals
  - godot-event-bus
---

# Signals

Signal patterns for decoupled communication in Godot.

## Defining Signals {#define}

```gdscript
extends Node

# Simple signal
signal died

# Signal with parameters
signal health_changed(new_health: int, max_health: int)

# Signal with typed parameter
signal item_collected(item: Resource)
```

## Emitting Signals

```gdscript
func take_damage(amount: int) -> void:
    health -= amount
    health_changed.emit(health, max_health)

    if health <= 0:
        died.emit()
```

## Connecting Signals {#connect}

### In Code

```gdscript
func _ready() -> void:
    # Connect to method
    player.health_changed.connect(_on_player_health_changed)

    # With bind (pass extra arguments)
    button.pressed.connect(_on_button_pressed.bind(button_id))

    # One-shot (auto-disconnects after first call)
    timer.timeout.connect(_on_timeout, CONNECT_ONE_SHOT)

func _on_player_health_changed(new_health: int, max_health: int) -> void:
    health_bar.value = float(new_health) / max_health
```

### In Inspector

1. Select node with signal
2. Node dock > Signals tab
3. Double-click signal > Choose target node and method

## Signal with Parameters {#parameters}

```gdscript
# Emitter
signal damage_dealt(amount: int, source: Node, target: Node)

func attack(target: Node) -> void:
    var damage := calculate_damage()
    damage_dealt.emit(damage, self, target)

# Receiver
func _ready() -> void:
    attacker.damage_dealt.connect(_on_damage_dealt)

func _on_damage_dealt(amount: int, source: Node, target: Node) -> void:
    if target == self:
        take_damage(amount)
        spawn_damage_number(amount, source.global_position)
```

## One-Shot Signals {#one-shot}

Auto-disconnect after first emission:

```gdscript
# Connect with flag
signal.connect(callback, CONNECT_ONE_SHOT)

# Or await the signal
await animation_player.animation_finished
print("Animation done!")
```

## Disconnecting

```gdscript
# Disconnect specific callback
player.died.disconnect(_on_player_died)

# Check if connected
if player.died.is_connected(_on_player_died):
    player.died.disconnect(_on_player_died)
```

## Event Bus Pattern {#event-bus}

Global autoload for cross-scene communication:

```gdscript
# events.gd - Add as Autoload named "Events"
extends Node

# Player events
signal player_died
signal player_spawned(player: Node)
signal player_health_changed(current: int, maximum: int)

# Game events
signal score_changed(new_score: int)
signal level_completed(level_id: int)
signal game_paused(is_paused: bool)

# Enemy events
signal enemy_defeated(enemy_type: String, position: Vector2)
signal boss_phase_changed(phase: int)

# UI events
signal dialog_started(dialog_id: String)
signal dialog_ended
signal notification_requested(message: String)
```

### Emitting Global Events

```gdscript
# From player script
func die() -> void:
    Events.player_died.emit()

# From enemy script
func _on_defeated() -> void:
    Events.enemy_defeated.emit(enemy_type, global_position)
    Events.score_changed.emit(GameManager.score + points)
```

### Subscribing to Global Events

```gdscript
# In UI script
func _ready() -> void:
    Events.player_health_changed.connect(_update_health_bar)
    Events.score_changed.connect(_update_score_display)
    Events.player_died.connect(_show_game_over)

func _exit_tree() -> void:
    # Clean up connections when removed
    Events.player_health_changed.disconnect(_update_health_bar)
```

## Awaiting Signals

```gdscript
# Wait for signal
await get_tree().create_timer(1.0).timeout

# Wait for custom signal
await player.died

# Wait for animation
animation_player.play("attack")
await animation_player.animation_finished

# Wait with timeout
var result := await Promise.race([
    player.died,
    get_tree().create_timer(5.0).timeout
])
```

## Signal Best Practices

### Do

```gdscript
# Use signals for loose coupling
signal died  # Other systems react to this

# Pass relevant data
signal item_picked_up(item_data: ItemResource, position: Vector2)

# Use descriptive names
signal interaction_started(interactable: Node)
signal interaction_ended
```

### Don't

```gdscript
# Don't pass self when unnecessary
signal updated(self_reference)  # Bad - receiver already has reference

# Don't use signals for tight coupling
signal please_call_this_specific_method  # Bad - just call it directly

# Don't create signals that only one thing listens to
signal _internal_state_changed  # Bad - use a method instead
```

## Typed Callable

For dynamic signal handling:

```gdscript
# Store callback for later
var callback: Callable = _on_something

# Connect later
some_signal.connect(callback)

# Call directly
callback.call()
callback.call(arg1, arg2)

# Bind arguments
var bound := callback.bind(extra_arg)
```

## Common Signal Patterns

### Observable Property

```gdscript
signal value_changed(new_value: int)

var _value: int = 0
var value: int:
    get: return _value
    set(v):
        if _value != v:
            _value = v
            value_changed.emit(_value)
```

### Request/Response

```gdscript
# Requester
signal data_requested(callback: Callable)

func request_data() -> void:
    data_requested.emit(_on_data_received)

func _on_data_received(data: Dictionary) -> void:
    process_data(data)

# Provider
func _ready() -> void:
    requester.data_requested.connect(_on_data_requested)

func _on_data_requested(callback: Callable) -> void:
    var data := fetch_data()
    callback.call(data)
```
