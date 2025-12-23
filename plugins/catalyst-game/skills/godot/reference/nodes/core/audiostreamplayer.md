---
class: AudioStreamPlayer
inherits: Node > Object
brief: A node for audio playback.
---

# AudioStreamPlayer

A node for audio playback.

## Description

The AudioStreamPlayer node plays an audio stream non-positionally. It is ideal for user interfaces, menus, or background music.

To use this node, stream needs to be set to a valid AudioStream resource. Playing more than one sound at the same time is also supported, see max_polyphony.

If you need to play audio at a specific position, use AudioStreamPlayer2D or AudioStreamPlayer3D instead.

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| autoplay | bool | false | If true, this node calls play() when entering the tree. |
| bus | StringName | &"Master" | The target bus name. All sounds from this node will be playing on this bus. |
| max_polyphony | int | 1 | The maximum number of sounds this node can play at the same time. Calling play() after this value is reached will cut off the oldest sounds. |
| mix_target | MixTarget | 0 | The mix target channels. Has no effect when two speakers or less are detected. |
| pitch_scale | float | 1.0 | The audio's pitch and tempo, as a multiplier of the stream's sample rate. A value of 2.0 doubles the audio's pitch, while a value of 0.5 halves the pitch. |
| playback_type | PlaybackType | 0 | (Experimental) The playback type of the stream player. If set other than to the default value, it will force that playback type. |
| playing | bool | false | If true, this node is playing sounds. Setting this property has the same effect as play() and stop(). |
| stream | AudioStream | | The AudioStream resource to be played. Setting this property stops all currently playing sounds. If left empty, the AudioStreamPlayer does not work. |
| stream_paused | bool | false | If true, the sounds are paused. Setting stream_paused to false resumes all sounds. |
| volume_db | float | 0.0 | Volume of sound, in decibels. This is an offset of the stream's volume. |
| volume_linear | float | | Volume of sound, as a linear value. (Convenience property that modifies volume_db) |

## Methods

| Returns | Method |
|---------|--------|
| float | get_playback_position() |
| AudioStreamPlayback | get_stream_playback() |
| bool | has_stream_playback() |
| void | play(from_position: float = 0.0) |
| void | seek(to_position: float) |
| void | stop() |

## Signals

**finished**()

Emitted when a sound finishes playing without interruptions. This signal is *not* emitted when calling stop(), or when exiting the tree while sounds are playing.

## Enumerations

**enum MixTarget:**

- **MIX_TARGET_STEREO** = 0 - The audio will be played only on the first channel. This is the default.
- **MIX_TARGET_SURROUND** = 1 - The audio will be played on all surround channels.
- **MIX_TARGET_CENTER** = 2 - The audio will be played on the second channel, which is usually the center.

## Notes

**Positional Audio:**
- At runtime, if no bus with the given name exists, all sounds will fall back on "Master".

**Playback Position:**
- The position is not always accurate, as the AudioServer does not mix audio every processed frame. To get more accurate results, add AudioServer.get_time_since_last_mix() to the returned position.
- This method always returns 0.0 if the stream is an AudioStreamInteractive, since it can have multiple clips playing at once.

**Pausing:**
- The stream_paused property is automatically changed when exiting or entering the tree, or when the node is paused (see Node.process_mode).

## Usage Example

```gdscript
# Basic playback
@onready var player: AudioStreamPlayer = $AudioStreamPlayer
player.stream = preload("res://sounds/music.ogg")
player.play()

# Volume control (linear)
player.volume_linear = 0.5  # 50% volume

# Volume control (decibels)
player.volume_db = -6.0  # -6dB

# Play from specific position
player.play(5.0)  # Start at 5 seconds

# Multiple sounds (polyphony)
player.max_polyphony = 4  # Up to 4 simultaneous sounds

# Connect to finished signal
player.finished.connect(_on_music_finished)
```

## Tutorials

- [Audio streams](https://docs.godotengine.org/en/stable/tutorials/audio/audio_streams.html)
- [2D Dodge The Creeps Demo](https://godotengine.org/asset-library/asset/2712)
