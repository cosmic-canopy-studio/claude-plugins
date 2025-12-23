# Navigation System Patterns

Extracted from Godot Engine documentation tutorials on NavigationServer, NavigationAgents, NavigationRegions, NavigationMeshes, and pathfinding.

## NavigationServer Patterns

### Problem: Need to query paths directly without NavigationAgent nodes

**Solution: Use NavigationServer API directly**

Query paths from the NavigationServer with map, start position, and target position. Must wait for physics frame synchronization after setup.

```gdscript
extends Node3D

func _ready() -> void:
    # Use call_deferred to ensure all scene tree nodes are ready
    custom_setup.call_deferred()

func custom_setup() -> void:
    # Create a new navigation map
    var map: RID = NavigationServer3D.map_create()
    NavigationServer3D.map_set_up(map, Vector3.UP)
    NavigationServer3D.map_set_active(map, true)

    # Create a new navigation region and add it to the map
    var region: RID = NavigationServer3D.region_create()
    NavigationServer3D.region_set_transform(region, Transform3D())
    NavigationServer3D.region_set_map(region, map)

    # Create a procedural navigation mesh for the region
    var new_navigation_mesh: NavigationMesh = NavigationMesh.new()
    var vertices: PackedVector3Array = PackedVector3Array([
        Vector3(0, 0, 0),
        Vector3(9.0, 0, 0),
        Vector3(0, 0, 9.0)
    ])
    new_navigation_mesh.set_vertices(vertices)
    var polygon: PackedInt32Array = PackedInt32Array([0, 1, 2])
    new_navigation_mesh.add_polygon(polygon)
    NavigationServer3D.region_set_navigation_mesh(region, new_navigation_mesh)

    # Wait for NavigationServer sync to adapt to made changes
    await get_tree().physics_frame

    # Query the path from the navigation server
    var start_position: Vector3 = Vector3(0.1, 0.0, 0.1)
    var target_position: Vector3 = Vector3(1.0, 0.0, 1.0)
    var optimize_path: bool = true

    var path: PackedVector3Array = NavigationServer3D.map_get_path(
        map,
        start_position,
        target_position,
        optimize_path
    )

    print("Found a path!")
    print(path)
```

**Key Points:**
- Use `call_deferred()` in `_ready()` to ensure all nodes are initialized before querying
- Always `await get_tree().physics_frame` after creating/modifying navigation data
- NavigationServer changes are queued and synchronized at end of physics frame
- Set `optimize_path` to `true` for smooth paths with funnel algorithm, `false` for grid-based movement
- All setters and delete functions require synchronization before results are available

---

### Problem: NavigationServer API calls don't take effect immediately

**Solution: Understand and wait for synchronization**

The NavigationServer uses threading and batches updates for efficiency. You must wait for the physics frame to synchronize after making changes.

```gdscript
extends Node3D

func setup_navigation() -> void:
    # Changes are queued but NOT applied immediately
    var region: RID = NavigationServer3D.region_create()
    NavigationServer3D.region_set_transform(region, Transform3D())

    # If you query now, old data is returned
    # Must wait for synchronization:
    await get_tree().physics_frame

    # Now the changes have been applied to the NavigationServer
    var path: PackedVector3Array = NavigationServer3D.map_get_path(
        get_world_3d().get_navigation_map(),
        Vector3.ZERO,
        Vector3(1, 0, 1),
        true
    )
```

**Key Points:**
- Most get() functions don't require synchronization (they query current state)
- All setters and modifications require a physics frame sync
- Exceptions: Node properties updated in same frame return new value from the node itself
- Use `call_deferred()` in `_ready()` to avoid synchronization issues with scene initialization
- Avoidance callbacks happen just before PhysicsServer synchronization

---

## NavigationAgent Patterns

### Problem: Set up a CharacterBody2D to follow navigation paths

**Solution: Configure NavigationAgent2D with velocity_computed signal**

Add a NavigationAgent2D child node and connect its `velocity_computed` signal. Update the agent's target position in `_physics_process()` and apply the safe velocity.

```gdscript
extends CharacterBody2D

@export var movement_speed: float = 4.0
@onready var navigation_agent: NavigationAgent2D = get_node("NavigationAgent2D")

func _ready() -> void:
    navigation_agent.velocity_computed.connect(Callable(_on_velocity_computed))

func set_movement_target(movement_target: Vector2) -> void:
    navigation_agent.set_target_position(movement_target)

func _physics_process(delta: float) -> void:
    # Do not query when the map has never synchronized and is empty
    if NavigationServer2D.map_get_iteration_id(navigation_agent.get_navigation_map()) == 0:
        return
    if navigation_agent.is_navigation_finished():
        return

    var next_path_position: Vector2 = navigation_agent.get_next_path_position()
    var new_velocity: Vector2 = global_position.direction_to(next_path_position) * movement_speed
    if navigation_agent.avoidance_enabled:
        navigation_agent.set_velocity(new_velocity)
    else:
        _on_velocity_computed(new_velocity)

func _on_velocity_computed(safe_velocity: Vector2) -> void:
    velocity = safe_velocity
    move_and_slide()
```

**Key Points:**
- Always check `map_get_iteration_id() == 0` before querying - indicates map hasn't synchronized
- Always check `is_navigation_finished()` early - stops unnecessary path updates
- Call `get_next_path_position()` once per physics frame in `_physics_process()`
- Connect `velocity_computed` signal for both avoidance and non-avoidance cases
- Set velocity on agent if avoidance is enabled, or call the velocity handler directly if disabled
- Never call `get_next_path_position()` after target is reached

---

### Problem: Set up a Node3D to follow navigation paths without CharacterBody

**Solution: Use NavigationAgent3D with custom movement logic**

For Node3D inheriting nodes that aren't physics-based, move using `global_position` instead of velocity.

```gdscript
extends Node3D

@export var movement_speed: float = 4.0
@onready var navigation_agent: NavigationAgent3D = get_node("NavigationAgent3D")
var physics_delta: float = 0.0

func _ready() -> void:
    navigation_agent.velocity_computed.connect(Callable(_on_velocity_computed))

func set_movement_target(movement_target: Vector3) -> void:
    navigation_agent.set_target_position(movement_target)

func _physics_process(delta: float) -> void:
    physics_delta = delta

    # Do not query when the map has never synchronized and is empty
    if NavigationServer3D.map_get_iteration_id(navigation_agent.get_navigation_map()) == 0:
        return
    if navigation_agent.is_navigation_finished():
        return

    var next_path_position: Vector3 = navigation_agent.get_next_path_position()
    var new_velocity: Vector3 = global_position.direction_to(next_path_position) * movement_speed
    if navigation_agent.avoidance_enabled:
        navigation_agent.set_velocity(new_velocity)
    else:
        _on_velocity_computed(new_velocity)

func _on_velocity_computed(safe_velocity: Vector3) -> void:
    global_position = global_position.move_toward(
        global_position + safe_velocity,
        physics_delta * movement_speed
    )
```

**Key Points:**
- Save delta in `_physics_process()` for use in velocity callback
- Use `move_toward()` for smooth movement on non-physics nodes
- Same synchronization checks as CharacterBody version
- Check navigation finished status immediately in `_physics_process()`

---

### Problem: Set up NavigationAgent with avoidance between multiple agents

**Solution: Enable avoidance and configure RVO properties**

Enable avoidance on the agent, set velocity each frame, and use the safe velocity from the signal to move the parent node. Configure agent radius, neighbor distance, and time horizons for realistic collision avoidance.

```gdscript
extends NavigationAgent3D

func _ready() -> void:
    var agent: RID = get_rid()
    # Enable avoidance
    NavigationServer3D.agent_set_avoidance_enabled(agent, true)
    # Create avoidance callback for safe velocity
    NavigationServer3D.agent_set_avoidance_callback(agent, Callable(self, "_avoidance_done"))

    # Configure avoidance parameters for realistic behavior
    # radius: size of agent for collision purposes
    radius = 0.5
    # neighbor_distance: how far to look for other agents
    neighbor_distance = 10.0
    # max_neighbors: limit agents to consider for performance
    max_neighbors = 10
    # time_horizon_agents: predict collisions this many seconds ahead
    time_horizon_agents = 1.5
    # time_horizon_obstacles: predict obstacle collisions ahead
    time_horizon_obstacles = 1.5
    # max_speed: limit velocity for accurate avoidance calculation
    max_speed = 5.0

func _physics_process(delta: float) -> void:
    # Get desired velocity from pathfinding
    var desired_velocity: Vector3 = calculate_desired_velocity()
    # Set velocity - NavigationServer will compute safe velocity
    set_velocity(desired_velocity)

func _avoidance_done(safe_velocity: Vector3) -> void:
    # Use safe velocity to move parent node
    # This happens in the same physics frame, thread-safe
    var parent: Node3D = get_parent()
    parent.velocity = safe_velocity
    if parent is CharacterBody3D:
        parent.move_and_slide()

func calculate_desired_velocity() -> Vector3:
    # Your pathfinding logic here
    return Vector3.ZERO
```

**Key Points:**
- Avoidance only considers other agents on the same map with matching avoidance layers
- Set velocity in `_physics_process()` - agent sends to NavigationServer
- Receive `safe_velocity` from signal in callback - happens before PhysicsServer sync
- Avoidance operates in its own space - no information from navigation meshes or physics
- Use `radius` for agent size, not collision shape size
- Lower `neighbor_distance` reduces processing cost
- Higher `time_horizon_*` values make agents slower to avoid collision
- `max_speed` must be >= actual movement speed or avoidance is inaccurate

---

### Problem: Debug pathfinding issues where agent appears stuck or "dancing"

**Solution: Understand and fix common pathfinding problems**

Common issues: empty paths, backtracking, dancing between positions. These are often caused by synchronization timing, path update frequency, or desired distance settings.

```gdscript
extends CharacterBody2D

@export var movement_speed: float = 4.0
@export var path_desired_distance: float = 1.0  # Distance to advance to next path point
@export var target_desired_distance: float = 0.5  # Distance to consider target reached
@onready var navigation_agent: NavigationAgent2D = get_node("NavigationAgent2D")

func _ready() -> void:
    navigation_agent.velocity_computed.connect(Callable(_on_velocity_computed))
    # Configure path following distances
    navigation_agent.path_desired_distance = path_desired_distance
    navigation_agent.target_desired_distance = target_desired_distance

func set_movement_target(movement_target: Vector2) -> void:
    navigation_agent.set_target_position(movement_target)

func _physics_process(delta: float) -> void:
    # IMPORTANT: Always check iteration ID first - 0 means map not synchronized
    if NavigationServer2D.map_get_iteration_id(navigation_agent.get_navigation_map()) == 0:
        return

    # IMPORTANT: Check is_navigation_finished() immediately
    # Calling get_next_path_position() after target reached causes jitter
    if navigation_agent.is_navigation_finished():
        return

    var next_path_position: Vector2 = navigation_agent.get_next_path_position()
    var new_velocity: Vector2 = global_position.direction_to(next_path_position) * movement_speed

    if navigation_agent.avoidance_enabled:
        navigation_agent.set_velocity(new_velocity)
    else:
        _on_velocity_computed(new_velocity)

func _on_velocity_computed(safe_velocity: Vector2) -> void:
    velocity = safe_velocity
    move_and_slide()
```

**Fixes for Common Issues:**

**Empty path returned:**
- Cause: Querying path before map synchronization (e.g., in `_ready()`)
- Fix: Use `call_deferred()` or await `physics_frame` before querying
- Symptom: Path is empty, `get_next_path_position()` returns agent position, navigation immediately finished

**Agent stuck dancing between two positions:**
- Cause: Path updates every frame, path points switching positions around agent
- Fix: Increase `path_desired_distance` to prevent constant re-indexing
- Symptom: Agent oscillates in place or between two nearby positions

**Agent backtracking or moving backwards:**
- Cause: Agent moves too fast, overshoots `path_desired_distance` without advancing path index
- Fix: Increase `path_desired_distance` for agent speed, or slow down movement
- Symptom: Agent occasionally moves backward to reach a path point

**Agent rotates backwards for a frame:**
- Cause: Path point slightly "behind" agent due to edge precision or dense polygon layout
- Fix: Don't instantly rotate to face path position; use smooth rotation
- Symptom: Occasional backward-facing frame when agent crosses mesh edges

**Key Points:**
- Always initialize navigation map before querying: check `map_get_iteration_id() == 0`
- Never call `get_next_path_position()` after `is_navigation_finished()` returns true
- Adjust `path_desired_distance` and `target_desired_distance` for your movement speed
- Use `call_deferred()` in `_ready()` to ensure scene is ready before navigation queries
- Path points can appear slightly behind agent near mesh edges - this is normal

---

## NavigationRegion Patterns

### Problem: Create and register navigation regions with the default world map

**Solution: Use NavigationRegion nodes or NavigationServer API**

NavigationRegion nodes automatically register to the world navigation map. Use `get_rid()` to access the RID for direct NavigationServer manipulation.

```gdscript
extends NavigationRegion3D

func _ready() -> void:
    # Get RID of this region from NavigationServer
    var region_rid: RID = get_rid()

    # Region automatically added to default world map
    # Region can be manipulated directly via NavigationServer:
    # NavigationServer3D.region_set_enabled(region_rid, false)
    # NavigationServer3D.region_set_transform(region_rid, new_transform)

# Create regions programmatically via NavigationServer API
func create_region_programmatically() -> RID:
    var new_region_rid: RID = NavigationServer3D.region_create()
    var default_map_rid: RID = get_world_3d().get_navigation_map()

    # Must assign region to a map
    NavigationServer3D.region_set_map(new_region_rid, default_map_rid)

    return new_region_rid
```

**Key Points:**
- NavigationRegion nodes automatically register to default world map
- Call `get_rid()` to get the RID for direct NavigationServer manipulation
- Programmatically created regions must be assigned to a map with `region_set_map()`
- A region can only be on one map at a time; assigning to new map removes from old map
- Transform changes are automatically synced to NavigationServer
- Scale changes are NOT synced - navigation mesh doesn't support scale

---

### Problem: Enable/disable regions dynamically during gameplay

**Solution: Use region_set_enabled() to toggle without recreation**

Disable regions that shouldn't contribute to pathfinding. Existing paths won't update automatically.

```gdscript
extends NavigationRegion3D

func _ready() -> void:
    var region_rid: RID = get_rid()

func disable_region() -> void:
    var region_rid: RID = get_rid()
    NavigationServer3D.region_set_enabled(region_rid, false)
    # Note: Existing paths are not automatically updated

func enable_region() -> void:
    var region_rid: RID = get_rid()
    NavigationServer3D.region_set_enabled(region_rid, true)
```

**Key Points:**
- Disabling regions doesn't update in-progress paths
- Re-enable by setting enabled to true
- Simpler than destroying and recreating regions
- Region must have a navigation mesh resource to function

---

## NavigationMesh Patterns

### Problem: Create a 2D navigation polygon programmatically

**Solution: Create NavigationPolygon with vertices and polygons**

Build a NavigationPolygon by adding vertices and polygon indices. This can be procedural or static.

```gdscript
extends Node2D

func create_procedural_navigation_polygon() -> NavigationPolygon:
    var navigation_polygon: NavigationPolygon = NavigationPolygon.new()

    # Add vertices for a rectangular walkable area
    navigation_polygon.vertices = PackedVector2Array([
        Vector2(0.0, 0.0),
        Vector2(100.0, 0.0),
        Vector2(100.0, 100.0),
        Vector2(0.0, 100.0),
    ])

    # Add polygon indices that reference the vertices
    navigation_polygon.add_polygon(
        PackedInt32Array([0, 1, 2, 3])
    )

    return navigation_polygon

func use_polygon_with_region() -> void:
    var region_rid: RID = NavigationServer2D.region_create()
    region_rid = NavigationServer2D.region_create()

    NavigationServer2D.region_set_enabled(region_rid, true)
    NavigationServer2D.region_set_map(region_rid, get_world_2d().get_navigation_map())

    var navigation_polygon: NavigationPolygon = create_procedural_navigation_polygon()
    NavigationServer2D.region_set_navigation_polygon(region_rid, navigation_polygon)
```

**Key Points:**
- Vertices are Vector2 positions in the plane
- Polygons reference vertices by index
- Add multiple polygons to create complex navigation meshes
- NavigationPolygon resource can be saved and reused
- Vertex order doesn't determine direction (unlike physics)

---

### Problem: Bake a 3D navigation mesh from source geometry at runtime

**Solution: Parse geometry, bake asynchronously, update region**

Parse source geometry from the scene tree, bake navigation mesh on background thread, then update region.

```gdscript
extends Node3D

var navigation_mesh: NavigationMesh
var source_geometry: NavigationMeshSourceGeometryData3D
var callback_parsing: Callable
var callback_baking: Callable
var region_rid: RID

func _ready() -> void:
    navigation_mesh = NavigationMesh.new()
    navigation_mesh.agent_radius = 0.5
    navigation_mesh.agent_height = 1.8
    navigation_mesh.cell_size = 0.25
    navigation_mesh.cell_height = 0.25

    source_geometry = NavigationMeshSourceGeometryData3D.new()
    callback_parsing = Callable(self, "on_parsing_done")
    callback_baking = Callable(self, "on_baking_done")

    region_rid = NavigationServer3D.region_create()

    # Enable the region and set it to the default navigation map
    NavigationServer3D.region_set_enabled(region_rid, true)
    NavigationServer3D.region_set_map(region_rid, get_world_3d().get_navigation_map())

    # GridMap and other complex nodes may not be ready first frame
    # Parse on main thread after scene is ready
    parse_source_geometry.call_deferred()

func parse_source_geometry() -> void:
    source_geometry.clear()
    var root_node: Node3D = self

    # Parse geometry from all mesh child nodes
    NavigationServer3D.parse_source_geometry_data(
        navigation_mesh,
        source_geometry,
        root_node,
        callback_parsing
    )

func on_parsing_done() -> void:
    # Bake on background thread - doesn't block main thread
    NavigationServer3D.bake_from_source_geometry_data_async(
        navigation_mesh,
        source_geometry,
        callback_baking
    )

func on_baking_done() -> void:
    # Update the region with the baked navigation mesh
    NavigationServer3D.region_set_navigation_mesh(region_rid, navigation_mesh)
```

**Key Points:**
- Use `parse_source_geometry_data()` to parse scene tree geometry on main thread
- Use `bake_from_source_geometry_data_async()` to bake on background thread
- Geometry parsing is expensive - done on main thread, so parse once and reuse
- Baking is expensive but done on thread - use async version to not block game
- `agent_radius` shrinks mesh to account for agent collision size
- `agent_height` excludes areas too short for agent to fit
- `cell_size` and `cell_height` control voxel grid resolution
- Small cell sizes can freeze or crash - use reasonable values
- Use callbacks to chain parsing and baking operations

---

### Problem: Create multiple navigation meshes for different actor sizes from same geometry

**Solution: Parse once, bake multiple times with different agent parameters**

Parse source geometry once, then bake separate meshes with different agent_radius and agent_height values for small, standard, and large actors.

```gdscript
extends Node3D

func create_multi_actor_navigation() -> void:
    # Create navigation mesh resources for each actor size
    var nav_mesh_standard: NavigationMesh = NavigationMesh.new()
    var nav_mesh_small: NavigationMesh = NavigationMesh.new()
    var nav_mesh_huge: NavigationMesh = NavigationMesh.new()

    # Set agent parameters for each size
    nav_mesh_standard.agent_radius = 0.5
    nav_mesh_standard.agent_height = 1.8

    nav_mesh_small.agent_radius = 0.25
    nav_mesh_small.agent_height = 0.7

    nav_mesh_huge.agent_radius = 1.5
    nav_mesh_huge.agent_height = 2.5

    # Get root node for geometry parsing
    var root_node: Node3D = self

    # Create source geometry resource (reusable)
    var source_geometry_data: NavigationMeshSourceGeometryData3D = NavigationMeshSourceGeometryData3D.new()

    # Parse source geometry once on main thread
    NavigationServer3D.parse_source_geometry_data(
        nav_mesh_standard,  # Any mesh resource works for parse settings
        source_geometry_data,
        root_node
    )

    # Bake multiple meshes from same source geometry
    NavigationServer3D.bake_from_source_geometry_data(nav_mesh_standard, source_geometry_data)
    NavigationServer3D.bake_from_source_geometry_data(nav_mesh_small, source_geometry_data)
    NavigationServer3D.bake_from_source_geometry_data(nav_mesh_huge, source_geometry_data)

    # Create separate navigation maps for each actor type
    var map_standard: RID = NavigationServer3D.map_create()
    var map_small: RID = NavigationServer3D.map_create()
    var map_huge: RID = NavigationServer3D.map_create()

    # Activate all maps
    NavigationServer3D.map_set_active(map_standard, true)
    NavigationServer3D.map_set_active(map_small, true)
    NavigationServer3D.map_set_active(map_huge, true)

    # Create regions for each map
    var region_standard: RID = NavigationServer3D.region_create()
    var region_small: RID = NavigationServer3D.region_create()
    var region_huge: RID = NavigationServer3D.region_create()

    # Assign regions to maps
    NavigationServer3D.region_set_map(region_standard, map_standard)
    NavigationServer3D.region_set_map(region_small, map_small)
    NavigationServer3D.region_set_map(region_huge, map_huge)

    # Set navigation meshes for each region
    NavigationServer3D.region_set_navigation_mesh(region_standard, nav_mesh_standard)
    NavigationServer3D.region_set_navigation_mesh(region_small, nav_mesh_small)
    NavigationServer3D.region_set_navigation_mesh(region_huge, nav_mesh_huge)

    # Now each actor type can query its appropriate map for pathfinding
```

**Key Points:**
- Parse geometry once - most expensive operation on main thread
- Bake multiple times with different parameters - can do on threads
- Each actor size needs own navigation map and mesh
- Agents use `navigation_layers` to limit which meshes they use
- Agents are defined by radius and height only - complex shapes not supported
- Use this pattern for flying, swimming, vs walking actors too

---

## NavigationPath Patterns

### Problem: Query a path and move an actor along it

**Solution: Get path with map_get_path, index through points in physics_process**

Query the path once, then move through each path point. Advance to next point when close enough.

```gdscript
extends Node3D

@onready var default_3d_map_rid: RID = get_world_3d().get_navigation_map()

var movement_speed: float = 4.0
var movement_delta: float = 0.0
var path_point_margin: float = 0.5

var current_path_index: int = 0
var current_path_point: Vector3 = Vector3.ZERO
var current_path: PackedVector3Array = PackedVector3Array()

func set_movement_target(target_position: Vector3) -> void:
    var start_position: Vector3 = global_transform.origin

    current_path = NavigationServer3D.map_get_path(
        default_3d_map_rid,
        start_position,
        target_position,
        true  # optimize with funnel algorithm
    )

    if not current_path.is_empty():
        current_path_index = 0
        current_path_point = current_path[0]

func _physics_process(delta: float) -> void:
    if current_path.is_empty():
        return

    movement_delta = movement_speed * delta

    # Check if reached current path point
    if global_transform.origin.distance_to(current_path_point) <= path_point_margin:
        current_path_index += 1
        if current_path_index >= current_path.size():
            # Reached end of path
            current_path = PackedVector3Array()
            current_path_index = 0
            current_path_point = global_transform.origin
            return

    # Get current target path point
    current_path_point = current_path[current_path_index]

    # Move toward current path point
    var new_velocity: Vector3 = global_transform.origin.direction_to(current_path_point) * movement_delta
    global_transform.origin = global_transform.origin.move_toward(
        global_transform.origin + new_velocity,
        movement_delta
    )

func _on_target_reached() -> void:
    # Called when path is complete
    pass
```

**Key Points:**
- `map_get_path()` takes: map RID, start Vector3, target Vector3, optimize bool
- Set `optimize` to true for natural paths (funnel algorithm), false for grid-based
- Returned path is PackedVector3Array with all path points in order
- Check if path is empty - target unreachable or on different disconnected mesh
- Path[0] is closest to start, path[size-1] is closest to target
- All path points are guaranteed on navigation mesh
- Use distance check with margin to advance to next point
- Stop calling `get_next_path_position()` after path complete

---

## NavigationObstacle Patterns

### Problem: Add static obstacles to block pathfinding areas during mesh baking

**Solution: Use NavigationObstacle nodes with affect_navigation_mesh enabled**

Place NavigationObstacle nodes in scene with affect_navigation_mesh enabled. When navigation mesh is baked, obstacles carve out areas.

```gdscript
# Place NavigationObstacle3D in scene with:
# - affect_navigation_mesh: true
# - carve_navigation_mesh: true (to cut through agent radius offset)
# - height: set to obstacle height on y-axis
# - vertices: drawn as polygon outline in editor

# Or create programmatically:
func add_obstacle_to_baking() -> void:
    var obstacle_outline = PackedVector3Array([
        Vector3(-5, 0, -5),
        Vector3(5, 0, -5),
        Vector3(5, 0, 5),
        Vector3(-5, 0, 5)
    ])

    var navigation_mesh = NavigationMesh.new()
    var source_geometry = NavigationMeshSourceGeometryData3D.new()

    # Parse source geometry first
    NavigationServer3D.parse_source_geometry_data(
        navigation_mesh,
        source_geometry,
        get_node("MyTestRootNode")
    )

    # Add projected obstruction (obstacle) to source geometry
    var obstacle_elevation: float = 0.0
    var obstacle_height: float = 50.0
    var obstacle_carve: bool = true

    source_geometry.add_projected_obstruction(
        obstacle_outline,
        obstacle_elevation,
        obstacle_height,
        obstacle_carve
    )

    # Bake with obstacles included
    NavigationServer3D.bake_from_source_geometry_data(navigation_mesh, source_geometry)
```

**Key Points:**
- Obstacles only remove geometry, they don't add geometry
- Effect is limited to cell resolution of baking process
- Small obstacles may not affect mesh if voxel cells are large
- `carve_navigation_mesh` makes obstacle cut through agent radius offset
- Y-axis vertices are ignored - obstacle projected to horizontal plane
- Obstacles don't add to baking, just parsed like other nodes if affect_navigation_mesh enabled

---

### Problem: Add dynamic obstacles for avoidance between moving objects

**Solution: Create obstacle with radius for soft avoidance**

Create dynamic obstacles with radius property. Agents will avoid them like other agents.

```gdscript
extends Node3D

var obstacle_rid: RID

func _ready() -> void:
    # Create obstacle and place on default map
    obstacle_rid = NavigationServer3D.obstacle_create()
    var default_map_rid: RID = get_world_3d().get_navigation_map()

    NavigationServer3D.obstacle_set_map(obstacle_rid, default_map_rid)
    NavigationServer3D.obstacle_set_position(obstacle_rid, global_position)

    # Use radius for dynamic obstacle (soft boundary)
    NavigationServer3D.obstacle_set_radius(obstacle_rid, 0.5)

    # Enable for avoidance
    NavigationServer3D.obstacle_set_avoidance_enabled(obstacle_rid, true)

    # Optional: add velocity for predictive avoidance
    NavigationServer3D.obstacle_set_velocity(obstacle_rid, Vector3.ZERO)

func _physics_process(delta: float) -> void:
    # Update obstacle position to match movement
    NavigationServer3D.obstacle_set_position(obstacle_rid, global_position)

    # Optional: update velocity for agents to predict movement
    # NavigationServer3D.obstacle_set_velocity(obstacle_rid, velocity)

func create_static_obstacle() -> void:
    # For static obstacles, use vertices instead of radius
    var obstacle_rid: RID = NavigationServer3D.obstacle_create()
    var default_map_rid: RID = get_world_3d().get_navigation_map()

    NavigationServer3D.obstacle_set_map(obstacle_rid, default_map_rid)
    NavigationServer3D.obstacle_set_position(obstacle_rid, global_position)

    # Define static boundary with vertices
    var outline = PackedVector3Array([
        Vector3(-5, 0, -5),
        Vector3(5, 0, -5),
        Vector3(5, 0, 5),
        Vector3(-5, 0, 5)
    ])
    NavigationServer3D.obstacle_set_vertices(obstacle_rid, outline)
    NavigationServer3D.obstacle_set_height(obstacle_rid, 1.0)

    # Enable for avoidance
    NavigationServer3D.obstacle_set_avoidance_enabled(obstacle_rid, true)
```

**Key Points:**
- Dynamic obstacles: use radius >= 0, agents avoid like soft boundaries
- Static obstacles: use vertices, agents push out like hard walls
- Dynamic obstacles can move without performance cost
- Static obstacles are rebuilt from scratch when moved - expensive
- Only works with agents using 2D avoidance mode in 3D
- Vertex winding order determines push-out vs pull-in direction
- Don't combine static and dynamic on same obstacle - use one or the other

---

## NavigationLink Patterns

### Problem: Connect navigation meshes across large gaps

**Solution: Create NavigationLink between two positions**

Use NavigationLink nodes to connect navigation mesh polygons over arbitrary distances. Define start and end positions.

```gdscript
extends Node3D

var link_rid: RID
var link_start_position: Vector3 = Vector3(-5, 0, 0)
var link_end_position: Vector3 = Vector3(5, 0, 10)  # Gap of 10 units

func _ready() -> void:
    link_rid = NavigationServer3D.link_create()

    var link_owner_id: int = get_instance_id()
    var link_enter_cost: float = 1.0
    var link_travel_cost: float = 1.0
    var link_navigation_layers: int = 1
    var link_bidirectional: bool = true

    NavigationServer3D.link_set_owner_id(link_rid, link_owner_id)
    NavigationServer3D.link_set_enter_cost(link_rid, link_enter_cost)
    NavigationServer3D.link_set_travel_cost(link_rid, link_travel_cost)
    NavigationServer3D.link_set_navigation_layers(link_rid, link_navigation_layers)
    NavigationServer3D.link_set_bidirectional(link_rid, link_bidirectional)

    # Enable and add to default map
    NavigationServer3D.link_set_enabled(link_rid, true)
    NavigationServer3D.link_set_map(link_rid, get_world_3d().get_navigation_map())

    # Set link start and end positions
    NavigationServer3D.link_set_start_position(link_rid, link_start_position)
    NavigationServer3D.link_set_end_position(link_rid, link_end_position)

func setup_link_for_ladder() -> void:
    # Example: connect bottom of ladder to top
    link_rid = NavigationServer3D.link_create()

    # Link goes from base of ladder to top
    var ladder_base: Vector3 = Vector3(0, 0, 0)
    var ladder_top: Vector3 = Vector3(0, 5, 0)

    NavigationServer3D.link_set_bidirectional(link_rid, true)
    NavigationServer3D.link_set_map(link_rid, get_world_3d().get_navigation_map())
    NavigationServer3D.link_set_start_position(link_rid, ladder_base)
    NavigationServer3D.link_set_end_position(link_rid, ladder_top)
    NavigationServer3D.link_set_enabled(link_rid, true)

func on_agent_reached_link_start() -> void:
    # When agent reaches link start position, provide movement through link
    # Example: animate up ladder or teleport to link end
    # NavigationLink doesn't provide movement - game code must handle it
    pass
```

**Key Points:**
- Links connect closest navigation mesh polygons within search radius
- Default search radius from ProjectSettings, or set per map with `map_set_link_connection_radius()`
- Links don't provide movement - game code must handle it (ladder climb, jump, teleport, etc.)
- Bidirectional links work both directions; one-way links only work start to end
- `enter_cost` and `travel_cost` affect pathfinding - higher costs avoid the link
- Use `navigation_layers` to limit which agents can use the link
- Editor debug shows link positions and search radius
- If no valid polygon found in radius, link disables automatically

---

## Anti-Patterns and Gotchas

### Anti-Pattern: Calling get_next_path_position() after path is finished

**Problem:**
```gdscript
# WRONG - causes agent jitter/dancing
func _physics_process(delta: float) -> void:
    var next_pos = navigation_agent.get_next_path_position()
    move_toward(next_pos, speed * delta)

    # Even after finishing, keep calling get_next_path_position()
    # This causes the agent to jitter as path keeps resetting
```

**Solution:**
```gdscript
# RIGHT - check is_navigation_finished() first
func _physics_process(delta: float) -> void:
    if navigation_agent.is_navigation_finished():
        return

    var next_pos = navigation_agent.get_next_path_position()
    move_toward(next_pos, speed * delta)
```

**Why:** Calling `get_next_path_position()` updates agent internal state. After finishing, repeated calls cause path to reset and bounce between positions.

---

### Anti-Pattern: Changing agent scale on navigation region

**Problem:**
```gdscript
# WRONG - scale changes don't sync to NavigationServer
extends NavigationRegion3D

func _ready() -> void:
    scale = Vector3(2, 2, 2)  # This WON'T affect navigation mesh size
```

**Solution:**
```gdscript
# RIGHT - scale navigation mesh before adding region
var navigation_mesh: NavigationMesh = NavigationMesh.new()
# Set vertices already scaled
navigation_mesh.vertices = scaled_vertices
region.navigation_mesh = navigation_mesh
```

**Why:** NavigationMesh doesn't support scale. Must scale geometry before baking or creating vertices.

---

### Anti-Pattern: Ignoring synchronization timing

**Problem:**
```gdscript
# WRONG - querying immediately after setup
func _ready() -> void:
    var region: RID = NavigationServer3D.region_create()
    NavigationServer3D.region_set_map(region, get_world_3d().get_navigation_map())

    # Path will be empty - map not synchronized yet
    var path = NavigationServer3D.map_get_path(...)
```

**Solution:**
```gdscript
# RIGHT - defer setup and wait for sync
func _ready() -> void:
    custom_setup.call_deferred()

func custom_setup() -> void:
    var region: RID = NavigationServer3D.region_create()
    NavigationServer3D.region_set_map(region, get_world_3d().get_navigation_map())

    # Wait for NavigationServer to sync changes
    await get_tree().physics_frame

    # Now map is ready
    var path = NavigationServer3D.map_get_path(...)
```

**Why:** NavigationServer queues changes and applies them at physics frame sync. Querying before sync returns empty/old data.

---

### Anti-Pattern: Not checking map iteration ID

**Problem:**
```gdscript
# WRONG - map might not be synchronized
func _physics_process(delta: float) -> void:
    # If called before first physics frame, map iteration is 0
    var path = NavigationServer2D.map_get_path(...)  # Empty!
```

**Solution:**
```gdscript
# RIGHT - check iteration ID indicates valid map
func _physics_process(delta: float) -> void:
    if NavigationServer2D.map_get_iteration_id(navigation_agent.get_navigation_map()) == 0:
        return  # Map not ready

    var path = NavigationServer2D.map_get_path(...)
```

**Why:** Map iteration ID of 0 means map hasn't synchronized since creation. Guarantees empty paths.

---

### Anti-Pattern: Large cell sizes hiding small details

**Problem:**
```gdscript
# WRONG - cell size too large for geometry
var navigation_mesh: NavigationMesh = NavigationMesh.new()
navigation_mesh.cell_size = 5.0  # Very large
navigation_mesh.agent_radius = 0.5

# Navigation mesh loses detail, all small obstacles ignored
```

**Solution:**
```gdscript
# RIGHT - cell size matches obstacle scale
var navigation_mesh: NavigationMesh = NavigationMesh.new()
navigation_mesh.cell_size = 0.25  # Smaller, captures detail
navigation_mesh.agent_radius = 0.5

# But warn: too small causes performance issues
# Balance between detail and performance
```

**Why:** Cell size determines voxel resolution. Too large loses detail, too small freezes game.

---

## Best Practices

### 1. Wait for map synchronization before querying paths

Always ensure the navigation map has synchronized before querying paths. Use `call_deferred()` in `_ready()` or check `map_get_iteration_id() == 0`.

```gdscript
func _ready() -> void:
    # Ensure scene is fully ready before setup
    setup_navigation.call_deferred()

func setup_navigation() -> void:
    var region = NavigationServer3D.region_create()
    # ... configure region ...
    await get_tree().physics_frame  # Wait for sync
    var path = NavigationServer3D.map_get_path(...)  # Now safe
```

---

### 2. Use avoidance callbacks for safe physics frame execution

Avoidance velocity callbacks happen in the same physics frame, just before PhysicsServer sync. This is safe for moving the parent node.

```gdscript
extends NavigationAgent3D

func _ready() -> void:
    velocity_computed.connect(_on_velocity_computed)
    var agent = get_rid()
    NavigationServer3D.agent_set_avoidance_enabled(agent, true)
    NavigationServer3D.agent_set_avoidance_callback(agent, Callable(self, "_on_velocity_computed"))

func _on_velocity_computed(safe_velocity: Vector3) -> void:
    # Safe to move parent here - same physics frame, before PhysicsServer commits
    var parent = get_parent() as CharacterBody3D
    parent.velocity = safe_velocity
    parent.move_and_slide()
```

---

### 3. Configure agent parameters for realistic behavior

Set agent radius, neighbor distance, and time horizon based on your game's scale and dynamics.

```gdscript
navigation_agent.radius = 0.5  # Agent "size" for collisions
navigation_agent.neighbor_distance = 10.0  # Look-ahead distance
navigation_agent.max_neighbors = 8  # Limit processing
navigation_agent.time_horizon_agents = 1.5  # Predict this far ahead
navigation_agent.time_horizon_obstacles = 1.5
navigation_agent.max_speed = 5.0  # Must match or exceed actual movement
```

---

### 4. Create separate maps for different actor types

Use different agent_radius and agent_height for different-sized actors. Each type needs its own map and navigation mesh.

```gdscript
# Bake once, create multiple meshes for different sizes
var nav_mesh_small = create_navmesh(0.25, 0.7)
var nav_mesh_large = create_navmesh(1.5, 2.5)

var map_small = NavigationServer3D.map_create()
var map_large = NavigationServer3D.map_create()

# Agents query their appropriate map
```

---

### 5. Use parse once, bake multiple times pattern

Parsing geometry is expensive (main thread). Baking is expensive but can be threaded. Parse once, reuse for multiple bakes.

```gdscript
var source_geometry = NavigationMeshSourceGeometryData3D.new()
NavigationServer3D.parse_source_geometry_data(mesh, source_geometry, root)

# Bake multiple times from same source
NavigationServer3D.bake_from_source_geometry_data_async(mesh1, source_geometry, callback1)
NavigationServer3D.bake_from_source_geometry_data_async(mesh2, source_geometry, callback2)
```

---

### 6. Use navigation layers to control agent access

Set navigation_layers on regions/links and navigation_layers/avoidance_mask on agents to control which agents use which paths.

```gdscript
# Flying enemies only use layer 2
flying_agent.navigation_layers = 2

# Ground enemies only use layer 1
ground_agent.navigation_layers = 1

# Create regions on specific layers
region_air = create_region_on_layer(2)
region_ground = create_region_on_layer(1)
```

---

## Performance Considerations

- **Parsing is expensive:** Main thread operation. Parse once per geometry change, reuse for multiple bakes.
- **Baking can block:** Use `bake_from_source_geometry_data_async()` instead of blocking version.
- **Avoidance is threaded:** Default behavior. Scales well with many agents.
- **Small cell sizes freeze game:** Too many voxels. Balance between detail and performance.
- **Large neighbor distances increase cost:** Lower `neighbor_distance` to reduce avoidance processing.
- **Many agents on same map:** Create separate maps for different types to reduce per-agent cost.
- **Dynamic obstacles with moving static obstacles:** Expensive. Use dynamic radius when moving, add static vertices when stationary.
