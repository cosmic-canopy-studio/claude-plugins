---
class: Tween
inherits: RefCounted > Object
brief: Lightweight object used for general-purpose animation via script, using Tweeners.
---

# Tween

Lightweight object used for general-purpose animation via script, using Tweeners.

## Description

Tweens are mostly useful for animations requiring a numerical property to be interpolated over a range of values. The name "tween" comes from "in-betweening", an animation technique where you specify keyframes and the computer interpolates the frames that appear between them.

Tween is more suited than AnimationPlayer for animations where you don't know the final values in advance. For example, interpolating a dynamically-chosen camera zoom value is best done with a Tween; it would be difficult to do the same thing with an AnimationPlayer node.

A Tween can be created by using either SceneTree.create_tween() or Node.create_tween(). Tweens created manually (i.e. by using Tween.new()) are invalid and can't be used for tweening values.

**Note:** Tweens are not designed to be reused and trying to do so results in an undefined behavior. Create a new Tween for each animation and every time you replay an animation from start. Keep in mind that Tweens start immediately, so only create a Tween when you want to start animating.

**Note:** The tween is processed after all of the nodes in the current frame, i.e. node's _process() method would be called before the tween (or _physics_process() depending on the value passed to set_process_mode()).

## Core Methods

| Returns | Method |
|---------|--------|
| PropertyTweener | tween_property(object: Object, property: NodePath, final_val: Variant, duration: float) |
| MethodTweener | tween_method(method: Callable, from: Variant, to: Variant, duration: float) |
| IntervalTweener | tween_interval(time: float) |
| CallbackTweener | tween_callback(callback: Callable) |
| SubtweenTweener | tween_subtween(subtween: Tween) |

## Configuration Methods

| Returns | Method |
|---------|--------|
| Tween | bind_node(node: Node) |
| Tween | set_trans(trans: TransitionType) |
| Tween | set_ease(ease: EaseType) |
| Tween | set_parallel(parallel: bool = true) |
| Tween | set_loops(loops: int = 0) |
| Tween | set_speed_scale(speed: float) |
| Tween | set_process_mode(mode: TweenProcessMode) |
| Tween | set_pause_mode(mode: TweenPauseMode) |
| Tween | set_ignore_time_scale(ignore: bool = true) |

## Control Methods

| Returns | Method |
|---------|--------|
| void | play() |
| void | pause() |
| void | stop() |
| void | kill() |
| Tween | parallel() |
| Tween | chain() |
| bool | custom_step(delta: float) |

## Query Methods

| Returns | Method |
|---------|--------|
| bool | is_running() |
| bool | is_valid() |
| int | get_loops_left() const |
| float | get_total_elapsed_time() const |

## Static Methods

| Returns | Method |
|---------|--------|
| Variant | interpolate_value(initial_value: Variant, delta_value: Variant, elapsed_time: float, duration: float, trans_type: TransitionType, ease_type: EaseType) |

## Signals

**finished**()

Emitted when the Tween has finished all tweening. Never emitted when the Tween is set to infinite looping (see set_loops()).

**loop_finished**(loop_count: int)

Emitted when a full loop is complete (see set_loops()), providing the loop index. This signal is not emitted after the final loop, use finished instead for this case.

**step_finished**(idx: int)

Emitted when one step of the Tween is complete, providing the step index. One step is either a single Tweener or a group of Tweeners running in parallel.

## Enumerations

**enum TweenProcessMode:**

- **TWEEN_PROCESS_PHYSICS** = 0 - The Tween updates after each physics frame
- **TWEEN_PROCESS_IDLE** = 1 - The Tween updates after each process frame

**enum TweenPauseMode:**

- **TWEEN_PAUSE_BOUND** = 0 - If the Tween has a bound node, it will process when that node can process
- **TWEEN_PAUSE_STOP** = 1 - If SceneTree is paused, the Tween will also pause
- **TWEEN_PAUSE_PROCESS** = 2 - The Tween will process regardless of whether SceneTree is paused

**enum TransitionType:**

- **TRANS_LINEAR** = 0 - Linear interpolation
- **TRANS_SINE** = 1 - Sine function interpolation
- **TRANS_QUINT** = 2 - Quintic (power of 5) interpolation
- **TRANS_QUART** = 3 - Quartic (power of 4) interpolation
- **TRANS_QUAD** = 4 - Quadratic (power of 2) interpolation
- **TRANS_EXPO** = 5 - Exponential interpolation
- **TRANS_ELASTIC** = 6 - Elastic interpolation with wiggling
- **TRANS_CUBIC** = 7 - Cubic (power of 3) interpolation
- **TRANS_CIRC** = 8 - Circular interpolation using square roots
- **TRANS_BOUNCE** = 9 - Bouncing interpolation at the end
- **TRANS_BACK** = 10 - Backing out interpolation at ends
- **TRANS_SPRING** = 11 - Spring-like interpolation towards the end

**enum EaseType:**

- **EASE_IN** = 0 - Interpolation starts slowly and speeds up towards the end
- **EASE_OUT** = 1 - Interpolation starts quickly and slows down towards the end
- **EASE_IN_OUT** = 2 - Combination of EASE_IN and EASE_OUT; slowest at both ends
- **EASE_OUT_IN** = 3 - Combination of EASE_IN and EASE_OUT; fastest at both ends

## Basic Usage Example

```gdscript
var tween: Tween = get_tree().create_tween()
tween.tween_property($Sprite, "modulate", Color.RED, 1.0)
tween.tween_property($Sprite, "scale", Vector2(), 1.0)
tween.tween_callback($Sprite.queue_free)
```

## Parallel Tweens Example

```gdscript
var tween: Tween = create_tween()
tween.tween_property(self, "position", Vector2(300, 0), 0.5)
tween.parallel().tween_property(self, "modulate", Color.GREEN, 0.5)
```

## Looping Example

```gdscript
var tween: Tween = get_tree().create_tween().set_loops()
tween.tween_callback(shoot).set_delay(1.0)  # Shoots every 1 second
```

## Resources

- [Tween easing and transition types cheatsheet](https://raw.githubusercontent.com/godotengine/godot-docs/master/img/tween_cheatsheet.webp)
- See [easings.net](https://easings.net/) for visual examples of transition types
