# Audio Systems Dispatcher

Routes to patterns for audio and music in Godot 4.

## Sound Effects

| I want to... | Go to |
|--------------|-------|
| Play one-shot sound | `reference/audio/players.md#one-shot` |
| Sound with variations | `reference/audio/players.md#random-pitch` |
| Pool sounds (many at once) | `reference/audio/players.md#pool` |
| Footstep sounds | `reference/audio/players.md#footsteps` |
| UI click sounds | `reference/audio/players.md#ui-sounds` |

## Music

| I want to... | Go to |
|--------------|-------|
| Background music loop | `reference/audio/music.md#loop` |
| Crossfade between tracks | `reference/audio/music.md#crossfade` |
| Music transitions | `reference/audio/music.md#transitions` |
| Adaptive/dynamic music | `reference/audio/music.md#adaptive` |
| Music layers | `reference/audio/music.md#layers` |

## Spatial Audio (2D/3D)

| I want to... | Go to |
|--------------|-------|
| Positional sound (2D) | `reference/audio/spatial.md#2d` |
| Positional sound (3D) | `reference/audio/spatial.md#3d` |
| Distance attenuation | `reference/audio/spatial.md#attenuation` |
| Doppler effect | `reference/audio/spatial.md#doppler` |
| Audio listener | `reference/audio/spatial.md#listener` |

## Audio Buses

| I want to... | Go to |
|--------------|-------|
| Create audio buses | `reference/audio/buses.md#create` |
| Master/Music/SFX buses | `reference/audio/buses.md#standard-layout` |
| Volume control | `reference/audio/buses.md#volume` |
| Mute/unmute buses | `reference/audio/buses.md#mute` |
| Audio effects (reverb, etc) | `reference/audio/buses.md#effects` |

## Settings & Persistence

| I want to... | Go to |
|--------------|-------|
| Volume sliders in settings | `reference/audio/settings.md#sliders` |
| Save/load audio settings | `reference/audio/settings.md#persistence` |
| Mute toggle | `reference/audio/settings.md#mute-toggle` |

## Quick Start: Sound Manager Autoload

```gdscript
# audio_manager.gd - Add as Autoload
extends Node

var music_player: AudioStreamPlayer
var sfx_players: Array[AudioStreamPlayer] = []
const SFX_POOL_SIZE := 8

func _ready() -> void:
    # Create music player
    music_player = AudioStreamPlayer.new()
    music_player.bus = "Music"
    add_child(music_player)

    # Create SFX pool
    for i in SFX_POOL_SIZE:
        var player := AudioStreamPlayer.new()
        player.bus = "SFX"
        add_child(player)
        sfx_players.append(player)

func play_music(stream: AudioStream, fade_in: float = 0.5) -> void:
    if fade_in > 0:
        var tween := create_tween()
        tween.tween_property(music_player, "volume_db", -80.0, fade_in * 0.5)
        await tween.finished

    music_player.stream = stream
    music_player.volume_db = -80.0
    music_player.play()

    if fade_in > 0:
        var tween := create_tween()
        tween.tween_property(music_player, "volume_db", 0.0, fade_in * 0.5)

func play_sfx(stream: AudioStream, pitch_variation: float = 0.0) -> void:
    for player in sfx_players:
        if not player.playing:
            player.stream = stream
            player.pitch_scale = 1.0 + randf_range(-pitch_variation, pitch_variation)
            player.play()
            return
    # All players busy - use first one
    sfx_players[0].stream = stream
    sfx_players[0].play()

func set_bus_volume(bus_name: String, linear_volume: float) -> void:
    var bus_idx := AudioServer.get_bus_index(bus_name)
    AudioServer.set_bus_volume_db(bus_idx, linear_to_db(linear_volume))

func set_bus_mute(bus_name: String, muted: bool) -> void:
    var bus_idx := AudioServer.get_bus_index(bus_name)
    AudioServer.set_bus_mute(bus_idx, muted)
```

**Usage:**
```gdscript
# Play music
AudioManager.play_music(preload("res://audio/music/battle.ogg"))

# Play sound effect with pitch variation
AudioManager.play_sfx(preload("res://audio/sfx/hit.wav"), 0.1)

# Set volumes (0.0 to 1.0)
AudioManager.set_bus_volume("Music", 0.8)
AudioManager.set_bus_volume("SFX", 1.0)
```

## Quick Start: Audio Bus Layout

Create `default_bus_layout.tres`:
```
Master
├── Music (for background music)
├── SFX (for sound effects)
└── UI (for interface sounds)
```

**Project Settings:** Audio > Default Bus Layout > Select your layout file.

## Quick Start: Positional Audio (2D)

```gdscript
extends AudioStreamPlayer2D

@export var sound: AudioStream
@export var max_distance: float = 500.0

func _ready() -> void:
    stream = sound
    max_distance = max_distance

func play_at_position(pos: Vector2) -> void:
    global_position = pos
    play()
```

**AudioStreamPlayer2D Properties:**
- `max_distance` - Sound fades to silence at this distance
- `attenuation` - How quickly sound fades (higher = faster)
- `panning_strength` - How much stereo panning based on position
