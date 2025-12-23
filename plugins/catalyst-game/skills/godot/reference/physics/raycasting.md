---
topic: raycasting
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/stable/tutorials/physics/ray-casting.html
  - https://docs.godotengine.org/en/stable/classes/class_raycast2d.html
  - https://docs.godotengine.org/en/stable/classes/class_raycast3d.html
  - https://docs.godotengine.org/en/stable/classes/class_physicsdirectspacestate2d.html
  - https://docs.godotengine.org/en/stable/classes/class_physicsdirectspacestate3d.html
  - repos/godot_node_essentials/screens/ray_cast_2d/
  - repos/godot_node_essentials/screens/ray_cast_3d/
---

# Raycasting

Cast rays to detect collisions for line of sight, shooting, ground detection, and more.

## Two Approaches {#approaches}

Godot provides two ways to raycast:

| Method | Use Case |
|--------|----------|
| **RayCast Node** | Continuous checks (e.g., ground detection, persistent line of sight) |
| **Direct Space Query** | One-time checks (e.g., mouse picking, hitscan shooting) |

## RayCast Nodes {#raycast-nodes}

### Basic Setup (2D)

```gdscript
extends Node2D

@onready var ray_cast: RayCast2D = $RayCast2D

func _ready() -> void:
    # Set where the ray points (relative to node)
    ray_cast.target_position = Vector2(100, 0)  # 100 pixels right
    ray_cast.enabled = true

    # Optional: set collision mask (what layers to detect)
    ray_cast.collision_mask = 0b101  # Layers 1 and 3

func _physics_process(delta: float) -> void:
    if ray_cast.is_colliding():
        var collision_point: Vector2 = ray_cast.get_collision_point()
        var collision_normal: Vector2 = ray_cast.get_collision_normal()
        var collider: Object = ray_cast.get_collider()

        if collider.is_in_group("enemy"):
            print("Enemy detected!")
```

### Basic Setup (3D)

```gdscript
extends Node3D

@onready var ray_cast: RayCast3D = $RayCast3D

func _ready() -> void:
    ray_cast.target_position = Vector3(0, -10, 0)  # 10 units down
    ray_cast.enabled = true
    ray_cast.collision_mask = 1  # Layer 1 only

func _physics_process(delta: float) -> void:
    if ray_cast.is_colliding():
        var collision_point: Vector3 = ray_cast.get_collision_point()
        var collision_normal: Vector3 = ray_cast.get_collision_normal()
        var collider: Object = ray_cast.get_collider()
```

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `enabled` | bool | Enable/disable raycasting |
| `target_position` | Vector2/3 | Where ray points (local coordinates) |
| `collision_mask` | int | Which physics layers to detect |
| `exclude_parent` | bool | Ignore parent body (default: true) |
| `hit_from_inside` | bool | Detect collisions when starting inside |
| `hit_back_faces` | bool | Detect backfaces of meshes (3D only) |

### Key Methods

```gdscript
# Check if currently colliding
if ray_cast.is_colliding():
    # Get collision details
    var point: Vector3 = ray_cast.get_collision_point()
    var normal: Vector3 = ray_cast.get_collision_normal()
    var collider: Object = ray_cast.get_collider()
    var collider_rid: RID = ray_cast.get_collider_rid()
    var shape_index: int = ray_cast.get_collider_shape()

# Force update (normally automatic in _physics_process)
ray_cast.force_raycast_update()

# Add exceptions (objects to ignore)
ray_cast.add_exception(body_to_ignore)
ray_cast.remove_exception(body)
ray_cast.clear_exceptions()
```

## Line of Sight (Single Ray) {#line-of-sight}

### 2D Turret Tracking

```gdscript
extends Node2D

@export var target: Node2D = null

var _has_line_of_sight: bool = false

@onready var ray_cast: RayCast2D = %RayCast2D

func _physics_process(delta: float) -> void:
    if target == null:
        return

    # Point ray at target
    look_at(target.global_position)

    # Check if we can see the target
    var can_see: bool = ray_cast.get_collider() == target

    if can_see != _has_line_of_sight:
        _has_line_of_sight = can_see
        if _has_line_of_sight:
            print("Target acquired!")
        else:
            print("Lost target")
```

### 3D Enemy Vision

```gdscript
extends Node3D

@export var player: Node3D = null
@export var vision_range: float = 10.0

@onready var ray_cast: RayCast3D = %RayCast3D

func _ready() -> void:
    ray_cast.target_position = Vector3(0, 0, -vision_range)

func _physics_process(delta: float) -> void:
    if player == null:
        return

    # Look at player
    look_at(player.global_position, Vector3.UP)

    # Check if player is visible
    if ray_cast.is_colliding():
        var hit: Object = ray_cast.get_collider()
        if hit == player:
            _attack_player()
```

## Multi-Ray Vision Cone {#vision-cone}

Create cone of vision using multiple rays:

### 2D Vision Cone

```gdscript
extends Node2D

@export var target: Node2D = null
@export var vision_range: float = 600.0
@export var rays_amount: int = 5
@export var rays_angle_interval: float = deg_to_rad(3.0)

var _rays: Array[RayCast2D] = []

func _ready() -> void:
    _create_rays()

func _create_rays() -> void:
    # Create rays in a cone pattern
    for i in range(-rays_amount / 2, rays_amount / 2 + 1):
        var ray_cast := RayCast2D.new()
        add_child(ray_cast)

        var angle: float = i * rays_angle_interval
        ray_cast.target_position = Vector2.RIGHT.rotated(angle) * vision_range

        # Detect player (layer 1) and obstacles (layer 3)
        ray_cast.collision_mask = 0b101

        _rays.append(ray_cast)

func _physics_process(delta: float) -> void:
    if target == null:
        return

    # Aim at target
    look_at(target.global_position)

    # Check if any ray sees the target
    var target_visible: bool = false
    for ray_cast: RayCast2D in _rays:
        if ray_cast.get_collider() == target:
            target_visible = true
            break
```

### 3D Vision Cone

```gdscript
extends Node3D

@export var target: Node3D = null
@export var ray_length: float = 8.0
@export var horizontal_ray_count: int = 3
@export var vertical_ray_count: int = 3
@export var horizontal_angle_interval: float = 2.0
@export var vertical_angle_interval: float = 2.0

@onready var ray_marker: Node3D = %RayCastMarker3D

func _ready() -> void:
    _generate_raycast_nodes()

func _generate_raycast_nodes() -> void:
    for v_layer in range(vertical_ray_count):
        for h_layer in range(horizontal_ray_count):
            var ray_cast := RayCast3D.new()
            ray_marker.add_child(ray_cast)

            # Center rays around 0
            var h_mult: float = remap(
                h_layer, 0.0, horizontal_ray_count,
                -horizontal_ray_count / 2.0, horizontal_ray_count / 2.0 + 1.0
            )
            var v_mult: float = remap(
                v_layer, 0.0, vertical_ray_count,
                -vertical_ray_count / 2.0, vertical_ray_count / 2.0 + 1.0
            )

            # Rotate rays to form cone
            ray_cast.rotate_y(deg_to_rad(horizontal_angle_interval) * h_mult)
            ray_cast.rotate_x(deg_to_rad(vertical_angle_interval) * v_mult)
            ray_cast.target_position = Vector3.FORWARD * ray_length
            ray_cast.collision_mask = 3  # Layers 1 and 2

func _is_seeing_target() -> bool:
    for ray_cast: RayCast3D in ray_marker.get_children():
        if ray_cast.is_colliding() and ray_cast.get_collider() == target:
            return true
    return false
```

## Ground Detection {#ground-detection}

Check if character is on floor:

```gdscript
extends RigidBody2D

@onready var ray_cast: RayCast2D = %RayCast2D

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    var gravity_direction: Vector2 = state.total_gravity.normalized()

    # Point ray toward gravity
    ray_cast.rotation = gravity_direction.angle()

    # Check if on floor
    if _is_on_floor(gravity_direction) and Input.is_action_just_pressed("jump"):
        state.apply_central_impulse(-gravity_direction * jump_strength)

func _is_on_floor(gravity: Vector2) -> bool:
    return ray_cast.is_colliding()
```

## Direct Space Queries {#direct-space}

For one-time raycasts (shooting, mouse picking):

### 2D Raycast Query

```gdscript
extends Node2D

func shoot_ray(from: Vector2, to: Vector2) -> Dictionary:
    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state

    var query := PhysicsRayQueryParameters2D.create(from, to)
    query.collision_mask = 0b111  # Layers 1, 2, 3
    query.exclude = [self]  # Don't hit ourselves

    var result: Dictionary = space_state.intersect_ray(query)
    return result

func _input(event: InputEvent) -> void:
    if event.is_action_pressed("shoot"):
        var from: Vector2 = global_position
        var to: Vector2 = get_global_mouse_position()

        var result: Dictionary = shoot_ray(from, to)
        if result:
            print("Hit: ", result.collider)
            print("Position: ", result.position)
            print("Normal: ", result.normal)
```

### 3D Raycast Query

```gdscript
extends Node3D

@onready var camera: Camera3D = %Camera3D

func _input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        var result: Dictionary = _raycast_from_mouse()
        if result:
            print("Hit: ", result.collider)
            print("Position: ", result.position)
            print("Normal: ", result.normal)

func _raycast_from_mouse() -> Dictionary:
    var mouse_pos: Vector2 = get_viewport().get_mouse_position()

    # Convert screen position to 3D ray
    var from: Vector3 = camera.project_ray_origin(mouse_pos)
    var to: Vector3 = from + camera.project_ray_normal(mouse_pos) * 1000.0

    var space_state: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
    var query := PhysicsRayQueryParameters3D.create(from, to)

    return space_state.intersect_ray(query)
```

### Query Result Dictionary

```gdscript
# Result dictionary contains:
if result:
    var position: Vector3 = result.position          # Hit point in world coords
    var normal: Vector3 = result.normal              # Surface normal
    var collider: Object = result.collider           # Object that was hit
    var collider_id: int = result.collider_id        # Instance ID
    var rid: RID = result.rid                        # Physics RID
    var shape: int = result.shape                    # Shape index hit
    var face_index: int = result.face_index          # Triangle index (3D)
else:
    print("Ray didn't hit anything")
```

### Advanced Query Parameters

```gdscript
func create_custom_query(from: Vector3, to: Vector3) -> Dictionary:
    var query := PhysicsRayQueryParameters3D.create(from, to)

    # Collision filtering
    query.collision_mask = 0b1110  # Layers 2, 3, 4
    query.exclude = [self, weapon]  # Bodies to ignore

    # Collision detection options
    query.hit_from_inside = false   # Ignore if starting inside
    query.hit_back_faces = true     # Detect backfaces
    query.collide_with_bodies = true
    query.collide_with_areas = false

    var space_state: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
    return space_state.intersect_ray(query)
```

## Hitscan Shooting {#hitscan}

Instant-hit weapons (lasers, bullets):

```gdscript
extends Node2D

@export var damage: int = 25
@export var max_range: float = 1000.0

func shoot(from: Vector2, direction: Vector2) -> void:
    var to: Vector2 = from + direction.normalized() * max_range

    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state
    var query := PhysicsRayQueryParameters2D.create(from, to)
    query.collision_mask = 0b11  # Layers 1 and 2

    var result: Dictionary = space_state.intersect_ray(query)

    if result:
        var hit_point: Vector2 = result.position
        var hit_body: Node2D = result.collider

        # Visual feedback
        _draw_shot_line(from, hit_point)
        _spawn_impact_effect(hit_point, result.normal)

        # Apply damage
        if hit_body.has_method("take_damage"):
            hit_body.take_damage(damage)
```

## Collision Layer Filtering {#layers}

Control what rays detect:

```gdscript
# Binary notation for layers
const LAYER_WORLD: int = 1 << 0      # Layer 1 (0b1)
const LAYER_PLAYER: int = 1 << 1     # Layer 2 (0b10)
const LAYER_ENEMY: int = 1 << 2      # Layer 3 (0b100)
const LAYER_PROJECTILE: int = 1 << 3 # Layer 4 (0b1000)

func setup_vision_ray() -> void:
    # See players and enemies, ignore projectiles
    ray_cast.collision_mask = LAYER_PLAYER | LAYER_ENEMY

func setup_ground_ray() -> void:
    # Only detect world geometry
    ray_cast.collision_mask = LAYER_WORLD

func set_collision_mask_layers(layers: Array[int]) -> void:
    var mask: int = 0
    for layer in layers:
        mask |= (1 << (layer - 1))
    ray_cast.collision_mask = mask
```

## Common Patterns

### Laser Sight

```gdscript
extends Line2D

@onready var ray_cast: RayCast2D = %RayCast2D

func _physics_process(delta: float) -> void:
    clear_points()

    var start: Vector2 = Vector2.ZERO
    var end: Vector2 = ray_cast.target_position

    if ray_cast.is_colliding():
        end = ray_cast.get_collision_point() - ray_cast.global_position

    add_point(start)
    add_point(end)
```

### Edge Detection

```gdscript
extends CharacterBody2D

@onready var edge_ray: RayCast2D = %EdgeDetectionRay

func _physics_process(delta: float) -> void:
    # Point ray down and forward
    edge_ray.target_position = Vector2(20, 30)

    if is_on_floor() and not edge_ray.is_colliding():
        # At edge of platform - turn around
        velocity.x *= -1
```

### Wall Detection

```gdscript
extends CharacterBody2D

@onready var wall_ray: RayCast2D = %WallRay

func _physics_process(delta: float) -> void:
    if wall_ray.is_colliding():
        var normal: Vector2 = wall_ray.get_collision_normal()
        # Slide along wall
        velocity = velocity.slide(normal)
```

## Performance Tips {#performance}

1. **Disable when not needed**: Set `enabled = false` to skip checks
2. **Use collision masks**: Only check relevant layers
3. **Limit ray count**: For vision cones, use minimum rays needed
4. **One-time checks**: Use direct space queries instead of nodes
5. **Group checks**: Update multiple rays in batches

```gdscript
# Good: Enable only when needed
func _on_player_entered_detection_zone() -> void:
    ray_cast.enabled = true

func _on_player_exited_detection_zone() -> void:
    ray_cast.enabled = false

# Good: Use direct queries for infrequent checks
func check_mouse_hover() -> void:
    if Input.is_action_just_pressed("click"):
        var result: Dictionary = _raycast_from_mouse()
        # Process result...
```

## Debugging Raycasts {#debug}

Visualize rays for debugging:

```gdscript
extends Node2D

@onready var ray_cast: RayCast2D = $RayCast2D

func _draw() -> void:
    var target: Vector2 = ray_cast.target_position
    var color: Color = Color.GREEN if ray_cast.is_colliding() else Color.RED

    if ray_cast.is_colliding():
        var collision_point: Vector2 = ray_cast.get_collision_point() - global_position
        draw_line(Vector2.ZERO, collision_point, Color.RED, 2.0)
        draw_circle(collision_point, 5.0, Color.YELLOW)
    else:
        draw_line(Vector2.ZERO, target, color, 2.0)

func _physics_process(delta: float) -> void:
    queue_redraw()  # Update debug drawing
```

## Common Issues {#troubleshooting}

### Ray not detecting Area nodes

```gdscript
# Areas are not detected by default
var query := PhysicsRayQueryParameters3D.create(from, to)
query.collide_with_areas = true  # Enable area detection
query.collide_with_bodies = false  # Optional: only detect areas
```

### Ray hitting parent

```gdscript
# Solution 1: Use exclude_parent (default: true)
ray_cast.exclude_parent = true

# Solution 2: Add explicit exception
ray_cast.add_exception(get_parent())

# Solution 3: Use different layers
# Put parent on layer 1, ray mask only checks layer 2+
```

### Ray not updating

```gdscript
# RayCasts update in physics frame, not process frame
func _physics_process(delta: float) -> void:  # Correct
    if ray_cast.is_colliding():
        # ...

# For immediate update (use sparingly)
ray_cast.force_raycast_update()
```

### Collision mask confusion

```gdscript
# WRONG: Collision layer (what object IS)
ray_cast.collision_layer = 2  # This does nothing!

# CORRECT: Collision mask (what object DETECTS)
ray_cast.collision_mask = 2  # Check layer 2
```
