---
topic: audio-playback
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-audio-stream-player
  - godot-audio-stream-player-2d
  - godot-audio-stream-player-3d
---

# Audio Players

AudioStreamPlayer patterns for sound effects and music.

## One-Shot Sound {#one-shot}

Play sound once and optionally free:

```gdscript
extends Node

@export var sound: AudioStream

func play_sound() -> void:
    var player := AudioStreamPlayer.new()
    player.stream = sound
    player.bus = "SFX"
    add_child(player)
    player.play()
    player.finished.connect(player.queue_free)
```

### Simpler One-Shot

```gdscript
@onready var audio: AudioStreamPlayer = $AudioStreamPlayer

func play_hit() -> void:
    audio.play()
```

## Sound with Pitch Variation {#random-pitch}

More natural-sounding repeated sounds:

```gdscript
@export var sound: AudioStream
@export var pitch_variation: float = 0.1

func play_varied() -> void:
    var player := AudioStreamPlayer.new()
    player.stream = sound
    player.pitch_scale = randf_range(1.0 - pitch_variation, 1.0 + pitch_variation)
    add_child(player)
    player.play()
    player.finished.connect(player.queue_free)
```

## Sound Pool {#pool}

For sounds that may play simultaneously:

```gdscript
extends Node

@export var pool_size: int = 8
@export var bus: String = "SFX"

var _players: Array[AudioStreamPlayer] = []

func _ready() -> void:
    for i in pool_size:
        var player := AudioStreamPlayer.new()
        player.bus = bus
        add_child(player)
        _players.append(player)

func play(stream: AudioStream, pitch: float = 1.0) -> void:
    for player in _players:
        if not player.playing:
            player.stream = stream
            player.pitch_scale = pitch
            player.play()
            return

    # All busy - use first (oldest sound)
    _players[0].stream = stream
    _players[0].pitch_scale = pitch
    _players[0].play()
```

## Footstep System {#footsteps}

```gdscript
extends Node

@export var footstep_sounds: Array[AudioStream]
@export var step_interval: float = 0.4

var _step_timer: float = 0.0
var _last_index: int = -1

@onready var player: AudioStreamPlayer2D = $AudioStreamPlayer2D

func update_footsteps(delta: float, is_moving: bool, is_grounded: bool) -> void:
    if is_moving and is_grounded:
        _step_timer -= delta
        if _step_timer <= 0:
            _play_footstep()
            _step_timer = step_interval
    else:
        _step_timer = 0  # Reset on stop

func _play_footstep() -> void:
    if footstep_sounds.is_empty():
        return

    # Avoid repeating same sound
    var index := randi() % footstep_sounds.size()
    if index == _last_index and footstep_sounds.size() > 1:
        index = (index + 1) % footstep_sounds.size()
    _last_index = index

    player.stream = footstep_sounds[index]
    player.pitch_scale = randf_range(0.9, 1.1)
    player.play()
```

## UI Sounds {#ui-sounds}

```gdscript
# ui_sounds.gd - Autoload
extends Node

@export var click_sound: AudioStream
@export var hover_sound: AudioStream

var _player: AudioStreamPlayer

func _ready() -> void:
    _player = AudioStreamPlayer.new()
    _player.bus = "UI"
    add_child(_player)

func play_click() -> void:
    _player.stream = click_sound
    _player.play()

func play_hover() -> void:
    _player.stream = hover_sound
    _player.play()

# Connect to all buttons
func _on_button_pressed() -> void:
    play_click()

func _on_button_mouse_entered() -> void:
    play_hover()
```

## Music Player

### Basic Loop

```gdscript
extends AudioStreamPlayer

@export var music: AudioStream

func _ready() -> void:
    stream = music
    bus = "Music"
    play()
```

### Crossfade Between Tracks

```gdscript
extends Node

var _current_player: AudioStreamPlayer
var _next_player: AudioStreamPlayer

func _ready() -> void:
    _current_player = AudioStreamPlayer.new()
    _current_player.bus = "Music"
    add_child(_current_player)

    _next_player = AudioStreamPlayer.new()
    _next_player.bus = "Music"
    _next_player.volume_db = -80
    add_child(_next_player)

func crossfade_to(stream: AudioStream, duration: float = 1.0) -> void:
    _next_player.stream = stream
    _next_player.volume_db = -80
    _next_player.play()

    var tween := create_tween()
    tween.set_parallel(true)
    tween.tween_property(_current_player, "volume_db", -80.0, duration)
    tween.tween_property(_next_player, "volume_db", 0.0, duration)

    await tween.finished
    _current_player.stop()

    # Swap references
    var temp := _current_player
    _current_player = _next_player
    _next_player = temp
```

## Positional Audio (2D)

```gdscript
extends AudioStreamPlayer2D

@export var sound: AudioStream

func _ready() -> void:
    stream = sound
    max_distance = 500.0  # Fade to silence at this distance
    attenuation = 1.0     # Higher = faster falloff

func play_at(pos: Vector2) -> void:
    global_position = pos
    play()
```

## Positional Audio (3D)

```gdscript
extends AudioStreamPlayer3D

@export var sound: AudioStream

func _ready() -> void:
    stream = sound
    unit_size = 10.0      # Distance for full volume
    max_distance = 100.0  # Cutoff distance
    attenuation_model = ATTENUATION_INVERSE_DISTANCE

func play_at(pos: Vector3) -> void:
    global_position = pos
    play()
```

## Volume Control

```gdscript
# Volume is in decibels (-80 to 0+ range)
# Convert from linear (0.0 to 1.0):
player.volume_db = linear_to_db(0.5)  # 50% volume

# Convert to linear for UI sliders:
var linear_volume := db_to_linear(player.volume_db)
```

## Audio Properties Reference

| Property | Description |
|----------|-------------|
| `stream` | AudioStream resource to play |
| `volume_db` | Volume in decibels (0 = full, -80 = silent) |
| `pitch_scale` | Playback speed (1.0 = normal) |
| `bus` | Audio bus name ("Master", "SFX", etc.) |
| `playing` | Is currently playing (read-only) |
| `autoplay` | Start playing on ready |
| `stream_paused` | Pause without stopping |

### AudioStreamPlayer2D/3D Additional

| Property | Description |
|----------|-------------|
| `max_distance` | Distance where sound fades to silence |
| `attenuation` | Falloff rate (higher = faster) |
| `panning_strength` | Stereo panning amount (2D) |
