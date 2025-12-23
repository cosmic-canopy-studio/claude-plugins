# Game Patterns Dispatcher

Routes to architectural patterns and best practices in Godot 4.

## Architecture

| I want to... | Go to |
|--------------|-------|
| Create global singleton | `reference/patterns/autoloads.md` |
| Event bus for decoupling | `reference/patterns/signals.md#event-bus` |
| Scene management | `reference/patterns/scenes.md` |
| Dependency injection | `reference/patterns/autoloads.md#di` |
| Component system | `reference/patterns/components.md` |

## Signals & Communication

| I want to... | Go to |
|--------------|-------|
| Define custom signals | `reference/patterns/signals.md#define` |
| Connect signals in code | `reference/patterns/signals.md#connect` |
| Signal with parameters | `reference/patterns/signals.md#parameters` |
| One-shot signals | `reference/patterns/signals.md#one-shot` |
| Cross-scene communication | `reference/patterns/signals.md#event-bus` |

## Data & Resources

| I want to... | Go to |
|--------------|-------|
| Create custom resource | `reference/patterns/resources.md#custom` |
| Item/weapon data | `reference/patterns/resources.md#item-data` |
| Enemy stats resource | `reference/patterns/resources.md#enemy-stats` |
| Configuration files | `reference/patterns/resources.md#config` |

## Save/Load

| I want to... | Go to |
|--------------|-------|
| Save game to file | `reference/patterns/save-load.md#save` |
| Load game from file | `reference/patterns/save-load.md#load` |
| JSON serialization | `reference/patterns/save-load.md#json` |
| ConfigFile for settings | `reference/patterns/save-load.md#config` |
| Autosave system | `reference/patterns/save-load.md#autosave` |

## State Machines

| I want to... | Go to |
|--------------|-------|
| Basic state machine | `reference/animation/state-machines.md#basic` |
| Hierarchical states | `reference/animation/state-machines.md#hierarchical` |
| Push/pop state stack | `reference/animation/state-machines.md#stack` |
| Animation state machine | `reference/animation/animation-tree.md` |

## Input Handling

| I want to... | Go to |
|--------------|-------|
| Define input actions | `reference/patterns/input.md#actions` |
| Check input pressed | `reference/patterns/input.md#pressed` |
| Input buffering | `reference/patterns/input.md#buffer` |
| Rebindable controls | `reference/patterns/input.md#rebind` |
| Gamepad vs keyboard | `reference/patterns/input.md#device` |

## Timing & Cooldowns

| I want to... | Go to |
|--------------|-------|
| Timer for cooldown | `reference/patterns/timer.md#cooldown` |
| Delayed action | `reference/patterns/timer.md#delay` |
| Repeating timer | `reference/patterns/timer.md#repeat` |
| Tween for smooth timing | `reference/animation/tween.md` |

## Object Pooling

| I want to... | Go to |
|--------------|-------|
| Pool projectiles | `reference/patterns/pooling.md#projectiles` |
| Pool particles | `reference/patterns/pooling.md#particles` |
| Pool enemies | `reference/patterns/pooling.md#enemies` |

## GDScript Patterns

| I want to... | Go to |
|--------------|-------|
| Static typing best practices | `reference/language/static-typing.md` |
| Export variables | `reference/language/exports.md` |
| Class inheritance | `reference/language/gdscript-basics.md#inheritance` |
| Static functions | `reference/language/gdscript-basics.md#static` |
| Enums | `reference/language/gdscript-basics.md#enums` |

## Testing

| I want to... | Go to |
|--------------|-------|
| Set up GDUnit4 | `reference/testing/gdunit4.md#setup` |
| Write unit tests | `reference/testing/gdunit4.md#unit` |
| Test scenes | `reference/testing/gdunit4.md#scene` |
| Mock dependencies | `reference/testing/gdunit4.md#mocking` |
| Run tests headless | `reference/testing/gdunit4.md#headless` |

## Quick Start: Event Bus

```gdscript
# events.gd - Add as Autoload named "Events"
extends Node

signal player_died
signal player_health_changed(new_health: int, max_health: int)
signal enemy_defeated(enemy_type: String, position: Vector2)
signal item_collected(item_id: String)
signal score_changed(new_score: int)
signal level_completed(level_id: int)
```

**Usage:**
```gdscript
# Emitting events
Events.player_health_changed.emit(current_health, max_health)
Events.enemy_defeated.emit("slime", global_position)

# Subscribing to events
func _ready() -> void:
    Events.player_died.connect(_on_player_died)
    Events.score_changed.connect(_on_score_changed)

func _on_player_died() -> void:
    show_game_over()
```

## Quick Start: Game Manager

```gdscript
# game_manager.gd - Add as Autoload
extends Node

enum GameState { MENU, PLAYING, PAUSED, GAME_OVER }

var current_state: GameState = GameState.MENU
var score: int = 0
var high_score: int = 0

signal state_changed(new_state: GameState)

func change_state(new_state: GameState) -> void:
    current_state = new_state
    state_changed.emit(new_state)

    match new_state:
        GameState.MENU:
            get_tree().paused = false
        GameState.PLAYING:
            get_tree().paused = false
        GameState.PAUSED:
            get_tree().paused = true
        GameState.GAME_OVER:
            get_tree().paused = true
            if score > high_score:
                high_score = score

func start_game() -> void:
    score = 0
    change_state(GameState.PLAYING)
    get_tree().change_scene_to_file("res://scenes/game.tscn")

func add_score(points: int) -> void:
    score += points
    Events.score_changed.emit(score)
```

## Quick Start: Custom Resource

```gdscript
# item_data.gd
class_name ItemData
extends Resource

@export var id: String
@export var display_name: String
@export_multiline var description: String
@export var icon: Texture2D
@export var value: int = 0
@export var stackable: bool = true
@export var max_stack: int = 99
```

**Create Item:** Right-click in FileSystem > New Resource > ItemData

**Usage:**
```gdscript
@export var item_data: ItemData

func use_item() -> void:
    print("Using: ", item_data.display_name)
```

## Quick Start: State Machine

```gdscript
# state_machine.gd
class_name StateMachine
extends Node

@export var initial_state: State
var current_state: State

func _ready() -> void:
    for child in get_children():
        if child is State:
            child.state_machine = self

    if initial_state:
        current_state = initial_state
        current_state.enter()

func _physics_process(delta: float) -> void:
    if current_state:
        current_state.physics_update(delta)

func transition_to(state_name: String) -> void:
    var new_state := get_node_or_null(state_name) as State
    if new_state and new_state != current_state:
        current_state.exit()
        current_state = new_state
        current_state.enter()

# state.gd
class_name State
extends Node

var state_machine: StateMachine

func enter() -> void:
    pass

func exit() -> void:
    pass

func physics_update(_delta: float) -> void:
    pass
```
