---
topic: animation-tree
version: 2025.12.21
godot_version: "4.3"
sources:
  - url: https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html
    type: official
    priority: 1
  - url: https://kidscancode.org/godot_recipes/4.x/animation/using_animation_sm/index.html
    type: community
    priority: 2
  - url: https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachine.html
    type: official
    priority: 1
  - url: https://github.com/godotengine/godot_node_essentials
    type: examples
    priority: 2
---

# AnimationTree

AnimationTree controls complex animation systems through state machines, blend spaces, and transitions. It works with AnimationPlayer to blend animations and manage state-based character behavior.

## Core Concepts

**State Machine**: Organizes animations into states with transitions between them. Use `travel()` to move between states following defined connections.

**Blend Spaces**: Interpolate between multiple animations based on input parameters (e.g., 8-directional movement).

**Root Motion**: Extract animation movement data to control character position programmatically.

**Playback Control**: Use `AnimationNodeStateMachinePlayback` to trigger state changes via code.

## Basic Setup

```gdscript
extends CharacterBody3D

@onready var _animation_tree: AnimationTree = %AnimationTree
@onready var _playback: AnimationNodeStateMachinePlayback = _animation_tree["parameters/playback"]

func _ready() -> void:
    _animation_tree.active = true

func _physics_process(delta: float) -> void:
    var speed: float = velocity.length()
    if speed > 0.1:
        _playback.travel("run")
    else:
        _playback.travel("idle")
```

**Key Steps**:
1. Add `AnimationTree` node to your scene
2. Set `Tree Root` property to "New AnimationNodeStateMachine"
3. Assign `Animation Player` property to your AnimationPlayer node
4. Set `Active` property to `true` (in code or inspector)
5. Access playback via `_animation_tree["parameters/playback"]`

## State Machine

### Creating States

In the AnimationTree editor panel:
1. Right-click → "Add Animation" to create state nodes
2. Click "Connect nodes" button, drag between nodes to create transitions
3. Select transitions to configure properties in Inspector

### Travel Method

```gdscript
@onready var _playback: AnimationNodeStateMachinePlayback = $AnimationTree["parameters/playback"]

func hurt() -> void:
    _playback.travel("hurt")

func attack() -> void:
    _playback.travel("attack")
    # Return early to prevent movement states from overriding attack
    return
```

**Best Practice**: Use `return` after calling `travel()` for action animations (attack, hurt, die) to prevent the same frame's movement logic from overriding the state.

### Querying Current State

```gdscript
func _get_input() -> void:
    var current: StringName = _playback.get_current_node()

    if Input.is_action_just_pressed("attack"):
        _playback.travel("attack")
        return

    # Only allow movement if not attacking
    if current != "attack":
        _handle_movement()
```

### Nested State Machines

```gdscript
# Access nested state machine playback
@onready var _ledge_playback: AnimationNodeStateMachinePlayback = (
    _animation_tree["parameters/ledge/playback"]
)

var is_on_ledge: bool = false:
    set(new_value):
        if new_value and not is_on_ledge:
            _playback.travel("ledge")  # Enter ledge state
        elif is_on_ledge and not new_value:
            _playback.travel("idle")  # Exit ledge state
        is_on_ledge = new_value

func _physics_process(delta: float) -> void:
    if is_on_ledge:
        if abs(move_horizontal_direction) > 0.0:
            _ledge_playback.travel("move")
        else:
            _ledge_playback.travel("idle")
```

**Limitation**: Direct transitions to states inside nested state machines via `travel()` may not work reliably. Only transitions between states at the same hierarchy level are guaranteed.

## Transition Configuration

### Switch Mode

| Mode | Behavior |
|------|----------|
| `Immediate` | Transition fires instantly when conditions are met |
| `At End` | Waits for current animation to finish before transitioning |

```gdscript
# Configure in editor: click transition → Inspector → Switch Mode
# With "At End": animations play in sequence (attack1 → attack2)
# With "Immediate": attack2 interrupts attack1 instantly
```

### Advance Mode

| Mode | Behavior |
|------|----------|
| `Disabled` | Stays on target state |
| `Enabled` | Requires explicit condition/expression |
| `Auto` | Automatically advances after animation completes |

**Auto Mode Pattern**: Connect states in a chain with "Auto" to create automatic sequences:
```
idle → attack1 [Auto] → attack2 [Auto] → idle
```
Connection icons turn green when Auto mode is enabled.

### Transition Priority

Lower priority values (0) are preferred over higher values (1, 2, etc.). When multiple transitions have valid conditions, the lowest priority fires first.

**Known Issue**: `Immediate` transitions may not fire when combined with `At End` transitions that have true advance expressions. Workaround: introduce intermediate states.

## Blend Spaces

### BlendSpace2D for Directional Movement

```gdscript
extends CharacterBody2D

@onready var _animation_tree: AnimationTree = $AnimationTree

func _physics_process(delta: float) -> void:
    var input_dir: Vector2 = Input.get_vector("left", "right", "up", "down")

    # Set blend position directly
    _animation_tree.set("parameters/movement/blend_position", input_dir)
```

**Setup in Editor**:
1. Add BlendSpace2D node to your state machine
2. Add animation points at positions: (0,0) = idle, (0,1) = forward, (-1,0) = left, (1,0) = right
3. BlendSpace2D automatically interpolates between animations based on the blend_position vector

### Smooth Blending

```gdscript
func _physics_process(delta: float) -> void:
    var input_direction: Vector2 = Input.get_vector("left", "right", "up", "down")
    var current_blend: Vector2 = _animation_tree.get("parameters/movement/blend_position")
    var smooth_speed: float = 8.0

    var smoothed: Vector2 = current_blend.lerp(input_direction, delta * smooth_speed)
    _animation_tree.set("parameters/movement/blend_position", smoothed)
```

**Best Practice**: Use `lerp()` to smooth blend position changes and prevent snappy transitions between animation directions.

### Speed-Based Blending

```gdscript
var max_ground_speed: float = 6.0

func _physics_process(delta: float) -> void:
    var speed_ratio: float = velocity.length() / max_ground_speed

    # Blend between idle (0.0) and run (1.0) based on speed
    _animation_tree["parameters/move/blend_position"] = speed_ratio
```

## Transition Conditions

### Boolean Conditions

```gdscript
func _physics_process(delta: float) -> void:
    var is_moving: bool = velocity.length_squared() >= 0.36  # Speed threshold
    var is_idle: bool = velocity.length_squared() <= 0.36

    # Set conditions that drive transitions
    _animation_tree["parameters/conditions/is_moving"] = is_moving
    _animation_tree["parameters/conditions/is_idle"] = is_idle
```

**Setup**: In transition properties, add a "Condition" and set it to match your parameter name (e.g., "is_moving").

### Expression-Based Transitions

More complex logic can use advance expressions, but they can be complex to configure. For most cases, use simple boolean conditions combined with `travel()` for explicit control.

## Root Motion

Root motion extracts bone movement from animations to control character position programmatically.

### Basic Root Motion Setup

```gdscript
extends CharacterBody3D

const MODEL_SCALE: float = 0.01  # Adjust based on your model's import scale

@onready var _animation_tree: AnimationTree = $AnimationTree
@onready var _skeleton: Skeleton3D = %Skeleton3D

func _physics_process(delta: float) -> void:
    # Get root motion transform
    var root_motion: Transform3D = _animation_tree.get_root_motion_transform()

    # Extract forward movement (z-axis for characters facing forward)
    var forward_movement: float = root_motion.origin.z * MODEL_SCALE

    # Convert to velocity and apply
    var movement_direction: Vector3 = -global_basis.z  # Character's forward
    velocity = movement_direction * forward_movement * 300.0

    move_and_slide()
```

**Configuration**:
1. In AnimationTree Inspector, set `Root Motion` → `Root Motion Track` to the bone path (e.g., "Skeleton3D:Root")
2. Choose which axes to capture (position, rotation, scale)
3. Call `get_root_motion_transform()` each frame to extract movement

### Resetting Root Motion

```gdscript
const ROOT_BONE_INDEX: int = 1

# Clear root motion override when exiting root motion animations
func _exit_ledge_state() -> void:
    _skeleton.clear_bones_global_pose_override()
    _skeleton.set_bone_global_pose_override(
        ROOT_BONE_INDEX,
        Transform3D.IDENTITY,
        1.0,
        true
    )
    position = Vector3.ZERO
```

**Use Case**: When mixing root motion animations (like ledge climbing) with non-root-motion animations (like running), reset bone overrides when transitioning out.

## OneShot Nodes

OneShot nodes play animations once and return to the base state. Useful for actions like jumping, attacking, or taking damage.

### Basic OneShot Pattern

```gdscript
# Configure in AnimationTree editor:
# Add OneShot node in a BlendTree
# Connect base animation to input1
# Connect action animation to input2

func jump() -> void:
    _animation_tree["parameters/oneshot_jump/request"] = AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE

func _is_jump_finished() -> bool:
    return not _animation_tree["parameters/oneshot_jump/active"]
```

**Fade Times**: Configure `Fade In` and `Fade Out` times in the OneShot node properties to blend smoothly.

**Known Issue**: OneShot may repeat or continue playing interrupted animations. If this occurs, use state machine `travel()` instead for more reliable control.

## Common Patterns

### Player Character Animation

```gdscript
class_name PlayerCharacter extends CharacterBody3D

@export var move_speed: float = 6.0

@onready var _animation_tree: AnimationTree = %AnimationTree
@onready var _playback: AnimationNodeStateMachinePlayback = _animation_tree["parameters/playback"]

func _ready() -> void:
    _animation_tree.active = true

func _physics_process(delta: float) -> void:
    _update_movement(delta)
    _update_animation()

func _update_movement(delta: float) -> void:
    var input_dir: Vector2 = Input.get_vector("move_left", "move_right", "move_up", "move_down")
    var direction: Vector3 = Vector3(input_dir.x, 0.0, input_dir.y)

    velocity.x = direction.x * move_speed
    velocity.z = direction.z * move_speed
    velocity.y -= 30.0 * delta  # Gravity

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = 12.0

    move_and_slide()

func _update_animation() -> void:
    # Priority: action animations first
    if Input.is_action_just_pressed("attack"):
        _playback.travel("attack")
        return

    # Movement states
    var speed: float = Vector2(velocity.x, velocity.z).length()

    if not is_on_floor():
        if velocity.y > 0.1:
            _playback.travel("jump")
        else:
            _playback.travel("fall")
    elif speed > 0.1:
        _playback.travel("run")
        _animation_tree["parameters/move/blend_position"] = speed / move_speed
    else:
        _playback.travel("idle")
```

### 8-Direction Character Animation

```gdscript
# AnimationTree structure:
# - Root: StateMachine
#   - idle: Single animation
#   - move: BlendSpace2D with 8 animations
#     - (0, 0): idle
#     - (0, 1): forward, (0, -1): backward
#     - (1, 0): right, (-1, 0): left
#     - (0.7, 0.7): forward-right, etc.

func _physics_process(delta: float) -> void:
    var input_dir: Vector2 = Input.get_vector("left", "right", "up", "down")

    if input_dir.length() > 0.1:
        _playback.travel("move")
        _animation_tree["parameters/move/blend_position"] = input_dir.normalized()
    else:
        _playback.travel("idle")
```

### Enemy AI Animation

```gdscript
extends CharacterBody3D

enum State { IDLE, PATROL, CHASE, ATTACK }

var current_state: State = State.IDLE
var target: Node3D = null

@onready var _playback: AnimationNodeStateMachinePlayback = $AnimationTree["parameters/playback"]

func _physics_process(delta: float) -> void:
    match current_state:
        State.IDLE:
            _playback.travel("idle")
        State.PATROL:
            _playback.travel("walk")
        State.CHASE:
            _playback.travel("run")
        State.ATTACK:
            if _playback.get_current_node() != "attack":
                _playback.travel("attack")
```

## Best Practices

**Organize State Hierarchies**: Use nested state machines for complex characters (e.g., ground states, air states, ledge states as sub-machines).

**Use `travel()` for Control**: While conditions and expressions work, explicit `travel()` calls provide clearer, more maintainable code.

**Return After Actions**: Always `return` after calling `travel()` for action animations to prevent movement logic from overriding them.

**Smooth Blend Positions**: Use `lerp()` when updating BlendSpace positions based on input to avoid snappy transitions.

**Check Current State**: Query `get_current_node()` before triggering states to avoid restarting animations unnecessarily.

**Normalize Input Vectors**: When using input for BlendSpace2D, normalize directional vectors for consistent animation blending.

**Cache Playback References**: Store `AnimationNodeStateMachinePlayback` references in `@onready` variables for cleaner code.

## Common Pitfalls

**Forgetting to Activate**: AnimationTree must have `active = true` set before it will process animations.

**Parameter Path Errors**: Use bracket syntax `_animation_tree["parameters/path"]` not dot notation. Parameter paths are strings.

**Overriding States**: Setting conditions or calling `travel()` in the same frame can cause race conditions. Structure your code to prevent conflicts.

**Nested State Limitations**: Direct `travel()` to nested states may fail. Always `travel()` to the parent state first, then control sub-states separately.

**BlendSpace Coordinate Mismatches**: Ensure your blend_position values match the coordinate system of your BlendSpace2D points.

**Missing Animation Player**: AnimationTree requires an assigned AnimationPlayer. Check that the `anim_player` property is set.

**Root Motion Scale Issues**: Model import scale affects root motion values. Store and apply scale constants when extracting movement data.

## Related Patterns

- **AnimationPlayer**: Base animation playback system that AnimationTree builds upon
- **State Pattern**: AnimationTree state machines implement the state pattern for character behavior
- **Input Handling**: Combine with input systems for responsive character control
- **CharacterBody3D/2D**: Integrate animations with physics-based character controllers

## Sources

**Official Documentation**:
- [Using AnimationTree - Godot Docs](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html)
- [AnimationNodeStateMachine - API Reference](https://docs.godotengine.org/en/stable/classes/class_animationnodestatemachine.html)

**Community Resources**:
- [Using the AnimationTree StateMachine - Godot 4 Recipes](https://kidscancode.org/godot_recipes/4.x/animation/using_animation_sm/index.html)

**Example Code**:
- [godot_node_essentials - AstronautSkin3D](https://github.com/gdquest-demos/godot-node-essentials) - Demonstrates state machines, root motion, and nested playback for 3D character
