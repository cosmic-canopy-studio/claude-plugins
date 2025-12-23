---
topic: audio-buses
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/stable/classes/class_audioserver.html
  - https://docs.godotengine.org/en/stable/tutorials/audio/audio_buses.html
  - https://www.gdquest.com/tutorial/godot/audio/volume-slider/
  - https://shaggydev.com/2023/05/22/volume-sliders/
  - https://gamedevartisan.com/tutorials/godot-fundamentals/audio-and-ui-controls
  - repos/godot_node_essentials/default_bus_layout.tres
  - repos/godot_node_essentials/screens/audio_stream_player/
---

# Audio Bus System

AudioServer manages audio buses for mixing, routing, and applying effects to audio.

## What Are Audio Buses? {#concept}

Audio buses are mixing channels that group and process audio. All audio in Godot flows through the bus system:

- **Master Bus**: Default bus where all audio routes (cannot be deleted)
- **Custom Buses**: Create separate channels for Music, SFX, UI, Voice, etc.
- **Bus Hierarchy**: Buses can send to other buses, creating a mix tree
- **Effects Chain**: Each bus can have multiple audio effects applied in order

**Common Setup:**
```
Master
├── Music
├── SFX
│   ├── PlayerSFX
│   └── EnemySFX
├── UI
└── Voice
```

## Basic Bus Operations {#operations}

### Get Bus Index

Buses are accessed by index, not name. Cache the index for performance:

```gdscript
extends Node

var music_bus_index: int
var sfx_bus_index: int

func _ready() -> void:
    music_bus_index = AudioServer.get_bus_index("Music")
    sfx_bus_index = AudioServer.get_bus_index("SFX")
```

### Set Audio Player Bus

Assign audio players to specific buses:

```gdscript
@onready var music_player: AudioStreamPlayer = $MusicPlayer
@onready var sfx_player: AudioStreamPlayer = $SFXPlayer

func _ready() -> void:
    music_player.bus = "Music"
    sfx_player.bus = "SFX"
```

### Create Buses at Runtime

```gdscript
func setup_audio_buses() -> void:
    # Add new buses (count starts at 1, Master is 0)
    var bus_count: int = AudioServer.bus_count
    AudioServer.add_bus(bus_count)
    AudioServer.set_bus_name(bus_count, "Music")

    AudioServer.add_bus(bus_count + 1)
    AudioServer.set_bus_name(bus_count + 1, "SFX")
```

## Volume Control {#volume}

### Understanding Audio Volume

- **Decibels (dB)**: Logarithmic scale, 0 dB = full volume, -80 dB = silent
- **Linear Scale**: 0.0 to 1.0 range used by UI sliders
- **Perception**: Volume doubles every +3 dB, halves every -3 dB

### Set Bus Volume

```gdscript
extends Node

var music_bus: int

func _ready() -> void:
    music_bus = AudioServer.get_bus_index("Music")

    # Set volume in decibels
    AudioServer.set_bus_volume_db(music_bus, -10.0)  # Quieter
    AudioServer.set_bus_volume_db(music_bus, 0.0)    # Full volume
    AudioServer.set_bus_volume_db(music_bus, 6.0)    # Boosted

func get_volume() -> float:
    return AudioServer.get_bus_volume_db(music_bus)
```

### Volume Slider Integration

Create intuitive volume controls using linear-to-dB conversion:

```gdscript
extends HSlider

@export var bus_name: String = "Master"

var bus_index: int

func _ready() -> void:
    # Configure slider
    min_value = 0.0
    max_value = 1.0
    step = 0.01

    # Get bus index
    bus_index = AudioServer.get_bus_index(bus_name)

    # Initialize slider to current volume
    value = db_to_linear(AudioServer.get_bus_volume_db(bus_index))

    # Connect signal
    value_changed.connect(_on_value_changed)

func _on_value_changed(linear_value: float) -> void:
    # Convert linear slider value to decibels
    AudioServer.set_bus_volume_db(bus_index, linear_to_db(linear_value))

    # Mute if too quiet (prevents distortion at very low volumes)
    AudioServer.set_bus_mute(bus_index, linear_value < 0.05)
```

### Complete Settings Menu Example

```gdscript
extends Control

@onready var music_slider: HSlider = %MusicSlider
@onready var sfx_slider: HSlider = %SFXSlider
@onready var music_label: Label = %MusicLabel
@onready var sfx_label: Label = %SFXLabel

var music_bus: int
var sfx_bus: int

func _ready() -> void:
    # Get bus indices
    music_bus = AudioServer.get_bus_index("Music")
    sfx_bus = AudioServer.get_bus_index("SFX")

    # Initialize sliders
    music_slider.value = db_to_linear(AudioServer.get_bus_volume_db(music_bus))
    sfx_slider.value = db_to_linear(AudioServer.get_bus_volume_db(sfx_bus))

    # Connect signals
    music_slider.value_changed.connect(_on_music_changed)
    sfx_slider.value_changed.connect(_on_sfx_changed)

    # Update labels
    _update_labels()

func _on_music_changed(value: float) -> void:
    AudioServer.set_bus_volume_db(music_bus, linear_to_db(value))
    AudioServer.set_bus_mute(music_bus, value < 0.05)
    _update_labels()

func _on_sfx_changed(value: float) -> void:
    AudioServer.set_bus_volume_db(sfx_bus, linear_to_db(value))
    AudioServer.set_bus_mute(sfx_bus, value < 0.05)
    _update_labels()

func _update_labels() -> void:
    music_label.text = "Music: %d%%" % int(music_slider.value * 100)
    sfx_label.text = "SFX: %d%%" % int(sfx_slider.value * 100)
```

## Muting and Soloing {#mute-solo}

### Mute Bus

Silence a bus without changing volume:

```gdscript
func toggle_music(enabled: bool) -> void:
    var music_bus: int = AudioServer.get_bus_index("Music")
    AudioServer.set_bus_mute(music_bus, not enabled)

func is_music_playing() -> bool:
    var music_bus: int = AudioServer.get_bus_index("Music")
    return not AudioServer.is_bus_mute(music_bus)
```

### Solo Bus

Play only one bus (mutes all others):

```gdscript
func solo_voice_chat() -> void:
    var voice_bus: int = AudioServer.get_bus_index("Voice")
    AudioServer.set_bus_solo(voice_bus, true)

func unsolo_all() -> void:
    for i in AudioServer.bus_count:
        AudioServer.set_bus_solo(i, false)
```

## Audio Effects {#effects}

### Add Effect to Bus

```gdscript
func add_reverb_to_music() -> void:
    var music_bus: int = AudioServer.get_bus_index("Music")

    # Create effect
    var reverb := AudioEffectReverb.new()
    reverb.room_size = 0.6
    reverb.damping = 0.5
    reverb.wet = 0.3

    # Add to bus (index 0 = first effect)
    AudioServer.add_bus_effect(music_bus, reverb, 0)
```

### Access Existing Effect

```gdscript
# Get reference to effect on bus
var record_bus: int = AudioServer.get_bus_index("Record")
var record_effect: AudioEffectRecord = AudioServer.get_bus_effect(record_bus, 0)

func start_recording() -> void:
    record_effect.set_recording_active(true)

func stop_recording() -> AudioStreamWAV:
    var recording: AudioStreamWAV = record_effect.get_recording()
    record_effect.set_recording_active(false)
    return recording
```

### Enable/Disable Effects

```gdscript
func toggle_underwater_effect(underwater: bool) -> void:
    var sfx_bus: int = AudioServer.get_bus_index("SFX")

    # Effect at index 0 is a low-pass filter
    AudioServer.set_bus_effect_enabled(sfx_bus, 0, underwater)
```

### Bypass All Effects

```gdscript
func set_low_quality_mode(enabled: bool) -> void:
    var music_bus: int = AudioServer.get_bus_index("Music")
    AudioServer.set_bus_bypass_effects(music_bus, enabled)
```

## Bus Routing {#routing}

### Set Bus Send Target

Route bus output to a different bus:

```gdscript
func setup_bus_routing() -> void:
    # SFX bus sends to Master
    var sfx_bus: int = AudioServer.get_bus_index("SFX")
    AudioServer.set_bus_send(sfx_bus, "Master")

    # Voice bus sends to SFX (for shared processing)
    var voice_bus: int = AudioServer.get_bus_index("Voice")
    AudioServer.set_bus_send(voice_bus, "SFX")
```

### Environment-Based Routing

Use Area2D/Area3D to override audio bus for environmental effects:

```gdscript
# In scene (environment_effects_2d.tscn example):
# WaterArea2D has these properties set:
#   audio_bus_override = true
#   audio_bus_name = "Water"

# When player enters water area, their audio automatically
# routes through "Water" bus which has low-pass filter
```

Scene setup:
```gdscript
# This is done in scene inspector, not code:
# Area2D properties:
var water_area := Area2D.new()
water_area.audio_bus_override = true
water_area.audio_bus_name = "Water"

# AudioStreamPlayer2D playing near water will use Water bus
var player := AudioStreamPlayer2D.new()
player.area_mask = 8  # Layer that water area is on
```

## Bus Layout Files {#layout}

### Save/Load Bus Configuration

```gdscript
func save_bus_layout() -> void:
    # Save current bus configuration
    AudioServer.save_bus_layout("user://audio_bus_layout.tres")

func load_bus_layout() -> void:
    # Load saved configuration
    var layout: AudioBusLayout = load("user://audio_bus_layout.tres")
    AudioServer.set_bus_layout(layout)
```

### Default Bus Layout Example

```gdscript
# default_bus_layout.tres
# Created in Godot Editor (Audio tab at bottom)
# Defines buses that load with project:

[gd_resource type="AudioBusLayout" load_steps=4 format=3]

[sub_resource type="AudioEffectLowPassFilter" id="1"]
cutoff_hz = 540.0
resonance = 0.25

[sub_resource type="AudioEffectReverb" id="2"]
room_size = 0.48

[resource]
bus/1/name = "Water"
bus/1/solo = false
bus/1/mute = false
bus/1/volume_db = 0.0
bus/1/send = "Master"
bus/1/effect/0/effect = SubResource("1")
bus/1/effect/1/effect = SubResource("2")
```

## Common Patterns {#patterns}

### Audio Manager Autoload

```gdscript
# audio_manager.gd (autoload)
extends Node

var master_bus: int
var music_bus: int
var sfx_bus: int
var ui_bus: int

func _ready() -> void:
    # Cache bus indices
    master_bus = AudioServer.get_bus_index("Master")
    music_bus = AudioServer.get_bus_index("Music")
    sfx_bus = AudioServer.get_bus_index("SFX")
    ui_bus = AudioServer.get_bus_index("UI")

    # Load saved volumes
    load_volume_settings()

func set_master_volume(linear_value: float) -> void:
    AudioServer.set_bus_volume_db(master_bus, linear_to_db(linear_value))

func set_music_volume(linear_value: float) -> void:
    AudioServer.set_bus_volume_db(music_bus, linear_to_db(linear_value))
    AudioServer.set_bus_mute(music_bus, linear_value < 0.05)

func set_sfx_volume(linear_value: float) -> void:
    AudioServer.set_bus_volume_db(sfx_bus, linear_to_db(linear_value))
    AudioServer.set_bus_mute(sfx_bus, linear_value < 0.05)

func save_volume_settings() -> void:
    var config := ConfigFile.new()
    config.set_value("audio", "master", db_to_linear(AudioServer.get_bus_volume_db(master_bus)))
    config.set_value("audio", "music", db_to_linear(AudioServer.get_bus_volume_db(music_bus)))
    config.set_value("audio", "sfx", db_to_linear(AudioServer.get_bus_volume_db(sfx_bus)))
    config.save("user://settings.cfg")

func load_volume_settings() -> void:
    var config := ConfigFile.new()
    if config.load("user://settings.cfg") == OK:
        set_master_volume(config.get_value("audio", "master", 1.0))
        set_music_volume(config.get_value("audio", "music", 0.8))
        set_sfx_volume(config.get_value("audio", "sfx", 1.0))
```

### Ducking (Lower Music During Voice)

```gdscript
extends Node

var music_bus: int
var original_music_volume: float

func _ready() -> void:
    music_bus = AudioServer.get_bus_index("Music")
    original_music_volume = AudioServer.get_bus_volume_db(music_bus)

func start_dialogue() -> void:
    # Lower music volume during dialogue
    var tween := create_tween()
    tween.tween_method(
        func(db: float) -> void: AudioServer.set_bus_volume_db(music_bus, db),
        original_music_volume,
        original_music_volume - 15.0,  # -15 dB quieter
        0.5
    )

func end_dialogue() -> void:
    # Restore music volume
    var tween := create_tween()
    tween.tween_method(
        func(db: float) -> void: AudioServer.set_bus_volume_db(music_bus, db),
        AudioServer.get_bus_volume_db(music_bus),
        original_music_volume,
        0.5
    )
```

### Dynamic Effect Control

```gdscript
extends Node

var sfx_bus: int
var lowpass_index: int = 0

func _ready() -> void:
    sfx_bus = AudioServer.get_bus_index("SFX")

func enter_underwater() -> void:
    # Enable low-pass filter
    AudioServer.set_bus_effect_enabled(sfx_bus, lowpass_index, true)

    # Adjust cutoff frequency
    var effect: AudioEffectLowPassFilter = AudioServer.get_bus_effect(sfx_bus, lowpass_index)
    effect.cutoff_hz = 400.0
    effect.resonance = 0.5

func exit_underwater() -> void:
    AudioServer.set_bus_effect_enabled(sfx_bus, lowpass_index, false)
```

## AudioServer API Reference {#api}

### Bus Management

| Method | Description |
|--------|-------------|
| `get_bus_count() -> int` | Get total number of buses |
| `add_bus(at_position: int = -1)` | Add new bus at position |
| `remove_bus(index: int)` | Remove bus (cannot remove Master) |
| `get_bus_index(name: String) -> int` | Get bus index by name |
| `get_bus_name(index: int) -> String` | Get bus name by index |
| `set_bus_name(index: int, name: String)` | Rename bus |
| `move_bus(index: int, to_index: int)` | Reorder buses |

### Volume and Muting

| Method | Description |
|--------|-------------|
| `set_bus_volume_db(index: int, db: float)` | Set volume in decibels |
| `get_bus_volume_db(index: int) -> float` | Get volume in decibels |
| `set_bus_mute(index: int, enable: bool)` | Mute/unmute bus |
| `is_bus_mute(index: int) -> bool` | Check if bus is muted |
| `set_bus_solo(index: int, enable: bool)` | Solo bus (mute others) |
| `is_bus_solo(index: int) -> bool` | Check if bus is soloed |

### Effects

| Method | Description |
|--------|-------------|
| `add_bus_effect(index: int, effect: AudioEffect, position: int = -1)` | Add effect to bus |
| `remove_bus_effect(index: int, effect_idx: int)` | Remove effect from bus |
| `get_bus_effect(index: int, effect_idx: int) -> AudioEffect` | Get effect instance |
| `get_bus_effect_count(index: int) -> int` | Number of effects on bus |
| `set_bus_effect_enabled(index: int, effect_idx: int, enabled: bool)` | Enable/disable effect |
| `is_bus_effect_enabled(index: int, effect_idx: int) -> bool` | Check if effect enabled |
| `set_bus_bypass_effects(index: int, enable: bool)` | Bypass all effects on bus |
| `is_bus_bypassing_effects(index: int) -> bool` | Check if effects bypassed |
| `swap_bus_effects(index: int, effect_idx1: int, effect_idx2: int)` | Reorder effects |

### Routing

| Method | Description |
|--------|-------------|
| `set_bus_send(index: int, send: StringName)` | Set which bus this sends to |
| `get_bus_send(index: int) -> StringName` | Get send target bus name |

### Layout

| Method | Description |
|--------|-------------|
| `set_bus_layout(layout: AudioBusLayout)` | Load bus configuration |
| `generate_bus_layout() -> AudioBusLayout` | Create layout from current state |

### Utility Functions

| Function | Description |
|----------|-------------|
| `linear_to_db(linear: float) -> float` | Convert 0-1 range to decibels |
| `db_to_linear(db: float) -> float` | Convert decibels to 0-1 range |

## Best Practices {#best-practices}

### Volume Control
- Always use `linear_to_db()` when converting slider values
- Mute buses when volume < 0.05 to prevent distortion
- Use tweens for smooth volume transitions

### Bus Organization
- Create buses in editor (Audio tab) for project-wide setup
- Use hierarchy: Master > Category > Subcategory
- Common buses: Master, Music, SFX, UI, Voice

### Performance
- Cache bus indices in `_ready()` - don't call `get_bus_index()` repeatedly
- Disable unused effects instead of removing them
- Use bus bypassing for quality settings

### Effects
- Order matters: compression before reverb, EQ before effects
- Test effects with different audio sources
- Use subtle settings - over-processing sounds unnatural

### Persistence
- Save user volume preferences with ConfigFile
- Don't save bus layout at runtime unless customization allowed
- Restore volumes in autoload's `_ready()`

## Common Pitfalls {#pitfalls}

### Volume Issues
- **Forgetting conversion**: Using linear values directly results in incorrect volume
- **No mute threshold**: Very low volumes cause audio artifacts
- **Clipping**: Multiple loud buses can exceed 0 dB and distort

### Bus Access
- **Assuming order**: Bus indices can change, always use `get_bus_index()`
- **Missing buses**: Check bus exists before accessing (returns -1 if not found)
- **Race conditions**: Access buses after scene tree ready

### Effect Problems
- **Wrong effect index**: Effects are 0-indexed, check count first
- **Type casting**: `get_bus_effect()` returns AudioEffect, cast to specific type
- **Bypass vs disable**: Bypass affects all effects, disable affects one

## Related Patterns {#related}

- [Audio Players](/home/sam/code/godot_advisor/.claude/skills/godot/reference/audio/players.md) - Playing sounds through buses
- [Spatial Audio](/home/sam/code/godot_advisor/.claude/skills/godot/reference/audio/spatial.md) - 2D/3D positional audio
- [Autoloads](/home/sam/code/godot_advisor/.claude/skills/godot/reference/patterns/autoloads.md) - Audio manager singleton
- [Save/Load](/home/sam/code/godot_advisor/.claude/skills/godot/reference/patterns/save-load.md) - Persisting volume settings
