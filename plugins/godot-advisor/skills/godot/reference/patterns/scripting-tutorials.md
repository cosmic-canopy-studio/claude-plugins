# Godot GDScript Scripting Patterns

Reference patterns extracted from Godot Engine tutorials. All code follows Godot 4.x with explicit static typing.

## GDScript Basics

### Problem: Setting up typed variables with proper syntax

**Solution:** Use explicit type annotations for all variables

```gdscript
# Variable with explicit type
var health: int = 100
var position: Vector2 = Vector2(0, 0)
var speed: float = 5.5

# Type inference with walrus operator
var inferred_type := "String"  # Type is inferred as String

# Untyped (not recommended)
var untyped = 5  # Works but loses type safety
```

**Key points:**
- Always use explicit types for better performance and IDE support
- Use `:=` for type inference when the type is obvious
- Avoid untyped variables in production code

---

### Problem: Organizing related constants and values

**Solution:** Use enums for related constant groups

```gdscript
extends Node

enum State { IDLE, RUNNING, JUMPING, FALLING }
enum Direction { LEFT = -1, RIGHT = 1 }

var current_state: State = State.IDLE

func _ready() -> void:
    # Access enum values with dot notation
    print(State.IDLE)        # Prints 0
    print(State.RUNNING)     # Prints 1
    print(Direction.LEFT)    # Prints -1
```

**Key points:**
- Named enums create a Dictionary-like structure
- Access values with `EnumName.VALUE` syntax
- Useful for state machines and direction constants

---

### Problem: Creating typed function parameters and return types

**Solution:** Specify types for all function parameters and return values

```gdscript
extends Node

# Function with typed parameters and return type
func calculate_damage(base_damage: float, multiplier: float) -> float:
    return base_damage * multiplier

# Function with multiple parameters
func move_entity(direction: Vector2, speed: float, delta: float) -> void:
    position += direction.normalized() * speed * delta

# Function with optional default values
func create_projectile(speed: float = 10.0, direction: Vector2 = Vector2.RIGHT) -> void:
    # Implementation
    pass

# Function that returns null for Objects
func find_enemy() -> Node:
    return null  # Valid for Object types
```

**Key points:**
- Always specify `-> return_type` at the end of function signature
- Use `-> void` for functions that don't return a value
- Only Object types can return `null`

---

## Signal Patterns

### Problem: Defining and emitting custom signals

**Solution:** Declare signals with optional typed parameters

```gdscript
extends Node

# Simple signal without parameters
signal health_depleted

# Signal with typed parameters
signal health_changed(old_value: int, new_value: int)
signal player_died(character_name: String, cause: String)

func take_damage(amount: int) -> void:
    var old_health: int = health
    health -= amount

    # Emit signal with parameters
    health_changed.emit(old_health, health)

    # Emit signal without parameters
    if health <= 0:
        health_depleted.emit()
```

**Key points:**
- Define signal parameter names for editor support
- Use `.emit()` method to emit signals with values
- Parameters are optional when defining signals

---

### Problem: Connecting signals from code

**Solution:** Use `.connect()` method with callback functions

```gdscript
extends Node

# Receiver script example
func _ready() -> void:
    var character_node: Node = get_node("Character")

    # Connect signal to callback method
    character_node.health_changed.connect(_on_character_health_changed)

    # Connect with target object specified
    character_node.health_depleted.connect(_on_health_depleted)

func _on_character_health_changed(old_value: int, new_value: int) -> void:
    print("Health changed from %d to %d" % [old_value, new_value])

func _on_health_depleted() -> void:
    print("Character is dead!")
    get_tree().reload_current_scene()
```

**Key points:**
- Connect signals in `_ready()` when scene tree is ready
- Callback method name is convention: `_on_{node_name}_{signal_name}`
- Parameters must match signal definition

---

### Problem: Passing extra data when connecting signals

**Solution:** Use `.bind()` to attach additional parameters

```gdscript
extends Node

# Emitter script
signal health_changed(old_value: int, new_value: int)

func take_damage(amount: int) -> void:
    var old_health: int = health
    health -= amount
    health_changed.emit(old_health, health)

# Receiver script
func _ready() -> void:
    var character_node: Node = get_node("Character")
    var battle_log: Node = get_node("UI/BattleLog")

    # Connect with bound parameter (character name)
    character_node.health_changed.connect(
        battle_log._on_character_health_changed.bind(character_node.name)
    )

func _on_character_health_changed(old_value: int, new_value: int, character_name: String) -> void:
    var damage: int = old_value - new_value
    print("%s took %d damage" % [character_name, damage])
```

**Key points:**
- Bound parameters appear after signal parameters in callback
- Use `.bind()` to inject context-specific data
- Useful for connecting multiple similar objects

---

### Problem: Waiting for a signal before continuing execution

**Solution:** Use `await` keyword for coroutines

```gdscript
extends Node

func _ready() -> void:
    # Wait for a signal before continuing
    await $Button.pressed
    print("Button was pressed!")

    # Explicit signal connection with await
    var result: bool = await some_node.signal_name

    # Multiple awaits in sequence
    await $Button1.pressed
    await $Button2.pressed
    print("Both buttons pressed!")

func show_dialog() -> void:
    print("Dialog shown")
    # Wait for dialog to close
    await $Dialog.closed
    print("Dialog closed, continuing...")
```

**Key points:**
- `await` pauses function execution until signal is emitted
- Creates coroutines without explicit callback functions
- More readable than `.connect()` for simple waiting

---

### Problem: Decoupling nodes with signals instead of direct references

**Solution:** Emit signals and let parent nodes handle connections

```gdscript
# player.gd - Decoupled player that doesn't know about bullets
extends Sprite2D

signal shoot(bullet_scene: PackedScene, direction: float, location: Vector2)

var Bullet: PackedScene = preload("res://bullet.tscn")

func _input(event: InputEvent) -> void:
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_LEFT and event.pressed:
            shoot.emit(Bullet, rotation, position)

func _process(delta: float) -> void:
    look_at(get_global_mouse_position())

# main_game.gd - Main scene handles bullet spawning
extends Node

func _ready() -> void:
    var player: Node = get_node("Player")
    player.shoot.connect(_on_player_shoot)

func _on_player_shoot(bullet_scene: PackedScene, direction: float, location: Vector2) -> void:
    var spawned_bullet: Node = bullet_scene.instantiate()
    add_child(spawned_bullet)
    spawned_bullet.rotation = direction
    spawned_bullet.position = location
    spawned_bullet.velocity = spawned_bullet.velocity.rotated(direction)
```

**Key points:**
- Player emits signal without knowing how bullets are spawned
- Main scene connects and handles instantiation
- Allows independent testing of player script
- More flexible scene structure changes

---

## Groups Patterns

### Problem: Managing sets of nodes without hard references

**Solution:** Use groups to organize nodes dynamically

```gdscript
extends Node

func _ready() -> void:
    # Add this node to a group
    add_to_group("enemies")
    add_to_group("damageable")

# Caller script - alert all enemies
func _on_player_spotted() -> void:
    # Call method on all nodes in a group
    get_tree().call_group("enemies", "enter_alert_mode")

# Get all nodes in a group as array
func get_all_enemies() -> Array[Node]:
    return get_tree().get_nodes_in_group("enemies") as Array[Node]
```

**Key points:**
- Add nodes to groups in `_ready()` using `add_to_group()`
- Remove nodes with `remove_from_group()`
- Use `call_group()` to invoke method on all group members
- Use `get_nodes_in_group()` to iterate manually

---

### Problem: Creating reusable group-based systems

**Solution:** Define behavior for grouped nodes

```gdscript
# enemy.gd
extends CharacterBody2D

func _ready() -> void:
    add_to_group("enemies")
    add_to_group("ai_controlled")

func enter_alert_mode() -> void:
    print("Alert mode activated!")
    # Change behavior, play animation, etc.

func take_damage(amount: int) -> void:
    print("Taking %d damage" % amount)
    add_to_group("damaged")

# game_manager.gd - Orchestrates group-based actions
extends Node

func _on_large_explosion(location: Vector2, radius: float) -> void:
    var enemies: Array[Node] = get_tree().get_nodes_in_group("enemies")

    for enemy in enemies:
        var distance: float = enemy.global_position.distance_to(location)
        if distance < radius:
            enemy.take_damage(50)

func pause_ai_entities() -> void:
    get_tree().call_group("ai_controlled", "pause")

func unpause_ai_entities() -> void:
    get_tree().call_group("ai_controlled", "unpause")
```

**Key points:**
- Groups allow flexible many-to-one relationships
- Decouple systems that need to manage collections
- Useful for game events affecting multiple nodes

---

## Autoload (Singleton) Patterns

### Problem: Sharing persistent data between scenes

**Solution:** Create autoload script for global state

```gdscript
# global_game_state.gd (added via Project Settings > Autoload)
extends Node

class_name GlobalGameState

var player_health: int = 100
var player_inventory: Array[String] = []
var current_level: int = 1
var total_score: int = 0

func _ready() -> void:
    # This runs automatically when game starts
    print("Global state initialized")

func add_to_inventory(item: String) -> void:
    player_inventory.append(item)
    print("Added %s to inventory" % item)

func increase_score(amount: int) -> void:
    total_score += amount

# Usage from any script
func _on_coin_collected() -> void:
    GlobalGameState.increase_score(10)
    GlobalGameState.add_to_inventory("coin")
```

**Key points:**
- Add script to Project Settings > Autoload
- Name in autoload list becomes the global reference
- Always loaded before first scene
- Persists across scene changes

---

### Problem: Implementing scene switching with custom logic

**Solution:** Use autoload to manage scene transitions

```gdscript
# scene_manager.gd (added as autoload named "SceneManager")
extends Node

var current_scene: Node = null

func _ready() -> void:
    var root: Viewport = get_tree().root
    # Last child is the currently loaded scene
    current_scene = root.get_child(-1)

func goto_scene(path: String) -> void:
    # Defer the scene change to avoid crashes
    # Current scene may still be executing code
    _deferred_goto_scene.call_deferred(path)

func _deferred_goto_scene(path: String) -> void:
    # Safe to remove the old scene now
    current_scene.free()

    # Load new scene
    var new_scene_resource: Resource = ResourceLoader.load(path)

    # Instance the scene
    current_scene = new_scene_resource.instantiate()

    # Add to root
    get_tree().root.add_child(current_scene)

    # Optional: set as current for compatibility
    get_tree().current_scene = current_scene

# Usage from game scenes
func _on_button_pressed() -> void:
    SceneManager.goto_scene("res://scenes/main_menu.tscn")
```

**Key points:**
- Use `call_deferred()` to defer scene changes
- Prevents crashes from scene changes during code execution
- Autoload persists data across scenes
- `get_child(-1)` gets the last child (current scene)

---

### Problem: Preventing autoload from being freed accidentally

**Solution:** Never call `free()` or `queue_free()` on autoloads

```gdscript
# WRONG - Never do this!
GlobalGameState.free()  # CRASH
GlobalGameState.queue_free()  # CRASH

# RIGHT - Store and restore state instead
func reset_game() -> void:
    # Clear the data but keep the autoload
    GlobalGameState.player_health = 100
    GlobalGameState.player_inventory.clear()
    GlobalGameState.current_level = 1
```

**Key points:**
- Autoloads are freed by engine only
- Freeing them causes engine crash
- Reset state by clearing data instead
- Autoload lifetime = entire game session

---

## Resource Patterns

### Problem: Loading resources from code

**Solution:** Use `load()` or `preload()` for different timing needs

```gdscript
extends Node

# Preload at compile-time (GDScript only)
# Must use constant string path
var LoadedTexture: Texture2D = preload("res://assets/player.png")

func _ready() -> void:
    # Load at runtime (works in GDScript and C#)
    # Can use variable paths
    var texture_path: String = "res://assets/weapon.png"
    var weapon_texture: Texture2D = load(texture_path) as Texture2D

    # Assign to sprite
    $Sprite2D.texture = weapon_texture

# Preload is faster since it happens at compile-time
# Load is flexible but slower
```

**Key points:**
- `preload()` happens at compile time (faster, GDScript only)
- `load()` happens at runtime (slower, flexible paths)
- Resources are cached - same path always returns same instance
- No need to manually free resources

---

### Problem: Instantiating scenes from code

**Solution:** Load PackedScene and call `instantiate()`

```gdscript
extends Node

# Preload scene resource (not instance)
var BulletScene: PackedScene = preload("res://projectiles/bullet.tscn")

func _ready() -> void:
    # Create instances on demand
    for i in range(5):
        var bullet_instance: Node = BulletScene.instantiate()
        add_child(bullet_instance)
        bullet_instance.position = Vector2(i * 20, 0)

func spawn_enemy_at(position: Vector2) -> void:
    var enemy: Node = preload("res://enemies/zombie.tscn").instantiate()
    get_parent().add_child(enemy)
    enemy.global_position = position

# Load scene from variable path
func load_level(level_name: String) -> void:
    var scene_path: String = "res://levels/%s.tscn" % level_name
    var level_resource: Resource = ResourceLoader.load(scene_path)
    var level_instance: Node = level_resource.instantiate()
    add_child(level_instance)
```

**Key points:**
- Scenes are stored as PackedScene resources
- Call `.instantiate()` to create instance from PackedScene
- Cached resources mean multiple instances share data
- Images, meshes, etc. are shared between instances

---

### Problem: Creating custom data resources

**Solution:** Extend Resource class with `@export` properties

```gdscript
# bot_stats.gd
class_name BotStats
extends Resource

@export var health: int = 100
@export var speed: float = 5.0
@export var damage: int = 10
@export var weapon: String = "laser"

# Parameters with defaults for creation
func _init(p_health: int = 100, p_speed: float = 5.0, p_damage: int = 10, p_weapon: String = "laser") -> void:
    health = p_health
    speed = p_speed
    damage = p_damage
    weapon = p_weapon

# Usage in game scripts
extends Node

@export var bot_stats: Resource  # Assign in inspector

func _ready() -> void:
    if bot_stats:
        print("Health: %d, Speed: %.1f" % [bot_stats.health, bot_stats.speed])

# Creating and saving custom resources
func create_custom_enemy() -> void:
    var stats: BotStats = BotStats.new(50, 3.0, 15, "gun")
    ResourceSaver.save(stats, "res://data/custom_enemy.tres")
```

**Key points:**
- Use `class_name` to make Resource appear in Create menu
- Use `@export` for editable properties
- Provide `_init()` with default values
- Resources auto-serialize to .tres files

---

### Problem: Using Resource collections as data tables

**Solution:** Create Resource that contains multiple other resources

```gdscript
# enemy_data_table.gd
class_name EnemyDataTable
extends Resource

const BotStats = preload("res://scripts/bot_stats.gd")

var enemy_data: Dictionary[String, BotStats] = {}

func _init() -> void:
    # Create lookup table of enemy types
    enemy_data = {
        "zombie": BotStats.new(30, 1.0, 5, "bite"),
        "ogre": BotStats.new(100, 0.5, 20, "club"),
        "ghost": BotStats.new(20, 2.5, 8, "curse"),
    }

func get_enemy_stats(enemy_type: String) -> BotStats:
    return enemy_data.get(enemy_type, BotStats.new())

# Usage
extends Node

var enemy_table: EnemyDataTable = preload("res://data/enemies.tres")

func spawn_enemy(enemy_type: String, position: Vector2) -> void:
    var stats: BotStats = enemy_table.get_enemy_stats(enemy_type)
    var enemy: Node = create_enemy_node(stats)
    enemy.global_position = position
    add_child(enemy)
```

**Key points:**
- Resources can contain other resources
- Dictionary maps strings to resource types
- Allows data-driven game design
- Inspector can edit resource tables

---

### Problem: Avoiding resource serialization issues

**Solution:** Don't use inner classes for Resource scripts

```gdscript
# WRONG - Resource script uses inner class
extends Node

class MyResource:
    extends Resource
    @export var value: int = 5

func _ready() -> void:
    var res: MyResource = MyResource.new()
    # This will NOT serialize the 'value' property!
    ResourceSaver.save(res, "res://my_res.tres")

# RIGHT - Use top-level class_name
# my_resource.gd
class_name MyResource
extends Resource

@export var value: int = 5

func _init(p_value: int = 5) -> void:
    value = p_value

# Now serialization works correctly
func _ready() -> void:
    var res: MyResource = MyResource.new(10)
    ResourceSaver.save(res, "res://my_res.tres")
```

**Key points:**
- Resource scripts must be top-level (class_name)
- Inner classes don't serialize properties
- Use separate files for custom Resource types
- Properties must have `@export` annotation

---

## Scene Instancing Patterns

### Problem: Getting references to nodes in the scene tree

**Solution:** Use `get_node()` with string paths

```gdscript
extends Node

# Direct child node
@onready var sprite: Sprite2D = get_node("Sprite2D")
@onready var animation: AnimationPlayer = $AnimationPlayer  # Shorthand

# Child of child using paths
@onready var health_bar: ProgressBar = get_node("UI/HealthBar")

# Absolute path from root
@onready var player: Node = get_node("/root/Game/Player")

# Using unique node names (one per scene)
@onready var important_node: Node = %ImportantNode

func _ready() -> void:
    # Access nodes in _ready() to ensure they exist
    sprite.position = Vector2(100, 100)
    animation.play("idle")
```

**Key points:**
- Use `get_node()` in `_ready()` when tree is ready
- Use `$` shorthand for simple paths
- Use absolute paths with `/root` if needed
- `@onready` initializes before `_ready()` is called
- Unique node names with `%` are set in inspector

---

### Problem: Creating nodes from code

**Solution:** Instantiate node class and add to tree

```gdscript
extends Node

func _ready() -> void:
    # Create new node
    var sprite: Sprite2D = Sprite2D.new()
    sprite.position = Vector2(100, 100)

    # Add to scene tree
    add_child(sprite)

    # Now it's active in the scene

func create_ui_label() -> Label:
    var label: Label = Label.new()
    label.text = "Score: 0"
    label.position = Vector2(10, 10)
    add_child(label)
    return label
```

**Key points:**
- New nodes aren't active until added with `add_child()`
- Node becomes active in `_ready()` when added to tree
- Configure node before or after adding
- Can return reference for further configuration

---

### Problem: Removing nodes from the scene

**Solution:** Use `queue_free()` for safe removal

```gdscript
extends Node

func destroy_after_delay() -> void:
    var sprite: Sprite2D = Sprite2D.new()
    add_child(sprite)

    # Queue for deletion at end of frame
    # Safe - sprite can finish its current code
    sprite.queue_free()
    # sprite is still usable here

func immediate_destroy() -> void:
    var node: Node = get_node("MyNode")
    # Immediate destruction - use with caution!
    # node.free()
    # This causes crashes if node code is still running

    # Better to use queue_free()
    node.queue_free()

func _on_bullet_hit() -> void:
    # Queue this bullet for deletion
    queue_free()  # When bullet script finishes, it's removed
```

**Key points:**
- Always use `queue_free()` instead of `free()`
- `queue_free()` waits until frame end
- Allows current code to finish safely
- Freeing parent also frees all children

---

## Best Practices

### Static Typing in All Code

Always use explicit type annotations:

```gdscript
# GOOD - All types specified
func calculate_health(base_health: int, multiplier: float) -> int:
    return int(base_health * multiplier)

var enemies: Array[Enemy] = []
var player_data: Dictionary = {}

# AVOID - Untyped
func calculate(a, b):
    return a * b

var data = {}
```

---

### Signal Connection Timing

Connect signals in `_ready()`, never in `_init()`:

```gdscript
extends Node

# WRONG - _init called before tree is ready
func _init() -> void:
    get_node("Button").pressed.connect(_on_button_pressed)  # May fail

# RIGHT - _ready called after tree is ready
func _ready() -> void:
    get_node("Button").pressed.connect(_on_button_pressed)  # Works
```

---

### Resource Caching

Leverage Godot's resource caching for efficiency:

```gdscript
extends Node

# Same path always returns same loaded resource
var texture1: Texture2D = load("res://sprite.png")
var texture2: Texture2D = load("res://sprite.png")
# texture1 and texture2 reference the same object in memory

# This works for scenes too
var scene1: PackedScene = load("res://enemy.tscn")
var scene2: PackedScene = load("res://enemy.tscn")
# Both reference same cached PackedScene

# But instances are separate
var enemy1: Node = scene1.instantiate()
var enemy2: Node = scene2.instantiate()
# enemy1 and enemy2 are different objects
```

---

### Deferring Expensive Operations

Use `call_deferred()` for scene changes and deletions:

```gdscript
extends Node

func _ready() -> void:
    var button: Button = get_node("Button")
    button.pressed.connect(_on_button_pressed)

func _on_button_pressed() -> void:
    # Wrong - changes scene while button code might still run
    # get_tree().change_scene_to_file("res://next_scene.tscn")

    # Right - defers until safe
    get_tree().change_scene_to_file.call_deferred("res://next_scene.tscn")

    # Or use autoload scene manager
    SceneManager.goto_scene("res://next_scene.tscn")
```

---

## Anti-Patterns

### Anti-Pattern 1: Direct Parent References

Problem: Tightly couples child to parent structure

```gdscript
# WRONG - Can't test independently
extends Node

func _ready() -> void:
    get_parent().handle_event()  # Depends on parent

# RIGHT - Emit signal and let parent decide
extends Node

signal event_occurred

func _ready() -> void:
    event_occurred.emit()
```

---

### Anti-Pattern 2: Untyped Functions

Problem: Loses type safety and IDE support

```gdscript
# WRONG - No type checking
func take_damage(amount):
    health -= amount

# RIGHT - Explicit types
func take_damage(amount: int) -> void:
    health -= amount
```

---

### Anti-Pattern 3: Freeing Autoloads

Problem: Causes engine crash

```gdscript
# WRONG - Crash!
GlobalState.free()
GlobalState.queue_free()

# RIGHT - Reset state instead
GlobalState.reset()
```

---

### Anti-Pattern 4: Connecting in `_init()`

Problem: Scene tree not ready yet

```gdscript
# WRONG - Scene tree not initialized
func _init() -> void:
    get_node("Button").pressed.connect(_on_pressed)

# RIGHT - Use _ready()
func _ready() -> void:
    get_node("Button").pressed.connect(_on_pressed)
```

---

### Anti-Pattern 5: Blocking on Scene Changes

Problem: Script continues running after scene changes

```gdscript
# WRONG - Dialog code continues after scene change
func show_next_level() -> void:
    get_tree().change_scene_to_file("res://level2.tscn")
    # This code still executes but scene is gone!
    var enemies: Array[Node] = get_tree().get_nodes_in_group("enemies")

# RIGHT - Use deferred or autoload
func show_next_level() -> void:
    get_tree().change_scene_to_file.call_deferred("res://level2.tscn")
    # Execution stops here safely

# Or with autoload
func show_next_level() -> void:
    SceneManager.goto_scene("res://level2.tscn")
```

---

### Anti-Pattern 6: Creating Resources as Inner Classes

Problem: Resource properties don't serialize

```gdscript
# WRONG - Won't serialize
extends Node

class MyData:
    extends Resource
    @export var value: int = 5

func _ready() -> void:
    var data: MyData = MyData.new()
    ResourceSaver.save(data, "res://data.tres")  # value not saved!

# RIGHT - Use top-level class_name
# my_data.gd
class_name MyData
extends Resource

@export var value: int = 5
```

---

## Performance Considerations

- Preload resources that are used frequently to avoid runtime loading overhead
- Cache node references with `@onready` instead of calling `get_node()` repeatedly
- Use `call_deferred()` for heavy operations to spread them across frames
- Groups are efficient for managing many objects with similar behavior
- Avoid `get_parent()` - use signals for loose coupling instead
- Resource instances share data, so modifying shared textures affects all users
- Signals are more efficient than polling for state changes

---

## Related Tutorials

- [GDScript Basics](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.rst) - Core language reference
- [Instancing with Signals](https://docs.godotengine.org/en/stable/tutorials/scripting/instancing_with_signals.rst) - Decoupling objects
- [Groups](https://docs.godotengine.org/en/stable/tutorials/scripting/groups.rst) - Managing node collections
- [Singletons (Autoload)](https://docs.godotengine.org/en/stable/tutorials/scripting/singletons_autoload.rst) - Global state management
- [Resources](https://docs.godotengine.org/en/stable/tutorials/scripting/resources.rst) - Data management
- [Nodes and Scene Instances](https://docs.godotengine.org/en/stable/tutorials/scripting/nodes_and_scene_instances.rst) - Scene tree manipulation
