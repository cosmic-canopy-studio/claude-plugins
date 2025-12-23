---
class: AnimationTree
inherits: AnimationMixer > Node > Object
brief: A node used for advanced animation transitions in an AnimationPlayer.
---

# AnimationTree

A node used for advanced animation transitions in an AnimationPlayer.

## Description

A node used for advanced animation transitions in an AnimationPlayer.

**Note:** When linked with an AnimationPlayer, several properties and methods of the corresponding AnimationPlayer will not function as expected. Playback and transitions should be handled using only the AnimationTree and its constituent AnimationNode(s). The AnimationPlayer node should be used solely for adding, deleting, and editing animations.

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| advance_expression_base_node | NodePath | NodePath(".") | The path to the Node used to evaluate the AnimationNode Expression if one is not explicitly specified internally. |
| anim_player | NodePath | NodePath("") | The path to the AnimationPlayer used for animating. |
| tree_root | AnimationRootNode | | The root animation node of this AnimationTree. See AnimationRootNode. |
| callback_mode_discrete | AnimationCallbackModeDiscrete | 2 | (Overrides AnimationMixer) |
| deterministic | bool | true | (Overrides AnimationMixer) |

## Methods

| Returns | Method |
|---------|--------|
| AnimationProcessCallback | get_process_callback() const |
| void | set_process_callback(mode: AnimationProcessCallback) |

**Note:** Both process callback methods are deprecated. Use AnimationMixer.callback_mode_process instead.

## Signals

**animation_player_changed**()

Emitted when the anim_player is changed.

## Enumerations

**enum AnimationProcessCallback:**

- **ANIMATION_PROCESS_PHYSICS** = 0 (Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_PHYSICS)
- **ANIMATION_PROCESS_IDLE** = 1 (Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_IDLE)
- **ANIMATION_PROCESS_MANUAL** = 2 (Deprecated: See AnimationMixer.ANIMATION_CALLBACK_MODE_PROCESS_MANUAL)

## Common Patterns

### 1. Basic Setup with AnimationPlayer

Connect an AnimationTree to an AnimationPlayer and set up a simple state machine:

```gdscript
extends CharacterBody2D

@onready var animation_player: AnimationPlayer = $AnimationPlayer
@onready var animation_tree: AnimationTree = $AnimationTree
@onready var state_machine: AnimationNodeStateMachinePlayback = animation_tree.get("parameters/playback")

func _ready() -> void:
	# AnimationTree automatically connects to AnimationPlayer via anim_player property
	# Set in the editor or via code:
	animation_tree.anim_player = animation_player.get_path()
	animation_tree.active = true

func _physics_process(delta: float) -> void:
	# Travel to different states based on movement
	if velocity.length() > 0:
		state_machine.travel("walk")
	else:
		state_machine.travel("idle")
```

### 2. BlendSpace2D for Directional Movement

Use BlendSpace2D to blend animations based on movement direction:

```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var state_machine: AnimationNodeStateMachinePlayback = animation_tree.get("parameters/playback")

func _physics_process(delta: float) -> void:
	var input_vector: Vector2 = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")

	if input_vector.length() > 0:
		# Transition to movement state
		state_machine.travel("move")

		# Update BlendSpace2D parameters for 8-directional movement
		# Assumes BlendSpace2D is named "move" in the state machine
		animation_tree.set("parameters/move/blend_position", input_vector)

		velocity = input_vector.normalized() * 200.0
	else:
		state_machine.travel("idle")
		velocity = Vector2.ZERO

	move_and_slide()
```

### 3. One-Shot Animations for Actions

Trigger one-shot animations (attacks, jumps) that return to the previous state:

```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var state_machine: AnimationNodeStateMachinePlayback = animation_tree.get("parameters/playback")

var can_attack: bool = true

func _ready() -> void:
	animation_tree.active = true

func _unhandled_input(event: InputEvent) -> void:
	if event.is_action_pressed("attack") and can_attack:
		perform_attack()

func perform_attack() -> void:
	can_attack = false

	# Travel to one-shot attack animation
	state_machine.travel("attack")

	# Wait for animation to finish using a one-shot signal
	# Note: Set up a OneShot node in the AnimationTree for this
	animation_tree.animation_finished.connect(_on_attack_finished, CONNECT_ONE_SHOT)

func _on_attack_finished(anim_name: StringName) -> void:
	if anim_name == "attack":
		can_attack = true
		# AnimationTree automatically returns to previous state
		# if using a OneShot node, or manually travel back
		state_machine.travel("idle")
```

### 4. Accessing and Modifying Parameters

Read and write AnimationTree parameters for blend trees and transitions:

```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree

var is_crouching: bool = false
var aim_direction: Vector2 = Vector2.ZERO

func _physics_process(delta: float) -> void:
	# Set blend amount for crouch transition (0.0 = standing, 1.0 = crouching)
	var crouch_blend: float = animation_tree.get("parameters/crouch_blend/blend_amount")
	var target_blend: float = 1.0 if is_crouching else 0.0
	crouch_blend = move_toward(crouch_blend, target_blend, delta * 5.0)
	animation_tree.set("parameters/crouch_blend/blend_amount", crouch_blend)

	# Set aiming direction for IK or aim offset blending
	animation_tree.set("parameters/aim_direction/blend_position", aim_direction)

	# Set animation speed multiplier (e.g., for sprint)
	var is_sprinting: bool = Input.is_action_pressed("sprint")
	var time_scale: float = 1.5 if is_sprinting else 1.0
	animation_tree.set("parameters/TimeScale/scale", time_scale)

func toggle_crouch() -> void:
	is_crouching = not is_crouching

func update_aim_direction(direction: Vector2) -> void:
	aim_direction = direction.normalized()
```

### 5. Conditional State Transitions

Use conditions and auto-advance for complex state machine logic:

```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var state_machine: AnimationNodeStateMachinePlayback = animation_tree.get("parameters/playback")

var is_grounded: bool = true
var is_attacking: bool = false

func _ready() -> void:
	animation_tree.active = true

func _physics_process(delta: float) -> void:
	# Update condition parameters for automatic transitions
	# These match transition conditions set up in the AnimationTree editor
	animation_tree.set("parameters/conditions/is_grounded", is_grounded)
	animation_tree.set("parameters/conditions/is_attacking", is_attacking)
	animation_tree.set("parameters/conditions/is_moving", velocity.length() > 10.0)

	# Manual state transitions when needed
	if Input.is_action_just_pressed("jump") and is_grounded:
		state_machine.travel("jump")
		is_grounded = false

	# Check current state
	var current_state: StringName = state_machine.get_current_node()
	if current_state == "fall" and is_on_floor():
		is_grounded = true
		state_machine.travel("land")
```

## Tutorials

- [Using AnimationTree](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html)
- [Third Person Shooter (TPS) Demo](https://godotengine.org/asset-library/asset/2710)
