---
class: AudioStreamPlayer3D
category: audio
complexity: intermediate
godot_version: "4.x"
---

# AudioStreamPlayer3D

**Inherits:** Node3D < Node < Object

Plays positional sound in 3D space.

## Description

AudioStreamPlayer3D plays audio with positional sound effects including distance attenuation, directionality, and the Doppler effect. A low-pass filter is applied to distant sounds for realism (disable by setting `attenuation_filter_cutoff_hz` to `20500`).

By default, audio is heard from the camera position unless an AudioListener3D is added and activated.

For non-positional audio, use AudioStreamPlayer instead.

**Note:** Hiding an AudioStreamPlayer3D does not disable audio. To disable, set `volume_db` to a very low value like `-100`.

## Core Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `stream` | AudioStream | `null` | The audio stream to play |
| `volume_db` | float | `0.0` | Base volume in decibels |
| `pitch_scale` | float | `1.0` | Pitch and tempo multiplier |
| `playing` | bool | `false` | Whether audio is playing/queued |
| `autoplay` | bool | `false` | Play when added to scene tree |
| `stream_paused` | bool | `false` | Whether playback is paused |

## Spatial Audio Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `unit_size` | float | `10.0` | Attenuation effect factor |
| `max_distance` | float | `0.0` | Distance where sound is inaudible (`0` = no limit) |
| `max_db` | float | `3.0` | Absolute maximum sound level (dB) |
| `attenuation_model` | enum | `ATTENUATION_INVERSE_DISTANCE` | How volume decreases with distance |
| `panning_strength` | float | `1.0` | Stereo panning strength multiplier |

## Attenuation Models

| Constant | Value | Description |
|----------|-------|-------------|
| `ATTENUATION_INVERSE_DISTANCE` | `0` | Linear distance attenuation |
| `ATTENUATION_INVERSE_SQUARE_DISTANCE` | `1` | Squared distance (realistic) |
| `ATTENUATION_LOGARITHMIC` | `2` | Logarithmic distance |
| `ATTENUATION_DISABLED` | `3` | No attenuation (still positional) |

## Distance Filter Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `attenuation_filter_cutoff_hz` | float | `5000.0` | Low-pass filter cutoff frequency |
| `attenuation_filter_db` | float | `-24.0` | Filter loudness effect (dB) |

## Directional Audio Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `emission_angle_enabled` | bool | `false` | Enable directional attenuation |
| `emission_angle_degrees` | float | `45.0` | Cone angle for unattenuated audio |
| `emission_angle_filter_attenuation_db` | float | `-12.0` | Attenuation outside cone (dB) |

## Doppler Effect Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `doppler_tracking` | enum | `DOPPLER_TRACKING_DISABLED` | When to calculate Doppler |

### Doppler Tracking Modes

| Constant | Value | Description |
|----------|-------|-------------|
| `DOPPLER_TRACKING_DISABLED` | `0` | No Doppler effect |
| `DOPPLER_TRACKING_IDLE_STEP` | `1` | Calculate during process frames |
| `DOPPLER_TRACKING_PHYSICS_STEP` | `2` | Calculate during physics frames |

## System Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `bus` | StringName | `"Master"` | Audio bus for playback |
| `max_polyphony` | int | `1` | Max simultaneous sounds |
| `area_mask` | int | `1` | Which Area3D layers affect audio |

## Essential Methods

### play(from_position: float = 0.0)

Queues audio to play on next physics frame from given position (in seconds).

```gdscript
# Play from beginning
audio_player.play()

# Play from 2.5 seconds in
audio_player.play(2.5)
```

### stop()

Stops the audio immediately.

### seek(to_position: float)

Sets playback position in seconds.

### get_playback_position() -> float

Returns current position in the AudioStream in seconds.

## Signals

### finished()

Emitted when audio stops playing.

```gdscript
func _ready() -> void:
    audio_player.finished.connect(_on_audio_finished)

func _on_audio_finished() -> void:
    print("Audio playback completed")
```

## Common Patterns

### Basic 3D Positional Sound

```gdscript
extends Node3D

@onready var audio_player: AudioStreamPlayer3D = $AudioStreamPlayer3D

func _ready() -> void:
    audio_player.stream = preload("res://sounds/explosion.wav")
    audio_player.unit_size = 10.0
    audio_player.max_distance = 100.0
    audio_player.play()
```

### Realistic Distance Attenuation

```gdscript
# Configure realistic sound falloff
audio_player.attenuation_model = AudioStreamPlayer3D.ATTENUATION_INVERSE_SQUARE_DISTANCE
audio_player.unit_size = 10.0     # Scale factor for attenuation
audio_player.max_distance = 50.0  # Silent beyond 50 units
```

### Directional Audio (e.g., Speaker, Megaphone)

```gdscript
# Sound is loudest when listener is in front
audio_player.emission_angle_enabled = true
audio_player.emission_angle_degrees = 60.0  # 60-degree cone
audio_player.emission_angle_filter_attenuation_db = -20.0  # Very quiet outside cone

# Point the Node3D in the direction of emission
audio_player.look_at(target_position)
```

### Doppler Effect for Moving Objects

```gdscript
# Enable Doppler for moving sound sources (vehicles, projectiles)
audio_player.doppler_tracking = AudioStreamPlayer3D.DOPPLER_TRACKING_PHYSICS_STEP

# Also enable on Camera3D or AudioListener3D for accurate effect
camera.doppler_tracking = Camera3D.DOPPLER_TRACKING_PHYSICS_STEP
```

### Distance Filter Configuration

```gdscript
# Strong low-pass filter for distant sounds (realistic)
audio_player.attenuation_filter_cutoff_hz = 3000.0  # Lower = more muffled
audio_player.attenuation_filter_db = -30.0          # Stronger effect

# Disable distance filtering
audio_player.attenuation_filter_cutoff_hz = 20500.0  # Above human hearing
```

### One-Shot 3D Sound Effects

```gdscript
func play_sound_at_position(sound: AudioStream, pos: Vector3) -> void:
    var audio: AudioStreamPlayer3D = AudioStreamPlayer3D.new()
    add_child(audio)
    audio.stream = sound
    audio.global_position = pos
    audio.finished.connect(audio.queue_free)
    audio.play()
```

### Ambient Sound with Large Range

```gdscript
# Large area ambient sound (wind, ocean)
audio_player.attenuation_model = AudioStreamPlayer3D.ATTENUATION_LOGARITHMIC
audio_player.unit_size = 50.0
audio_player.max_distance = 500.0
audio_player.attenuation_filter_cutoff_hz = 20500.0  # No filtering
```

## Attenuation Model Comparison

### ATTENUATION_INVERSE_DISTANCE (Linear)
- Volume decreases linearly with distance
- Simplest model
- Use for: Simple games, stylized audio

```gdscript
audio_player.attenuation_model = AudioStreamPlayer3D.ATTENUATION_INVERSE_DISTANCE
audio_player.unit_size = 10.0
```

### ATTENUATION_INVERSE_SQUARE_DISTANCE (Realistic)
- Volume decreases with square of distance
- Matches real-world physics
- Use for: Realistic games, simulations

```gdscript
audio_player.attenuation_model = AudioStreamPlayer3D.ATTENUATION_INVERSE_SQUARE_DISTANCE
audio_player.unit_size = 10.0
```

### ATTENUATION_LOGARITHMIC
- Gentle falloff, audible over larger distances
- Use for: Ambient sounds, background audio

```gdscript
audio_player.attenuation_model = AudioStreamPlayer3D.ATTENUATION_LOGARITHMIC
audio_player.unit_size = 20.0
```

### ATTENUATION_DISABLED
- No volume attenuation
- Sound still positional (panning works)
- Can combine with `max_distance` for clamped linear attenuation
- Use for: UI sounds in 3D space, special effects

```gdscript
audio_player.attenuation_model = AudioStreamPlayer3D.ATTENUATION_DISABLED
audio_player.max_distance = 50.0  # Hard cutoff at 50 units
```

## Unit Size and Max Distance

The `unit_size` and `max_distance` work together:

- **unit_size**: Scales the attenuation curve (larger = audible farther)
- **max_distance**: Hard cutoff distance (0 = no limit, saves CPU)

```gdscript
# Small sound source (footstep)
audio_player.unit_size = 5.0
audio_player.max_distance = 25.0

# Medium sound source (door slam)
audio_player.unit_size = 10.0
audio_player.max_distance = 50.0

# Large sound source (explosion)
audio_player.unit_size = 30.0
audio_player.max_distance = 200.0
```

## Panning Configuration

Controls stereo and surround sound panning:

```gdscript
# Strong panning (default) - clear positional audio
audio_player.panning_strength = 1.0

# Weaker panning - less dramatic directional effect
audio_player.panning_strength = 0.5

# No panning - same volume in all channels (still has distance attenuation)
audio_player.panning_strength = 0.0
```

**Note:** Panning uses WebAudio standard for stereo and SPCAP algorithm for 5.1/7.1 surround.

## Doppler Effect Setup

Enable accurate Doppler effect:

```gdscript
# On sound source
audio_player.doppler_tracking = AudioStreamPlayer3D.DOPPLER_TRACKING_PHYSICS_STEP

# ALSO enable on camera/listener for accurate effect
camera.doppler_tracking = Camera3D.DOPPLER_TRACKING_PHYSICS_STEP
# OR
audio_listener.doppler_tracking = AudioListener3D.DOPPLER_TRACKING_PHYSICS_STEP
```

**Note:** Doppler requires BOTH source and listener to have tracking enabled.

## Volume Control

```gdscript
# Using decibels (logarithmic)
audio_player.volume_db = -10.0  # Quieter
audio_player.volume_db = 0.0    # Normal
audio_player.volume_db = 3.0    # Maximum (default max_db)

# Using linear volume (0.0 to 1.0+)
audio_player.volume_linear = 0.5  # Half volume
audio_player.volume_linear = 1.0  # Full volume

# Set maximum possible volume
audio_player.max_db = 6.0  # Allow louder sounds
```

## Best Practices

### Performance

- Set `max_distance` to avoid processing distant inaudible sounds
- Use `max_polyphony` to limit simultaneous sounds
- Pool AudioStreamPlayer3D nodes for frequent sound effects
- Use compressed formats (Ogg Vorbis) for longer sounds

### Realism

- Use `ATTENUATION_INVERSE_SQUARE_DISTANCE` for realistic physics
- Enable distance filtering for outdoor environments
- Use Doppler effect for fast-moving objects
- Set appropriate `unit_size` based on sound source size

### Listener Setup

```gdscript
# By default, camera is the listener
# To use custom listener:
var listener: AudioListener3D = AudioListener3D.new()
add_child(listener)
listener.make_current()
```

### Audio Formats

- **WAV**: Best for short sound effects
- **Ogg Vorbis**: Best for music and longer sounds
- **MP3**: Supported but Ogg Vorbis preferred

## Common Pitfalls

1. **Not setting max_distance** - Sound audible from entire level, wastes CPU
2. **Wrong attenuation model** - DISABLED when you wanted realistic falloff
3. **Forgetting Doppler on listener** - Doppler won't work correctly
4. **Unit size too small** - Sound inaudible even when close
5. **Hiding node to mute** - Use `volume_db = -80.0` or `stop()` instead

## Area3D Integration

Use `area_mask` to make Area3D nodes affect audio (e.g., reverb zones):

```gdscript
# Only affected by Area3D on layer 1
audio_player.area_mask = 1

# Affected by Area3D on layers 1 and 3
audio_player.area_mask = 0b101  # Binary: 5

# Example: underwater area redirects to "Underwater" bus with reverb
```

## Directional Emission Example

For a loudspeaker pointing forward:

```gdscript
extends Node3D

@onready var audio: AudioStreamPlayer3D = $AudioStreamPlayer3D

func _ready() -> void:
    # Enable cone emission
    audio.emission_angle_enabled = true
    audio.emission_angle_degrees = 45.0  # 45-degree forward cone
    audio.emission_angle_filter_attenuation_db = -15.0

    # Point forward (local -Z axis in Godot 3D)
    audio.rotation_degrees.x = 0

    audio.play()
```

## Related Classes

- **AudioStreamPlayer** - Non-positional audio playback
- **AudioStreamPlayer2D** - Positional audio in 2D
- **AudioListener3D** - Custom audio listener position
- **Camera3D** - Also acts as audio listener
- **AudioServer** - Global audio system management

## Official Resources

- [Audio Streams Tutorial](https://docs.godotengine.org/en/stable/tutorials/audio/audio_streams.html)
- [AudioServer API](https://docs.godotengine.org/en/stable/classes/class_audioserver.html)
