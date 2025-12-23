---
topic: autoloads
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-autoloads
  - godot-autoload-patterns
---

# Autoloads (Singletons)

Global autoload patterns for game-wide systems.

## Creating an Autoload

1. Create script (e.g., `game_manager.gd`)
2. Project > Project Settings > Globals tab
3. Add path, set name (e.g., "GameManager")
4. Enable checkbox

Access anywhere:
```gdscript
GameManager.start_game()
Events.player_died.emit()
```

## Common Autoloads

### Game Manager

```gdscript
# game_manager.gd
extends Node

enum GameState { MENU, PLAYING, PAUSED, GAME_OVER }

var current_state: GameState = GameState.MENU
var score: int = 0
var high_score: int = 0

signal state_changed(new_state: GameState)

func change_state(new_state: GameState) -> void:
    if current_state == new_state:
        return

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
            _check_high_score()

func start_game() -> void:
    score = 0
    change_state(GameState.PLAYING)
    get_tree().change_scene_to_file("res://scenes/game.tscn")

func add_score(points: int) -> void:
    score += points

func _check_high_score() -> void:
    if score > high_score:
        high_score = score
        SaveManager.save_high_score(high_score)
```

### Event Bus

```gdscript
# events.gd
extends Node

# Player events
signal player_died
signal player_health_changed(current: int, maximum: int)

# Game events
signal score_changed(new_score: int)
signal level_completed(level_id: int)

# UI events
signal show_notification(message: String)
```

### Audio Manager

```gdscript
# audio_manager.gd
extends Node

var music_player: AudioStreamPlayer
var sfx_pool: Array[AudioStreamPlayer] = []

func _ready() -> void:
    music_player = AudioStreamPlayer.new()
    music_player.bus = "Music"
    add_child(music_player)

    for i in 8:
        var player := AudioStreamPlayer.new()
        player.bus = "SFX"
        add_child(player)
        sfx_pool.append(player)

func play_music(stream: AudioStream) -> void:
    music_player.stream = stream
    music_player.play()

func play_sfx(stream: AudioStream) -> void:
    for player in sfx_pool:
        if not player.playing:
            player.stream = stream
            player.play()
            return
```

### Save Manager

```gdscript
# save_manager.gd
extends Node

const SAVE_PATH := "user://save.json"

var save_data: Dictionary = {}

func _ready() -> void:
    load_game()

func save_game() -> void:
    var file := FileAccess.open(SAVE_PATH, FileAccess.WRITE)
    if file:
        file.store_string(JSON.stringify(save_data))

func load_game() -> void:
    if FileAccess.file_exists(SAVE_PATH):
        var file := FileAccess.open(SAVE_PATH, FileAccess.READ)
        if file:
            var json := JSON.new()
            if json.parse(file.get_as_text()) == OK:
                save_data = json.data

func set_value(key: String, value: Variant) -> void:
    save_data[key] = value

func get_value(key: String, default: Variant = null) -> Variant:
    return save_data.get(key, default)
```

## Dependency Injection {#di}

Avoid tight coupling with autoloads:

```gdscript
# Bad - tight coupling
class_name Player
extends CharacterBody2D

func take_damage(amount: int) -> void:
    health -= amount
    GameManager.check_game_over()  # Direct dependency

# Good - loose coupling with signals
class_name Player
extends CharacterBody2D

signal died

func take_damage(amount: int) -> void:
    health -= amount
    if health <= 0:
        died.emit()  # Let others react
```

### Service Locator Pattern

```gdscript
# services.gd
extends Node

var _services: Dictionary = {}

func register(service_name: String, service: Object) -> void:
    _services[service_name] = service

func get_service(service_name: String) -> Object:
    return _services.get(service_name)

# Usage
func _ready() -> void:
    var audio := Services.get_service("audio") as AudioManager
    audio.play_sfx(hit_sound)
```

## Autoload Best Practices

### Do

```gdscript
# Keep autoloads focused
# game_manager.gd - game state only
# audio_manager.gd - audio only
# save_manager.gd - persistence only

# Use signals for communication
signal game_started
signal game_ended

# Provide clear interfaces
func start_game() -> void:
func pause_game() -> void:
func resume_game() -> void:
```

### Don't

```gdscript
# Don't put everything in one autoload
class_name EverythingManager  # Bad

# Don't store scene-specific data
var current_enemies: Array  # Bad - belongs in level

# Don't call scene-specific methods
func update_all_enemies() -> void:  # Bad - use signals
```

## Autoload Order

Autoloads initialize in order listed in Project Settings. If one autoload depends on another, order them correctly:

```
1. Events (no dependencies)
2. SaveManager (no dependencies)
3. AudioManager (no dependencies)
4. GameManager (may use SaveManager)
```

## Testing with Autoloads

For unit testing, inject dependencies:

```gdscript
# Testable class
class_name Player
extends CharacterBody2D

var audio_manager: Node  # Injected dependency

func _ready() -> void:
    if audio_manager == null:
        audio_manager = AudioManager  # Fallback to autoload

func play_jump_sound() -> void:
    audio_manager.play_sfx(jump_sound)

# In tests
func test_player() -> void:
    var mock_audio := MockAudioManager.new()
    player.audio_manager = mock_audio
    player.play_jump_sound()
    assert(mock_audio.last_played == player.jump_sound)
```

## Common Autoload Setups

| Autoload | Purpose | Dependencies |
|----------|---------|--------------|
| Events | Global signals | None |
| Config | Settings/options | None |
| SaveManager | Persistence | None |
| AudioManager | Sound/music | None |
| GameManager | Game state | SaveManager |
| SceneManager | Scene transitions | None |
