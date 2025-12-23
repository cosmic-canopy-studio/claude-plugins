---
topic: scene-transitions
version: 2025.12.21
godot_version: "4.3"
sources:
  - godot-autoloads
  - official-docs
---

# Scene Transitions

Patterns for loading and switching between scenes in Godot 4.

## Quick Start

```gdscript
# Simplest approach - direct scene change
get_tree().change_scene_to_file("res://scenes/game.tscn")
```

## GameManager Autoload Pattern

Centralize scene transitions in an autoload for better organization:

```gdscript
# autoloads/game_manager.gd
extends Node

enum GameState { MENU, PLAYING, PAUSED, GAME_OVER }

var current_state: GameState = GameState.MENU

signal state_changed(new_state: GameState)

func start_game() -> void:
    current_state = GameState.PLAYING
    state_changed.emit(current_state)
    get_tree().change_scene_to_file("res://scenes/game.tscn")

func go_to_practice() -> void:
    current_state = GameState.PLAYING
    state_changed.emit(current_state)
    get_tree().change_scene_to_file("res://scenes/practice.tscn")

func return_to_menu() -> void:
    current_state = GameState.MENU
    state_changed.emit(current_state)
    get_tree().change_scene_to_file("res://scenes/main_menu.tscn")

func quit_game() -> void:
    get_tree().quit()
```

Register in Project Settings → Autoload as `GameManager`.

## Main Menu Implementation

```gdscript
# scenes/main_menu.gd
extends Control

@onready var play_button: Button = $VBoxContainer/PlayButton
@onready var practice_button: Button = $VBoxContainer/PracticeButton
@onready var quit_button: Button = $VBoxContainer/QuitButton

func _ready() -> void:
    play_button.pressed.connect(_on_play_pressed)
    practice_button.pressed.connect(_on_practice_pressed)
    quit_button.pressed.connect(_on_quit_pressed)

    # Optional: set initial focus for keyboard/gamepad navigation
    play_button.grab_focus()

func _on_play_pressed() -> void:
    GameManager.start_game()

func _on_practice_pressed() -> void:
    GameManager.go_to_practice()

func _on_quit_pressed() -> void:
    GameManager.quit_game()
```

## Transition Effects

### Fade Transition with CanvasLayer

```gdscript
# autoloads/scene_manager.gd
extends CanvasLayer

@onready var color_rect: ColorRect = $ColorRect
@onready var animation_player: AnimationPlayer = $AnimationPlayer

var _next_scene_path: String = ""

func change_scene_with_fade(path: String) -> void:
    _next_scene_path = path
    animation_player.play("fade_out")

func _on_fade_out_finished() -> void:
    get_tree().change_scene_to_file(_next_scene_path)
    animation_player.play("fade_in")
```

Scene structure:
```
SceneManager (CanvasLayer, layer=100)
├── ColorRect (full screen, modulate alpha animated)
└── AnimationPlayer
    ├── fade_out: ColorRect modulate.a from 0 → 1
    └── fade_in: ColorRect modulate.a from 1 → 0
```

### Simple Tween Fade

```gdscript
# autoloads/scene_manager.gd
extends CanvasLayer

@onready var fade_rect: ColorRect = $FadeRect

func change_scene_with_fade(path: String, duration: float = 0.5) -> void:
    var tween := create_tween()
    tween.tween_property(fade_rect, "modulate:a", 1.0, duration)
    await tween.finished

    get_tree().change_scene_to_file(path)

    tween = create_tween()
    tween.tween_property(fade_rect, "modulate:a", 0.0, duration)
```

## Async Loading for Large Scenes

For scenes that take time to load:

```gdscript
# autoloads/scene_manager.gd
extends Node

signal loading_progress(progress: float)
signal loading_finished

var _loader_path: String = ""

func load_scene_async(path: String) -> void:
    _loader_path = path
    ResourceLoader.load_threaded_request(path)
    set_process(true)

func _process(_delta: float) -> void:
    if _loader_path.is_empty():
        set_process(false)
        return

    var progress: Array = []
    var status := ResourceLoader.load_threaded_get_status(_loader_path, progress)

    match status:
        ResourceLoader.THREAD_LOAD_IN_PROGRESS:
            loading_progress.emit(progress[0])
        ResourceLoader.THREAD_LOAD_LOADED:
            var scene: PackedScene = ResourceLoader.load_threaded_get(_loader_path)
            get_tree().change_scene_to_packed(scene)
            _loader_path = ""
            loading_finished.emit()
            set_process(false)
        ResourceLoader.THREAD_LOAD_FAILED:
            push_error("Failed to load scene: " + _loader_path)
            _loader_path = ""
            set_process(false)

func _ready() -> void:
    set_process(false)
```

### Loading Screen

```gdscript
# scenes/loading_screen.gd
extends Control

@onready var progress_bar: ProgressBar = $ProgressBar
@onready var status_label: Label = $StatusLabel

func _ready() -> void:
    SceneManager.loading_progress.connect(_on_loading_progress)
    SceneManager.loading_finished.connect(_on_loading_finished)

func _on_loading_progress(progress: float) -> void:
    progress_bar.value = progress * 100
    status_label.text = "Loading... %d%%" % int(progress * 100)

func _on_loading_finished() -> void:
    status_label.text = "Complete!"
```

## Common Pitfalls

### Double-Click Prevention

Disable buttons during scene transition:

```gdscript
func _on_play_pressed() -> void:
    play_button.disabled = true
    practice_button.disabled = true
    quit_button.disabled = true
    GameManager.start_game()
```

### Hardcoded Scene Paths

Centralize paths in autoload or constants:

```gdscript
# Bad - scattered paths
get_tree().change_scene_to_file("res://scenes/game.tscn")

# Good - centralized in autoload
class_name Scenes

const MAIN_MENU := "res://scenes/main_menu.tscn"
const GAME := "res://scenes/game.tscn"
const PRACTICE := "res://scenes/practice.tscn"
```

### Scene Not Found Errors

Validate scene exists before changing:

```gdscript
func change_scene_safe(path: String) -> void:
    if ResourceLoader.exists(path):
        get_tree().change_scene_to_file(path)
    else:
        push_error("Scene not found: " + path)
```

## Scene Change Methods

| Method | Use Case |
|--------|----------|
| `change_scene_to_file(path)` | Simple scene changes |
| `change_scene_to_packed(scene)` | Pre-loaded or async-loaded scenes |
| `reload_current_scene()` | Restart current level |

## Related Patterns

- [Autoloads](autoloads.md) - GameManager as global singleton
- [Signals](signals.md) - Event-driven scene management
- [UI Controls](../ui/controls.md) - Button configuration
