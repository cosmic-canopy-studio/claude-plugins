---
class: AudioStreamPlayer2D
category: audio
complexity: basic
godot_version: "4.x"
---

# AudioStreamPlayer2D

**Inherits:** Node2D < CanvasItem < Node < Object

Plays positional sound in 2D space.

## Description

AudioStreamPlayer2D plays audio that is attenuated with distance to the listener. By default, audio is heard from the screen center unless an AudioListener2D is added and activated.

For non-positional audio, use AudioStreamPlayer instead.

**Note:** Hiding an AudioStreamPlayer2D does not disable audio. To disable, set `volume_db` to a very low value like `-100`.

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
| `max_distance` | float | `2000.0` | Maximum hearable distance |
| `attenuation` | float | `1.0` | Distance attenuation exponent |
| `panning_strength` | float | `1.0` | Stereo panning strength multiplier |

## System Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `bus` | StringName | `"Master"` | Audio bus for playback |
| `max_polyphony` | int | `1` | Max simultaneous sounds |
| `area_mask` | int | `1` | Which Area2D layers affect audio |

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

```gdscript
audio_player.stop()
```

### seek(to_position: float)

Sets playback position in seconds.

```gdscript
# Jump to 5 seconds into the track
audio_player.seek(5.0)
```

### get_playback_position() -> float

Returns current position in the AudioStream in seconds.

```gdscript
var current_time: float = audio_player.get_playback_position()
print("Playing at: ", current_time, " seconds")
```

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

### Basic Positional Sound

```gdscript
extends Node2D

@onready var audio_player: AudioStreamPlayer2D = $AudioStreamPlayer2D

func _ready() -> void:
    # Load and play a sound
    audio_player.stream = preload("res://sounds/explosion.wav")
    audio_player.play()
```

### Distance-Based Volume

```gdscript
# Configure distance attenuation
audio_player.max_distance = 1000.0  # Audible up to 1000 pixels
audio_player.attenuation = 2.0      # Quadratic falloff (realistic)
```

### Looping Background Music

```gdscript
# Use an AudioStreamOggVorbis with loop enabled in import settings
audio_player.stream = preload("res://music/background.ogg")
audio_player.autoplay = true
```

### One-Shot Sound Effects

```gdscript
func play_sound_at_position(sound: AudioStream, pos: Vector2) -> void:
    var audio: AudioStreamPlayer2D = AudioStreamPlayer2D.new()
    add_child(audio)
    audio.stream = sound
    audio.global_position = pos
    audio.finished.connect(audio.queue_free)
    audio.play()
```

### Polyphony for Repeated Sounds

```gdscript
# Allow up to 5 simultaneous instances (e.g., rapid gunfire)
audio_player.max_polyphony = 5
audio_player.stream = preload("res://sounds/gunshot.wav")

# Play() multiple times quickly - oldest sounds get cut off
audio_player.play()
audio_player.play()
audio_player.play()
```

### Pause and Resume

```gdscript
func pause_audio() -> void:
    audio_player.stream_paused = true

func resume_audio() -> void:
    audio_player.stream_paused = false
```

### Volume Control

```gdscript
# Using decibels (logarithmic, -80 to +6 typical range)
audio_player.volume_db = -10.0  # Quieter
audio_player.volume_db = 0.0    # Normal
audio_player.volume_db = 6.0    # Louder

# Using linear volume (0.0 to 1.0+)
audio_player.volume_linear = 0.5  # Half volume
audio_player.volume_linear = 1.0  # Full volume
```

## Attenuation Models

The `attenuation` property controls how volume decreases with distance:

| Value | Model | Description |
|-------|-------|-------------|
| `1.0` | Linear | Volume decreases linearly with distance |
| `2.0` | Quadratic | Realistic physical attenuation |
| `0.5` | Root | Slower falloff, audible at greater distance |
| `3.0+` | Steep | Very rapid falloff |

```gdscript
# Realistic distance attenuation (inverse square law)
audio_player.attenuation = 2.0

# Slower falloff for ambient sounds
audio_player.attenuation = 0.5

# Rapid falloff for close-range effects
audio_player.attenuation = 3.0
```

## Panning Strength

Controls left-right stereo panning based on listener position:

```gdscript
# Strong panning (default) - clear directional audio
audio_player.panning_strength = 1.0

# Weaker panning - less dramatic stereo effect
audio_player.panning_strength = 0.5

# No panning - same volume in both channels
audio_player.panning_strength = 0.0
```

## Audio Buses

Route audio through different buses for effects or volume control:

```gdscript
# Use the "SFX" bus (must exist in Audio Bus settings)
audio_player.bus = "SFX"

# Use the "Music" bus
audio_player.bus = "Music"
```

## Area2D Integration

Use `area_mask` to make Area2D nodes affect audio (e.g., reverb zones):

```gdscript
# Only affected by Area2D on layer 1
audio_player.area_mask = 1

# Affected by Area2D on layers 1 and 3
audio_player.area_mask = 0b101  # Binary: 5

# Example Area2D setup for "water" reverb:
# 1. Create Area2D on layer 2
# 2. Set AudioStreamPlayer2D.area_mask = 2
# 3. Area2D redirects audio to "Underwater" bus with reverb
```

## Best Practices

### Performance

- Use `max_polyphony` to limit simultaneous sounds
- Set appropriate `max_distance` to avoid processing distant inaudible sounds
- Pool AudioStreamPlayer2D nodes for frequent sound effects
- Use compressed formats (Ogg Vorbis) for music, WAV for short effects

### Audio Formats

- **WAV**: Best for short sound effects, uncompressed
- **Ogg Vorbis**: Best for music and longer sounds, compressed
- **MP3**: Supported but Ogg Vorbis preferred for licensing

### Listener Setup

```gdscript
# By default, camera is the listener
# To use custom listener:
var listener: AudioListener2D = AudioListener2D.new()
add_child(listener)
listener.make_current()
```

### Volume Ranges

- Decibels: `-80.0` (silent) to `6.0` (louder than source)
- `0.0 dB` = original volume
- `-80.0 dB` = effectively muted
- Each `-6 dB` ≈ half volume
- Each `+6 dB` ≈ double volume

## Common Pitfalls

1. **Not setting max_distance** - Sound can be heard from anywhere by default if distance is too high
2. **Using play() in a loop** - Use `playing` check or `finished` signal to avoid restarting
3. **Expecting instant playback** - play() queues for next physics frame
4. **Hiding node to mute** - Use `volume_db = -80.0` or `stop()` instead
5. **Wrong bus name** - Falls back to "Master" silently if bus doesn't exist

## Playback State Checks

```gdscript
# Check if currently playing
if audio_player.playing:
    print("Audio is playing")

# Check if paused
if audio_player.stream_paused:
    print("Audio is paused")

# Get stream duration (if available)
if audio_player.stream:
    var length: float = audio_player.stream.get_length()
    print("Stream length: ", length, " seconds")
```

## Related Classes

- **AudioStreamPlayer** - Non-positional audio playback
- **AudioStreamPlayer3D** - Positional audio in 3D
- **AudioListener2D** - Custom audio listener position
- **AudioServer** - Global audio system management
- **AudioStream** - Base class for audio resources

## Common AudioStream Types

- **AudioStreamWAV** - Uncompressed wave files
- **AudioStreamOggVorbis** - Compressed ogg files
- **AudioStreamMP3** - MP3 files
- **AudioStreamGenerator** - Procedural audio generation
- **AudioStreamRandomizer** - Random selection from pool

## Official Resources

- [Audio Streams Tutorial](https://docs.godotengine.org/en/stable/tutorials/audio/audio_streams.html)
- [AudioServer API](https://docs.godotengine.org/en/stable/classes/class_audioserver.html)
