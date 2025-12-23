---
topic: state-machines
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-state-machine
  - godot-animation-tree
---

# State Machines

State machine patterns for character behavior, AI, and game logic.

## Basic State Machine {#basic}

Simple enum-based state machine:

```gdscript
extends CharacterBody2D

enum State { IDLE, RUN, JUMP, FALL }

var current_state: State = State.IDLE

func _physics_process(delta: float) -> void:
    match current_state:
        State.IDLE:
            _state_idle(delta)
        State.RUN:
            _state_run(delta)
        State.JUMP:
            _state_jump(delta)
        State.FALL:
            _state_fall(delta)

func _state_idle(delta: float) -> void:
    velocity.x = 0

    if not is_on_floor():
        _change_state(State.FALL)
    elif Input.is_action_just_pressed("jump"):
        _change_state(State.JUMP)
    elif Input.get_axis("move_left", "move_right") != 0:
        _change_state(State.RUN)

func _state_run(delta: float) -> void:
    velocity.x = Input.get_axis("move_left", "move_right") * speed

    if not is_on_floor():
        _change_state(State.FALL)
    elif Input.is_action_just_pressed("jump"):
        _change_state(State.JUMP)
    elif velocity.x == 0:
        _change_state(State.IDLE)

func _state_jump(delta: float) -> void:
    velocity.x = Input.get_axis("move_left", "move_right") * speed
    velocity.y += gravity * delta

    if velocity.y > 0:
        _change_state(State.FALL)

func _state_fall(delta: float) -> void:
    velocity.x = Input.get_axis("move_left", "move_right") * speed
    velocity.y += gravity * delta

    if is_on_floor():
        _change_state(State.IDLE)

func _change_state(new_state: State) -> void:
    current_state = new_state
    # Could emit signal or play animation here
```

## Node-Based State Machine

More scalable pattern with separate state nodes:

### StateMachine Node

```gdscript
# state_machine.gd
class_name StateMachine
extends Node

@export var initial_state: State

var current_state: State
var states: Dictionary = {}

func _ready() -> void:
    for child in get_children():
        if child is State:
            states[child.name.to_lower()] = child
            child.state_machine = self
            child.process_mode = Node.PROCESS_MODE_DISABLED

    if initial_state:
        change_state(initial_state.name)

func _physics_process(delta: float) -> void:
    if current_state:
        current_state.physics_update(delta)

func _process(delta: float) -> void:
    if current_state:
        current_state.update(delta)

func change_state(state_name: String) -> void:
    var new_state := states.get(state_name.to_lower()) as State
    if new_state == null or new_state == current_state:
        return

    if current_state:
        current_state.exit()
        current_state.process_mode = Node.PROCESS_MODE_DISABLED

    current_state = new_state
    current_state.process_mode = Node.PROCESS_MODE_INHERIT
    current_state.enter()
```

### State Base Class

```gdscript
# state.gd
class_name State
extends Node

var state_machine: StateMachine

func enter() -> void:
    pass

func exit() -> void:
    pass

func update(_delta: float) -> void:
    pass

func physics_update(_delta: float) -> void:
    pass
```

### Example State Implementation

```gdscript
# idle_state.gd
extends State

@onready var player: CharacterBody2D = owner

func enter() -> void:
    player.velocity.x = 0
    player.animation_player.play("idle")

func physics_update(delta: float) -> void:
    if not player.is_on_floor():
        state_machine.change_state("fall")
    elif Input.is_action_just_pressed("jump"):
        state_machine.change_state("jump")
    elif Input.get_axis("move_left", "move_right") != 0:
        state_machine.change_state("run")

    player.move_and_slide()
```

### Scene Structure

```
CharacterBody2D (player)
├── CollisionShape2D
├── AnimatedSprite2D
├── AnimationPlayer
└── StateMachine
    ├── Idle (State)
    ├── Run (State)
    ├── Jump (State)
    └── Fall (State)
```

## Hierarchical State Machine {#hierarchical}

States containing sub-states:

```gdscript
# ground_state.gd - Parent state
extends State

var sub_state_machine: StateMachine

func _ready() -> void:
    sub_state_machine = $SubStateMachine

func enter() -> void:
    sub_state_machine.change_state("idle")

func physics_update(delta: float) -> void:
    # Check for transitions to non-ground states
    if not owner.is_on_floor():
        state_machine.change_state("air")
    elif Input.is_action_just_pressed("attack"):
        state_machine.change_state("attack")
    else:
        # Let sub-state handle ground movement
        sub_state_machine.current_state.physics_update(delta)
```

## Push/Pop State Stack {#stack}

For interruptible states:

```gdscript
class_name StackStateMachine
extends Node

var state_stack: Array[State] = []

func push_state(state_name: String) -> void:
    var new_state := states.get(state_name.to_lower()) as State
    if new_state == null:
        return

    if not state_stack.is_empty():
        state_stack[-1].pause()

    state_stack.push_back(new_state)
    new_state.enter()

func pop_state() -> void:
    if state_stack.is_empty():
        return

    var old_state := state_stack.pop_back()
    old_state.exit()

    if not state_stack.is_empty():
        state_stack[-1].resume()
```

**Use case:** Player gets stunned mid-attack, then returns to attack state after stun ends.

## Animation State Machine

Using AnimationTree for animation-driven states:

```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var state_machine: AnimationNodeStateMachinePlayback = animation_tree["parameters/playback"]

func _physics_process(delta: float) -> void:
    # Transition based on conditions
    if is_on_floor():
        if velocity.x != 0:
            state_machine.travel("run")
        else:
            state_machine.travel("idle")
    else:
        if velocity.y < 0:
            state_machine.travel("jump")
        else:
            state_machine.travel("fall")
```

See `reference/animation/animation-tree.md` for full AnimationTree patterns.

## AI State Machine

Enemy behavior states:

```gdscript
# patrol_state.gd
extends State

@export var patrol_speed: float = 100.0
@export var detection_range: float = 200.0

@onready var enemy: CharacterBody2D = owner
@onready var raycast: RayCast2D = owner.get_node("DetectionRay")

var patrol_direction: float = 1.0

func physics_update(delta: float) -> void:
    # Move in patrol direction
    enemy.velocity.x = patrol_direction * patrol_speed

    # Turn at walls or edges
    if enemy.is_on_wall():
        patrol_direction *= -1

    # Check for player
    raycast.target_position.x = detection_range * patrol_direction
    if raycast.is_colliding():
        var collider := raycast.get_collider()
        if collider.is_in_group("player"):
            state_machine.change_state("chase")

    enemy.move_and_slide()

# chase_state.gd
extends State

@export var chase_speed: float = 200.0
@export var attack_range: float = 50.0

@onready var enemy: CharacterBody2D = owner
var target: Node2D

func enter() -> void:
    target = get_tree().get_first_node_in_group("player")

func physics_update(delta: float) -> void:
    if target == null:
        state_machine.change_state("patrol")
        return

    var direction := (target.global_position - enemy.global_position).normalized()
    enemy.velocity.x = direction.x * chase_speed

    var distance := enemy.global_position.distance_to(target.global_position)
    if distance < attack_range:
        state_machine.change_state("attack")
    elif distance > 400:  # Lost player
        state_machine.change_state("patrol")

    enemy.move_and_slide()
```
