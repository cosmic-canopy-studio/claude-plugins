---
topic: exports
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/4.3/tutorials/scripting/gdscript/gdscript_exports.html
  - https://github.com/godotengine/godot-docs/blob/master/tutorials/scripting/gdscript/gdscript_exports.rst
  - https://docs.godotengine.org/en/stable/tutorials/scripting/gdscript/gdscript_exports.html
status: complete
---

# Export Variables

Expose script properties to the editor inspector for visual editing and scene persistence.

## Quick Start

```gdscript
extends Node

# Basic exports
@export var speed: float = 5.0
@export var max_health: int = 100
@export var player_name: String = "Player"

# Nodes and resources
@export var target_node: Node = null
@export var texture: Texture2D = null
@export var config: Resource = null
```

## Core Annotations

### @export

Exposes a variable to the inspector. Must be initialized or have a type specifier.

```gdscript
# Type inference from value
@export var count = 10
@export var message = "Hello"

# Explicit typing (recommended)
@export var speed: float = 5.0
@export var health: int = 100

# Typed but no default (shows null/0 in inspector)
@export var target: Node
@export var damage: int
```

**Best practice:** Always use explicit typing for clarity and reliability.

### @export_range

Constrains numeric values with optional slider controls.

```gdscript
# Basic range (integer slider 0-20)
@export_range(0, 20) var player_count: int

# Float with step (slider with 0.2 increments)
@export_range(-10, 20, 0.2) var temperature: float

# Allow values beyond range
@export_range(0, 100, 1, "or_less", "or_greater") var score: int

# Exponential slider (better for large ranges)
@export_range(0, 100000, 0.01, "exp") var distance: float

# Hide slider, show spin box only
@export_range(0, 1000, 0.01, "hide_slider") var precise_value: float

# With suffix for clarity
@export_range(0, 100, 1, "suffix:m") var height_meters: int
@export_range(0, 100, 1, "suffix:%") var completion: int

# Angles - display as degrees, store as radians
@export_range(0, 360, 0.1, "radians_as_degrees") var rotation_angle: float
@export_range(0, 360, 1, "degrees") var heading: float
```

**Parameters:**
- `min`, `max` - Value bounds
- `step` - Increment size (default 1.0)
- `"or_less"` - Allow values below min
- `"or_greater"` - Allow values above max
- `"exp"` - Exponential scaling for wide ranges
- `"hide_slider"` - Only show numeric input
- `"suffix:text"` - Display unit label
- `"radians_as_degrees"` - Show degrees, store radians
- `"degrees"` - Angle in degrees

### @export_enum

Restricts selection to predefined choices via dropdown.

```gdscript
# Named enum (recommended)
enum CharacterClass { WARRIOR, MAGE, ROGUE }
@export var player_class: CharacterClass

# Inline enum for integers
@export_enum("Warrior", "Mage", "Rogue") var character_type: int

# Enum with explicit values
@export_enum("Slow:30", "Normal:60", "Fast:120") var frame_rate: int

# String enums
@export_enum("Rebecca", "Mary", "Leah") var character_name: String = "Rebecca"

# Enum arrays (Godot 4.3+)
@export_enum("Espresso", "Mocha", "Latte", "Cappuccino") var drinks: Array[String] = []
```

**When to use:**
- Fixed set of choices (difficulty levels, character types)
- Config options with named values
- String selections from predefined list

### @export_flags

Creates checkboxes for bitwise flag combinations.

```gdscript
# Basic flags (auto-assigns bit values 1, 2, 4, 8...)
@export_flags("Fire", "Water", "Earth", "Wind") var resistances: int = 0

# Explicit bit values (must be powers of 2)
@export_flags("Self:4", "Allies:8", "Foes:16") var spell_targets: int = 0

# Combined flags
@export_flags(
    "Self:4",
    "Allies:8",
    "Self and Allies:12",  # 4 + 8
    "Foes:16"
) var complex_targeting: int = 0

# Check flags in code
func can_target_allies() -> bool:
    return spell_targets & 8  # Check bit 8
```

**Layer-specific flags:**
```gdscript
# Physics/rendering/navigation layers
@export_flags_2d_physics var collision_layers: int
@export_flags_2d_render var render_layers: int
@export_flags_2d_navigation var nav_layers: int

@export_flags_3d_physics var collision_layers_3d: int
@export_flags_3d_render var render_layers_3d: int
@export_flags_3d_navigation var nav_layers_3d: int
```

**Best practice:** Use bit values starting at 1, not 0. Flags require powers of 2 (1, 2, 4, 8, 16...).

## File & Path Annotations

### @export_file

Restricts strings to file paths with optional filtering.

```gdscript
# Any file
@export_file var config_path: String

# Filter by extension
@export_file("*.txt") var text_file: String
@export_file("*.json") var data_file: String
@export_file("*.png", "*.jpg") var image_file: String

# File arrays
@export_file("*.json") var skill_trees: Array[String] = []
```

### @export_dir

Directory path selection.

```gdscript
@export_dir var asset_directory: String
@export_dir var save_folder: String
```

### @export_global_file / @export_global_dir

Access global filesystem (requires `@tool` script).

```gdscript
@tool
extends Node

@export_global_file("*.png") var external_texture: String
@export_global_dir var external_assets: String
```

**Use case:** Tool scripts importing assets from outside project.

### @export_multiline

Multi-line text editor for strings.

```gdscript
@export_multiline var description: String
@export_multiline var dialogue: String = "Multiple\nlines\nof text"
```

## Node & Resource Annotations

### @export_node_path

Restricts NodePath to specific node types.

```gdscript
# Any button type
@export_node_path("Button", "TouchScreenButton") var button_path: NodePath

# Specific node class
@export_node_path("AnimationPlayer") var animator_path: NodePath
@export_node_path("Camera3D") var camera_path: NodePath

# Use in code
@onready var animator: AnimationPlayer = get_node(animator_path)
```

### Exporting Nodes Directly

```gdscript
# Any node
@export var target: Node = null

# Specific type (recommended)
@export var camera: Camera3D = null
@export var animation_player: AnimationPlayer = null

# Custom classes
@export var player: AstronautPlayer2D = null
```

### Exporting Resources

```gdscript
# Base resource type
@export var data: Resource = null

# Specific resource types
@export var texture: Texture2D = null
@export var material: Material = null
@export var audio: AudioStream = null

# Custom resources
@export var enemy_stats: EnemyData = null
@export var inventory: InventoryResource = null

# Resource arrays
@export var textures: Array[Texture2D] = []
@export var loot_table: Array[ItemResource] = []
```

**Custom resource example:**
```gdscript
# res://resources/enemy_data.gd
class_name EnemyData extends Resource

@export var health: int = 100
@export var speed: float = 3.0
@export var damage: int = 10

# In enemy script
@export var stats: EnemyData = null

func _ready() -> void:
    if stats:
        health = stats.health
        speed = stats.speed
```

## Visual & Color Annotations

### @export_color_no_alpha

RGB color picker without alpha channel.

```gdscript
@export_color_no_alpha var background_color: Color = Color.WHITE
@export_color_no_alpha var ui_theme_color: Color

# Regular color export includes alpha
@export var tint_color: Color = Color(1, 1, 1, 0.5)
```

### @export_exp_easing

Easing curve visualizer for animation timing.

```gdscript
@export_exp_easing var transition_curve: float = 1.0
@export_exp_easing var fade_easing: float = 2.0

# Use in tweens
func animate() -> void:
    var tween := create_tween()
    tween.set_ease(Tween.EASE_IN)
    tween.set_trans(transition_curve as Tween.TransitionType)
```

## Organization Annotations

### @export_group

Groups related properties under collapsible headers.

```gdscript
@export_group("Movement")
@export var speed: float = 5.0
@export var acceleration: float = 10.0
@export var jump_height: float = 3.0

@export_group("Combat")
@export var max_health: int = 100
@export var damage: int = 10

# With prefix for auto-grouping
@export_group("Player Stats", "stat_")
@export var stat_health: int = 100
@export var stat_stamina: int = 50
```

### @export_subgroup

Creates subcategories within groups (cannot nest).

```gdscript
@export_group("Character")
@export var character_name: String = "Hero"

@export_subgroup("Movement")
@export var move_speed: float = 5.0
@export var turn_speed: float = 3.0

@export_subgroup("Combat")
@export var attack_damage: int = 10
@export var defense: int = 5
```

### @export_category

Top-level categories beyond class hierarchy.

```gdscript
@export_category("Core Properties")
@export var health: int = 100
@export var speed: float = 5.0

@export_category("Visual Settings")
@export var color: Color = Color.WHITE
@export var texture: Texture2D = null
```

**Visual hierarchy:**
- `@export_category` - Top level
- `@export_group` - Second level
- `@export_subgroup` - Third level

## Advanced Annotations

### @export_custom

Low-level control via PropertyHint constants.

```gdscript
@export_custom(PROPERTY_HINT_NONE, "suffix:m") var altitude: float
@export_custom(PROPERTY_HINT_RANGE, "0,100,0.1") var percentage: float
```

**Warning:** GDScript doesn't validate `@export_custom` syntax. Use specialized annotations when available.

### @export_storage

Persists to scene/resource without inspector visibility.

```gdscript
var runtime_only: int          # Not stored, not visible
@export_storage var saved: int  # Stored, not visible
@export var visible: int        # Stored, visible

# Use case: internal state that must persist
@export_storage var _session_id: String
@export_storage var _cached_data: Array
```

**Benefit:** Enables `duplicate()` for non-exported variables.

### @export_tool_button

Clickable inspector button triggering callables (requires `@tool`).

```gdscript
@tool
extends Node

@export_tool_button("Regenerate", "Reload") var regenerate_action: Callable = regenerate

func regenerate() -> void:
    print("Regenerating procedural content...")
    # Tool-time generation code
```

## Typed Arrays

All export annotations support typed arrays.

```gdscript
# Basic typed arrays
@export var integers: Array[int] = [1, 2, 3]
@export var names: Array[String] = []

# Range-constrained arrays
@export_range(-360, 360, 0.1, "degrees") var angles: Array[float] = []

# File path arrays
@export_file("*.json") var config_files: Array[String] = []

# Enum arrays
@export_enum("Small", "Medium", "Large") var sizes: Array[String] = []

# Node arrays
@export var waypoints: Array[Node3D] = []

# Resource arrays
@export var items: Array[ItemResource] = []

# PackedArrays
@export var colors: PackedColorArray = []
@export var positions: PackedVector2Array = []
```

## Best Practices

### Type Safety

```gdscript
# Good - explicit typing
@export var speed: float = 5.0
@export var target: Node3D = null

# Avoid - type inference can be ambiguous
@export var speed = 5.0  # int or float?
@export var target = null  # Unknown type
```

### Documentation Comments

```gdscript
## Maximum player health points.
@export var max_health: int = 100

## Movement speed in meters per second.
## Higher values make the character faster.
@export_range(0, 20, 0.1) var speed: float = 5.0
```

### Initialization Timing

```gdscript
extends Node

@export var damage: int = 10

func _init() -> void:
    # Export values NOT loaded yet
    print(damage)  # Shows default: 10

func _ready() -> void:
    # Export values loaded from inspector
    print(damage)  # Shows inspector value
```

**Rule:** Inspector values load after `_init()`, before `_ready()`. Use `_ready()` or setters to respond to exported values.

### Setters with Exports

```gdscript
@tool  # Required for setter to run in editor
extends Node2D

@export var radius: float = 10.0:
    set(value):
        radius = value
        queue_redraw()  # Update visuals in editor

func _draw() -> void:
    draw_circle(Vector2.ZERO, radius, Color.RED)
```

### Resource Organization

```gdscript
# Define custom resource
# res://resources/weapon_stats.gd
class_name WeaponStats extends Resource

@export var damage: int = 10
@export var fire_rate: float = 1.0
@export var ammo: int = 30

# Use in multiple scripts
extends Node

@export var primary_weapon: WeaponStats = null
@export var secondary_weapon: WeaponStats = null
```

**Benefit:** Reusable data, editor-friendly, version control safe (.tres format).

## Common Patterns

### Player Configuration

```gdscript
class_name Player extends CharacterBody2D

@export_group("Movement")
@export var speed: float = 300.0
@export var acceleration: float = 1500.0
@export_range(0, 2000, 10) var jump_strength: float = 600.0
@export var gravity: float = 2000.0

@export_group("Combat")
@export var max_health: int = 100
@export var invincibility_time: float = 1.0

@export_group("References")
@export var animation_player: AnimationPlayer = null
@export var sprite: Sprite2D = null
```

### Enemy Configuration

```gdscript
extends CharacterBody2D

enum Behavior { PATROL, CHASE, ATTACK, FLEE }

@export_category("Stats")
@export var health: int = 50
@export_range(0, 500, 1, "suffix:px/s") var move_speed: float = 100.0
@export var damage: int = 10

@export_category("Behavior")
@export var initial_behavior: Behavior = Behavior.PATROL
@export_range(0, 1000, 1, "suffix:px") var detection_range: float = 300.0
@export var patrol_points: Array[Node2D] = []

@export_category("Resources")
@export var loot_table: Array[ItemResource] = []
```

### Weapon System

```gdscript
extends Node2D

@export_group("Projectile")
@export var bullet_scene: PackedScene = null
@export var bullet_speed: float = 500.0

@export_group("Firing")
@export_range(0.1, 10, 0.1, "suffix:s") var fire_rate: float = 0.5
@export var automatic: bool = false
@export var ammo: int = 30

@export_group("Audio")
@export var shoot_sound: AudioStream = null
@export var reload_sound: AudioStream = null

@export_group("Effects")
@export var muzzle_flash: PackedScene = null
@export var shell_casing: PackedScene = null
```

### UI Theme Configuration

```gdscript
extends Control

@export_category("Colors")
@export_color_no_alpha var primary_color: Color = Color("4a90e2")
@export_color_no_alpha var secondary_color: Color = Color("50c878")
@export_color_no_alpha var text_color: Color = Color.WHITE

@export_category("Fonts")
@export var title_font: Font = null
@export var body_font: Font = null
@export_range(12, 72, 1, "suffix:px") var title_size: int = 32
@export_range(8, 48, 1, "suffix:px") var body_size: int = 16

@export_category("Layout")
@export_range(0, 50, 1, "suffix:px") var padding: int = 10
@export_range(0, 50, 1, "suffix:px") var spacing: int = 5
```

## Common Pitfalls

### Missing Type Specifier

```gdscript
# Error: Cannot infer type
@export var data

# Fix: Add type or default value
@export var data: Dictionary = {}
@export var data = {}
```

### Modifying During _init()

```gdscript
@export var max_health: int = 100
var health: int

func _init() -> void:
    # Wrong - inspector value not loaded yet
    health = max_health  # Always uses default (100)

func _ready() -> void:
    # Correct - inspector value loaded
    health = max_health  # Uses inspector value
```

### Flag Values Must Be Powers of 2

```gdscript
# Wrong - 3 is not a power of 2
@export_flags("A:1", "B:2", "C:3") var flags: int

# Correct - use 4 (2^2)
@export_flags("A:1", "B:2", "C:4") var flags: int
```

### Enum Arrays in Godot < 4.3

```gdscript
# Not supported in Godot 4.0-4.2
@export_enum("A", "B", "C") var items: Array[String] = []

# Workaround: Use regular export
@export var items: Array[String] = []
```

## Reference

### Export Annotation Summary

| Annotation | Purpose | Example |
|------------|---------|---------|
| `@export` | Basic inspector exposure | `@export var speed: float` |
| `@export_range` | Numeric constraints + slider | `@export_range(0, 100) var health: int` |
| `@export_enum` | Dropdown selection | `@export_enum("A", "B") var choice: String` |
| `@export_flags` | Bitwise checkbox flags | `@export_flags("Fire", "Ice") var resist: int` |
| `@export_file` | File path with filter | `@export_file("*.json") var config: String` |
| `@export_dir` | Directory path | `@export_dir var folder: String` |
| `@export_multiline` | Multi-line text editor | `@export_multiline var text: String` |
| `@export_color_no_alpha` | RGB color picker | `@export_color_no_alpha var bg: Color` |
| `@export_exp_easing` | Easing curve editor | `@export_exp_easing var curve: float` |
| `@export_node_path` | Type-filtered NodePath | `@export_node_path("Camera3D") var path: NodePath` |
| `@export_group` | Property grouping | `@export_group("Movement")` |
| `@export_subgroup` | Nested group | `@export_subgroup("Advanced")` |
| `@export_category` | Top-level category | `@export_category("Stats")` |
| `@export_custom` | Custom PropertyHint | `@export_custom(PROPERTY_HINT_NONE, "")` |
| `@export_storage` | Save without visibility | `@export_storage var cache: Array` |
| `@export_tool_button` | Inspector button | `@export_tool_button("Run") var fn: Callable` |

### Layer Flags

| Annotation | Layer Type |
|------------|------------|
| `@export_flags_2d_physics` | 2D physics layers |
| `@export_flags_2d_render` | 2D render layers |
| `@export_flags_2d_navigation` | 2D navigation layers |
| `@export_flags_3d_physics` | 3D physics layers |
| `@export_flags_3d_render` | 3D render layers |
| `@export_flags_3d_navigation` | 3D navigation layers |

## Related

- [Static Typing](static-typing.md) - Type system fundamentals
- [GDScript Basics](gdscript-basics.md) - Language overview
- [Custom Resources](../core/resources.md) - Creating reusable data types

## Sources

1. **Official Godot 4.3 Documentation**: [GDScript Exported Properties](https://docs.godotengine.org/en/4.3/tutorials/scripting/gdscript/gdscript_exports.html)
2. **Godot Docs Repository**: [GDScript Exports RST Source](https://github.com/godotengine/godot-docs/blob/master/tutorials/scripting/gdscript/gdscript_exports.rst)
3. **Community Resources**: [Custom Resources Tutorial](https://ezcha.net/news/3-1-23-custom-resources-are-op-in-godot-4), [Resource Arrays Discussion](https://forum.godotengine.org/t/how-to-save-load-custom-resource-arrays/37035)
