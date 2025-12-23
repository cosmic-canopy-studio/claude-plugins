---
topic: static-typing
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html
  - https://gdscript.com/articles/godot-4-gdscript/
  - https://school.gdquest.com/glossary/type_inference
  - https://www.gdquest.com/tutorial/godot/gdscript/typed-gdscript/
  - repos/godot_node_essentials/common/2d/astronaut_player_2d/astronaut_player_2d.gd
  - repos/godot_node_essentials/common/3d/astronaut_player_3d/astronaut_player_3d.gd
---

# Static Typing

Type annotation system in GDScript for improved code safety, editor support, and performance.

## Overview

GDScript is **optionally typed**: you can add type hints to variables, function parameters, and return values, but the language allows dynamic typing as well. Static typing provides better autocompletion, earlier error detection, and performance optimizations.

## Type Annotation Syntax

### Variable Types

```gdscript
# Explicit type annotation
var health: int = 100
var speed: float = 5.5
var player_name: String = "Hero"
var is_alive: bool = true
var position: Vector2 = Vector2.ZERO

# Built-in types
var velocity: Vector3
var transform: Transform3D
var color: Color
var rect: Rect2

# Node types
var sprite: Sprite2D
var body: CharacterBody2D
var area: Area3D
var timer: Timer

# Resource types
var texture: Texture2D
var material: Material
var scene: PackedScene
```

### Type Inference with `:=`

Let GDScript infer the type automatically from the assigned value:

```gdscript
# Type inferred from literal value
var count := 0              # int
var speed := 100.0          # float
var name := "Player"        # String
var active := true          # bool

# Type inferred from constructor
var position := Vector2(10, 20)    # Vector2
var color := Color.RED              # Color

# Type inferred from constant
const MAX_HEALTH := 100             # int (inferred)
const SPEED := 5.5                  # float (inferred)

# Type inferred from function return
var player := get_node("Player") as CharacterBody2D  # CharacterBody2D
```

**Best Practice:** Use `:=` instead of `: Type` when the type is obvious from the value. It's less error-prone and cleaner.

### Function Parameters and Return Types

```gdscript
# Basic function with typed parameters and return
func calculate_damage(base: int, multiplier: float) -> int:
    return int(base * multiplier)

# Void return type (returns nothing)
func take_damage(amount: int) -> void:
    health -= amount

# No return type annotation (dynamic, avoid this)
func bad_example(value):  # Untyped - loses type safety
    return value

# Multiple parameters with different types
func spawn_enemy(enemy_type: String, position: Vector2, level: int) -> Enemy:
    var enemy := enemy_scene.instantiate() as Enemy
    enemy.global_position = position
    enemy.level = level
    return enemy

# Optional parameters with types
func heal(amount: int = 10) -> void:
    health += amount
```

### Constants

```gdscript
# Explicit constant type
const MAX_SPEED: float = 500.0
const PLAYER_NAME: String = "Hero"

# Inferred constant type (preferred)
const GRAVITY := 9.8
const JUMP_FORCE := 1000
const MAX_HEALTH := 100
```

### @onready Variables

```gdscript
# Typed @onready variables with unique node path %
@onready var animation_player: AnimationPlayer = %AnimationPlayer
@onready var sprite: Sprite2D = %Sprite2D
@onready var collision: CollisionShape2D = %CollisionShape2D

# Type inference with @onready
@onready var timer := %Timer as Timer
@onready var player := get_node("Player") as CharacterBody2D

# Without type (loses autocompletion)
@onready var generic_node = %SomeNode  # Bad - type is Node, not specific
```

## Typed Arrays

### Array Type Syntax

```gdscript
# Typed array declaration
var scores: Array[int] = []
var names: Array[String] = ["Alice", "Bob"]
var positions: Array[Vector2] = [Vector2.ZERO, Vector2.ONE]

# Node type arrays
var enemies: Array[Enemy] = []
var buttons: Array[Button] = []
var timers: Array[Timer] = []

# Resource type arrays
var textures: Array[Texture2D] = []
var scenes: Array[PackedScene] = []

# Type inference with arrays
var items := Array[int]([1, 2, 3])
var colors := Array[Color]([Color.RED, Color.BLUE])

# Initialize empty typed array
var waypoints: Array[Marker2D] = []
var particles: Array[GPUParticles2D] = []
```

### Working with Typed Arrays

```gdscript
class_name InventorySystem
extends Node

var items: Array[String] = []

func add_item(item: String) -> void:
    items.append(item)  # Type-safe: only strings allowed

func get_item_count() -> int:
    return items.size()

func clear_items() -> void:
    items.clear()

# Iterating typed arrays
func print_items() -> void:
    for item: String in items:  # item is typed as String
        print(item)
```

### Array Performance

Typed arrays are **faster** than untyped arrays but **slower** than PackedArrays:

| Array Type | Performance | Memory | Flexibility |
|------------|-------------|---------|-------------|
| `PackedInt32Array` | Fastest | Least | Limited methods |
| `Array[int]` | Fast | Moderate | Full Array methods |
| `Array` (untyped) | Slowest | Most | Most flexible |

**Rule of Thumb:**
- Use `PackedArray` for large data sets (thousands of elements)
- Use `Array[T]` for game logic with type safety
- Avoid untyped `Array` in performance-critical code

## Type Casting

### The `as` Keyword

```gdscript
# Safe casting with 'as' - returns null if type doesn't match
var sprite := get_node("Sprite") as Sprite2D
if sprite:
    sprite.texture = preload("res://icon.png")

# Casting function returns
var player := get_parent() as CharacterBody2D
if player:
    player.velocity = Vector2.ZERO

# Casting in signal callbacks
func _on_area_entered(area: Area2D) -> void:
    var collectible := area as Collectible
    if collectible:
        collectible.collect()

# Casting get_node results
@onready var timer := get_node("Timer") as Timer
@onready var label := %Label as Label
```

### Direct Type Annotation vs `as` Casting

```gdscript
# Direct type hint - throws error if type is wrong
var sprite: Sprite2D = get_node("Sprite")  # Error if not Sprite2D

# 'as' casting - returns null if type is wrong
var sprite := get_node("Sprite") as Sprite2D  # null if not Sprite2D

# Safe pattern: check before use
var enemy := body as Enemy
if enemy:
    enemy.take_damage(10)
else:
    print("Not an enemy")
```

### Unsafe Casting (Godot 4.3+)

In Godot 4.3+, casting `Variant` to specific types may produce `UNSAFE_CAST` warnings:

```gdscript
# May produce UNSAFE_CAST warning
var intersection: Variant = raycast.get_collision_point()
var point := intersection as Vector3  # Warning: unsafe cast

# Solution 1: Suppress with comment
var point := intersection as Vector3  # gdlint: ignore=unsafe-cast

# Solution 2: Check type first
if intersection is Vector3:
    var point := intersection as Vector3
```

## Custom Classes as Types

### Using class_name

```gdscript
# enemy.gd
class_name Enemy
extends CharacterBody2D

var health: int = 100

func take_damage(amount: int) -> void:
    health -= amount
```

```gdscript
# player.gd
class_name Player
extends CharacterBody2D

# Use Enemy as a type
func attack_enemy(enemy: Enemy) -> void:
    enemy.take_damage(10)

# Typed array of custom class
var nearby_enemies: Array[Enemy] = []

func find_enemies() -> void:
    for body in detection_area.get_overlapping_bodies():
        var enemy := body as Enemy
        if enemy:
            nearby_enemies.append(enemy)
```

### Preloading Scripts as Types

If you don't use `class_name`, preload the script:

```gdscript
# Without class_name
const Enemy := preload("res://enemy.gd")

var current_enemy: Enemy
var enemies: Array[Enemy] = []

func spawn_enemy() -> Enemy:
    var enemy := Enemy.new()
    add_child(enemy)
    return enemy
```

## Type Inference Benefits

### Better Autocompletion

```gdscript
# Without type - limited autocompletion
var player = get_node("Player")
player.  # Only shows Node methods

# With type - full autocompletion
var player := get_node("Player") as CharacterBody2D
player.  # Shows all CharacterBody2D methods + properties
```

### Earlier Error Detection

```gdscript
# Error caught at edit-time, not runtime
var speed: int = 100
speed = "fast"  # ERROR: Cannot assign String to int

# Without type, error only appears at runtime
var speed = 100
speed = "fast"  # No error until you try to use speed as a number
```

### Improved Refactoring

```gdscript
# When you rename a method, typed code shows errors immediately
func apply_damage(amount: int) -> void:
    health -= amount

# If you rename to 'take_damage', all typed calls show errors
enemy.apply_damage(10)  # Error: Enemy has no method 'apply_damage'
```

## Performance Benefits

### Optimization in Godot 4

Typed GDScript enables **compile-time optimizations**:

```gdscript
# Optimized: types known at compile time
func add_numbers(a: int, b: int) -> int:
    return a + b

# Not optimized: types checked at runtime
func add_numbers(a, b):
    return a + b
```

**Performance Hierarchy:**
1. Typed code with inferred/explicit types - **Fastest**
2. Untyped code - Slower (runtime type checks)
3. Heavy use of `Variant` - Slowest (maximum flexibility)

### Typed vs Untyped Performance

```gdscript
# Fast: typed arithmetic
var damage: int = 10
var multiplier: float = 1.5
var result := int(damage * multiplier)  # Optimized operations

# Slower: untyped arithmetic
var damage = 10
var multiplier = 1.5
var result = damage * multiplier  # Runtime type checks

# Typed arrays are faster to iterate
var positions: Array[Vector2] = []
for pos: Vector2 in positions:  # Optimized loop
    process_position(pos)
```

## Common Patterns

### Typed Node References

```gdscript
class_name Player
extends CharacterBody2D

# Typed node references with %UniqueNodePath
@onready var animation_player: AnimationPlayer = %AnimationPlayer
@onready var sprite: Sprite2D = %Sprite2D
@onready var collision: CollisionShape2D = %CollisionShape2D
@onready var health_bar: ProgressBar = %HealthBar

func _ready() -> void:
    animation_player.play("idle")
    sprite.modulate = Color.WHITE
    health_bar.max_value = 100.0
```

### Typed Signal Parameters

```gdscript
class_name HealthComponent
extends Node

# Signal with typed parameters
signal health_changed(current: int, maximum: int)
signal died(killer: Node)

var health: int = 100
var max_health: int = 100

func take_damage(amount: int, attacker: Node) -> void:
    health -= amount
    health_changed.emit(health, max_health)

    if health <= 0:
        died.emit(attacker)
```

### Typed Exports

```gdscript
class_name Enemy
extends CharacterBody2D

# Typed export variables
@export var max_health: int = 100
@export var move_speed: float = 200.0
@export var patrol_radius: float = 500.0

# Export node paths with type hints
@export var target: CharacterBody2D
@export var spawn_point: Marker2D

# Export arrays with types
@export var patrol_points: Array[Marker2D] = []
@export var loot_items: Array[PackedScene] = []
```

### Typed Dictionaries

```gdscript
# Dictionary with typed values (keys are always Variant)
var player_stats: Dictionary = {
    "health": 100,  # int
    "mana": 50,     # int
    "speed": 5.5,   # float
}

# Type-safe dictionary access
func get_stat(stat_name: String) -> int:
    if player_stats.has(stat_name):
        return player_stats[stat_name] as int
    return 0

# Alternative: use custom class for type safety
class_name PlayerStats
extends Resource

@export var health: int = 100
@export var mana: int = 50
@export var speed: float = 5.5
```

## Best Practices & Pitfalls

### Do

```gdscript
# Use type inference for clarity
var count := 0
var position := Vector2.ZERO

# Always type function parameters and returns
func calculate_score(kills: int, deaths: int) -> int:
    return kills * 100 - deaths * 50

# Use 'as' for safe casting
var player := body as Player
if player:
    player.take_damage(10)

# Type @onready variables
@onready var timer: Timer = %Timer
@onready var sprite: Sprite2D = %Sprite2D

# Use typed arrays for collections
var enemies: Array[Enemy] = []
var waypoints: Array[Vector2] = []

# Check types before operations
func _on_body_entered(body: Node2D) -> void:
    var enemy := body as Enemy
    if enemy:
        enemy.take_damage(damage)
```

### Don't

```gdscript
# Don't omit return types
func get_player():  # Bad - return type unknown
    return player

# Don't use Variant unless necessary
var data: Variant = 10  # Bad - use specific type

# Don't cast without checking
var player := get_node("Player") as Player
player.move()  # Bad - player might be null

# Don't mix typed and untyped code
var health: int = 100
var speed = 5.0  # Bad - inconsistent style

# Don't ignore UNSAFE_CAST warnings without understanding
var pos := data as Vector3  # Potentially dangerous

# Don't use direct type hints on get_node without as
var sprite: Sprite2D = get_node("Sprite")  # Error if not Sprite2D
# Use this instead:
var sprite := get_node("Sprite") as Sprite2D
```

## Enforcing Static Typing (Godot 4.2+)

Enable warnings to enforce type safety project-wide:

### Project Settings

**Project > Project Settings > GDScript > Warnings**

1. **UNTYPED_DECLARATION** - Warn on all untyped variables
2. **INFERRED_DECLARATION** - Warn when using `:=` (prefer explicit types)
3. **UNSAFE_CAST** - Warn on potentially unsafe casts

### Per-File Enforcement

```gdscript
# At top of file
#gdlint: disable=untyped-declaration

# Or suppress specific warnings
var value := data as int  # gdlint: ignore=unsafe-cast
```

## Type System Limitations

### Cannot Infer from All Functions

```gdscript
# Some functions don't specify return types
var result := round(5.5)  # ERROR - round() return type is ambiguous

# Solution: explicit type
var result: float = round(5.5)
var result := round(5.5) as float
```

### Generic get_node() Returns Node

```gdscript
# get_node returns Node, not specific type
var timer = get_node("Timer")  # Type: Node (not Timer)

# Solution: cast to specific type
var timer := get_node("Timer") as Timer
var timer: Timer = %Timer  # Using unique node path
```

### Variant Fallback

```gdscript
# When Godot can't infer type, it uses Variant
var data := some_complex_function()  # May be Variant

# Check type at runtime if uncertain
if data is int:
    print("Integer: ", data)
elif data is String:
    print("String: ", data)
```

## Migration Strategy

### Gradual Typing

Start adding types incrementally to existing projects:

```gdscript
# Phase 1: Type function signatures
func take_damage(amount: int) -> void:
    health -= amount  # health still untyped

# Phase 2: Type member variables
var health: int = 100

func take_damage(amount: int) -> void:
    health -= amount  # Now fully typed

# Phase 3: Type local variables
func calculate_damage() -> int:
    var base_damage: int = 10
    var multiplier: float = 1.5
    return int(base_damage * multiplier)
```

### Converting Untyped to Typed

```gdscript
# Before: untyped
var speed = 100
var player = get_node("Player")

func move(direction):
    position += direction * speed

# After: typed
var speed: float = 100.0
var player: CharacterBody2D

func move(direction: Vector2) -> void:
    position += direction * speed
```

## Performance Comparison

### Benchmark Results

From community testing and official documentation:

```gdscript
# Untyped code
var total = 0
for i in range(1000000):
    total += i
# ~120ms

# Typed code
var total: int = 0
for i: int in range(1000000):
    total += i
# ~80ms (33% faster)
```

**Key Takeaways:**
- Typed code is **10-40% faster** in compute-heavy loops
- Minimal difference for simple property access
- Biggest gains in arithmetic and array operations
- Future JIT/AOT compilation will increase the gap

## Related Patterns

- [GDScript Basics](gdscript-basics.md) - Foundation for type system
- [Exports](exports.md) - Typed export variables for inspector
- [Signals](../patterns/signals.md) - Typed signal parameters
- [Resources](../patterns/resources.md) - Custom resource types

## See Also

- [Official Static Typing Documentation](https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/static_typing.html)
- [GDQuest Type Inference Guide](https://school.gdquest.com/glossary/type_inference)
- [GDQuest Typed GDScript Tutorial](https://www.gdquest.com/tutorial/godot/gdscript/typed-gdscript/)
- [Godot 4 GDScript Features](https://gdscript.com/articles/godot-4-gdscript/)
