---
topic: enemy-ai
version: 2025.12.21
godot_version: "4.3"
sources:
  - godot_node_essentials
  - official-godot-docs
  - gdquest-tutorials
  - community-tutorials
---

# Enemy AI

Comprehensive patterns for implementing enemy behavior including detection, patrol, chase, attack, and navigation.

## Quick Start

```gdscript
# Basic chase enemy with detection area
extends CharacterBody2D

@export var speed: float = 300.0
@export var drag: float = 14.0

var _target: Node2D = null

func _physics_process(_delta: float) -> void:
    var desired_velocity := Vector2.ZERO

    if _target:
        var direction := global_position.direction_to(_target.global_position)
        desired_velocity = direction * speed

    var steering := desired_velocity - velocity
    velocity += steering / drag
    move_and_slide()

func _on_detection_area_body_entered(body: Node2D) -> void:
    _target = body

func _on_detection_area_body_exited(_body: Node2D) -> void:
    _target = null
```

## Detection Patterns

### Area-Based Detection

Simplest approach using Area2D/Area3D nodes:

```gdscript
# 2D enemy with circular detection
extends CharacterBody2D

var _target: CharacterBody2D = null

@onready var _detection_area: Area2D = %DetectionArea

func _ready() -> void:
    _detection_area.body_entered.connect(_on_detection_area_body_entered)
    _detection_area.body_exited.connect(_on_detection_area_body_exited)

func _on_detection_area_body_entered(body: Node2D) -> void:
    if body.is_in_group("player"):
        _target = body

func _on_detection_area_body_exited(_body: Node2D) -> void:
    _target = null
```

**Scene structure:**
```
Enemy (CharacterBody2D)
├── CollisionShape2D
├── Sprite2D
└── DetectionArea (Area2D)
    └── CollisionShape2D (CircleShape2D with large radius)
```

### Raycast Line-of-Sight Detection

More realistic detection that requires clear line of sight:

```gdscript
# 3D turret with raycast detection
extends Node3D

@export var target: Node3D = null
@export var ray_length: float = 50.0

var _is_targeting: bool = false

@onready var _ray_cast: RayCast3D = %RayCast3D

func _process(_delta: float) -> void:
    if target == null:
        return

    var target_position: Vector3 = target.global_position + Vector3.UP
    _ray_cast.look_at(target_position)

    var does_see_player: bool = (
        _ray_cast.is_colliding() and
        _ray_cast.get_collider() == target
    )

    _is_targeting = does_see_player
```

**Key differences:**
- Area detection: Triggers through walls, simpler to implement
- Raycast detection: Requires line of sight, more realistic behavior

## Chase Behavior

### Steering-Based Chase (2D)

Smooth steering behavior using velocity interpolation:

```gdscript
extends CharacterBody2D

@export var speed: float = 450.0
@export var drag: float = 14.0

var _target: Node2D = null

func _physics_process(_delta: float) -> void:
    var desired_velocity := Vector2.ZERO

    if _target:
        var direction := global_position.direction_to(_target.global_position)
        desired_velocity = direction * speed

    # Steering force creates smooth acceleration
    var steering := desired_velocity - velocity
    velocity += steering / drag

    # Orient to movement direction
    rotation = velocity.angle() + PI / 2
    move_and_slide()
```

### Direct Chase (3D)

Simpler approach that directly sets velocity:

```gdscript
extends CharacterBody3D

@export var speed: float = 6.0
@export var rotation_speed: float = 8.0

var _target: Node3D = null

@onready var _skin: Node3D = %RobotSkin3D

func _physics_process(delta: float) -> void:
    if _target == null:
        return

    var direction := global_position.direction_to(_target.global_position)
    direction.y = 0.0  # Keep movement on ground plane
    direction = direction.normalized()

    velocity = direction * speed
    move_and_slide()

    _orient_character_to_direction(delta, direction)

func _orient_character_to_direction(delta: float, direction: Vector3) -> void:
    if direction.is_zero_approx():
        return

    var left_axis := Vector3.UP.cross(direction)
    var rotation_basis := Basis(left_axis, Vector3.UP, direction).orthonormalized()
    _skin.basis = _skin.basis.orthonormalized().slerp(
        rotation_basis,
        delta * rotation_speed
    ).scaled(_skin.scale)
```

## Navigation & Pathfinding

### NavigationAgent2D Pattern

Use for enemies that need to navigate around obstacles:

```gdscript
class_name NavigationEnemy2D
extends CharacterBody2D

@export var player: Node2D = null
@export var speed: float = 350.0
@export var rotation_speed: float = 10.0

@onready var _navigation_agent: NavigationAgent2D = %NavigationAgent2D
@onready var _timer: Timer = %Timer

func _ready() -> void:
    if player == null:
        set_physics_process(false)
        return

    _timer.timeout.connect(_update_target_position)
    _update_target_position.call_deferred()

func _physics_process(delta: float) -> void:
    # Check if already reached target
    if _navigation_agent.is_navigation_finished():
        return

    var next_location := _navigation_agent.get_next_path_position()
    var direction := global_position.direction_to(next_location)

    velocity = direction * speed
    move_and_slide()

    _orient_character_to_direction(delta, direction)

func _update_target_position() -> void:
    # Update pathfinding with player's current location
    _navigation_agent.target_position = player.global_position

func _orient_character_to_direction(delta: float, direction: Vector2) -> void:
    rotation = lerp_angle(rotation, direction.angle() + PI / 2.0, 10.0 * delta)
```

**Setup requirements:**
1. Add NavigationRegion2D to level scene
2. Assign NavigationPolygon to NavigationRegion2D
3. Add NavigationAgent2D as child of enemy
4. Add Timer to update target position periodically (0.2-0.5 seconds)

### NavigationAgent3D Pattern

Similar pattern for 3D:

```gdscript
extends CharacterBody3D

@export var player: Node3D = null
@export var move_speed: float = 2.0
@export var rotation_speed: float = 8.0

@onready var _navigation_agent: NavigationAgent3D = %NavigationAgent3D
@onready var _skin: Node3D = %RobotSkin3D
@onready var _timer: Timer = %Timer

func _ready() -> void:
    if player == null:
        set_physics_process(false)
        return

    _timer.timeout.connect(_update_target_location)
    _update_target_location.call_deferred()

func _physics_process(delta: float) -> void:
    if _navigation_agent.is_navigation_finished():
        return

    var direction := global_position.direction_to(
        _navigation_agent.get_next_path_position()
    )
    direction.y = 0.0  # Keep on ground plane

    velocity = direction * move_speed
    move_and_slide()

    _orient_character_to_direction(delta, direction)

func _update_target_location() -> void:
    _navigation_agent.target_position = player.global_position

func _orient_character_to_direction(delta: float, direction: Vector3) -> void:
    if direction.is_zero_approx():
        return

    var left_axis := Vector3.UP.cross(direction)
    var rotation_basis := Basis(left_axis, Vector3.UP, direction).orthonormalized()
    _skin.basis = _skin.basis.orthonormalized().slerp(
        rotation_basis,
        delta * rotation_speed
    ).scaled(_skin.scale)
```

**Performance tip:** Use Timer (0.2-0.5s interval) to update target position instead of every frame.

## Patrol Patterns

### Wall-Bounce Patrol (2D)

Simple patrol that reverses direction when hitting walls:

```gdscript
extends CharacterBody2D

@export var speed: float = 300.0
@export var gravity: float = 4500.0

var _horizontal_direction: float = -1.0

@onready var _skin: Node2D = %RobotSkin2D

func _physics_process(delta: float) -> void:
    velocity.x = _horizontal_direction * speed
    velocity.y += gravity * delta

    move_and_slide()

    if is_on_wall():
        _horizontal_direction *= -1

    _skin.scale.x = _horizontal_direction
```

### Waypoint Patrol

Patrol between defined points:

```gdscript
extends CharacterBody2D

@export var patrol_points: Array[Marker2D] = []
@export var speed: float = 200.0
@export var wait_time: float = 2.0
@export var stopping_distance: float = 10.0

var _current_point_index: int = 0
var _is_waiting: bool = false

func _physics_process(delta: float) -> void:
    if _is_waiting or patrol_points.is_empty():
        return

    var target := patrol_points[_current_point_index].global_position
    var direction := global_position.direction_to(target)
    var distance := global_position.distance_to(target)

    if distance < stopping_distance:
        _reach_waypoint()
        return

    velocity = direction * speed
    move_and_slide()

func _reach_waypoint() -> void:
    _is_waiting = true
    velocity = Vector2.ZERO

    await get_tree().create_timer(wait_time).timeout

    _current_point_index = (_current_point_index + 1) % patrol_points.size()
    _is_waiting = false
```

## State Machine AI

Combine multiple behaviors using state machines:

```gdscript
# enemy_ai.gd
extends CharacterBody2D

enum State { PATROL, CHASE, ATTACK, RETREAT }

@export var patrol_speed: float = 100.0
@export var chase_speed: float = 200.0
@export var detection_range: float = 300.0
@export var attack_range: float = 50.0

var current_state: State = State.PATROL
var _target: Node2D = null
var _patrol_direction: float = 1.0

func _physics_process(delta: float) -> void:
    match current_state:
        State.PATROL:
            _state_patrol(delta)
        State.CHASE:
            _state_chase(delta)
        State.ATTACK:
            _state_attack(delta)
        State.RETREAT:
            _state_retreat(delta)

func _state_patrol(delta: float) -> void:
    velocity.x = _patrol_direction * patrol_speed

    if is_on_wall():
        _patrol_direction *= -1

    # Check for player in range
    if _target and global_position.distance_to(_target.global_position) < detection_range:
        _change_state(State.CHASE)

    move_and_slide()

func _state_chase(delta: float) -> void:
    if _target == null:
        _change_state(State.PATROL)
        return

    var distance := global_position.distance_to(_target.global_position)

    if distance < attack_range:
        _change_state(State.ATTACK)
        return
    elif distance > detection_range * 1.5:
        _change_state(State.PATROL)
        return

    var direction := global_position.direction_to(_target.global_position)
    velocity.x = direction.x * chase_speed
    move_and_slide()

func _state_attack(delta: float) -> void:
    if _target == null:
        _change_state(State.PATROL)
        return

    velocity = Vector2.ZERO

    var distance := global_position.distance_to(_target.global_position)
    if distance > attack_range:
        _change_state(State.CHASE)

    # Perform attack logic here
    look_at(_target.global_position)

func _state_retreat(delta: float) -> void:
    # Implement retreat behavior
    pass

func _change_state(new_state: State) -> void:
    current_state = new_state

    # Optional: emit signal or play animation
    match new_state:
        State.PATROL:
            pass  # Play patrol animation
        State.CHASE:
            pass  # Play run animation
        State.ATTACK:
            pass  # Play attack animation

func _on_detection_area_body_entered(body: Node2D) -> void:
    if body.is_in_group("player"):
        _target = body

func _on_detection_area_body_exited(body: Node2D) -> void:
    if body == _target:
        _target = null
```

See `reference/animation/state-machines.md` for node-based state machine patterns.

## Attack Patterns

### Direct Damage

Simple collision-based damage:

```gdscript
extends CharacterBody2D

@onready var _hit_box: Area2D = %HitBox

func _ready() -> void:
    _hit_box.body_entered.connect(_on_hit_box_body_entered)

func _on_hit_box_body_entered(body: Node2D) -> void:
    if body.has_method("take_damage"):
        body.take_damage()
```

### Turret Attack Pattern

Rotation-based aiming with cooldown patterns:

```gdscript
extends Node2D

const ATTACK_PATTERN_REPETITIONS := {
    "cooldown": 2,
    "burst": 3,
    "spray": 1
}

@export var player: Node2D = null

@onready var _shoot_animation_player: AnimationPlayer = %ShootAnimationPlayer
@onready var _pattern_animation_player: AnimationPlayer = %PatternAnimationPlayer
@onready var _launcher_marker: Marker2D = %LauncherMarker2D

func _ready() -> void:
    _pattern_animation_player.animation_finished.connect(_queue_shooting_pattern)
    _queue_shooting_pattern()

func _process(_delta: float) -> void:
    if player:
        look_at(player.global_position)

func _queue_shooting_pattern(_anim_name := &"") -> void:
    var animations: Array = ATTACK_PATTERN_REPETITIONS.keys()
    var key: String = animations.pick_random()
    var repeat: int = ATTACK_PATTERN_REPETITIONS[key]

    for _x in range(repeat):
        _pattern_animation_player.queue(key)

func shoot() -> void:
    _launcher_marker.fire()
    _shoot_animation_player.stop()
    _shoot_animation_player.play("shoot")
```

## Advanced Behaviors

### Jump Over Obstacles

Enemy that jumps when detecting obstacles ahead:

```gdscript
extends CharacterBody3D

@export var speed: float = 6.0
@export var jump_force: float = 6.0

var _target: Node3D = null

@onready var _ray_cast: RayCast3D = %RayCast3D
@onready var _gravity: float = -ProjectSettings.get_setting("physics/3d/default_gravity")

func _physics_process(delta: float) -> void:
    var direction := Vector3.ZERO

    if _target:
        direction = global_position.direction_to(_target.global_position)
        direction.y = 0.0
        direction = direction.normalized()

    var y_velocity := velocity.y
    if is_on_floor():
        y_velocity = 0.0
    else:
        y_velocity += _gravity * delta

    # Jump when obstacle detected
    if _ray_cast.is_colliding() and is_on_floor():
        y_velocity = jump_force

    velocity = direction * speed
    velocity.y = y_velocity
    move_and_slide()
```

### Boids/Flocking Behavior

Multiple enemies moving as a coordinated group:

```gdscript
# Basic boid separation for enemies
extends CharacterBody2D

@export var separation_weight: float = 0.5
@export var separation_distance: float = 100.0

var nearby_enemies: Array[Node2D] = []

func _physics_process(delta: float) -> void:
    var separation := Vector2.ZERO

    for enemy in nearby_enemies:
        var distance := global_position.distance_to(enemy.global_position)
        if distance < separation_distance and distance > 0:
            var away := global_position - enemy.global_position
            separation += away.normalized() / distance

    var desired_velocity := _get_base_movement()  # Chase/patrol logic
    desired_velocity += separation * separation_weight

    velocity = desired_velocity
    move_and_slide()

func _on_separation_area_body_entered(body: Node2D) -> void:
    if body.is_in_group("enemy") and body != self:
        nearby_enemies.append(body)

func _on_separation_area_body_exited(body: Node2D) -> void:
    nearby_enemies.erase(body)
```

### Visibility-Based AI

Enemy that only activates when on screen:

```gdscript
extends CharacterBody3D

@onready var _visibility_notifier: VisibleOnScreenNotifier3D = %VisibleOnScreenNotifier3D

func _ready() -> void:
    _visibility_notifier.screen_entered.connect(_on_screen_entered)
    _visibility_notifier.screen_exited.connect(_on_screen_exited)
    set_physics_process(false)

func _on_screen_entered() -> void:
    set_physics_process(true)

func _on_screen_exited() -> void:
    set_physics_process(false)
```

**Performance benefit:** Disables enemy logic when off-screen.

## Common Pitfalls

### Target Reference Loss

Always null-check target before using:

```gdscript
# Bad - crashes if target deleted
var direction := global_position.direction_to(_target.global_position)

# Good - safe null check
if _target and is_instance_valid(_target):
    var direction := global_position.direction_to(_target.global_position)
```

### Navigation Setup Issues

Common navigation problems:
- NavigationRegion2D/3D not baked
- Enemy not inside NavigationRegion bounds
- Collision layers blocking pathfinding
- Target position updated every frame (performance issue)

**Solution:** Use Timer to update navigation target every 0.2-0.5 seconds.

### Z-Fighting in 2D

Enemies at same position appear to flicker:

```gdscript
# Add slight Y offset for each enemy
func _ready() -> void:
    z_index = get_instance_id() % 100
```

### Stuck on Walls

Use small timer to detect stuck state:

```gdscript
var _stuck_timer: float = 0.0
var _last_position: Vector2

func _physics_process(delta: float) -> void:
    # Movement logic here

    if global_position.distance_to(_last_position) < 1.0:
        _stuck_timer += delta
        if _stuck_timer > 2.0:
            _handle_stuck_state()
    else:
        _stuck_timer = 0.0

    _last_position = global_position

func _handle_stuck_state() -> void:
    # Jump, change direction, or teleport
    _patrol_direction *= -1
    _stuck_timer = 0.0
```

## Best Practices

### Separate Logic from Visuals

Keep AI logic separate from rendering:

```
Enemy (CharacterBody2D)
├── EnemyAI (Node) - Logic only
├── Sprite2D - Rendering
├── AnimationPlayer - Visuals
└── CollisionShape2D - Physics
```

### Use Signals for Events

Decouple enemy death/damage from UI updates:

```gdscript
signal health_changed(new_health: int)
signal died

func take_damage(amount: int) -> void:
    health -= amount
    health_changed.emit(health)

    if health <= 0:
        died.emit()
        _die()
```

### Performance Optimization

- Use `distance_squared_to()` instead of `distance_to()` when comparing distances
- Pool enemies using object pooling for spawning
- Disable processing for off-screen enemies
- Update navigation targets with Timer, not every frame
- Use groups to find targets instead of storing references

### Configuration Over Code

Export enemy parameters for easy tuning:

```gdscript
@export_group("Movement")
@export var speed: float = 300.0
@export var rotation_speed: float = 8.0

@export_group("Detection")
@export var detection_range: float = 400.0
@export var attack_range: float = 100.0

@export_group("Behavior")
@export var patrol_speed: float = 150.0
@export var chase_speed: float = 250.0
```

## Related Patterns

- [State Machines](../animation/state-machines.md) - Organize complex AI behaviors
- [Navigation](../movement/navigation.md) - NavigationAgent setup details
- [Hitbox/Hurtbox](../physics/hitbox-hurtbox.md) - Damage system integration
- [Raycasting](../physics/raycasting.md) - Line-of-sight detection
- [Signals](../patterns/signals.md) - Event-driven AI communication

## Sources

1. **Official Godot Docs:** [Using NavigationAgents](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html)
2. **Official Godot Docs:** [2D Navigation Overview](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_introduction_2d.html)
3. **GDQuest Tutorial:** [Finite State Machine in Godot 4](https://www.gdquest.com/tutorial/godot/design-patterns/finite-state-machine/)
4. **Examples:** godot_node_essentials - robot_enemy_2d, robot_enemy_3d, navigation_ship_enemy_2d, turret implementations
