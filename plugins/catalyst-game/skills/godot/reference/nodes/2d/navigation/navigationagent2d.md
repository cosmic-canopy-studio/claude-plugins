---
class: NavigationAgent2D
category: navigation
complexity: intermediate
godot_version: "4.x"
experimental: true
---

# NavigationAgent2D

**Inherits:** Node < Object

A 2D agent used to pathfind to a position while avoiding obstacles.

## Description

NavigationAgent2D calculates paths to a target position while avoiding static and dynamic obstacles using RVO collision avoidance. Requires navigation data to work correctly.

The agent uses the NavigationServer2D for pathfinding calculations. Avoidance is computed before physics, allowing safe use in the physics step.

**Key Usage Pattern:**
1. Set `target_position` to destination
2. Call `get_next_path_position()` once per physics frame
3. Move parent node toward returned position

## Core Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `target_position` | Vector2 | `(0, 0)` | Destination for pathfinding |
| `target_desired_distance` | float | `10.0` | How close to consider target reached |
| `path_desired_distance` | float | `20.0` | Distance threshold for waypoint reach |
| `max_speed` | float | `100.0` | Maximum agent movement speed |
| `radius` | float | `10.0` | Avoidance agent body radius |
| `navigation_layers` | int | `1` | Which navigation layers to use |

## Avoidance Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `avoidance_enabled` | bool | `false` | Enable RVO collision avoidance |
| `avoidance_layers` | int | `1` | Layers this agent belongs to |
| `avoidance_mask` | int | `1` | Layers this agent avoids |
| `avoidance_priority` | float | `1.0` | Higher priority agents don't adjust for lower |
| `neighbor_distance` | float | `500.0` | How far to search for neighbors |
| `max_neighbors` | int | `10` | Max neighbors to consider |

## Essential Methods

### get_next_path_position() -> Vector2

Returns next position in global coordinates to move toward. **Must be called once per physics frame** to update internal path logic.

```gdscript
func _physics_process(delta: float) -> void:
    if not navigation_agent.is_navigation_finished():
        var next_position: Vector2 = navigation_agent.get_next_path_position()
        var direction: Vector2 = global_position.direction_to(next_position)
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

### get_final_position() -> Vector2

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

### velocity_computed(safe_velocity: Vector2)

Emitted when avoidance velocity calculated (requires `avoidance_enabled = true`).

### path_changed()

Emitted when path updates due to: empty path, map change, or exceeding `path_max_distance`.

## Common Patterns

### Basic Navigation

```gdscript
extends CharacterBody2D

@onready var navigation_agent: NavigationAgent2D = $NavigationAgent2D

var speed: float = 200.0

func _ready() -> void:
    # Wait for first physics frame for navigation map sync
    await get_tree().physics_frame
    navigation_agent.target_position = target_location

func _physics_process(delta: float) -> void:
    if not navigation_agent.is_navigation_finished():
        var next_position: Vector2 = navigation_agent.get_next_path_position()
        var direction: Vector2 = global_position.direction_to(next_position)
        velocity = direction * speed
        move_and_slide()
```

### Navigation with Avoidance

```gdscript
func _ready() -> void:
    navigation_agent.avoidance_enabled = true
    navigation_agent.velocity_computed.connect(_on_velocity_computed)
    await get_tree().physics_frame
    navigation_agent.target_position = target_location

func _physics_process(delta: float) -> void:
    if navigation_agent.is_navigation_finished():
        return

    var next_position: Vector2 = navigation_agent.get_next_path_position()
    var direction: Vector2 = global_position.direction_to(next_position)
    var desired_velocity: Vector2 = direction * speed

    # Set velocity for avoidance calculation
    navigation_agent.velocity = desired_velocity

func _on_velocity_computed(safe_velocity: Vector2) -> void:
    velocity = safe_velocity
    move_and_slide()
```

### Target Reached Handling

```gdscript
func _ready() -> void:
    navigation_agent.target_reached.connect(_on_target_reached)
    navigation_agent.navigation_finished.connect(_on_navigation_finished)

func _on_target_reached() -> void:
    print("Reached target successfully")

func _on_navigation_finished() -> void:
    if navigation_agent.is_target_reachable():
        print("Target was reachable")
    else:
        print("Got as close as possible to unreachable target")
```

## Best Practices

### Initialization

- Wait for first physics frame before setting `target_position`
- Navigation maps sync at start of physics frame
- Call `get_next_path_position()` once per physics frame, no more

### Distance Tuning

- `path_desired_distance` too high: skips waypoints, leaves navigation mesh
- `path_desired_distance` too low: gets stuck in repath loop
- `target_desired_distance` can be different from `path_desired_distance`
- Set `target_desired_distance > path_desired_distance` to end early
- Set `target_desired_distance < path_desired_distance` to get closer (but avoid too low)

### Avoidance Performance

- Only enable `avoidance_enabled` when needed
- Many agents with avoidance has significant performance cost
- Use layers/masks to limit which agents interact

### Signal Safety

- Avoid calling path update methods in signal callbacks
- Methods like `get_next_path_position()` can trigger new calculations
- Can cause infinite recursion in signals like `waypoint_reached`
- Use `call_deferred()` or wait until next physics frame

## Common Pitfalls

1. **Calling get_next_path_position() multiple times per frame** - Updates internal logic, causes incorrect movement
2. **Setting target before physics frame** - Map not synced, may fail
3. **Complex logic in signals** - Can cause recursion or performance issues
4. **Not checking is_navigation_finished()** - Causes jittering when standing still
5. **Wrong distance thresholds** - Either skips waypoints or gets stuck

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
| `path_max_distance` | float | `100.0` | Max deviation before repath |
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

- **NavigationAgent3D** - 3D equivalent
- **NavigationServer2D** - Underlying pathfinding service
- **NavigationRegion2D** - Defines walkable areas
- **NavigationLink2D** - Connects separate navigation regions

## Official Resources

- [Using NavigationAgents Tutorial](https://docs.godotengine.org/en/stable/tutorials/navigation/navigation_using_navigationagents.html)
- [NavigationServer2D API](https://docs.godotengine.org/en/stable/classes/class_navigationserver2d.html)
