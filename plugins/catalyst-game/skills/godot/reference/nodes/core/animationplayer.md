---
class: AnimationPlayer
source: repos/godot-docs/classes/class_animationplayer.rst
generated: 2025-12-21
---

# AnimationPlayer

**Inherits:** AnimationMixer < Node < Object

A node used for animation playback.

## Description

An animation player is used for general-purpose playback of animations. It contains a dictionary of AnimationLibrary resources and custom blend times between animation transitions.

Some methods and properties use a single key to reference an animation directly. These keys are formatted as the key for the library, followed by a forward slash, then the key for the animation within the library, for example "movement/run". If the library's key is an empty string (known as the default library), the forward slash is omitted.

AnimationPlayer is better-suited than Tween for more complex animations, for example ones with non-trivial timings. It can also be used over Tween if the animation track editor is more convenient than doing it in code.

Updating the target properties of animations occurs at the process frame.

## Properties

| Type | Property | Default |
|------|----------|---------|
| String | assigned_animation | |
| String | autoplay | "" |
| String | current_animation | "" |
| float | current_animation_length | |
| float | current_animation_position | |
| bool | movie_quit_on_finish | false |
| bool | playback_auto_capture | true |
| float | playback_auto_capture_duration | -1.0 |
| EaseType | playback_auto_capture_ease_type | 0 |
| TransitionType | playback_auto_capture_transition_type | 0 |
| float | playback_default_blend_time | 0.0 |
| float | speed_scale | 1.0 |

## Methods

| Return Type | Method |
|-------------|--------|
| StringName | `animation_get_next(animation_from: StringName)` const |
| void | `animation_set_next(animation_from: StringName, animation_to: StringName)` |
| void | `clear_queue()` |
| float | `get_blend_time(animation_from: StringName, animation_to: StringName)` const |
| float | `get_playing_speed()` const |
| PackedStringArray | `get_queue()` |
| bool | `is_playing()` const |
| void | `pause()` |
| void | `play(name: StringName = &"", custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false)` |
| void | `play_backwards(name: StringName = &"", custom_blend: float = -1)` |
| void | `play_with_capture(name: StringName = &"", duration: float = -1.0, custom_blend: float = -1, custom_speed: float = 1.0, from_end: bool = false, trans_type: TransitionType = 0, ease_type: EaseType = 0)` |
| void | `queue(name: StringName)` |
| void | `seek(seconds: float, update: bool = false, update_only: bool = false)` |
| void | `set_blend_time(animation_from: StringName, animation_to: StringName, sec: float)` |
| void | `stop(keep_state: bool = false)` |

## Signals

- **animation_changed**(old_name: StringName, new_name: StringName)
  - Emitted when a queued animation plays after the previous animation finished

- **current_animation_changed**(name: String)
  - Emitted when current_animation changes

## Key Properties

- **current_animation**: The key of the currently playing animation. Changing this value does not restart the animation.
- **assigned_animation**: If playing, the current animation's key, otherwise, the animation last played.
- **autoplay**: The key of the animation to play when the scene loads.
- **speed_scale**: The speed scaling ratio. For example, if this value is 1, then the animation plays at normal speed. If it's 0.5, then it plays at half speed. If it's 2, then it plays at double speed.
- **current_animation_length**: The length (in seconds) of the currently playing animation. (Read-only)
- **current_animation_position**: The position (in seconds) of the currently playing animation. (Read-only)
- **playback_default_blend_time**: The default time in which to blend animations. Ranges from 0 to 4096 with 0.01 precision.

## Common Methods

- **play(name, custom_blend, custom_speed, from_end)**: Plays the animation with key name. Custom blend times and speed can be set.
- **play_backwards(name, custom_blend)**: Plays the animation with key name in reverse.
- **pause()**: Pauses the currently playing animation. The current_animation_position will be kept.
- **stop(keep_state)**: Stops the currently playing animation. The animation position is reset to 0 and the custom_speed is reset to 1.0.
- **seek(seconds, update, update_only)**: Seeks the animation to the seconds point in time (in seconds).
- **queue(name)**: Queues an animation for playback once the current animation and all previously queued animations are done.
- **is_playing()**: Returns true if an animation is currently playing.
- **get_playing_speed()**: Returns the actual playing speed of current animation or 0 if not playing.

## Section Playback Methods

- **play_section(name, start_time, end_time, custom_blend, custom_speed, from_end)**: Plays the animation with a section from start_time to end_time.
- **play_section_with_markers(name, start_marker, end_marker, custom_blend, custom_speed, from_end)**: Plays the animation with a section between markers.
- **set_section(start_time, end_time)**: Changes the start and end times of the section being played.
- **has_section()**: Returns true if an animation is currently playing with a section.
- **reset_section()**: Resets the current section.

## Common Usage

```gdscript
# Play an animation
$AnimationPlayer.play("walk")

# Play with custom speed
$AnimationPlayer.play("run", -1, 2.0)  # Double speed

# Play backwards
$AnimationPlayer.play_backwards("death")

# Queue animations
$AnimationPlayer.play("idle")
$AnimationPlayer.queue("attack")
$AnimationPlayer.queue("idle")

# Check if playing
if $AnimationPlayer.is_playing():
    print("Animation running")

# Connect to animation finished
$AnimationPlayer.animation_finished.connect(_on_animation_finished)
```

## Notes

- The AnimationPlayer keeps track of its current or last played animation with assigned_animation.
- If play() is called with that same animation name, or with no name parameter, the assigned animation will resume playing if it was paused.
- The animation will be updated the next time the AnimationPlayer is processed.
- Seeking to the end of the animation doesn't emit animation_finished.
