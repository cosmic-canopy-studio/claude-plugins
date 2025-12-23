# Godot Physics Patterns

Extracted from official physics tutorials covering collision detection, character movement, rigid bodies, and collision layer systems.

## Problem: Understanding Physics Bodies and When to Use Them

**Source:** Physics Introduction Tutorial

### Solution: Choose the Right Collision Object

Godot provides four collision object types, each with specific use cases:

**Area2D** - Detection and influence without physics
```gdscript
# Use for: Overlap detection, physics override zones, trigger areas
extends Area2D

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)

func _on_body_entered(body: Node2D) -> void:
    print("Body entered area: ", body.name)

func _on_body_exited(body: Node2D) -> void:
    print("Body left area: ", body.name)
```

**StaticBody2D** - Non-moving collider (walls, platforms)
```gdscript
# Use for: Environmental objects, immovable obstacles
extends StaticBody2D

# Can have constant velocity to simulate moving platforms
constant_linear_velocity: Vector2 = Vector2(100, 0)
constant_angular_velocity: float = 1.0
```

**RigidBody2D** - Physics-simulated body
```gdscript
# Use for: Objects that need realistic physics simulation
extends RigidBody2D

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    if Input.is_action_pressed("ui_up"):
        state.apply_force(Vector2(0, -250))
```

**CharacterBody2D** - Code-controlled collision detection
```gdscript
# Use for: Player characters, enemies with custom movement
extends CharacterBody2D

var velocity: Vector2 = Vector2.ZERO

func _physics_process(delta: float) -> void:
    velocity.y += 2500 * delta  # Apply gravity manually
    move_and_slide()
```

**Key Points:**
- Area2D only detects overlaps, doesn't simulate physics
- StaticBody2D participates in collisions but doesn't move
- RigidBody2D is fully physics-simulated (don't move directly)
- CharacterBody2D requires code for all movement and response


## Problem: Setting Up Collision Shapes Correctly

**Source:** Collision Shapes (2D) and Collision Shapes (3D) Tutorials

### Solution: Use Primitive Shapes First, Scale Only via Size Handles

```gdscript
# WRONG - Never scale collision shapes this way
collision_shape.scale = Vector2(2, 2)  # Causes unexpected behavior

# RIGHT - Always use size handles or adjust shape properties
# In 2D:
collision_shape_2d = CollisionShape2D.new()
rect_shape = RectangleShape2D.new()
rect_shape.size = Vector2(100, 200)  # Use size property
collision_shape_2d.shape = rect_shape
add_child(collision_shape_2d)
collision_shape_2d.position = Vector2.ZERO  # Keep scale at (1, 1)

# In 3D:
collision_shape_3d = CollisionShape3D.new()
box_shape = BoxShape3D.new()
box_shape.size = Vector3(100, 200, 100)  # Use size property
collision_shape_3d.shape = box_shape
add_child(collision_shape_3d)
```

**Collision Shape Hierarchy:**

1. **Primitive Shapes** (fastest) - Use for dynamic objects
   - 2D: RectangleShape2D, CircleShape2D, CapsuleShape2D, SegmentShape2D
   - 3D: BoxShape3D, SphereShape3D, CapsuleShape3D, CylinderShape3D

2. **Convex Shapes** (medium) - Use for complex shapes
   - Represent any convex shape
   - Better performance than concave for simple objects
   - Generate via editor using Quickhull or V-HACD algorithms

3. **Concave/Trimesh Shapes** (slowest, most accurate) - Use only with StaticBody
   - Can represent any shape including hollow objects
   - Best for level collision
   - CANNOT be used with CharacterBody or RigidBody (except Static mode)

**Key Points:**
- Always keep CollisionShape scale at (1, 1) in Inspector
- Never scale shapes - adjust size via shape properties instead
- Primitive shapes provide most reliable collision behavior
- Multiple collision shapes on one body won't collide with each other
- Non-transformed shapes allow engine broad-phase optimization


## Problem: Detecting When Your Character Hits Something

**Source:** Using CharacterBody2D/3D and Physics Introduction Tutorials

### Solution: Use move_and_collide for Direct Collision Data

```gdscript
extends CharacterBody2D

var speed: float = 300.0

func _physics_process(delta: float) -> void:
    var input_dir: Vector2 = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = input_dir * speed

    # Use move_and_collide when you need collision info
    var collision: KinematicCollision2D = move_and_collide(velocity * delta)

    if collision:
        print("Hit: ", collision.get_collider().name)
        print("Hit position: ", collision.get_position())
        print("Hit normal: ", collision.get_normal())
        print("Hit point on collider: ", collision.get_remainder())
```

**KinematicCollision2D Data Available:**
- `get_collider()` - The object hit
- `get_position()` - World position of collision point
- `get_normal()` - Surface normal at collision
- `get_remainder()` - Remaining movement after collision

**Key Points:**
- move_and_collide() returns null if no collision
- Multiply velocity by delta before passing to move_and_collide()
- Returns immediately on first collision (doesn't slide)
- Perfect for bullets, bouncing objects, custom responses


## Problem: Implementing Smooth Sliding Movement (Platformers/TopDown)

**Source:** Using CharacterBody2D/3D Tutorial

### Solution: Use move_and_slide with Proper Configuration

```gdscript
extends CharacterBody2D

var speed: float = 300.0
var jump_force: float = -400.0
var gravity: float = ProjectSettings.get_setting("physics/2d/default_gravity")

func _physics_process(delta: float) -> void:
    # Apply gravity (acceleration, so multiply by delta)
    velocity.y += gravity * delta

    # Handle jumping
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_force

    # Get horizontal input
    var direction: float = Input.get_axis("ui_left", "ui_right")
    velocity.x = direction * speed

    # move_and_slide handles timestep internally - DON'T multiply velocity by delta!
    move_and_slide()
```

**Important: move_and_slide Behavior**

```gdscript
# WRONG - move_and_slide already includes timestep
move_and_slide(velocity * delta)  # This breaks the function

# RIGHT - pass velocity directly
move_and_slide()  # Uses internal velocity property
```

**Key Properties for move_and_slide:**
- `velocity` - Body's velocity in pixels/second (modified by function)
- `motion_mode` - MOTION_MODE_GROUNDED (default) or MOTION_MODE_FLOATING
- `up_direction` - What defines "floor" (default: Vector2(0, -1))
- `floor_stop_on_slope` - Prevents sliding down slopes (default: true)
- `floor_max_angle` - Max angle to treat as floor (default: 45°)

**Helper Methods After move_and_slide:**
```gdscript
func _physics_process(delta: float) -> void:
    move_and_slide()

    # Check what you're touching
    if is_on_floor():
        print("Standing on ground")
    if is_on_wall():
        print("Touching a wall")
    if is_on_ceiling():
        print("Hitting ceiling")

    # Handle multiple collisions from sliding
    for i in range(get_slide_collision_count()):
        var collision: KinematicCollision2D = get_slide_collision(i)
        print("Slid into: ", collision.get_collider().name)
```

**Key Points:**
- move_and_slide() includes timestep - pass velocity directly
- Automatically modifies velocity property on collision
- Ideal for platformers and top-down games
- Handles slopes, friction, and wall sliding automatically
- can_sleep gets overridden when body is in contact


## Problem: Making Objects Bounce Off Walls

**Source:** Using CharacterBody2D/3D Tutorial - Bouncing/Reflecting Example

### Solution: Bounce Using Collision Normal

```gdscript
# For bullets or bouncing objects
extends CharacterBody2D

var speed: float = 750.0

func start(start_position: Vector2, direction: float) -> void:
    rotation = direction
    position = start_position
    velocity = Vector2(speed, 0).rotated(rotation)

func _physics_process(delta: float) -> void:
    var collision: KinematicCollision2D = move_and_collide(velocity * delta)

    if collision:
        # Reflect velocity using surface normal
        velocity = velocity.bounce(collision.get_normal())

        # Optional: call hit method on colliding object
        if collision.get_collider().has_method("hit"):
            collision.get_collider().call("hit")
```

**Why Bouncing Uses move_and_collide, Not move_and_slide:**
- move_and_slide implements sliding response (default)
- Bouncing needs custom response (reflection)
- move_and_collide returns immediately so you can modify velocity

**Key Points:**
- Vector2.bounce(normal) reflects velocity around surface
- Use collision normal to determine reflection angle
- Can check collider methods with has_method()
- More flexible than move_and_slide for custom responses


## Problem: Controlling Physics-Simulated Objects

**Source:** Physics Introduction and Using RigidBody Tutorials

### Solution: Apply Forces in _integrate_forces Callback

```gdscript
# WRONG - Modifying position/velocity directly
extends RigidBody2D

func _physics_process(delta: float) -> void:
    position += Vector2(100, 0) * delta  # Breaks physics simulation
    linear_velocity = Vector2(100, 0)     # Conflicts with forces

# RIGHT - Use _integrate_forces callback
extends RigidBody2D

var thrust: Vector2 = Vector2(0, -250)
var torque_force: float = 20000.0

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    if Input.is_action_pressed("ui_up"):
        state.apply_force(thrust.rotated(rotation))

    var rotation_direction: int = 0
    if Input.is_action_pressed("ui_right"):
        rotation_direction += 1
    if Input.is_action_pressed("ui_left"):
        rotation_direction -= 1

    state.apply_torque(rotation_direction * torque_force)
```

**When _integrate_forces Gets Called:**
- Called before each physics step
- Has access to PhysicsDirectBodyState2D
- Safe place to modify physics properties
- NOT called when body is sleeping

**Avoiding RigidBody Common Mistake:**
```gdscript
# WRONG - Using Node3D's look_at every frame breaks physics
extends RigidBody3D

func _physics_process(delta: float) -> void:
    look_at(target_position, Vector3.UP)  # Breaks angular velocity

# RIGHT - Use _integrate_forces with angular velocity
extends RigidBody3D

var speed: float = 0.1

func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
    var forward_axis: Vector3 = Vector3(1, 0, 0)
    var forward_dir: Vector3 = (global_transform.basis * forward_axis).normalized()
    var target_dir: Vector3 = (target_position - global_position).normalized()

    if forward_dir.dot(target_dir) > 1e-4:
        state.angular_velocity = speed * forward_dir.cross(target_dir) / state.step
```

**Key Points:**
- Never set position/velocity directly in _physics_process
- Use _integrate_forces for safe physics manipulation
- apply_force() and apply_torque() integrate over time
- Body goes to sleep when inactive (use can_sleep property to disable)


## Problem: Setting Up Collision Layers and Masks

**Source:** Physics Introduction - Collision Layers and Masks

### Solution: Configure Layers and Masks for Complex Interactions

```gdscript
# Setup: 4 body types need different interaction rules
# Walls collide with everything
# Player collides with walls, enemies, coins
# Enemies collide with walls only
# Coins collide with nothing

extends CharacterBody2D

func _ready() -> void:
    # Set which layer this body is in
    collision_layer = 0  # Not on any layer
    set_collision_layer_value(2, true)  # Add to "player" layer (2)

    # Set which layers to scan for collisions
    collision_mask = 0  # Clear all
    set_collision_mask_value(1, true)   # Scan "walls" layer (1)
    set_collision_mask_value(3, true)   # Scan "enemies" layer (3)
    set_collision_mask_value(4, true)   # Scan "coins" layer (4)
```

**Manual Bitmask Approach (Advanced):**
```gdscript
extends CharacterBody2D

func _ready() -> void:
    # Using binary: layers 1, 3, 4 enabled = 0b1101 = 0xd = 13
    # Method 1: Binary notation
    collision_mask = 0b00001101

    # Method 2: Hexadecimal
    collision_mask = 0xd

    # Method 3: Bit shifting (fastest)
    collision_mask = (1 << (1 - 1)) | (1 << (3 - 1)) | (1 << (4 - 1))
    # = (1 << 0) | (1 << 2) | (1 << 3)
    # = 1 | 4 | 8 = 13
```

**Using Export Annotations:**
```gdscript
extends CharacterBody2D

@export_flags_2d_physics var interaction_layers: int

func _ready() -> void:
    collision_mask = interaction_layers
```

**Naming Layers for Easy Reference:**
In Project Settings > Layer Names > 2D Physics, name layers:
- Layer 1: "walls"
- Layer 2: "player"
- Layer 3: "enemies"
- Layer 4: "coins"

**Key Points:**
- collision_layer: Which layers this body appears in
- collision_mask: Which layers this body scans for collisions
- 32 total layers available per physics space
- set_collision_layer_value(layer, true) is cleaner than bitmasks
- Bit shifting: (1 << (layer - 1)) converts layer number to bit position


## Problem: Detecting Objects in a Specific Region

**Source:** Physics Introduction - Area2D Overview

### Solution: Use Area2D for Region Detection

```gdscript
extends Node2D

func _ready() -> void:
    var area: Area2D = Area2D.new()
    var collision_shape: CollisionShape2D = CollisionShape2D.new()
    var rect_shape: RectangleShape2D = RectangleShape2D.new()

    rect_shape.size = Vector2(400, 300)
    collision_shape.shape = rect_shape

    area.add_child(collision_shape)
    add_child(area)

    # Connect signals for overlap events
    area.body_entered.connect(_on_body_entered)
    area.body_exited.connect(_on_body_exited)
    area.area_entered.connect(_on_area_entered)

func _on_body_entered(body: Node2D) -> void:
    print("Body entered detection zone: ", body.name)

func _on_body_exited(body: Node2D) -> void:
    print("Body left detection zone: ", body.name)

func _on_area_entered(other_area: Area2D) -> void:
    print("Area entered detection zone: ", other_area.name)
```

**Checking What's in an Area:**
```gdscript
extends Area2D

func _physics_process(delta: float) -> void:
    # Get all bodies currently overlapping
    var overlapping_bodies: Array[Node2D] = get_overlapping_bodies()
    for body in overlapping_bodies:
        print("Currently touching: ", body.name)

    # Get all areas currently overlapping
    var overlapping_areas: Array[Area2D] = get_overlapping_areas()
    for area in overlapping_areas:
        print("Currently overlapping area: ", area.name)
```

**Overriding Physics in a Region:**
```gdscript
extends Area2D

func _ready() -> void:
    body_entered.connect(_on_body_entered)

func _on_body_entered(body: Node2D) -> void:
    if body is RigidBody2D:
        # Override gravity in this area
        gravity_scale = 0.5
        gravity_direction = Vector2(0, 1)  # Downward
```

**Key Points:**
- Area2D detects overlaps but doesn't simulate physics
- Signals: body_entered, body_exited, area_entered, area_exited
- Can get current overlapping bodies/areas anytime
- Can override physics properties in a region


## Problem: Casting Rays to Find Objects

**Source:** Ray-casting Tutorial

### Solution: Use Direct Space State for Raycast Queries

```gdscript
extends CharacterBody2D

const RAY_LENGTH: float = 1000.0

func _physics_process(delta: float) -> void:
    # Get the physics space
    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state

    # Create raycast query
    var query: PhysicsRayQueryParameters2D = PhysicsRayQueryParameters2D.create(
        global_position,
        global_position + Vector2(RAY_LENGTH, 0)
    )

    # Execute raycast
    var result: Dictionary = space_state.intersect_ray(query)

    if result:
        print("Hit: ", result["collider"].name)
        print("Position: ", result["position"])
        print("Normal: ", result["normal"])
```

**Ray Result Dictionary Contents:**
```gdscript
if result:
    var hit_position: Vector2 = result["position"]      # World collision point
    var hit_normal: Vector2 = result["normal"]          # Surface normal
    var hit_object: Object = result["collider"]         # Node that was hit
    var hit_object_id: int = result["collider_id"]      # ObjectID
    var hit_shape_index: int = result["shape"]          # Which shape was hit
    var hit_metadata: Variant = result["metadata"]      # Custom metadata
```

**Excluding Self from Raycast Results:**
```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state
    var query: PhysicsRayQueryParameters2D = PhysicsRayQueryParameters2D.create(
        global_position,
        target_position
    )

    # Exclude self from results
    query.exclude = [self]

    var result: Dictionary = space_state.intersect_ray(query)
```

**Using Collision Mask for Selective Raycasting:**
```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state
    var query: PhysicsRayQueryParameters2D = PhysicsRayQueryParameters2D.create(
        global_position,
        target_position,
        collision_mask,  # Use same mask as this body
        [self]           # Exclude self
    )

    var result: Dictionary = space_state.intersect_ray(query)
```

**3D Raycast from Camera/Mouse:**
```gdscript
extends Node3D

const RAY_LENGTH: float = 1000.0

func _physics_process(delta: float) -> void:
    var space_state: PhysicsDirectSpaceState3D = get_world_3d().direct_space_state
    var camera: Camera3D = $Camera3D
    var mouse_pos: Vector2 = get_viewport().get_mouse_position()

    # Get ray from camera through mouse position
    var origin: Vector3 = camera.project_ray_origin(mouse_pos)
    var normal: Vector3 = camera.project_ray_normal(mouse_pos)
    var end: Vector3 = origin + normal * RAY_LENGTH

    var query: PhysicsRayQueryParameters3D = PhysicsRayQueryParameters3D.create(origin, end)
    query.collide_with_areas = true  # Include Area3D nodes

    var result: Dictionary = space_state.intersect_ray(query)
```

**Critical: Access Space Only in _physics_process**
```gdscript
# WRONG - Space is locked outside _physics_process
func _input(event: InputEvent) -> void:
    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state
    var result: Dictionary = space_state.intersect_ray(query)  # ERROR: Space locked

# RIGHT - Query in _physics_process
func _physics_process(delta: float) -> void:
    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state
    var result: Dictionary = space_state.intersect_ray(query)  # Works fine
```

**Key Points:**
- Always access physics space in _physics_process (space is locked otherwise)
- Ray cast returns empty dictionary if nothing was hit
- Can exclude specific objects or use collision masks
- Use camera.project_ray_origin/normal for 3D screen raycasts
- For simple cases, use RayCast2D or RayCast3D nodes instead


## Problem: Optimizing Collision Performance

**Source:** Collision Shapes (2D/3D) Performance Caveats

### Solution: Minimize Collision Shape Count and Keep Them Unscaled

```gdscript
# WRONG - Many collision shapes hurt performance
extends StaticBody2D

func _ready() -> void:
    for i in range(50):
        var shape: CollisionShape2D = CollisionShape2D.new()
        shape.shape = CircleShape2D.new()
        add_child(shape)
        shape.position = Vector2(i * 10, 0)  # Avoid translating shapes

# RIGHT - Consolidate shapes when possible
extends StaticBody2D

func _ready() -> void:
    var shape: CollisionShape2D = CollisionShape2D.new()
    var rect: RectangleShape2D = RectangleShape2D.new()
    rect.size = Vector2(500, 100)
    shape.shape = rect
    add_child(shape)
```

**Optimization Rules:**

```gdscript
# Rule 1: Minimize shape count (especially for StaticBody2D)
# Multiple shapes prevent broad-phase optimization

# Rule 2: Keep shapes at local position (0, 0) with scale (1, 1)
# Transforming collision shapes disables engine optimizations
extends StaticBody2D

func _ready() -> void:
    var shape: CollisionShape2D = CollisionShape2D.new()
    var rect: RectangleShape2D = RectangleShape2D.new()

    rect.size = Vector2(200, 200)  # Correct: use size
    shape.shape = rect
    shape.position = Vector2.ZERO  # Correct: no translation
    shape.scale = Vector2.ONE      # Correct: no scaling

    add_child(shape)

# Rule 3: Prefer primitive shapes for dynamic bodies
# Primitive shapes are most reliable for RigidBody2D/CharacterBody2D
extends RigidBody2D

func _ready() -> void:
    # Good: Single primitive shape
    var rect: RectangleShape2D = RectangleShape2D.new()
    rect.size = Vector2(100, 100)

    var shape: CollisionShape2D = CollisionShape2D.new()
    shape.shape = rect
    add_child(shape)

# Rule 4: Use concave shapes only with StaticBody
# Concave shapes don't work with dynamic bodies
extends StaticBody2D

func _ready() -> void:
    # Correct: Concave shape with StaticBody
    var concave: ConcavePolygonShape2D = ConcavePolygonShape2D.new()
    # ... set polygon data ...

    var shape: CollisionShape2D = CollisionShape2D.new()
    shape.shape = concave
    add_child(shape)
```

**When to Accept Accuracy Tradeoffs:**
```gdscript
# If you have performance issues, you may need to trade accuracy
# Most games don't use 100% accurate collision

# Example: Simplified collision for decorative details
# Instead of per-pixel collision, use simplified shapes
extends StaticBody2D

func _ready() -> void:
    # Create simplified sprite for rendering (many details)
    var sprite: Sprite2D = Sprite2D.new()
    sprite.texture = load("res://detailed_sprite.png")
    add_child(sprite)

    # Use separate simplified shape for collision (fewer details)
    var collision: CollisionPolygon2D = CollisionPolygon2D.new()
    # Generate from simplified sprite, excluding small details
    add_child(collision)
```

**Key Points:**
- StaticBody with single non-transformed shape: broad-phase works (fast)
- StaticBody with multiple shapes: broad-phase fails (slow)
- Always adjust shape size, never scale transforms
- Primitive shapes work with all body types
- Concave shapes only work with StaticBody
- Most games use simplified collision, not pixel-perfect


## Problem: Handling Contact Information on RigidBodies

**Source:** Physics Introduction - Contact Reporting

### Solution: Enable Contact Monitoring and Reporting

```gdscript
extends RigidBody2D

func _ready() -> void:
    # Enable contact signals
    contact_monitor = true

    # Enable contact info queries (set to get_contact_count)
    max_contacts_reported = 10

    # Connect contact signals
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)

func _on_body_entered(body: Node2D) -> void:
    print("Collided with: ", body.name)

func _on_body_exited(body: Node2D) -> void:
    print("Stopped colliding with: ", body.name)

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    # Query contacts directly
    var contact_count: int = state.get_contact_count()
    for i in range(contact_count):
        var contact_pos: Vector2 = state.get_contact_local_position(i)
        var contact_normal: Vector2 = state.get_contact_local_normal(i)
        var contact_collider: RID = state.get_contact_collider(i)

        print("Contact at: ", contact_pos)
```

**Key Points:**
- contact_monitor must be enabled for signals to work
- max_contacts_reported limits memory usage (non-zero to enable reporting)
- Query contacts in _integrate_forces for best accuracy
- RigidBody provides both signals and direct access methods
- Sleeping bodies don't report contacts


## Anti-Pattern: Misusing move_and_slide Timestep

**Source:** Using CharacterBody2D/3D Tutorial - move_and_slide Warning

### Problem: move_and_slide Already Includes Timestep

```gdscript
# WRONG - Double-multiplying timestep
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var input_dir: Vector2 = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = input_dir * 300
    move_and_slide(velocity * delta)  # Velocity gets scaled twice!

# RIGHT - Don't multiply by delta for move_and_slide
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var input_dir: Vector2 = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = input_dir * 300
    move_and_slide()  # Function uses internal velocity
```

**Gravity Handling Exception:**
```gdscript
# Gravity IS an acceleration and MUST be multiplied by delta
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    # Gravity is acceleration - multiply by delta
    velocity.y += gravity * delta

    # But don't multiply velocity by delta for move_and_slide
    move_and_slide()
```


## Anti-Pattern: Directly Modifying RigidBody Position

**Source:** Using RigidBody and Physics Introduction

### Problem: Direct Position Changes Break Physics Simulation

```gdscript
# WRONG - Position changes override physics
extends RigidBody2D

func _physics_process(delta: float) -> void:
    position += Vector2(100, 0) * delta  # Breaks physics engine

# WRONG - Setting velocity directly ignores forces
func _physics_process(delta: float) -> void:
    linear_velocity = Vector2(100, 0)  # Conflicts with applied forces

# RIGHT - Use _integrate_forces for safe manipulation
extends RigidBody2D

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    if Input.is_action_pressed("move_right"):
        state.apply_force(Vector2(100, 0))

# RIGHT - One-time setup is okay
func _ready() -> void:
    position = Vector2(100, 200)  # Setting once is fine
    global_position = get_tree().root.position  # Okay in _ready
```

**Key Points:**
- Never modify position/velocity in _physics_process
- Use _integrate_forces for all dynamic physics changes
- apply_force() and apply_torque() respect other forces
- Position changes in _ready() are safe


## Anti-Pattern: Using look_at() Every Frame on RigidBody

**Source:** Using RigidBody Tutorial

### Problem: look_at() Each Frame Breaks Angular Physics

```gdscript
# WRONG - look_at every frame breaks physics simulation
extends RigidBody3D

func _physics_process(delta: float) -> void:
    look_at(target_position, Vector3.UP)  # Overrides angular_velocity

# RIGHT - Use angular velocity in _integrate_forces
extends RigidBody3D

var speed: float = 0.1

func _integrate_forces(state: PhysicsDirectBodyState3D) -> void:
    var forward_local_axis: Vector3 = Vector3(1, 0, 0)
    var forward_dir: Vector3 = (global_transform.basis * forward_local_axis).normalized()
    var target_dir: Vector3 = (target_position - global_position).normalized()

    var local_speed: float = clampf(speed, 0, acos(forward_dir.dot(target_dir)))

    if forward_dir.dot(target_dir) > 1e-4:
        state.angular_velocity = local_speed * forward_dir.cross(target_dir) / state.step
```

**Key Points:**
- Never use look_at(), set_global_transform() each frame on RigidBody
- These break the physics simulation
- Use _integrate_forces with angular_velocity instead
- The cross product gives rotation axis
- clampf prevents over-rotation


## Anti-Pattern: Not Excluding Self in Raycast

**Source:** Ray-casting Tutorial - Collision Exceptions

### Problem: Ray Hits the Casting Body Itself

```gdscript
# WRONG - Ray hits this character's own collider
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state
    var query: PhysicsRayQueryParameters2D = PhysicsRayQueryParameters2D.create(
        global_position,
        target_position
    )

    var result: Dictionary = space_state.intersect_ray(query)
    # Result will always hit THIS character first

# RIGHT - Exclude self from results
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state
    var query: PhysicsRayQueryParameters2D = PhysicsRayQueryParameters2D.create(
        global_position,
        target_position
    )

    query.exclude = [self]  # Exclude this body

    var result: Dictionary = space_state.intersect_ray(query)
    # Now result skips this character's collider
```

**Large Scale Exclusion Using Masks:**
```gdscript
# If you need to exclude many objects, use collision masks instead
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state
    var query: PhysicsRayQueryParameters2D = PhysicsRayQueryParameters2D.create(
        global_position,
        target_position,
        collision_mask,  # Use specific mask
        [self]           # Also exclude self
    )

    var result: Dictionary = space_state.intersect_ray(query)
```

**Key Points:**
- Always exclude the casting body itself
- Use collision masks for larger exclusion lists
- Exceptions array can contain objects or RIDs


## Anti-Pattern: Scaling Collision Shapes

**Source:** Collision Shapes (2D) and Physics Introduction

### Problem: Scaled Collision Shapes Cause Unexpected Behavior

```gdscript
# WRONG - Scaling shapes causes physics issues
extends Node2D

func _ready() -> void:
    var shape: CollisionShape2D = CollisionShape2D.new()
    shape.scale = Vector2(2, 2)  # Never do this
    add_child(shape)

# WRONG - Using Node2D scale property on collision shape
extends Node2D

func _ready() -> void:
    var shape: CollisionShape2D = CollisionShape2D.new()
    var rect: RectangleShape2D = RectangleShape2D.new()
    rect.size = Vector2(50, 50)
    shape.shape = rect
    # Using the inspector's Scale property = Bad
    # Instead use size handles in editor
    add_child(shape)

# RIGHT - Use size properties to resize
extends Node2D

func _ready() -> void:
    var shape: CollisionShape2D = CollisionShape2D.new()
    var rect: RectangleShape2D = RectangleShape2D.new()
    rect.size = Vector2(100, 100)  # Use size property
    shape.shape = rect
    shape.position = Vector2.ZERO  # Keep scale at (1, 1)
    shape.scale = Vector2.ONE      # Explicitly set to (1, 1)
    add_child(shape)
```

**In the Editor:**
- Select CollisionShape2D
- Use the blue resize handles at corners/edges (not the scale handles)
- Keep the Scale property at (1, 1) at all times

**Key Points:**
- Never scale collision shapes
- Use shape properties (size, radius) to resize instead
- Scaled shapes disable engine optimizations
- Causes unpredictable collision behavior
- Scale should remain (1, 1) in Inspector


## Best Practice: Use Static Typing with Physics Code

All physics examples use explicit type annotations for safety and clarity:

```gdscript
# Static typing with physics
extends CharacterBody2D

var velocity: Vector2 = Vector2.ZERO
var speed: float = 300.0

func _physics_process(delta: float) -> void:
    var input_dir: Vector2 = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = input_dir * speed
    move_and_slide()

# Type annotations on parameters and return values
func calculate_bounce(incoming: Vector2, normal: Vector2) -> Vector2:
    return incoming.bounce(normal)

# Typed arrays for collision queries
func check_nearby_objects() -> Array[Node2D]:
    var space_state: PhysicsDirectSpaceState2D = get_world_2d().direct_space_state
    # ... query and collect results ...
    var results: Array[Node2D] = []
    return results
```

**Key Points:**
- Always use type annotations on variables and parameters
- Use return type annotations (-> Type)
- Type array elements: Array[NodeType]
- Helps catch physics setup errors early
- Improves code clarity for complex physics logic
