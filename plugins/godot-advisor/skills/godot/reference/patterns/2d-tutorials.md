# Godot 2D Tutorials: Extracted Patterns

Patterns extracted from Godot documentation tutorials: 2D movement, CharacterBody2D, Physics introduction, and TileMaps.

## Movement Patterns

### Problem: Basic 8-way movement with keyboard input

**Solution:** Use `Input.get_vector()` to gather directional input and multiply by speed constant.

Source: [2D movement overview](https://docs.godotengine.org/en/stable/tutorials/2d/2d_movement.rst)

```gdscript
extends CharacterBody2D

@export var speed: float = 400.0

func get_input() -> void:
    var input_direction: Vector2 = Input.get_vector("left", "right", "up", "down")
    velocity = input_direction * speed

func _physics_process(delta: float) -> void:
    get_input()
    move_and_slide()
```

**Key points:**
- `Input.get_vector()` returns normalized direction (-1, 0, or 1 on each axis)
- Multiplying by a constant `speed` gives consistent movement in all directions
- Works for 8-way movement (4 directions plus diagonals)
- Use `move_and_slide()` for automatic sliding collision response

---

### Problem: Rotation-based movement (Asteroids-style)

**Solution:** Use `transform.x` to get forward direction vector and apply input rotation to the body.

Source: [2D movement overview](https://docs.godotengine.org/en/stable/tutorials/2d/2d_movement.rst)

```gdscript
extends CharacterBody2D

@export var speed: float = 400.0
@export var rotation_speed: float = 1.5

var rotation_direction: float = 0.0

func get_input() -> void:
    rotation_direction = Input.get_axis("left", "right")
    velocity = transform.x * Input.get_axis("down", "up") * speed

func _physics_process(delta: float) -> void:
    get_input()
    rotation += rotation_direction * rotation_speed * delta
    move_and_slide()
```

**Key points:**
- `transform.x` is the node's forward direction vector
- Rotation is applied directly to the node's rotation property
- Use `Input.get_axis()` to get -1, 0, or 1 values
- Delta time is essential for smooth rotation speed

---

### Problem: Mouse-look rotation with keyboard forward/back movement

**Solution:** Use `look_at()` method with mouse position, combine with forward/back input.

Source: [2D movement overview](https://docs.godotengine.org/en/stable/tutorials/2d/2d_movement.rst)

```gdscript
extends CharacterBody2D

@export var speed: float = 400.0

func get_input() -> void:
    look_at(get_global_mouse_position())
    velocity = transform.x * Input.get_axis("down", "up") * speed

func _physics_process(delta: float) -> void:
    get_input()
    move_and_slide()
```

**Alternative (manual rotation calculation):**

```gdscript
# Instead of look_at():
rotation = get_global_mouse_position().angle_to(position)
```

**Key points:**
- `look_at()` automatically calculates rotation to point at target
- Mouse movement drives rotation each frame
- Forward/back still controlled by keyboard input
- Works well for twin-stick style or point-and-click movement

---

### Problem: Click-to-move pathfinding (point and click movement)

**Solution:** Store target position from mouse click, calculate direction each frame, check distance to stop jitter.

Source: [2D movement overview](https://docs.godotengine.org/en/stable/tutorials/2d/2d_movement.rst)

```gdscript
extends CharacterBody2D

@export var speed: float = 400.0

var target: Vector2

func _ready() -> void:
    target = position

func _input(event: InputEvent) -> void:
    # Only accept single clicks, not dragging
    if event.is_action_pressed(&"click"):
        target = get_global_mouse_position()

func _physics_process(delta: float) -> void:
    velocity = position.direction_to(target) * speed
    # Optional: face direction of movement
    # look_at(target)
    if position.distance_to(target) > 10:
        move_and_slide()
```

**Key points:**
- Store click position as target, not intermediate waypoints
- Use `direction_to()` to get normalized direction vector
- **Critical:** Distance check prevents jitter when reaching target
- Body overshoots then oscillates if distance check is omitted
- Can be used for following any target (player, NPC, etc.)

---

## CharacterBody2D Patterns

### Problem: Understanding when to use move_and_collide vs move_and_slide

**Solution:** Use `move_and_collide()` for custom responses, `move_and_slide()` for common cases like platformers.

Source: [Using CharacterBody2D/3D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.rst)

**Use `move_and_collide()` when:**
- You need custom collision response (bouncing, reflecting)
- You want fine control over what happens after collision
- Returns `KinematicCollision2D` object with collision data

```gdscript
extends CharacterBody2D

var speed: float = 300.0

func get_input() -> void:
    var input_dir: Vector2 = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = input_dir * speed

func _physics_process(delta: float) -> void:
    get_input()
    move_and_collide(velocity * delta)
```

**Use `move_and_slide()` when:**
- You want sliding collision response (sliding along walls/slopes)
- You're making a platformer or top-down game
- You want automatic velocity adjustment after collision

```gdscript
extends CharacterBody2D

var speed: float = 300.0

func get_input() -> void:
    var input_dir: Vector2 = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")
    velocity = input_dir * speed

func _physics_process(delta: float) -> void:
    get_input()
    move_and_slide()
```

**Key points:**
- `move_and_collide()` doesn't multiply by delta internally
- `move_and_slide()` **does** multiply by delta internally (don't multiply velocity by delta)
- Both must be called in `_physics_process()`, not `_process()`

---

### Problem: Bouncing projectiles off walls

**Solution:** Use `move_and_collide()` with `velocity.bounce()` method on collision normal.

Source: [Using CharacterBody2D/3D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.rst)

```gdscript
extends CharacterBody2D

var speed: float = 750.0

func start(start_position: Vector2, direction: float) -> void:
    rotation = direction
    position = start_position
    velocity = Vector2(speed, 0).rotated(rotation)

func _physics_process(delta: float) -> void:
    var collision: KinematicCollision2D = move_and_collide(velocity * delta)
    if collision:
        # Bounce velocity off the collision normal
        velocity = velocity.bounce(collision.get_normal())
        # Call method on colliding object if it exists
        if collision.get_collider().has_method("hit"):
            collision.get_collider().hit()

func _on_VisibilityNotifier2D_screen_exited() -> void:
    # Clean up when off-screen
    queue_free()
```

**Key points:**
- `move_and_collide()` returns `KinematicCollision2D` on collision, `null` otherwise
- `collision.get_normal()` gives the perpendicular to the collision surface
- `Vector2.bounce()` reflects velocity correctly off surfaces
- Can check collider with `has_method()` before calling custom methods

---

### Problem: Platformer movement with gravity and jumping

**Solution:** Apply gravity to velocity each frame, check `is_on_floor()` before jumping, use `move_and_slide()`.

Source: [Using CharacterBody2D/3D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.rst)

```gdscript
extends CharacterBody2D

var speed: float = 300.0
var jump_speed: float = -400.0

# Get gravity from project settings to sync with RigidBody2D
var gravity: float = ProjectSettings.get_setting("physics/2d/default_gravity")

func _physics_process(delta: float) -> void:
    # Apply gravity every frame
    velocity.y += gravity * delta

    # Allow jump only when touching ground
    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_speed

    # Get horizontal input
    var direction: float = Input.get_axis("ui_left", "ui_right")
    velocity.x = direction * speed

    move_and_slide()
```

**Key points:**
- Gravity is acceleration (velocity per second), must be multiplied by delta
- Jump velocity is velocity (pixels per second), already accounts for frame time in `move_and_slide()`
- `is_on_floor()` checks collision with surfaces below the body
- `ProjectSettings.get_setting()` keeps gravity in sync with RigidBody2D physics
- Don't multiply velocity by delta when using `move_and_slide()`

---

### Problem: Detecting and processing collisions with move_and_slide

**Solution:** Use `get_slide_collision_count()` and `get_slide_collision()` in a loop after calling `move_and_slide()`.

Source: [Using CharacterBody2D/3D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.rst)

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    move_and_slide()

    # Process all collisions that occurred
    for i in range(get_slide_collision_count()):
        var collision: KinematicCollision2D = get_slide_collision(i)
        print("Collided with: ", collision.get_collider().name)

        # Access collision data
        var collision_point: Vector2 = collision.get_position()
        var collision_normal: Vector2 = collision.get_normal()
```

**Alternative with move_and_collide:**

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var collision: KinematicCollision2D = move_and_collide(velocity * delta)
    if collision:
        print("Collided with: ", collision.get_collider().name)
```

**Key points:**
- `get_slide_collision_count()` only counts direction changes, not every contact
- Works after `move_and_slide()` returns
- `move_and_collide()` returns collision directly
- `KinematicCollision2D` contains position, normal, collider, and more

---

## Physics Fundamentals

### Problem: Choosing the right physics body type

**Solution:** Select body type based on movement control needs.

Source: [Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.rst)

| Type | Control | Physics | Use Case |
|------|---------|---------|----------|
| **CharacterBody2D** | Full code control | None (manual) | Players, NPCs |
| **RigidBody2D** | Forces applied | Full simulation | Objects, debris |
| **StaticBody2D** | None | None | Walls, platforms |
| **Area2D** | N/A (detection only) | None | Triggers, zones |

**CharacterBody2D (player-controlled):**

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    # You calculate all movement
    velocity = calculate_movement()
    move_and_slide()
```

**RigidBody2D (physics-simulated):**

```gdscript
extends RigidBody2D

func _integrate_forces(state: PhysicsDirectBodyState2D) -> void:
    # Apply forces, engine calculates movement
    if Input.is_action_pressed("ui_up"):
        state.apply_force(Vector2(0, -250))
```

**StaticBody2D (environment):**

```gdscript
# No script needed, just collision shapes
# Can be configured in editor with physics materials
```

**Area2D (detection):**

```gdscript
extends Area2D

func _ready() -> void:
    area_entered.connect(_on_area_entered)

func _on_area_entered(area: Area2D) -> void:
    print("Something entered!")
```

**Key points:**
- CharacterBody2D: Use for full movement control (players, enemies with AI)
- RigidBody2D: Use for realistic physics (gravity, bouncing, stacking)
- StaticBody2D: Use for environment (doesn't need to move)
- Area2D: Use for detection and triggers (no physical collision response)

---

### Problem: Setting up collision layers and masks correctly

**Solution:** Assign collision layer per object type, set masks for what to detect.

Source: [Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.rst)

**Example game setup:**

1. Define layer names in **Project Settings > Layer Names > 2D Physics:**
   - Layer 1: `walls`
   - Layer 2: `player`
   - Layer 3: `enemies`
   - Layer 4: `coins`

2. Configure each object:
   - **Walls** (StaticBody2D): Layer=1, Mask=1
   - **Player** (CharacterBody2D): Layer=2, Mask=0b1101 (walls + enemies + coins)
   - **Enemy** (CharacterBody2D): Layer=3, Mask=0b0001 (walls only)
   - **Coin** (Area2D): Layer=4, Mask=0b0000 (detection only)

**In code:**

```gdscript
extends CharacterBody2D

func _ready() -> void:
    # Player on layer 2, detect walls(1), enemies(3), coins(4)
    collision_layer = 2
    collision_mask = 0b1101  # Binary: layers 1, 3, 4

    # Or set individually:
    set_collision_layer_value(2, true)
    set_collision_mask_value(1, true)
    set_collision_mask_value(3, true)
    set_collision_mask_value(4, true)
```

**Decimal equivalent:**

```gdscript
# Layer 2 only: 2^(2-1) = 2^1 = 2
collision_layer = 2

# Mask for layers 1, 3, 4: 2^(1-1) + 2^(3-1) + 2^(4-1) = 1 + 4 + 8 = 13
collision_mask = 13
```

**Key points:**
- Layer: Which layer(s) this object belongs to
- Mask: Which layers this object detects/collides with
- Collision happens only if A detects B's layer AND B detects A's layer
- Use layer names in Project Settings for clarity

---

### Problem: Understanding physics process vs idle process

**Solution:** Run physics code in `_physics_process()`, visual code in `_process()`.

Source: [Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.rst)

```gdscript
extends CharacterBody2D

func _process(delta: float) -> void:
    # Runs variable rate, synced with frame rate
    # Use for: animation, visual effects, non-physics logic
    update_animation()
    play_sound()

func _physics_process(delta: float) -> void:
    # Runs fixed rate (default 60 Hz)
    # Use for: all movement, collision detection, physics
    apply_gravity()
    move_and_slide()
```

**Key points:**
- Physics runs at fixed timestep (default 60 Hz) for consistency
- Frame rate varies based on rendering load
- Physics code must use `_physics_process()` for predictable behavior
- Visual code can use `_process()` (non-critical timing)
- Delta is different in each callback (fixed vs variable)

---

## TileMap Patterns

### Problem: Setting up a TileMap with reusable TileSet

**Solution:** Save TileSet to external resource, reference from multiple TileMapLayers.

Source: [Using TileMaps](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.rst)

**Step 1: Create and save TileSet**

```gdscript
# In editor: TileMapLayer > TileSet dropdown > Save
# This saves the TileSet to a .tres file
```

**Step 2: Use TileSet in multiple TileMapLayers**

```gdscript
# Scene structure:
# - Level (Node2D)
#   - Tilemap_Background (TileMapLayer)  # Points to level_tileset.tres
#   - Tilemap_Main (TileMapLayer)        # Points to level_tileset.tres
#   - Tilemap_Foreground (TileMapLayer)  # Points to level_tileset.tres
```

**In code:**

```gdscript
extends Node2D

@onready var tilemap_bg: TileMapLayer = $Tilemap_Background
@onready var tilemap_main: TileMapLayer = $Tilemap_Main

func _ready() -> void:
    # All tilemap layers use the same external TileSet resource
    var shared_tileset: TileSet = load("res://tilesets/level_tileset.tres")

    # Can verify they're using it
    assert(tilemap_bg.tile_set == shared_tileset)
    assert(tilemap_main.tile_set == shared_tileset)
```

**Key points:**
- Save TileSet to `.tres` file to reuse across multiple levels
- Built-in TileSets are useful for prototyping but not production
- TileMapLayers at different Z heights create visual layering
- All layers can share the same TileSet resource

---

### Problem: Organizing tilemaps with multiple layers for foreground/background

**Solution:** Create multiple TileMapLayer nodes, assign different visual priorities.

Source: [Using TileMaps](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.rst)

```gdscript
# Scene structure (order matters for rendering):
# - Level (Node2D)
#   - Tilemap_Background (TileMapLayer, Z=0)
#     - Grass, sky, distant hills
#   - Character (CharacterBody2D, Z=1)
#   - Tilemap_Main (TileMapLayer, Z=2)
#     - Ground tiles, walls
#   - Tilemap_Foreground (TileMapLayer, Z=3)
#     - Trees, buildings that block character

extends Node2D

func _ready() -> void:
    # Set Z indices to control draw order
    $Tilemap_Background.z_index = 0
    $Tilemap_Main.z_index = 2
    $Tilemap_Foreground.z_index = 3

    # Enable Y-sorting for depth-based layering
    $Tilemap_Main.y_sort_enabled = true
```

**Key points:**
- Higher Z index draws on top
- Multiple layers enable foreground/background effects
- Y-sorting creates pseudo-3D depth based on Y position
- Removing a layer deletes all tiles on that layer (be careful!)

---

### Problem: Enabling collision on specific tiles in a TileMap

**Solution:** Configure collision shapes in TileSet editor, enable collision in TileMapLayer properties.

Source: [Using TileMaps](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.rst)

**In TileSet editor:**

```gdscript
# 1. Select tile in TileSet editor
# 2. Click "Physics" layer
# 3. Draw collision shape on tile
# 4. Save TileSet
```

**In TileMapLayer inspector:**

```gdscript
# - Physics > Collision Enabled: ON
# - Physics > Collision Visibility Mode: Show when debugging (default)
```

**In code (checking collisions):**

```gdscript
extends CharacterBody2D

@onready var tilemap: TileMapLayer = $TileMap

func _physics_process(delta: float) -> void:
    move_and_slide()

    # Check what tile we're standing on
    var tile_coords: Vector2i = tilemap.local_to_map(global_position)
    var tile_data: TileData = tilemap.get_tile_data(tile_coords)

    if tile_data:
        print("Standing on tile: ", tile_data)
        # Can check custom data or physics properties
```

**Key points:**
- Collision shapes are stored in TileSet, not TileMapLayer
- Each tile can have multiple collision shapes
- Enable collision in TileMapLayer properties for it to work
- Can access tile data at runtime for custom logic

---

### Problem: Painting terrain with automatic connections

**Solution:** Set up terrain sets in TileSet, use Connect or Path mode in TileMap editor.

Source: [Using TileMaps](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.rst)

**In TileSet editor:**

```gdscript
# 1. Create terrain set (e.g., "Ground")
# 2. Add terrain type (e.g., "Grass")
# 3. Assign terrain bits to tiles that should connect
# 4. Save TileSet
```

**In TileMap editor:**

- Switch to "Terrains" tab
- Select "Connect" mode (auto-connects to adjacent tiles)
- Or select "Path" mode (connects only in current stroke)
- Paint terrain tiles

**Benefits:**

```gdscript
# With terrain mode:
# - Painting grass next to grass auto-transitions edges
# - Prevents manual edge-matching tiles
# - Saves time on large areas
# - Path mode gives more control than Connect mode
```

**Key points:**
- Terrain system reduces tile-painting tedium
- Requires setup in TileSet editor (terrain sets and bits)
- Connect mode auto-corrects edges (less control)
- Path mode connects only in current stroke (more control)

---

### Problem: Missing tiles in TileMap

**Solution:** Placeholders show in editor, invisible in game. Re-add matching tile ID to fix.

Source: [Using TileMaps](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.rst)

```gdscript
# Workflow:
# 1. Delete a tile from TileSet (accidentally or intentionally)
# 2. TileMapLayer shows placeholder icon in editor
# 3. Placeholder is NOT visible in running game
# 4. Tile data is preserved on disk
# 5. Re-add tile with same ID to restore appearance
```

**To prevent data loss:**

```gdscript
# Best practice: Don't delete tiles, mark as deprecated instead
# Or save separate version before removing tiles
# TileMap will preserve data even without visual feedback
```

**Key points:**
- Missing tile placeholders only appear in editor
- Data persists even without visual feedback
- Can safely close and reopen scene
- Re-adding tile with same ID restores it immediately

---

## Kinematic Character Movement (Legacy-style)

### Problem: Basic kinematic character movement with gravity

**Solution:** Apply gravity to velocity, use `move_and_slide()` for collision-aware movement.

Source: [Kinematic character (2D)](https://docs.godotengine.org/en/stable/tutorials/physics/kinematic_character_2d.rst)

```gdscript
extends CharacterBody2D

const GRAVITY: float = 200.0
const WALK_SPEED: int = 200

func _physics_process(delta: float) -> void:
    # Apply gravity (acceleration)
    velocity.y += delta * GRAVITY

    # Get input
    if Input.is_action_pressed("ui_left"):
        velocity.x = -WALK_SPEED
    elif Input.is_action_pressed("ui_right"):
        velocity.x = WALK_SPEED
    else:
        velocity.x = 0

    # Move with slide collision response
    move_and_slide()
```

**Key points:**
- Gravity is acceleration (constant value scaled by delta)
- Walk speed is velocity (pixels per second)
- `move_and_slide()` automatically incorporates delta
- Character falls, stops at ground, can walk on platforms

---

### Problem: Detecting specific collision surfaces (floor, wall, ceiling)

**Solution:** Use `is_on_floor()`, `is_on_wall()`, `is_on_ceiling()` after `move_and_slide()`.

Source: [Using CharacterBody2D/3D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.rst)

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    move_and_slide()

    # Check what surfaces we're touching
    if is_on_floor():
        print("Standing on ground")

    if is_on_wall():
        print("Touching wall")

    if is_on_ceiling():
        print("Head hit ceiling")
```

**Configuration:**

```gdscript
extends CharacterBody2D

func _ready() -> void:
    # Define what's considered "floor"
    up_direction = Vector2.UP  # Default: Vector2(0, -1)

    # Set maximum floor angle (default 45 degrees)
    floor_max_angle = deg_to_rad(45.0)

    # Prevent sliding down slopes when standing still
    floor_stop_on_slope = true
```

**Key points:**
- `up_direction` defines floor relative to character orientation
- Default up is negative Y (top of screen in 2D)
- These checks work with `move_and_slide()` only
- Use with jump logic to prevent mid-air jumps

---

## Anti-Patterns

### Anti-Pattern: Setting position directly instead of using move methods

**Wrong - Bypasses collision detection:**

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    # BAD: Position changes ignore collisions
    position += velocity * delta
    # Character will clip through walls
```

**Right - Uses collision-aware movement:**

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    # GOOD: Detects and responds to collisions
    move_and_slide()
```

**Why:** `position` changes are instant with no collision checking. Use `move_and_collide()` or `move_and_slide()` to detect collisions before moving.

---

### Anti-Pattern: Multiplying velocity by delta twice

**Wrong - Velocity scaled twice:**

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    velocity = input_direction * speed * delta  # BAD
    move_and_slide()  # move_and_slide also scales by delta
    # Effective speed is (speed * delta * delta), too slow
```

**Right - Let move_and_slide handle delta:**

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    velocity = input_direction * speed  # GOOD
    move_and_slide()  # Applies delta internally
```

**Exception for move_and_collide:**

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var collision = move_and_collide(velocity * delta)  # CORRECT
    # move_and_collide does NOT scale delta internally
```

**Why:** `move_and_slide()` applies delta internally, `move_and_collide()` does not.

---

### Anti-Pattern: Scaling collision shapes instead of adjusting parameters

**Wrong - Causes physics engine errors:**

```gdscript
# In editor: Selected CollisionShape2D
# Scale property set to (2, 2) - BAD
# OR in code:
extends Node2D

func _ready() -> void:
    $CollisionShape2D.scale = Vector2(2, 2)  # BAD
```

**Right - Adjust shape parameters:**

```gdscript
# In editor: Selected CollisionShape2D > Shape
# CircleShape2D > Radius: 60 (instead of scale)
# OR in code:
extends Node2D

func _ready() -> void:
    var circle: CircleShape2D = $CollisionShape2D.shape
    circle.radius = 60  # GOOD
```

**Why:** Physics engine doesn't handle scale well on collision shapes. Leads to clipping, tunneling, and unpredictable behavior.

---

### Anti-Pattern: Jittering when reaching click-to-move target

**Wrong - No distance check causes oscillation:**

```gdscript
extends CharacterBody2D

var target: Vector2

func _physics_process(delta: float) -> void:
    velocity = position.direction_to(target) * speed
    move_and_slide()  # Overshoots, tries to correct, overshoots again
```

**Right - Check distance before moving:**

```gdscript
extends CharacterBody2D

var target: Vector2

func _physics_process(delta: float) -> void:
    velocity = position.direction_to(target) * speed
    if position.distance_to(target) > 10:  # GOOD: threshold distance
        move_and_slide()
```

**Why:** Without distance check, character overshoots target, moves back, overshoots again, creating visible jitter. Small threshold distance (10-15 pixels) prevents this.

---

### Anti-Pattern: Running physics code in _process instead of _physics_process

**Wrong - Physics code in wrong callback:**

```gdscript
extends CharacterBody2D

func _process(delta: float) -> void:  # BAD
    move_and_slide()  # Unreliable timing
```

**Right - Physics code in physics callback:**

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:  # GOOD
    move_and_slide()  # Fixed timestep, predictable
```

**Why:** Physics engine runs at fixed rate (60 Hz default). Using `_process()` (variable frame rate) causes inconsistent physics behavior, sliding speeds vary based on FPS.

---

### Anti-Pattern: Not using velocity property with move_and_slide

**Wrong - Creates new vector each frame:**

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    var current_velocity: Vector2 = calculate_movement()
    move_and_slide()  # Uses velocity property, not current_velocity
```

**Right - Store in velocity property:**

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    velocity = calculate_movement()
    move_and_slide()  # Uses stored velocity property
```

**Why:** `move_and_slide()` reads from the node's `velocity` property. If you don't store your calculated velocity there, `move_and_slide()` may use stale or zero velocity.

---

### Anti-Pattern: Assuming gravity constant across projects

**Wrong - Hardcoded gravity:**

```gdscript
extends CharacterBody2D

const GRAVITY: float = 800.0  # Breaks if project gravity changes
```

**Right - Read from project settings:**

```gdscript
extends CharacterBody2D

var gravity: float

func _ready() -> void:
    gravity = ProjectSettings.get_setting("physics/2d/default_gravity")
```

**Why:** Different projects may use different gravity values. Using project settings keeps physics in sync across RigidBody2D and CharacterBody2D.

---

## Best Practices

### Practice 1: Use normalized input vectors for consistent movement

**Explanation:** `Input.get_vector()` returns a normalized vector (length 1) unless multiple keys are pressed diagonally, then it's normalized to sqrt(2)/2. This ensures consistent speed in all directions.

```gdscript
extends CharacterBody2D

@export var speed: float = 300.0

func _physics_process(delta: float) -> void:
    # Normalized direction (length = 1 or 0)
    var direction: Vector2 = Input.get_vector("ui_left", "ui_right", "ui_up", "ui_down")

    # Diagonal movement is same speed as cardinal
    velocity = direction * speed
    move_and_slide()
```

---

### Practice 2: Organize TileMap layers by depth and function

**Explanation:** Use multiple TileMapLayers for different visual depths and game logic. Keeps scenes organized and enables easy reordering.

```gdscript
# Recommended structure:
# - Level
#   - Tilemap_Background (Z=-1)     # Sky, far scenery
#   - Tilemap_Platforms (Z=0)       # Ground, collisions
#   - Character (Z=1)               # Player sprite
#   - Tilemap_Objects (Z=2)         # Trees, props
#   - Tilemap_Foreground (Z=3)      # UI overlays
```

---

### Practice 3: Cache frequently accessed nodes with @onready

**Explanation:** Avoids repeated `get_node()` calls and makes code more readable.

```gdscript
extends CharacterBody2D

@onready var tilemap: TileMapLayer = $TileMap
@onready var sprite: Sprite2D = $Sprite2D
@onready var collision: CollisionShape2D = $CollisionShape2D

func _physics_process(delta: float) -> void:
    # Use cached references instead of $TileMap each frame
    var tile_data: TileData = tilemap.get_tile_data(...)
```

---

### Practice 4: Use constants for exported values with sensible defaults

**Explanation:** Constants allow easy tweaking while making intent clear.

```gdscript
extends CharacterBody2D

const DEFAULT_SPEED: float = 300.0
const DEFAULT_JUMP_SPEED: float = -400.0

@export var speed: float = DEFAULT_SPEED
@export var jump_speed: float = DEFAULT_JUMP_SPEED
@export var gravity: float = ProjectSettings.get_setting("physics/2d/default_gravity")
```

---

### Practice 5: Separate input handling into dedicated function

**Explanation:** Makes code modular and easier to refactor. Useful for UI blocking or input rebinding.

```gdscript
extends CharacterBody2D

func get_input() -> void:
    var direction: float = Input.get_axis("ui_left", "ui_right")
    velocity.x = direction * speed

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_speed

func _physics_process(delta: float) -> void:
    velocity.y += gravity * delta
    get_input()
    move_and_slide()
```

---

### Practice 6: Check collision after move_and_slide for effects

**Explanation:** Process collisions immediately after moving to trigger sounds, particles, or damage.

```gdscript
extends CharacterBody2D

func _physics_process(delta: float) -> void:
    move_and_slide()

    # Process any collisions that occurred
    for i in range(get_slide_collision_count()):
        var collision: KinematicCollision2D = get_slide_collision(i)
        var collider = collision.get_collider()

        if collider.is_in_group("enemy"):
            take_damage(10)
        elif collider.is_in_group("coin"):
            collider.collect()
```

---

## Performance Considerations

- **TileMap optimization:** Use appropriate quadrant size (larger = fewer draw calls, slower edits)
- **Collision checks:** Disable collision on objects that don't need it (Area2D vs StaticBody2D)
- **Physics update rate:** Lower fixed physics timestep (60 Hz default) for faster game, higher for smoother motion
- **Movement methods:** `move_and_slide()` may do multiple collision passes (up to 5 default); use `move_and_collide()` for single check if performance critical
- **Layer and mask:** Properly configure collision layers/masks to reduce unnecessary collision checks
- **Debug visualization:** Disable "Visible Collision Shapes" in production for performance

---

## Related Tutorials

- [2D movement overview](https://docs.godotengine.org/en/stable/tutorials/2d/2d_movement.rst) - Movement technique patterns
- [Using CharacterBody2D/3D](https://docs.godotengine.org/en/stable/tutorials/physics/using_character_body_2d.rst) - Detailed body physics
- [Physics introduction](https://docs.godotengine.org/en/stable/tutorials/physics/physics_introduction.rst) - Body types and layers
- [Kinematic character (2D)](https://docs.godotengine.org/en/stable/tutorials/physics/kinematic_character_2d.rst) - Classic movement setup
- [Using TileMaps](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.rst) - Tilemap editor and workflow
- [Using TileSets](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.rst) - TileSet creation and terrains
