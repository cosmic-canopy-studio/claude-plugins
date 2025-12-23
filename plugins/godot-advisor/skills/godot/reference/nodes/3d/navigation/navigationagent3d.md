---
class: NavigationAgent3D
category: navigation
complexity: intermediate
godot_version: "4.x"
experimental: true
---

# NavigationAgent3D

**Inherits:** Node < Object

A 3D agent used to pathfind to a position while avoiding obstacles.

## Description

NavigationAgent3D calculates paths to a target position while avoiding static and dynamic obstacles using RVO collision avoidance. Requires navigation data to work correctly.

The agent uses the NavigationServer3D for pathfinding calculations. Avoidance is computed before physics, allowing safe use in the physics step.

**Key Usage Pattern:**
1. Set `target_position` to destination
2. Call `get_next_path_position()` once per physics frame
3. Move parent node toward returned position

## Core Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `target_position` | Vector3 | `(0, 0, 0)` | Destination for pathfinding |
| `target_desired_distance` | float | `1.0` | How close to consider target reached |
| `path_desired_distance` | float | `1.0` | Distance threshold for waypoint reach |
| `max_speed` | float | `10.0` | Maximum agent movement speed |
| `radius` | float | `0.5` | Avoidance agent body radius |
| `height` | float | `1.0` | Agent height (for 2D avoidance) |
| `navigation_layers` | int | `1` | Which navigation layers to use |

## 3D-Specific Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `use_3d_avoidance` | bool | `false` | Use 3D omnidirectional avoidance |
| `keep_y_velocity` | bool | `true` | Preserve Y velocity in 2D avoidance |
| `path_height_offset` | float | `0.0` | Offset subtracted from path Y values |

## Avoidance Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `avoidance_enabled` | bool | `false` | Enable RVO collision avoidance |
| `avoidance_layers` | int | `1` | Layers this agent belongs to |
| `avoidance_mask` | int | `1` | Layers this agent avoids |
| `avoidance_priority` | float | `1.0` | Higher priority agents don't adjust for lower |
| `neighbor_distance` | float | `50.0` | How far to search for neighbors |
| `max_neighbors` | int | `10` | Max neighbors to consider |

## Essential Methods

### get_next_path_position() -> Vector3

Returns next position in global coordinates to move toward. **Must be called once per physics frame** to update internal path logic.

```gdscript
func _physics_process(delta: float) -> void:
    if not navigation_agent.is_navigation_finished():
        var next_position: Vector3 = navigation_agent.get_next_path_position()
        var direction: Vector3 = global_position.direction_to(next_position)
        velocity = direction * speed
```

### is_navigation_finished() -> bool

Returns `true` when target reached (reachable) or final waypoint reached (unreachable).

### is_target_reached() -> bool

Returns `true` when agent moved within `target_desired_distance` of `target_position`.

### is_target_reachable() -> bool

Returns `true` if final position is within `target_desired_distance` of target.

### distance_to_target() -> float

Returns distance to target position using agent's global position.

### get_final_position() -> Vector3

Returns reachable final position in global coordinates (may differ from target if unreachable).

## Key Signals

### target_reached()

Emitted when agent moves within `target_desired_distance` of target. Emitted before `navigation_finished`.

### navigation_finished()

Emitted when navigation ends (target reached or final waypoint reached). Emitted only once per path.

### waypoint_reached(details: Dictionary)

Emitted when agent moves within `path_desired_distance` of next waypoint.

**Details dictionary keys:**
- `position`: Waypoint position
- `type`: Navigation primitive type (region/link)
- `rid`: RID of containing primitive
- `owner`: Object managing the primitive

### velocity_computed(safe_velocity: Vector3)

Emitted when avoidance velocity calculated (requires `avoidance_enabled = true`).

### path_changed()

Emitted when path updates due to: empty path, map change, or exceeding `path_max_distance`.

## Common Patterns

### Basic 3D Navigation

```gdscript
extends CharacterBody3D

@onready var navigation_agent: NavigationAgent3D = $NavigationAgent3D

var speed: float = 5.0

func _ready() -> void:
    # Wait for first physics frame for navigation map sync
    await get_tree().physics_frame
    navigation_agent.target_position = target_location

func _physics_process(delta: float) -> void:
    if not navigation_agent.is_navigation_finished():
        var next_position: Vector3 = navigation_agent.get_next_path_position()
        var direction: Vector3 = global_position.direction_to(next_position)
        velocity = direction * speed
        move_and_slide()
```

### 3D Omnidirectional Avoidance

For air/underwater/space movement where agents can move freely in all directions:

```gdscript
func _ready() -> void:
    navigation_agent.use_3d_avoidance = true
    navigation_agent.avoidance_enabled = true
    navigation_agent.velocity_computed.connect(_on_velocity_computed)
    await get_tree().physics_frame
    navigation_agent.target_position = target_location

func _physics_process(delta: float) -> void:
    if navigation_agent.is_navigation_finished():
        return

    var next_position: Vector3 = navigation_agent.get_next_path_position()
    var direction: Vector3 = global_position.direction_to(next_position)
    var desired_velocity: Vector3 = direction * speed

    navigation_agent.velocity = desired_velocity

func _on_velocity_computed(safe_velocity: Vector3) -> void:
    velocity = safe_velocity
    move_and_slide()
```

### Ground-Based with 2D Avoidance

For typical ground-based characters (maintains Y velocity):

```gdscript
func _ready() -> void:
    navigation_agent.use_3d_avoidance = false  # Use 2D avoidance
    navigation_agent.keep_y_velocity = true     # Preserve vertical movement
    navigation_agent.height = 2.0               # Agent height for avoidance
    navigation_agent.avoidance_enabled = true
    navigation_agent.velocity_computed.connect(_on_velocity_computed)
    await get_tree().physics_frame
    navigation_agent.target_position = target_location

func _physics_process(delta: float) -> void:
    if navigation_agent.is_navigation_finished():
        return

    var next_position: Vector3 = navigation_agent.get_next_path_position()
    var direction: Vector3 = global_position.direction_to(next_position)
    var desired_velocity: Vector3 = direction * speed

    # Apply gravity
    if not is_on_floor():
        desired_velocity.y = velocity.y - gravity * delta

    navigation_agent.velocity = desired_velocity

func _on_velocity_computed(safe_velocity: Vector3) -> void:
    velocity = safe_velocity
    move_and_slide()
```

## 2D vs 3D Avoidance

### 2D Avoidance (`use_3d_avoidance = false`)
- Calculates avoidance on X-Z plane, ignores Y axis
- Suitable for ground-based characters
- Agents above/below each other (considering `height`) are ignored
- Can use radius-based OR vertex-based obstacles
- Set `keep_y_velocity = true` to soften clipping on uneven terrain

### 3D Avoidance (`use_3d_avoidance = true`)
- Calculates avoidance omnidirectionally in all 3 axes
- Suitable for flying, swimming, or space movement
- Uses radius-based avoidance obstacles only
- Ignores vertex-based obstacles
- Only avoids other agents also using 3D avoidance

## Best Practices

### Initialization

- Wait for first physics frame before setting `target_position`
- Navigation maps sync at start of physics frame
- Call `get_next_path_position()` once per physics frame, no more

### Distance Tuning

- `path_desired_distance` too high: skips waypoints, leaves navigation mesh
- `path_desired_distance` too low: gets stuck in repath loop
- Typical 3D values are smaller than 2D (1.0 vs 20.0)
- Adjust based on agent size and movement speed

### Avoidance Performance

- Only enable `avoidance_enabled` when needed
- Many agents with avoidance has significant performance cost
- Use layers/masks to limit which agents interact
- 3D avoidance is more expensive than 2D

### Signal Safety

- Avoid calling path update methods in signal callbacks
- Methods like `get_next_path_position()` can trigger new calculations
- Can cause infinite recursion in signals like `waypoint_reached`
- Use `call_deferred()` or wait until next physics frame

## Common Pitfalls

1. **Calling get_next_path_position() multiple times per frame** - Updates internal logic, causes incorrect movement
2. **Setting target before physics frame** - Map not synced, may fail
3. **Mixing 2D and 3D avoidance agents** - They won't avoid each other
4. **Not preserving Y velocity for gravity** - Use `keep_y_velocity = true` or manually handle gravity
5. **Wrong avoidance mode for use case** - Flying agents need 3D, ground agents need 2D

## Height Offset Usage

The `path_height_offset` is useful for:
- Adjusting visual position of agent relative to path
- Faking different height levels in top-down games
- Does NOT affect navigation mesh or pathfinding queries

```gdscript
# Make agent appear to walk 0.5 units above the navigation mesh
navigation_agent.path_height_offset = 0.5
```

## Navigation Layers

Use bit masks to control which navigation regions the agent can use:

```gdscript
# Use only layer 1
navigation_agent.navigation_layers = 1

# Use layers 1 and 3
navigation_agent.navigation_layers = 0b101  # Binary: 5

# Check/set individual layers
func set_navigation_layer_value(layer: int, enabled: bool) -> void:
    pass
func get_navigation_layer_value(layer: int) -> bool:
    pass
```

## Path Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `path_max_distance` | float | `5.0` | Max deviation before repath |
| `pathfinding_algorithm` | enum | `0` | Algorithm to use (A*) |
| `path_postprocessing` | enum | `0` | Post-process raw corridor |
| `simplify_path` | bool | `false` | Remove non-critical points |
| `simplify_epsilon` | float | `0.0` | Simplification amount |

## Debug Visualization

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `debug_enabled` | bool | `false` | Show debug visuals |
| `debug_use_custom` | bool | `false` | Use custom debug settings |
| `debug_path_custom_color` | Color | `(1,1,1,1)` | Custom path color |
| `debug_path_custom_point_size` | float | `4.0` | Custom point size |

## Related Classes

- **NavigationAgent2D** - 2D equivalent
- **NavigationServer3D** - Underlying pathfinding service
- **NavigationRegion3D** - Defines walkable areas
- **NavigationLink3D** - Connects separate navigation regions

## Official Resources

- [Using NavigationAgents Tutorial](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html)
- [NavigationServer3D API](https://docs.godotengine.org/en/stable/classes/class_navigationserver3d.html)
