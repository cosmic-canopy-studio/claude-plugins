---
class: Timer
source: repos/godot-docs/classes/class_timer.rst
generated: 2025-12-21
---

# Timer

**Inherits:** Node < Object

A countdown timer.

## Description

The Timer node is a countdown timer and is the simplest way to handle time-based logic in the engine. When a timer reaches the end of its wait_time, it will emit the timeout signal.

After a timer enters the scene tree, it can be manually started with `start()`. A timer node is also started automatically if autostart is true.

Note: To create a one-shot timer without instantiating a node, use `SceneTree.create_timer()`.

Note: Timers are affected by `Engine.time_scale` unless ignore_time_scale is true. The higher the time scale, the sooner timers will end. How often a timer processes may depend on the framerate or `Engine.physics_ticks_per_second`.

## Properties

| Type | Property | Default |
|------|----------|---------|
| bool | autostart | false |
| bool | ignore_time_scale | false |
| bool | one_shot | false |
| bool | paused | |
| TimerProcessCallback | process_callback | 1 |
| float | time_left | |
| float | wait_time | 1.0 |

## Methods

| Return Type | Method |
|-------------|--------|
| bool | `is_stopped()` const |
| void | `start(time_sec: float = -1)` |
| void | `stop()` |

## Signals

- **timeout**()
  - Emitted when the timer reaches the end

## Enumerations

### TimerProcessCallback

- **TIMER_PROCESS_PHYSICS** = 0
  - Update the timer every physics process frame

- **TIMER_PROCESS_IDLE** = 1
  - Update the timer every process (rendered) frame

## Key Properties

- **wait_time**: The time required for the timer to end, in seconds. This property can also be set every time start() is called.
- **one_shot**: If true, the timer will stop after reaching the end. Otherwise, as by default, the timer will automatically restart.
- **autostart**: If true, the timer will start immediately when it enters the scene tree.
- **paused**: If true, the timer is paused. A paused timer does not process until this property is set back to false.
- **time_left**: The timer's remaining time in seconds. This is always 0 if the timer is stopped. (Read-only)
- **process_callback**: Specifies when the timer is updated during the main loop.
- **ignore_time_scale**: If true, the timer will ignore Engine.time_scale and update with the real, elapsed time.

## Common Usage

```gdscript
# Create a timer in code
var timer: Timer = Timer.new()
timer.wait_time = 1.5
timer.one_shot = true
timer.timeout.connect(_on_timer_timeout)
add_child(timer)
timer.start()

func _on_timer_timeout() -> void:
    print("Timer finished!")
```

## Notes

- Timers can only process once per physics or process frame (depending on the process_callback).
- An unstable framerate may cause the timer to end inconsistently, especially for very short timers (< 0.05 seconds).
- For very short timers, consider writing custom code instead of using a Timer node.
- Calling stop() does not emit the timeout signal.
