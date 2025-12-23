---
topic: navigation-pathfinding
version: 2025.12.21
godot_version: "4.3"
sources:
  - repos/godot_node_essentials/screens/navigation_2d/
  - repos/godot_node_essentials/screens/navigation_3d/
  - https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html
  - https://docs.godotengine.org/en/stable/classes/class_navigationagent2d.html
  - https://docs.godotengine.org/en/stable/classes/class_astar2d.html
---

# Navigation and Pathfinding

NavigationAgent2D/3D for AI pathfinding and AStar2D/3D for custom grid-based pathfinding.

## NavigationAgent2D (Basic Setup) {#navigationagent2d-basic}

AI enemy that follows a target using pathfinding:

```gdscript
extends CharacterBody2D

@export var player: CharacterBody2D = null
@export var speed: float = 350.0

@onready var _navigation_agent: NavigationAgent2D = $NavigationAgent2D
@onready var _timer: Timer = $Timer

func _ready() -> void:
    if player == null:
        set_physics_process(false)
        return

    _timer.timeout.connect(_update_target_position)
    _update_target_position.call_deferred()

func _physics_process(delta: float) -> void:
    if _navigation_agent.is_navigation_finished():
        return

    var next_location: Vector2 = _navigation_agent.get_next_path_position()
    var direction := global_position.direction_to(next_location)
    velocity = direction * speed
    move_and_slide()

func _update_target_position() -> void:
    _navigation_agent.target_position = player.global_position
```

**Key Points:**
- Use `call_deferred()` for first target update to ensure navigation map is ready
- Check `is_navigation_finished()` before moving to prevent jittering
- Update target periodically with Timer, not every frame (expensive)

## NavigationAgent3D (Basic Setup) {#navigationagent3d-basic}

3D enemy that follows player on a navigation mesh:

```gdscript
extends CharacterBody3D

@export var player: CharacterBody3D = null
@export var move_speed: float = 2.0
@export var rotation_speed: float = 8.0

@onready var _navigation_agent: NavigationAgent3D = $NavigationAgent3D
@onready var _skin: Node3D = $Skin
@onready var _timer: Timer = $Timer

func _ready() -> void:
    if player == null:
        set_physics_process(false)
        return

    _timer.timeout.connect(_update_target_location)
    _update_target_location.call_deferred()

func _physics_process(delta: float) -> void:
    if _navigation_agent.is_navigation_finished():
        return

    var direction := global_position.direction_to(_navigation_agent.get_next_path_position())
    direction.y = 0.0  # Keep movement on horizontal plane
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
    _skin.basis = _skin.basis.orthonormalized().slerp(rotation_basis, delta * rotation_speed).scaled(_skin.scale)
```

**3D Rotation Tips:**
- Rotate a child `skin` node, not the CharacterBody3D root (prevents physics conflicts)
- Use `slerp()` for smooth 3D rotation interpolation
- Zero out Y direction if movement should stay on horizontal plane

## NavigationAgent with Avoidance {#avoidance}

Enable collision avoidance between multiple agents:

```gdscript
extends CharacterBody3D

@export var target: CharacterBody3D = null
@export var move_speed: float = 2.0
@export var acceleration: float = 14.0

@onready var _navigation_agent: NavigationAgent3D = $NavigationAgent3D

func _ready() -> void:
    # Connect avoidance signal
    _navigation_agent.velocity_computed.connect(_on_velocity_computed)
    _update_target_location.call_deferred()

func _physics_process(delta: float) -> void:
    if _navigation_agent.is_navigation_finished():
        return

    var direction := (_navigation_agent.get_next_path_position() - global_position).normalized()
    direction.y = 0.0

    # Set desired velocity (NavigationServer computes safe velocity)
    _navigation_agent.velocity = velocity.lerp(direction * move_speed, acceleration * delta)

func _on_velocity_computed(safe_velocity: Vector3) -> void:
    # Use safe velocity computed by NavigationServer
    velocity = safe_velocity
    move_and_slide()
```

**Avoidance Setup:**
1. Connect `velocity_computed` signal
2. Set `_navigation_agent.velocity` to desired velocity
3. Use `safe_velocity` from signal for actual movement
4. Configure avoidance layers/masks in inspector

**Inspector Settings:**
- `Avoidance Enabled`: true
- `Avoidance Layers`: Which layers this agent belongs to
- `Avoidance Mask`: Which layers this agent avoids
- `Radius`: Agent collision radius

## Grid Navigation (Click to Move) {#grid-navigation}

Click on grid to move character to location:

```gdscript
extends Node2D

@onready var _player: CharacterBody2D = $Player
@onready var _cursor: Sprite2D = $Cursor
@onready var _camera: Camera2D = $Camera2D
@onready var _navigation_region: NavigationRegion2D = $NavigationRegion2D

@onready var _map: RID = _navigation_region.get_navigation_map()

func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        # Snap cursor to nearest navigation point
        var mouse_pos := get_local_mouse_position()
        _cursor.position = NavigationServer2D.map_get_closest_point(_map, mouse_pos)

    elif Input.is_action_just_pressed("click"):
        _player.set_destination(_cursor.position)
```

**Player Script:**

```gdscript
extends Sprite2D

@export var speed: float = 350.0

@onready var _navigation_agent: NavigationAgent2D = $NavigationAgent2D

func _ready() -> void:
    set_physics_process(false)

func _physics_process(delta: float) -> void:
    var next_location: Vector2 = _navigation_agent.get_next_path_position()
    var direction := (next_location - global_position).normalized()
    translate(direction * speed * delta)

    if _navigation_agent.is_navigation_finished():
        set_physics_process(false)

func set_destination(target: Vector2) -> void:
    _navigation_agent.target_position = target
    set_physics_process(true)
```

## Dynamic Obstacles {#dynamic-obstacles}

Enable/disable navigation regions at runtime:

```gdscript
extends Node2D

@export var west_door: StaticBody2D = null
@export var north_door: StaticBody2D = null

@onready var _door_map := {
    west_door: $WestNavigationRegion2D,
    north_door: $NorthNavigationRegion2D,
}

func _ready() -> void:
    # Open west door initially
    west_door.activate()
    _door_map[west_door].enabled = true

func activate_all_doors() -> void:
    for door in _door_map:
        door.activate()
        _door_map[door].enabled = door.is_activated
```

**Key Points:**
- Set `NavigationRegion2D/3D.enabled` to add/remove from navigation map
- Changes take effect immediately
- Existing paths are NOT recalculated automatically
- Call `target_position = target_position` to force path recalculation

## AStar2D Grid Pathfinding {#astar2d}

Manual pathfinding using AStar2D for grid-based games:

```gdscript
extends Node2D

const DIRECTIONS := [Vector2i.RIGHT, Vector2i.DOWN]

var _astar := AStar2D.new()
var _tile_map_rect := Rect2i()

@onready var _tile_map_layer: TileMapLayer = $TileMapLayer

func _ready() -> void:
    _initialize_astar_graph()

func _initialize_astar_graph() -> void:
    _tile_map_rect = _tile_map_layer.get_used_rect()

    # Add all walkable points
    for x in range(_tile_map_rect.size.x):
        for y in range(_tile_map_rect.size.y):
            var point := Vector2i(x, y)
            if not point in _tile_map_layer.get_used_cells():
                var point_index := _xy_to_index(point)
                _astar.add_point(point_index, point)

    # Connect adjacent points (bi-directional)
    for point1_index in _astar.get_point_ids():
        var point1 := _index_to_xy(point1_index)
        for offset in DIRECTIONS:
            var point2: Vector2i = point1 + offset
            var point2_index := _xy_to_index(point2)
            if _astar.has_point(point2_index):
                _astar.connect_points(point1_index, point2_index)

func find_path_to(mouse_position: Vector2) -> PackedVector2Array:
    var start_index := _xy_to_index(_tile_map_layer.local_to_map(_player.position))
    var finish_index := _xy_to_index(_tile_map_layer.local_to_map(mouse_position))

    if _astar.has_point(start_index) and _astar.has_point(finish_index):
        return _astar.get_point_path(start_index, finish_index)

    return PackedVector2Array()

# Convert grid coords to 1D index
func _xy_to_index(offset: Vector2i) -> int:
    return int(offset.x + _tile_map_rect.size.x * offset.y)

# Convert 1D index to grid coords
func _index_to_xy(index: int) -> Vector2i:
    return Vector2i(index % _tile_map_rect.size.x, index / _tile_map_rect.size.x)
```

**AStar2D Workflow:**
1. `add_point(id, position)` - Add walkable cells
2. `connect_points(id1, id2)` - Connect adjacent cells (bi-directional by default)
3. `get_point_path(start_id, end_id)` - Get path as array of positions
4. Convert grid coordinates ↔ unique IDs for lookups

## AStarGrid2D (Simplified) {#astargrid2d}

New in Godot 4 - easier grid pathfinding:

```gdscript
var _astar_grid := AStarGrid2D.new()

func _ready() -> void:
    _astar_grid.region = Rect2i(0, 0, 32, 32)
    _astar_grid.cell_size = Vector2(16, 16)
    _astar_grid.diagonal_mode = AStarGrid2D.DIAGONAL_MODE_NEVER
    _astar_grid.update()

    # Set obstacles
    for cell in _tile_map_layer.get_used_cells():
        _astar_grid.set_point_solid(cell, true)

func find_path(from: Vector2, to: Vector2) -> PackedVector2Array:
    var start_cell := Vector2i(from / 16)
    var end_cell := Vector2i(to / 16)
    return _astar_grid.get_point_path(start_cell, end_cell)
```

**AStarGrid2D vs AStar2D:**
- ✅ No need to manually add points and connections
- ✅ Built-in grid coordinate handling
- ✅ Faster setup for uniform grids
- ❌ Cannot handle non-uniform costs per cell
- ❌ Grid-only (cannot handle arbitrary graphs)

## NavigationServer (Advanced) {#navigationserver}

Direct NavigationServer access for advanced use cases:

```gdscript
# Get closest point on navigation mesh
var map_rid: RID = _navigation_region.get_navigation_map()
var closest_point := NavigationServer2D.map_get_closest_point(map_rid, world_position)

# Check if point is on navigation mesh
var is_on_navmesh := NavigationServer2D.map_is_point_on_navmesh(map_rid, world_position)

# Get navigation path directly (without agent)
var path := NavigationServer2D.map_get_path(map_rid, start_pos, end_pos, true)
```

## Scene Setup

### NavigationAgent2D Setup

```
Node2D or CharacterBody2D (root)
├── NavigationAgent2D
├── CollisionShape2D (if CharacterBody2D)
├── Sprite2D
└── Timer (for periodic target updates)

Scene Root
└── NavigationRegion2D
    └── TileMapLayer or Polygon2D (navigation mesh)
```

### NavigationAgent3D Setup

```
CharacterBody3D (root)
├── NavigationAgent3D
├── CollisionShape3D
└── Skin (Node3D - rotated for facing direction)

Scene Root
└── NavigationRegion3D
    └── MeshInstance3D (baked navigation mesh)
```

## Common Properties {#properties}

### NavigationAgent2D/3D Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `target_position` | Vector2/3 | (0,0,0) | Destination point for pathfinding |
| `path_desired_distance` | float | 1.0 | Distance to waypoint to consider "reached" |
| `target_desired_distance` | float | 1.0 | Distance to final target to consider "reached" |
| `max_speed` | float | 200.0 | Maximum speed for avoidance calculations |
| `avoidance_enabled` | bool | false | Enable RVO (Reciprocal Velocity Obstacles) |
| `radius` | float | 10.0 | Agent collision radius for avoidance |

### NavigationAgent2D/3D Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_next_path_position()` | Vector2/3 | Next waypoint to move toward |
| `is_navigation_finished()` | bool | True if agent reached target |
| `is_target_reachable()` | bool | True if target can be reached |
| `distance_to_target()` | float | Distance to final target |
| `get_current_navigation_path()` | PackedVector2/3Array | Full path to target |

### NavigationAgent Signals

| Signal | Parameters | Description |
|--------|------------|-------------|
| `navigation_finished` | - | Emitted when target is reached |
| `target_reached` | - | Emitted just before navigation_finished |
| `waypoint_reached` | `details: Dictionary` | Emitted when waypoint is reached |
| `velocity_computed` | `safe_velocity: Vector2/3` | Emitted with avoidance-adjusted velocity |
| `link_reached` | `details: Dictionary` | Emitted when navigation link is reached |

## Best Practices {#best-practices}

### Performance Optimization

**Update target periodically, not every frame:**
```gdscript
# ✅ Good - update every 0.5 seconds
@onready var _timer: Timer = $Timer

func _ready() -> void:
    _timer.wait_time = 0.5
    _timer.timeout.connect(_update_target_position)
    _timer.start()

# ❌ Bad - expensive calculation every frame
func _physics_process(delta: float) -> void:
    _navigation_agent.target_position = player.global_position
```

**Frame counter alternative (no Timer node needed):**
```gdscript
const FRAMES_BETWEEN_UPDATES := 10
var _frame_counter := 0

func _physics_process(delta: float) -> void:
    _frame_counter += 1
    if _frame_counter >= FRAMES_BETWEEN_UPDATES:
        _frame_counter = 0
        _navigation_agent.target_position = player.global_position
```

### Initialization

**Always defer first target update:**
```gdscript
func _ready() -> void:
    # ✅ Correct - wait for navigation map to sync
    _update_target_position.call_deferred()

    # ❌ Wrong - navigation map not ready yet
    _navigation_agent.target_position = player.global_position
```

### Smooth Movement

**Smooth rotation in 2D:**
```gdscript
func _orient_character_to_direction(delta: float, direction: Vector2) -> void:
    if direction.is_zero_approx():
        return

    rotation = lerp_angle(rotation, direction.angle() + PI / 2.0, 10.0 * delta)
```

**Smooth rotation in 3D:**
```gdscript
func _orient_character_to_direction(delta: float, direction: Vector3) -> void:
    if direction.is_zero_approx():
        return

    var left_axis := Vector3.UP.cross(direction)
    var rotation_basis := Basis(left_axis, Vector3.UP, direction).orthonormalized()
    _skin.basis = _skin.basis.orthonormalized().slerp(rotation_basis, delta * rotation_speed).scaled(_skin.scale)
```

### Common Pitfalls

**Problem: Agent jitters at destination**
```gdscript
# ✅ Solution: Check is_navigation_finished()
func _physics_process(delta: float) -> void:
    if _navigation_agent.is_navigation_finished():
        return  # Stop moving

    var next_pos := _navigation_agent.get_next_path_position()
    # ... movement code
```

**Problem: Navigation not working after scene load**
```gdscript
# ✅ Solution: Use call_deferred() in _ready()
func _ready() -> void:
    _update_target_position.call_deferred()  # Wait for map sync
```

**Problem: Agent doesn't avoid obstacles**
```gdscript
# Avoidance only works between agents, NOT static obstacles
# Static obstacles must be part of NavigationRegion baking
# Use NavigationObstacle2D/3D for dynamic obstacles
```

**Problem: Path doesn't update when obstacles change**
```gdscript
# ✅ Solution: Force path recalculation
func on_door_opened() -> void:
    _navigation_region.enabled = true
    # Force recalculation by re-setting target
    var current_target := _navigation_agent.target_position
    _navigation_agent.target_position = current_target
```

## Use Case Decision Guide {#decision-guide}

**Use NavigationAgent2D/3D when:**
- AI enemies/NPCs need to follow player
- Need collision avoidance between multiple agents
- Navigation mesh can be pre-baked or generated
- Movement on irregular terrain or polygonal areas

**Use AStar2D/3D when:**
- Grid-based movement (tactical RPG, puzzle games)
- Custom pathfinding with specific cost functions
- Need full control over path calculation
- Runtime dynamic grid changes

**Use AStarGrid2D when:**
- Simple uniform grid pathfinding
- Tile-based games with equal movement costs
- Want easier setup than AStar2D
- Don't need custom per-cell costs

**Use NavigationServer directly when:**
- Need low-level control over navigation system
- Implementing custom navigation behavior
- Checking if points are on navigation mesh
- Advanced multi-map scenarios

## Related Patterns

- [2D Character Movement](./2d-character.md) - Basic character controllers
- [3D Character Movement](./3d-character.md) - 3D character controllers
- [Enemy AI](../ai/enemy.md) - AI behavior patterns
- [State Machines](../animation/state-machines.md) - Complex behavior states
- [Raycasting](../physics/raycasting.md) - Line-of-sight checks for AI
