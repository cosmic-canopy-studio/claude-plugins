# Scene Management

## Basic Scene Change

```gdscript
# Direct file load (simple, common)
get_tree().change_scene_to_file("res://scenes/level.tscn")

# From preloaded/packed scene (performant)
const LEVEL_SCENE: PackedScene = preload("res://scenes/level.tscn")
get_tree().change_scene_to_packed(LEVEL_SCENE)
```

## Scene Manager Pattern

```gdscript
# scene_manager.gd - Add as Autoload
extends Node

signal scene_changed(scene_name: String)
var current_scene: Node

func _ready() -> void:
    var root: Window = get_tree().root
    current_scene = root.get_child(root.get_child_count() - 1)

func goto_scene(path: String) -> void:
    call_deferred("_deferred_goto_scene", path)

func _deferred_goto_scene(path: String) -> void:
    current_scene.free()
    var new_scene: PackedScene = load(path)
    current_scene = new_scene.instantiate()
    get_tree().root.add_child(current_scene)
    get_tree().current_scene = current_scene
    scene_changed.emit(path)
```

## With Fade Transition

```gdscript
# Requires a ColorRect named FadeRect as child of SceneManager
# FadeRect should be full-screen with black color and start transparent

func goto_scene_with_fade(path: String, duration: float = 0.5) -> void:
    var tween: Tween = create_tween()
    tween.tween_property($FadeRect, "color:a", 1.0, duration / 2.0)
    await tween.finished
    _deferred_goto_scene(path)
    tween = create_tween()
    tween.tween_property($FadeRect, "color:a", 0.0, duration / 2.0)
```

## Background Loading (Large Scenes)

```gdscript
# For scenes that take time to load
extends Node

var loader: ResourceLoader.ThreadedLoadStatus
var loading_path: String

func load_scene_async(path: String) -> void:
    loading_path = path
    ResourceLoader.load_threaded_request(path)

func _process(_delta: float) -> void:
    if loading_path.is_empty():
        return

    var status: ResourceLoader.ThreadLoadStatus = ResourceLoader.load_threaded_get_status(loading_path)

    match status:
        ResourceLoader.THREAD_LOAD_LOADED:
            var scene: PackedScene = ResourceLoader.load_threaded_get(loading_path)
            get_tree().change_scene_to_packed(scene)
            loading_path = ""
        ResourceLoader.THREAD_LOAD_FAILED:
            push_error("Failed to load scene: " + loading_path)
            loading_path = ""
```

## Child Swap Pattern (State Preservation)

From Godot official demo: `2d/role_playing_game/game.gd`

Keep both scenes in memory and swap visibility. State is preserved across transitions.

```gdscript
# game.gd - Root node managing scene swaps
extends Node

var exploration_scene: Node
var combat_scene: Node

func _ready() -> void:
    exploration_scene = $Exploration
    combat_scene = preload("res://combat/combat.tscn").instantiate()

func start_combat() -> void:
    # Remove exploration from tree but keep in memory
    remove_child(exploration_scene)
    add_child(combat_scene)

func end_combat() -> void:
    # Swap back - exploration state preserved
    remove_child(combat_scene)
    add_child(exploration_scene)
```

**With Fade Animation:**
```gdscript
func start_combat_with_fade() -> void:
    $AnimationPlayer.play("fade")
    await $AnimationPlayer.animation_finished
    remove_child(exploration_scene)
    add_child(combat_scene)
    $AnimationPlayer.play_backwards("fade")
```

**Best For:**
- Preserving scene state between transitions
- Scenes that frequently swap back and forth
- When you need to "pause" one scene while showing another

**Trade-offs:**
- Both scenes stay in memory
- More complex than change_scene_*
- Must manually manage scene lifecycle

## When to Use Each

| Approach | Use When | State | Memory |
|----------|----------|-------|--------|
| `change_scene_to_file()` | Simple games, prototyping | Lost | Freed |
| `change_scene_to_packed()` | Preloaded, editor-validated | Lost | Freed |
| Child swap | Return to previous state (RPG combat) | Preserved | Both loaded |
| SceneManager autoload | Transitions, history, loading screens | Configurable | Freed |
| Background loading | Large scenes, avoid frame drops | Lost | Freed |

## Main Menu Example

```gdscript
extends Control

func _ready() -> void:
    # Focus first button for keyboard/gamepad navigation
    $VBoxContainer/StartButton.grab_focus()

func _on_start_button_pressed() -> void:
    get_tree().change_scene_to_file("res://scenes/game.tscn")

func _on_practice_button_pressed() -> void:
    get_tree().change_scene_to_file("res://scenes/practice.tscn")

func _on_options_button_pressed() -> void:
    $OptionsPanel.visible = true

func _on_quit_button_pressed() -> void:
    get_tree().quit()
```

**Scene Structure:**
```
Control (root, full rect anchor)
└── VBoxContainer (centered)
    ├── Label (game title)
    ├── StartButton
    ├── PracticeButton
    ├── OptionsButton
    └── QuitButton
```

## Common Patterns

### Return to Previous Scene

```gdscript
# In SceneManager autoload
var scene_history: Array[String] = []

func goto_scene(path: String) -> void:
    if current_scene:
        scene_history.append(current_scene.scene_file_path)
    call_deferred("_deferred_goto_scene", path)

func go_back() -> void:
    if scene_history.is_empty():
        return
    var previous: String = scene_history.pop_back()
    call_deferred("_deferred_goto_scene", previous)
```

### Passing Data Between Scenes

```gdscript
# In SceneManager autoload
var scene_data: Dictionary = {}

func goto_scene_with_data(path: String, data: Dictionary) -> void:
    scene_data = data
    goto_scene(path)

# In new scene's _ready()
func _ready() -> void:
    if not SceneManager.scene_data.is_empty():
        var level_id: int = SceneManager.scene_data.get("level_id", 0)
        var difficulty: String = SceneManager.scene_data.get("difficulty", "normal")
        SceneManager.scene_data.clear()
```
