---
topic: spatial-audio
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/stable/classes/class_audiostreamplayer2d.html
  - https://docs.godotengine.org/en/4.1/classes/class_audiostreamplayer3d.html
  - https://github.com/godotengine/godot-proposals/issues/3551
  - https://github.com/godotengine/godot-proposals/issues/3384
  - repos/godot_node_essentials/screens/audio_stream_player/
status: complete
---

# Spatial Audio

Positional audio with distance attenuation, panning, and doppler effects.

## AudioStreamPlayer2D {#2d-basics}

Plays audio attenuated by distance to the listener. By default, audio is heard from the screen center. Add an `AudioListener2D` node to change the listening position.

### Basic Positional Sound

```gdscript
extends AudioStreamPlayer2D

@export var sound: AudioStream

func _ready() -> void:
    stream = sound
    max_distance = 500.0  # Fade to silence at this distance
    attenuation = 1.0     # Linear falloff (higher = faster)
    autoplay = true
```

### Dynamic Sound Position

Play sound at a specific position:

```gdscript
extends Node2D

@export var explosion_sound: AudioStream

func play_explosion(pos: Vector2) -> void:
    var player := AudioStreamPlayer2D.new()
    player.stream = explosion_sound
    player.max_distance = 800.0
    player.attenuation = 2.0  # Faster falloff
    player.bus = "SFX"
    add_child(player)
    player.global_position = pos
    player.play()
    player.finished.connect(player.queue_free)
```

## Distance-Based Footsteps (2D) {#footsteps-2d}

Footsteps that play different sounds based on tile data:

```gdscript
extends AudioStreamPlayer2D

const STEP_DISTANCE := 160.0

var _step_measure: float = 0.0

@onready var _player: CharacterBody2D = get_parent()
@onready var _tile_map_layer: TileMapLayer = %BaseTileMapLayer

func _physics_process(delta: float) -> void:
    # Accumulate step distance based on velocity
    _step_measure += _player.velocity.length() * delta

    # Play sound only after traveling a certain distance
    if _step_measure > STEP_DISTANCE:
        _play_footstep()
        _step_measure = 0.0

func _play_footstep() -> void:
    # Get tile at player position
    var tile_map_position := _tile_map_layer.local_to_map(_player.position)
    var tile_data := _tile_map_layer.get_cell_tile_data(tile_map_position)

    if tile_data != null:
        # Use custom data to determine footstep sound
        stream = tile_data.get_custom_data("Footstep")
        play()
```

## AudioStreamPlayer3D {#3d-basics}

Plays audio with 3D positional effects including distance attenuation, directionality, doppler effect, and low-pass filtering for distant sounds.

### Basic 3D Positional Sound

```gdscript
extends AudioStreamPlayer3D

@export var sound: AudioStream

func _ready() -> void:
    stream = sound
    unit_size = 10.0      # Distance for full volume
    max_distance = 100.0  # Cutoff distance (0 = unlimited)
    attenuation_model = ATTENUATION_INVERSE_DISTANCE
    autoplay = true
```

### One-Shot 3D Sound

```gdscript
extends Node3D

@export var impact_sound: AudioStream

func play_impact_at(pos: Vector3) -> void:
    var player := AudioStreamPlayer3D.new()
    player.stream = impact_sound
    player.unit_size = 5.0
    player.max_distance = 50.0
    player.bus = "SFX"
    add_child(player)
    player.global_position = pos
    player.play()
    player.finished.connect(player.queue_free)
```

## Attenuation Models {#attenuation}

Control how volume decreases with distance:

```gdscript
extends AudioStreamPlayer3D

func _ready() -> void:
    # ATTENUATION_INVERSE_DISTANCE (default)
    # Realistic falloff: volume = 1 / (1 + distance / unit_size)
    attenuation_model = ATTENUATION_INVERSE_DISTANCE

    # ATTENUATION_INVERSE_SQUARE_DISTANCE
    # Faster falloff: volume = 1 / (1 + (distance / unit_size)^2)
    # attenuation_model = ATTENUATION_INVERSE_SQUARE_DISTANCE

    # ATTENUATION_LOGARITHMIC
    # Logarithmic falloff (most dramatic)
    # attenuation_model = ATTENUATION_LOGARITHMIC

    # ATTENUATION_DISABLED
    # No volume attenuation (still has panning/directionality)
    # attenuation_model = ATTENUATION_DISABLED

    unit_size = 10.0   # Reference distance for attenuation
    max_distance = 0.0 # 0 = unlimited range (still attenuates)
```

### Attenuation Configuration Table

| Model | Behavior | Use Case |
|-------|----------|----------|
| `INVERSE_DISTANCE` | Realistic 1/d falloff | Most sounds, ambient audio |
| `INVERSE_SQUARE_DISTANCE` | Rapid 1/d² falloff | Localized sounds, effects |
| `LOGARITHMIC` | Very dramatic falloff | Small areas, dramatic effects |
| `DISABLED` | No attenuation | Panning only, constant volume |

## Distance Configuration {#distance}

```gdscript
extends AudioStreamPlayer3D

func _ready() -> void:
    # unit_size: Distance for "full volume" reference point
    # Lower = sound stays loud closer
    # Higher = sound stays loud further away
    unit_size = 10.0

    # max_distance: Hard cutoff (saves CPU)
    # 0 = unlimited (still attenuates, just no hard cutoff)
    # >0 = sound completely silent beyond this distance
    max_distance = 100.0
```

**Examples:**
- **Ambient fire**: `unit_size = 5.0`, `max_distance = 30.0` (localized)
- **Music speaker**: `unit_size = 20.0`, `max_distance = 100.0` (wide range)
- **Distant waterfall**: `unit_size = 50.0`, `max_distance = 0` (very far, unlimited)

## Doppler Effect {#doppler}

Pitch shift based on relative velocity (like passing ambulance):

```gdscript
extends AudioStreamPlayer3D

func _ready() -> void:
    stream = engine_sound
    doppler_tracking = DOPPLER_TRACKING_PHYSICS_STEP
    # Options:
    # DOPPLER_TRACKING_DISABLED - No doppler
    # DOPPLER_TRACKING_IDLE_STEP - Update every frame
    # DOPPLER_TRACKING_PHYSICS_STEP - Update every physics frame (best)
```

**Moving Projectile Example:**

```gdscript
extends Area3D

var velocity: Vector3 = Vector3.ZERO

@onready var audio: AudioStreamPlayer3D = $AudioStreamPlayer3D

func _ready() -> void:
    audio.stream = whoosh_sound
    audio.unit_size = 3.0
    audio.doppler_tracking = DOPPLER_TRACKING_PHYSICS_STEP
    audio.play()

func _physics_process(delta: float) -> void:
    global_position += velocity * delta
```

## Low-Pass Filter {#filter}

Distant sounds are automatically muffled with a low-pass filter:

```gdscript
extends AudioStreamPlayer3D

func _ready() -> void:
    # attenuation_filter_cutoff_hz: Frequency cutoff for distant sounds
    # Default: ~5000 Hz (muffled)
    # 20500 Hz = disable filter (full clarity at all distances)
    attenuation_filter_cutoff_hz = 5000.0

    # attenuation_filter_db: How much the filter affects volume
    # Default: -24.0 (strong muffling)
    # Higher = less muffling
    attenuation_filter_db = -24.0
```

**Examples:**
- **Disable filter**: `attenuation_filter_cutoff_hz = 20500.0`
- **Underwater effect**: `attenuation_filter_cutoff_hz = 2000.0`, `attenuation_filter_db = -36.0`
- **Through walls**: `attenuation_filter_cutoff_hz = 3000.0`, `attenuation_filter_db = -18.0`

## Directional Audio {#directional}

Sound emitted in a cone (like a speaker or megaphone):

```gdscript
extends AudioStreamPlayer3D

func _ready() -> void:
    # Enable emission angle
    emission_angle_enabled = true

    # Cone angle in degrees (default: 45)
    # Sound is loudest in front, quieter to the sides/back
    emission_angle_degrees = 90.0

    # How quickly volume drops outside the cone
    # 1.0 = linear, higher = sharper cutoff
    emission_angle_filter_attenuation_db = -12.0
```

**Speaker Setup:**

```gdscript
# Speaker facing forward (Z-axis)
extends AudioStreamPlayer3D

func _ready() -> void:
    stream = music
    emission_angle_enabled = true
    emission_angle_degrees = 120.0  # Wide cone
    attenuation_model = ATTENUATION_INVERSE_DISTANCE
    unit_size = 5.0
    autoplay = true
```

## Panning Strength {#panning}

Control left/right stereo panning intensity:

```gdscript
# AudioStreamPlayer2D
extends AudioStreamPlayer2D

func _ready() -> void:
    # panning_strength: 0.0 to 1.0
    # 0.0 = no panning (mono in center)
    # 1.0 = full panning (uses ProjectSettings.audio/general/2d_panning_strength)
    # >1.0 = exaggerated panning
    panning_strength = 1.0

# AudioStreamPlayer3D
extends AudioStreamPlayer3D

func _ready() -> void:
    # Same concept, uses ProjectSettings.audio/general/3d_panning_strength
    panning_strength = 1.0
```

**Note:** A common request is to disable panning while keeping distance attenuation for ambient sounds. Currently, set `panning_strength = 0.0` as a workaround.

## Footsteps with Surface Detection (3D) {#footsteps-3d}

Play different sounds based on GridMap cell type:

```gdscript
extends AudioStreamPlayer3D

@export var grass_step_sound: AudioStream
@export var concrete_step_sound: AudioStream
@export var grass_cell_ids: PackedInt32Array
@export var concrete_cell_ids: PackedInt32Array
@export var step_distance: float = 2.8

var _current_step_distance: float = 0.0
var _grid_map_types: Dictionary = {}

@onready var _level_grid_map: GridMap = %LevelGridMap
@onready var _player: CharacterBody3D = get_parent()

func _ready() -> void:
    # Build sound lookup dictionary
    for id in grass_cell_ids:
        _grid_map_types[id] = grass_step_sound
    for id in concrete_cell_ids:
        _grid_map_types[id] = concrete_step_sound

func _physics_process(delta: float) -> void:
    if _player.is_on_floor():
        _current_step_distance += _player.velocity.length() * delta

    if _current_step_distance > step_distance:
        _current_step_distance = 0.0
        _footstep()

func _footstep() -> void:
    # Find grid cell under player
    var grid_position := Vector3i(_level_grid_map.to_local(global_position + Vector3.DOWN).floor())
    var grid_coordinate := _level_grid_map.local_to_map(grid_position)
    var cell_item := _level_grid_map.get_cell_item(grid_coordinate)

    # Check if we have a sound for this cell type
    if not _grid_map_types.has(cell_item):
        return

    var footstep_sound: AudioStream = _grid_map_types[cell_item]

    # Only assign if different (changing stream stops playback)
    if stream != footstep_sound:
        stream = footstep_sound
    play()
```

## Polyphonic Audio {#polyphonic}

Play multiple sounds simultaneously from one player:

```gdscript
extends AudioStreamPlayer2D

@export var audio_clip_pitch_scale: float = 1.0:
    set(value):
        audio_clip_pitch_scale = value

        # Only relevant for AudioStreamPolyphonic
        if stream == null or not stream is AudioStreamPolyphonic:
            return

        var stream_playback: AudioStreamPlaybackPolyphonic = get_stream_playback()

        # Set pitch for all active streams
        for current_index in range(stream.polyphony):
            stream_playback.set_stream_pitch_scale(current_index, audio_clip_pitch_scale)
```

**Setup:**
1. Set `stream` to `AudioStreamPolyphonic` resource
2. Configure `polyphony` count (number of simultaneous sounds)
3. Play individual sounds via `get_stream_playback().play_stream()`

## Properties Reference

### Common Properties (All Audio Players)

| Property | Type | Description |
|----------|------|-------------|
| `stream` | AudioStream | Audio resource to play |
| `volume_db` | float | Volume in decibels (0 = full, -80 = silent) |
| `pitch_scale` | float | Playback speed (1.0 = normal, 2.0 = double speed) |
| `playing` | bool | Is currently playing (read-only) |
| `autoplay` | bool | Start playing when node enters scene |
| `stream_paused` | bool | Pause without stopping |
| `bus` | StringName | Audio bus name ("Master", "SFX", "Music", etc.) |

### AudioStreamPlayer2D Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `max_distance` | float | 2000.0 | Distance where sound becomes silent |
| `attenuation` | float | 1.0 | Falloff rate (higher = faster volume drop) |
| `panning_strength` | float | 1.0 | Stereo panning multiplier (0 = no panning) |
| `area_mask` | int | 1 | Physics layers for listener detection |

### AudioStreamPlayer3D Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `attenuation_model` | int | 0 | Attenuation curve (see [Attenuation Models](#attenuation)) |
| `unit_size` | float | 10.0 | Reference distance for attenuation |
| `max_distance` | float | 0.0 | Cutoff distance (0 = unlimited) |
| `max_db` | float | 3.0 | Maximum volume boost in decibels |
| `panning_strength` | float | 1.0 | Stereo panning multiplier |
| `doppler_tracking` | int | 0 | Doppler effect mode (see [Doppler Effect](#doppler)) |
| `emission_angle_enabled` | bool | false | Enable directional audio |
| `emission_angle_degrees` | float | 45.0 | Cone angle for directional audio |
| `emission_angle_filter_attenuation_db` | float | -12.0 | Volume drop outside cone |
| `attenuation_filter_cutoff_hz` | float | 5000.0 | Low-pass filter frequency for distance |
| `attenuation_filter_db` | float | -24.0 | Low-pass filter strength |
| `area_mask` | int | 1 | Physics layers for listener/reverb detection |

## Audio Listeners

### AudioListener2D

Change where 2D audio is heard from:

```gdscript
extends AudioListener2D

func _ready() -> void:
    # Make this listener active
    make_current()

    # Typically attached to camera or player
```

**Default behavior:** If no `AudioListener2D` exists, audio is heard from screen center.

### AudioListener3D

Change where 3D audio is heard from:

```gdscript
extends AudioListener3D

func _ready() -> void:
    # Make this listener active (only one can be active)
    make_current()

    # Typically attached to Camera3D
```

**Default behavior:** If no `AudioListener3D` exists, audio is heard from active `Camera3D`.

## Best Practices

### Performance Optimization

```gdscript
# Use max_distance to cull distant sounds (saves CPU)
audio.max_distance = 100.0

# Pool players instead of creating/destroying frequently
# (See audio/players.md for pooling pattern)

# Disable doppler if not needed
audio.doppler_tracking = DOPPLER_TRACKING_DISABLED
```

### Spatial Sound Design

- **Ambient loops**: Use longer `unit_size`, disable `max_distance`
- **Impact sounds**: Use short `unit_size`, enable `max_distance`
- **Doppler**: Only for fast-moving objects (projectiles, vehicles)
- **Directional**: Use for speakers, megaphones, directional emitters
- **Panning strength**: Reduce for ambient/background, increase for effects

### Common Pitfalls

- **Changing stream stops playback**: Check if `stream` differs before assigning
- **No spatial effect**: Ensure `AudioListener2D/3D` is active (or using default)
- **Too quiet**: Check `unit_size` (higher = louder at distance)
- **Doppler too strong**: Lower pitch variation or disable if object isn't fast
- **Filter too muffled**: Increase `attenuation_filter_cutoff_hz` or set to 20500

## Scene Setup Examples

### 2D Positional Audio
```
Node2D (World)
├── CharacterBody2D (Player)
│   └── Camera2D
│       └── AudioListener2D
└── Node2D (SoundSource)
    └── AudioStreamPlayer2D
```

### 3D Positional Audio
```
Node3D (World)
├── CharacterBody3D (Player)
│   └── Camera3D
│       └── AudioListener3D
└── Node3D (SoundSource)
    └── AudioStreamPlayer3D
```

### Speaker with Directional Audio
```
StaticBody3D (Speaker)
├── MeshInstance3D (Visual)
├── CollisionShape3D
└── AudioStreamPlayer3D
    - emission_angle_enabled = true
    - emission_angle_degrees = 120.0
    - rotation: facing desired direction
```
