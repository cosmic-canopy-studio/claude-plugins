---
class: AnimatedSprite3D
godot_version: "4.x"
sources:
  - repos/godot-docs/classes/class_animatedsprite3d.rst
status: extracted
---

# AnimatedSprite3D

**Inherits:** SpriteBase3D < GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

2D sprite node in 3D world, that can use multiple 2D textures for animation.

## Description

AnimatedSprite3D is similar to the Sprite3D node, except it carries multiple textures as animation sprite_frames. Animations are created using a SpriteFrames resource, which allows you to import image files (or a folder containing said files) to provide the animation frames for the sprite. The SpriteFrames resource can be configured in the editor via the SpriteFrames bottom panel.

## Signals

- **animation_changed()** - Emitted when animation changes.
- **animation_finished()** - Emitted when the animation reaches the end, or the start if it is played in reverse. When the animation finishes, it pauses the playback. Note: This signal is not emitted if an animation is looping.
- **animation_looped()** - Emitted when the animation loops.
- **frame_changed()** - Emitted when frame changes.
- **sprite_frames_changed()** - Emitted when sprite_frames changes.

## Properties

| Property | Type | Default |
|----------|------|---------|
| animation | StringName | &"default" |
| autoplay | String | "" |
| frame | int | 0 |
| frame_progress | float | 0.0 |
| speed_scale | float | 1.0 |
| sprite_frames | SpriteFrames | |

## Methods

| Return | Method |
|--------|--------|
| float | get_playing_speed() const |
| bool | is_playing() const |
| void | pause() |
| void | play(name: StringName = &"", custom_speed: float = 1.0, from_end: bool = false) |
| void | play_backwards(name: StringName = &"") |
| void | set_frame_and_progress(frame: int, progress: float) |
| void | stop() |

## Property Details

### sprite_frames

The SpriteFrames resource containing the animation(s). Allows you the option to load, edit, clear, make unique and save the states of the SpriteFrames resource.

### animation

The current animation from the sprite_frames resource. If this value is changed, the frame counter and the frame_progress are reset.

### autoplay

The key of the animation to play when the scene loads.

### frame

The displayed animation frame's index. Setting this property also resets frame_progress. If this is not desired, use set_frame_and_progress().

### frame_progress

The progress value between 0.0 and 1.0 until the current frame transitions to the next frame. If the animation is playing backwards, the value transitions from 1.0 to 0.0.

### speed_scale

The speed scaling ratio. For example, if this value is 1, then the animation plays at normal speed. If it's 0.5, then it plays at half speed. If it's 2, then it plays at double speed.

If set to a negative value, the animation is played in reverse. If set to 0, the animation will not advance.

## Method Details

### play()

Plays the animation with key name. If custom_speed is negative and from_end is true, the animation will play backwards (which is equivalent to calling play_backwards()).

If this method is called with that same animation name, or with no name parameter, the assigned animation will resume playing if it was paused.

### play_backwards()

Plays the animation with key name in reverse.

This method is a shorthand for play() with custom_speed = -1.0 and from_end = true.

### pause()

Pauses the currently playing animation. The frame and frame_progress will be kept and calling play() or play_backwards() without arguments will resume the animation from the current playback position.

See also stop().

### stop()

Stops the currently playing animation. The animation position is reset to 0 and the custom_speed is reset to 1.0. See also pause().

### is_playing()

Returns true if an animation is currently playing (even if speed_scale and/or custom_speed are 0).

### get_playing_speed()

Returns the actual playing speed of current animation or 0 if not playing. This speed is the speed_scale property multiplied by custom_speed argument specified when calling the play() method.

Returns a negative value if the current animation is playing backwards.

### set_frame_and_progress()

Sets frame and frame_progress to the given values. Unlike setting frame, this method does not reset the frame_progress to 0.0 implicitly.

Example: Change the animation while keeping the same frame and frame_progress:

```gdscript
var current_frame: int = animated_sprite.get_frame()
var current_progress: float = animated_sprite.get_frame_progress()
animated_sprite.play("walk_another_skin")
animated_sprite.set_frame_and_progress(current_frame, current_progress)
```

## Usage Notes

### Creating Animations

1. Create a SpriteFrames resource
2. Add animations and frames in the SpriteFrames panel
3. Assign the SpriteFrames to the sprite_frames property
4. Use play() to start the animation

### Animation Control

```gdscript
# Play default animation
animated_sprite.play()

# Play specific animation
animated_sprite.play("walk")

# Play at custom speed
animated_sprite.play("run", 2.0)  # Double speed

# Play backwards
animated_sprite.play_backwards("idle")

# Pause/resume
animated_sprite.pause()
animated_sprite.play()  # Resume

# Stop completely
animated_sprite.stop()
```

### Frame Control

```gdscript
# Jump to specific frame
animated_sprite.frame = 5

# Check current frame
if animated_sprite.frame == 0:
    print("First frame")

# Preserve progress when changing animations
var f: int = animated_sprite.frame
var p: float = animated_sprite.frame_progress
animated_sprite.animation = "new_animation"
animated_sprite.set_frame_and_progress(f, p)
```
