---
topic: gdscript-basics
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html
  - https://learnxinyminutes.com/gdscript/
  - https://school.gdquest.com/cheatsheets/gdscript
  - https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html
  - repos/godot_node_essentials (GDQuest examples)
---

# GDScript Basics

Comprehensive reference for GDScript syntax, types, and core language features.

## Script Structure {#structure}

Every GDScript file is implicitly a class:

```gdscript
# Optional: Give your class a global name
class_name PlayerController

# Optional: Extend a base class (default: RefCounted)
extends CharacterBody2D

# Optional: Docstring for the class
## Handles player movement and input for 2D platformer.

# Constants (compile-time values)
const MAX_SPEED: float = 600.0
const JUMP_STRENGTH: float = 1400.0

# Exports (visible in Inspector)
@export var speed: float = 600.0
@export var gravity: float = 4500.0

# Signals
signal health_changed(new_health: int, max_health: int)
signal died

# Private variables (convention: prefix with _)
var _horizontal_direction: float = 0.0

# Onready variables (initialized when node enters scene tree)
@onready var _animation_player: AnimationPlayer = %AnimationPlayer
@onready var _skin: Node2D = %Skin

# Lifecycle methods
func _ready() -> void:
    # Called when node enters scene tree
    pass

func _process(delta: float) -> void:
    # Called every frame
    pass

func _physics_process(delta: float) -> void:
    # Called every physics frame (default: 60 FPS)
    pass

# Custom methods
func take_damage(amount: int) -> void:
    health -= amount
    health_changed.emit(health, max_health)
```

**Order Convention:**
1. `class_name` and `extends`
2. Docstring
3. Signals
4. Enums
5. Constants
6. `@export` variables
7. Public variables
8. Private variables (prefixed with `_`)
9. `@onready` variables
10. Lifecycle methods (`_init`, `_ready`, `_process`, etc.)
11. Public methods
12. Private methods

## Variables {#variables}

### Static Typing (Recommended)

Use type hints for better performance and IDE support:

```gdscript
# Explicit type annotation
var health: int = 100
var player_name: String = "Hero"
var is_alive: bool = true
var position: Vector2 = Vector2.ZERO

# Type inference with :=
var speed := 600.0  # float inferred
var items := []  # Array inferred
var config := {}  # Dictionary inferred

# Typed arrays
var enemies: Array[Node] = []
var scores: Array[int] = [10, 20, 30]

# Typed dictionaries
var settings: Dictionary = {}
var data: Dictionary[String, int] = {"coins": 100, "lives": 3}

# Node references with type
var player: CharacterBody2D = null
@onready var sprite: Sprite2D = $Sprite2D
@onready var timer: Timer = %RespawnTimer  # Unique name with %
```

### Dynamic Typing

Variables without type hints are dynamically typed:

```gdscript
var dynamic_var  # Can hold any type
dynamic_var = 42
dynamic_var = "Now a string"
dynamic_var = Vector2(10, 20)
```

### Constants

Constants are always statically typed:

```gdscript
const MAX_HEALTH: int = 100
const PI_DOUBLE: float = PI * 2.0
const GRAVITY: Vector2 = Vector2(0, 980)

# Enums create integer constants
enum Direction { UP, DOWN, LEFT, RIGHT }
enum { IDLE, WALK, RUN, JUMP }  # Anonymous enum

# Typed enums (Godot 4.2+)
enum MoveState { IDLE = 0, WALKING = 1, RUNNING = 2 }

# Use in code
var current_direction: Direction = Direction.RIGHT
var state: MoveState = MoveState.IDLE
```

## Functions {#functions}

### Function Declaration

```gdscript
# No return value
func say_hello() -> void:
    print("Hello!")

# With return type
func add(a: int, b: int) -> int:
    return a + b

# Multiple parameters
func attack(target: Node, damage: int, knockback: Vector2) -> void:
    target.take_damage(damage)
    target.apply_impulse(knockback)

# Default parameter values
func spawn_enemy(position: Vector2, health: int = 100) -> void:
    var enemy := Enemy.new()
    enemy.global_position = position
    enemy.health = health

# Optional parameters (must be at end)
func create_item(item_type: String, count: int = 1, rare: bool = false) -> void:
    pass
```

### Lambda Functions

Anonymous functions for callbacks:

```gdscript
# Basic lambda
var greet := func() -> void: print("Hi!")
greet.call()

# Lambda with parameters
var multiply := func(a: int, b: int) -> int: return a * b
var result := multiply.call(5, 3)  # 15

# Multi-line lambda
var process_data := func(items: Array) -> void:
    for item in items:
        print(item)
    print("Done!")

# Lambda in signal connection
button.pressed.connect(func() -> void:
    print("Button clicked!")
)

# Lambda with captured variables (capture by value for primitives)
var counts: Array[int] = [0]
var increment := func() -> void:
    counts[0] += 1  # Modify array element, not primitive

signal.connect(increment)
```

### Static Functions

Can be called without an instance:

```gdscript
static func calculate_distance(a: Vector2, b: Vector2) -> float:
    return a.distance_to(b)

# Call from another script
var dist := MyScript.calculate_distance(Vector2.ZERO, Vector2(10, 10))
```

## Built-in Types {#types}

### Primitives

```gdscript
# Boolean
var is_ready: bool = true
var can_jump: bool = false

# Integers
var score: int = 100
var level: int = 5

# Floats
var health: float = 75.5
var speed: float = 300.0

# Strings
var name: String = "Player"
var message: String = "Hello, World!"
var multiline := """
    This is a
    multiline string
"""

# String formatting
var text := "Score: %d" % score
var info := "Player: %s, Level: %d" % [name, level]
```

### Vectors

```gdscript
# Vector2 (2D position, direction, velocity)
var position: Vector2 = Vector2(100, 50)
var velocity: Vector2 = Vector2.ZERO
var direction: Vector2 = Vector2.RIGHT

# Common Vector2 operations
var normalized := direction.normalized()  # Unit vector
var length := velocity.length()  # Magnitude
var distance := position.distance_to(Vector2(200, 100))
var dot_product := Vector2.RIGHT.dot(direction)

# Vector2 constants
Vector2.ZERO      # (0, 0)
Vector2.ONE       # (1, 1)
Vector2.UP        # (0, -1)
Vector2.DOWN      # (0, 1)
Vector2.LEFT      # (-1, 0)
Vector2.RIGHT     # (1, 0)

# Vector3 (3D position, direction, velocity)
var pos_3d: Vector3 = Vector3(10, 20, 30)
var forward: Vector3 = Vector3.FORWARD

# Vector3 operations
var cross := Vector3.UP.cross(forward)
var normalized_3d := pos_3d.normalized()

# Vector3 constants
Vector3.ZERO      # (0, 0, 0)
Vector3.ONE       # (1, 1, 1)
Vector3.UP        # (0, 1, 0)
Vector3.DOWN      # (0, -1, 0)
Vector3.LEFT      # (-1, 0, 0)
Vector3.RIGHT     # (1, 0, 0)
Vector3.FORWARD   # (0, 0, -1)
Vector3.BACK      # (0, 0, 1)
```

### Color

```gdscript
# RGBA (each component 0.0-1.0)
var red: Color = Color(1.0, 0.0, 0.0, 1.0)
var transparent_blue: Color = Color(0.0, 0.0, 1.0, 0.5)

# Named colors
var white := Color.WHITE
var black := Color.BLACK
var transparent := Color.TRANSPARENT

# From hex
var purple := Color("8b00ff")
var with_alpha := Color("ff0000aa")

# HSV (hue, saturation, value)
var color := Color.from_hsv(0.5, 1.0, 1.0)  # Cyan

# Accessing components
var r := red.r  # Red component
var g := red.g  # Green component
var b := red.b  # Blue component
var a := red.a  # Alpha component

# Color operations
var lighter := red.lightened(0.3)
var darker := red.darkened(0.3)
var inverted := red.inverted()
```

### Arrays

```gdscript
# Generic array (mixed types)
var items: Array = [1, "two", Vector2(3, 4), true]

# Typed arrays (better performance)
var numbers: Array[int] = [1, 2, 3, 4, 5]
var names: Array[String] = ["Alice", "Bob", "Charlie"]
var enemies: Array[Node] = []

# Array operations
numbers.append(6)           # Add to end
numbers.insert(0, 0)        # Insert at index
numbers.erase(3)            # Remove first occurrence of value
numbers.pop_back()          # Remove and return last
numbers.pop_front()         # Remove and return first

# Array access
var first := numbers[0]
var last := numbers[-1]
var size := numbers.size()
var is_empty := numbers.is_empty()

# Array iteration
for num in numbers:
    print(num)

for i in range(numbers.size()):
    print("Index %d: %d" % [i, numbers[i]])

# Array methods
var has_five := numbers.has(5)
var index := numbers.find(3)
numbers.sort()
numbers.reverse()
var sum := numbers.reduce(func(acc, val): return acc + val, 0)

# Packed arrays (optimized for specific types)
var packed_ints := PackedInt32Array([1, 2, 3])
var packed_floats := PackedFloat32Array([1.0, 2.0, 3.0])
var packed_vectors := PackedVector2Array([Vector2.ZERO, Vector2.ONE])
var packed_colors := PackedColorArray([Color.RED, Color.BLUE])
```

### Dictionaries

```gdscript
# Generic dictionary
var player_stats: Dictionary = {
    "health": 100,
    "mana": 50,
    "level": 5
}

# Typed dictionary (Godot 4.2+)
var scores: Dictionary[String, int] = {
    "player1": 1000,
    "player2": 850
}

# Access and modify
var health := player_stats["health"]
player_stats["health"] = 90
player_stats.health = 90  # Dot notation (string keys only)

# Dictionary operations
player_stats["stamina"] = 100  # Add new key
player_stats.erase("mana")     # Remove key
var has_health := player_stats.has("health")
var keys := player_stats.keys()
var values := player_stats.values()

# Iterate dictionary
for key in player_stats:
    print("%s: %s" % [key, player_stats[key]])

for key in player_stats.keys():
    print(key)

# Merge dictionaries
var defaults := {"speed": 100, "jump": 200}
var custom := {"speed": 150}
defaults.merge(custom)  # defaults now has speed: 150

# Lua-style syntax (alternative)
var config := {
    max_health = 100,
    max_mana = 50,
    speed = 300.0
}
```

## Control Flow {#control-flow}

### If/Elif/Else

```gdscript
# Basic if
if health <= 0:
    die()

# If-else
if is_on_floor():
    can_jump = true
else:
    can_jump = false

# If-elif-else chain
if health > 75:
    status = "healthy"
elif health > 25:
    status = "injured"
else:
    status = "critical"

# Ternary operator
var status := "alive" if health > 0 else "dead"
var direction := 1 if is_moving_right else -1
```

### Logical Operators

```gdscript
# And
if is_on_floor() and Input.is_action_just_pressed("jump"):
    jump()

# Or
if health <= 0 or fell_off_map:
    respawn()

# Not
if not is_invincible:
    take_damage(10)

# Short-circuit evaluation
if player != null and player.is_alive():
    player.update()

# Comparison operators
var equal := a == b
var not_equal := a != b
var less := a < b
var greater := a > b
var less_equal := a <= b
var greater_equal := a >= b
```

### Match Statement

Pattern matching (similar to switch-case):

```gdscript
# Basic match
match state:
    "idle":
        play_idle_animation()
    "walk":
        play_walk_animation()
    "run":
        play_run_animation()
    _:
        # Default case
        print("Unknown state")

# Match with values
match score:
    0:
        print("Try again!")
    1, 2, 3:
        print("Getting started")
    _:
        print("Good job!")

# Match with ranges
match level:
    0:
        print("Beginner")
    1, 2, 3:
        print("Novice")
    4, 5, 6, 7, 8, 9:
        print("Intermediate")
    _:
        print("Expert")

# Match with types
match value:
    var n when n is int:
        print("Integer: %d" % n)
    var s when s is String:
        print("String: %s" % s)
    _:
        print("Unknown type")

# Match with arrays
match input:
    []:
        print("Empty")
    [var first]:
        print("One element: %s" % first)
    [var first, var second]:
        print("Two elements: %s, %s" % [first, second])
    _:
        print("Many elements")
```

### For Loops

```gdscript
# Range loop (0 to 9)
for i in range(10):
    print(i)

# Range with start and end
for i in range(5, 10):  # 5, 6, 7, 8, 9
    print(i)

# Range with step
for i in range(0, 10, 2):  # 0, 2, 4, 6, 8
    print(i)

# Iterate array
var items: Array[String] = ["sword", "shield", "potion"]
for item in items:
    print(item)

# Typed loop variable (Godot 4.2+)
for enemy: Node in enemies:
    enemy.take_damage(10)

# Iterate dictionary
var stats := {"health": 100, "mana": 50}
for key in stats:
    print("%s: %d" % [key, stats[key]])

# Nested loops
for x in range(10):
    for y in range(10):
        spawn_tile(x, y)

# Break and continue
for i in range(100):
    if i == 50:
        break  # Exit loop
    if i % 2 == 0:
        continue  # Skip to next iteration
    print(i)
```

### While Loops

```gdscript
# Basic while
var count := 0
while count < 10:
    print(count)
    count += 1

# While with condition check
while is_alive and not game_over:
    process_game_logic()

# Infinite loop with break
while true:
    var input := get_player_input()
    if input == "quit":
        break
    process_input(input)

# While with continue
var i := 0
while i < 10:
    i += 1
    if i % 2 == 0:
        continue
    print(i)  # Only odd numbers
```

## Classes and Inheritance {#classes}

### Class Definition

```gdscript
# Global class (accessible from any script)
class_name Player extends CharacterBody2D

# Docstring
## A platformer player controller with jump and movement.
##
## Handles input, physics, and animation for a 2D player character.
## Emits signals when taking damage or dying.
```

### Inheritance

```gdscript
# Extend built-in node
extends CharacterBody2D

# Extend custom class
extends Player

# Override parent methods
func _ready() -> void:
    super._ready()  # Call parent implementation
    print("Child ready!")

func take_damage(amount: int) -> void:
    # Override without calling parent
    print("Custom damage logic")
```

### Inner Classes

Define classes within a script:

```gdscript
class_name Inventory

# Inner class
class Item:
    var name: String
    var weight: float
    var value: int

    func _init(item_name: String, item_weight: float, item_value: int) -> void:
        name = item_name
        weight = item_weight
        value = item_value

    func get_description() -> String:
        return "%s (%.1fkg, %d gold)" % [name, weight, value]

# Use inner class
var items: Array[Item] = []

func add_item(name: String, weight: float, value: int) -> void:
    var item := Item.new(name, weight, value)
    items.append(item)
```

### Constructor

```gdscript
class_name Enemy

var health: int
var damage: int

# Constructor
func _init(starting_health: int = 100, attack_damage: int = 10) -> void:
    health = starting_health
    damage = attack_damage
    print("Enemy created with %d health" % health)

# Create instance
var goblin := Enemy.new(50, 5)
var dragon := Enemy.new(500, 25)
```

## Operators {#operators}

### Arithmetic

```gdscript
var sum := a + b        # Addition
var diff := a - b       # Subtraction
var product := a * b    # Multiplication
var quotient := a / b   # Division
var remainder := a % b  # Modulo

# Compound assignment
health += 10   # health = health + 10
health -= 5    # health = health - 5
health *= 2    # health = health * 2
health /= 2    # health = health / 2
health %= 3    # health = health % 3

# Note: No ++ or -- operators
count += 1  # Use this instead of count++
```

### Math Functions

```gdscript
# Built-in functions
var power := pow(2, 8)           # 256
var square_root := sqrt(16)      # 4
var absolute := abs(-10)         # 10
var rounded := round(3.7)        # 4
var floored := floor(3.7)        # 3
var ceiled := ceil(3.2)          # 4
var clamped := clamp(value, 0, 100)

# Min/max
var minimum := min(a, b)
var maximum := max(a, b)

# Trigonometry
var sine := sin(angle)
var cosine := cos(angle)
var tangent := tan(angle)

# Constants
var pi := PI          # 3.14159...
var tau := TAU        # 2 * PI
var infinity := INF
var not_a_number := NAN
```

### Comparison

```gdscript
# Approximate comparison for floats
var is_close := is_equal_approx(a, b)
var is_zero := is_zero_approx(velocity.x)

# Type checking
var is_node := entity is Node
var is_player := entity is Player

# Null checking
if player != null:
    player.update()

# Safe navigation (check before access)
if player and player.health > 0:
    player.take_damage(10)
```

## Best Practices {#best-practices}

### Naming Conventions

```gdscript
# Constants: SCREAMING_SNAKE_CASE
const MAX_HEALTH: int = 100
const GRAVITY_FORCE: float = 980.0

# Variables and functions: snake_case
var player_health: int = 100
func calculate_damage(base_damage: int) -> int:
    return base_damage

# Private members: prefix with _
var _internal_state: int = 0
func _update_internal() -> void:
    pass

# Classes: PascalCase
class_name PlayerController
class_name EnemyAI

# Signals: past tense
signal died
signal health_changed
signal item_collected
```

### Static Typing Benefits

```gdscript
# GOOD: Type safety and performance
var player: Player = get_player()
var enemies: Array[Enemy] = []

func deal_damage(target: Enemy, amount: int) -> void:
    target.health -= amount

# AVOID: Dynamic typing (slower, error-prone)
var player = get_player()
var enemies = []

func deal_damage(target, amount):
    target.health -= amount
```

### Code Organization

```gdscript
# Group related exports
@export_group("Movement")
@export var speed: float = 300.0
@export var acceleration: float = 1000.0

@export_group("Combat")
@export var max_health: int = 100
@export var damage: int = 10

# Use @export_range for bounded values
@export_range(0, 100) var health: int = 100
@export_range(0.0, 1.0) var volume: float = 1.0

# Use @export_flags for bitflags
@export_flags("Fire", "Water", "Earth", "Air") var element: int
```

### Performance Tips

```gdscript
# Cache node references in @onready
@onready var sprite: Sprite2D = $Sprite2D
@onready var timer: Timer = %RespawnTimer

# Use static typing for arrays
var enemies: Array[Enemy] = []  # Faster than Array

# Prefer const for unchanging values
const SPEED: float = 300.0  # Compile-time optimization

# Use is_zero_approx() for float comparisons
if is_zero_approx(velocity.x):
    velocity.x = 0.0
```

## Common Patterns {#patterns}

### Property Getters/Setters

```gdscript
var _health: int = 100

var health: int:
    get:
        return _health
    set(value):
        _health = clampi(value, 0, max_health)
        health_changed.emit(_health, max_health)

# Short form for simple getters
var speed: float:
    get: return _speed
```

### Null Safety

```gdscript
# Check before accessing
if player != null and player.is_alive():
    player.update()

# Early return pattern
func process_player() -> void:
    if player == null:
        return

    player.update()
    player.check_input()
```

### Flags and Bitwise Operations

```gdscript
# Define flags as powers of 2
const FLAG_NONE := 0
const FLAG_CAN_JUMP := 1 << 0  # 1
const FLAG_CAN_DASH := 1 << 1  # 2
const FLAG_CAN_ATTACK := 1 << 2  # 4

var abilities: int = FLAG_CAN_JUMP | FLAG_CAN_ATTACK

# Check flag
if abilities & FLAG_CAN_JUMP:
    jump()

# Add flag
abilities |= FLAG_CAN_DASH

# Remove flag
abilities &= ~FLAG_CAN_DASH

# Toggle flag
abilities ^= FLAG_CAN_ATTACK
```

## See Also

- [Static Typing](static-typing.md) - Deep dive into type system
- [Export Variables](exports.md) - Making variables editable in Inspector
- [Signals](../patterns/signals.md) - Event-driven communication
- [Input Handling](../patterns/input.md) - Processing player input

## Sources

1. **Official:** [Static typing in GDScript](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html) - Type system and performance
2. **Official:** [GDScript reference](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_basics.html) - Language fundamentals
3. **Community:** [Learn GDScript in Y Minutes](https://learnxinyminutes.com/gdscript/) - Syntax overview
4. **Community:** [GDQuest GDScript Cheatsheet](https://school.gdquest.com/cheatsheets/gdscript) - Quick reference
5. **Examples:** repos/godot_node_essentials - Working code examples from GDQuest
