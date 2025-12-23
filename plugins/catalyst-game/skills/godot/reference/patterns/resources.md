---
topic: custom-resources
version: 2025.12.21
godot_version: "4.3"
sources:
  - official-godot-docs
  - simondalvai-blog
  - kodeco-tutorial
  - gdquest-save-guide
---

# Custom Resources

Data containers for structured game data, configuration, and save files.

## Quick Start

```gdscript
# Create a custom resource
class_name ItemData
extends Resource

@export var item_name: String = ""
@export var icon: Texture2D
@export var value: int = 0
@export var stackable: bool = false

# Use in your game
var health_potion := ItemData.new()
health_potion.item_name = "Health Potion"
health_potion.value = 50
```

## Creating Resources

### Basic Resource

```gdscript
# data/player_stats.gd
class_name PlayerStats
extends Resource

@export var max_health: int = 100
@export var speed: float = 200.0
@export var jump_force: float = 400.0

func take_damage(amount: int) -> void:
    max_health = max(0, max_health - amount)
```

### Resource with Enums

```gdscript
# data/item.gd
class_name Item
extends Resource

enum ItemType { WEAPON, ARMOR, CONSUMABLE, QUEST }
enum Rarity { COMMON, UNCOMMON, RARE, EPIC, LEGENDARY }

@export var item_name: String = ""
@export var description: String = ""
@export var type: ItemType = ItemType.CONSUMABLE
@export var rarity: Rarity = Rarity.COMMON
@export var icon: Texture2D
@export var value: int = 0
@export var weight: float = 0.0
@export var stackable: bool = false
@export var max_stack: int = 1
```

### Nested Resources

```gdscript
# data/character_stats.gd
class_name CharacterStats
extends Resource

@export var character_name: String = ""
@export var level: int = 1
@export var health: int = 100
@export var mana: int = 50

# Nested resource
@export var equipment: Equipment

@export var abilities: Array[Ability] = []

# data/equipment.gd
class_name Equipment
extends Resource

@export var weapon: Item
@export var armor: Item
@export var accessory: Item

# data/ability.gd
class_name Ability
extends Resource

@export var ability_name: String = ""
@export var damage: int = 0
@export var mana_cost: int = 10
@export var cooldown: float = 1.0
```

## Export Annotations

### Basic Types

```gdscript
class_name GameConfig
extends Resource

# Primitives
@export var player_name: String = "Hero"
@export var max_level: int = 50
@export var xp_multiplier: float = 1.0
@export var hardcore_mode: bool = false

# Godot types
@export var spawn_position: Vector2 = Vector2.ZERO
@export var tint_color: Color = Color.WHITE
```

### Export Hints

```gdscript
class_name EnemyData
extends Resource

# Range slider
@export_range(1, 100) var health: int = 50
@export_range(0.0, 10.0, 0.1) var move_speed: float = 3.0

# Multiline text
@export_multiline var description: String = ""

# File path
@export_file("*.png", "*.jpg") var portrait_path: String = ""

# Color with no alpha
@export_color_no_alpha var team_color: Color = Color.RED

# Dropdown enum
@export_enum("Easy", "Normal", "Hard") var difficulty: String = "Normal"

# Flags (bit mask)
@export_flags("Fire:1", "Ice:2", "Lightning:4") var resistances: int = 0
```

### Typed Arrays

```gdscript
class_name QuestData
extends Resource

# Array of built-in types
@export var reward_amounts: Array[int] = []
@export var dialogue_lines: Array[String] = []

# Array of resources
@export var objectives: Array[QuestObjective] = []
@export var rewards: Array[Item] = []

# Array of node paths
@export var npc_paths: Array[NodePath] = []
```

### Export Groups

```gdscript
class_name WeaponData
extends Resource

@export_group("Basic Info")
@export var weapon_name: String = ""
@export var description: String = ""
@export var icon: Texture2D

@export_group("Stats")
@export_range(1, 100) var damage: int = 10
@export_range(0.1, 5.0) var attack_speed: float = 1.0
@export_range(1, 100) var durability: int = 100

@export_group("Requirements")
@export var required_level: int = 1
@export var required_strength: int = 0
@export var required_dexterity: int = 0

@export_subgroup("Visual")
@export var sprite: Texture2D
@export var animation: String = "default"
```

## Loading Resources

### Preload (Compile-Time)

```gdscript
# Best for static data - loaded at compile time
const SWORD_DATA: Item = preload("res://data/items/sword.tres")
const HEALTH_POTION: Item = preload("res://data/items/health_potion.tres")

func _ready() -> void:
    print(SWORD_DATA.item_name)  # Available immediately
```

### Load (Runtime)

```gdscript
# For dynamic loading - loaded at runtime
func load_item(item_id: String) -> Item:
    var path := "res://data/items/%s.tres" % item_id
    if ResourceLoader.exists(path):
        return load(path) as Item
    return null

func load_all_items() -> Array[Item]:
    var items: Array[Item] = []
    var dir := DirAccess.open("res://data/items/")
    if dir:
        dir.list_dir_begin()
        var file_name := dir.get_next()
        while file_name != "":
            if file_name.ends_with(".tres"):
                var item := load("res://data/items/" + file_name) as Item
                if item:
                    items.append(item)
            file_name = dir.get_next()
        dir.list_dir_end()
    return items
```

### Resource Cache

```gdscript
# Resources are cached by default - same instance returned
var item1: Item = load("res://data/items/sword.tres")
var item2: Item = load("res://data/items/sword.tres")
print(item1 == item2)  # true - same instance!

# Force reload from disk
var fresh_item: Item = ResourceLoader.load(
    "res://data/items/sword.tres",
    "",
    ResourceLoader.CACHE_MODE_IGNORE
) as Item
```

### Duplicate for Unique Instances

```gdscript
# Bad - modifying shared resource
var player_item: Item = preload("res://data/items/sword.tres")
player_item.durability -= 10  # Affects ALL references!

# Good - create unique copy
var player_item: Item = preload("res://data/items/sword.tres").duplicate()
player_item.durability -= 10  # Only affects this copy

# Deep duplicate for nested resources
var character: CharacterStats = base_stats.duplicate(true)
character.equipment.weapon = new_weapon  # Won't affect base_stats
```

## Saving Resources

### Save to Disk

```gdscript
# Save as text format (.tres) - human-readable, VCS-friendly
func save_item(item: Item, file_name: String) -> void:
    var path := "user://items/%s.tres" % file_name
    var error := ResourceSaver.save(item, path)
    if error != OK:
        push_error("Failed to save item: " + error_string(error))

# Save as binary (.res) - smaller, faster
func save_item_binary(item: Item, file_name: String) -> void:
    var path := "user://items/%s.res" % file_name
    var error := ResourceSaver.save(item, path, ResourceSaver.FLAG_BUNDLE_RESOURCES)
    if error != OK:
        push_error("Failed to save item: " + error_string(error))
```

### Save Game Pattern

```gdscript
# autoloads/save_manager.gd
extends Node

const SAVE_PATH := "user://save_game.res"

class_name SaveGame
extends Resource

@export var player_name: String = ""
@export var level: int = 1
@export var experience: int = 0
@export var gold: int = 0
@export var position: Vector2 = Vector2.ZERO
@export var inventory: Array[Item] = []
@export var completed_quests: Array[String] = []

func save_game(save_data: SaveGame) -> void:
    # Use binary in release builds for security
    var path := SAVE_PATH
    if OS.is_debug_build():
        path = SAVE_PATH.replace(".res", ".tres")

    var error := ResourceSaver.save(save_data, path)
    if error != OK:
        push_error("Failed to save game: " + error_string(error))

func load_game() -> SaveGame:
    # Try both formats
    var paths := [SAVE_PATH, SAVE_PATH.replace(".res", ".tres")]

    for path in paths:
        if FileAccess.file_exists(path):
            var save := ResourceLoader.load(
                path,
                "",
                ResourceLoader.CACHE_MODE_IGNORE
            ) as SaveGame
            if save:
                return save

    # No save found, return new game
    return SaveGame.new()

func delete_save() -> void:
    for path in [SAVE_PATH, SAVE_PATH.replace(".res", ".tres")]:
        if FileAccess.file_exists(path):
            DirAccess.remove_absolute(path)
```

### Auto-Save Pattern

```gdscript
# autoloads/auto_save_manager.gd
extends Node

const AUTO_SAVE_INTERVAL := 300.0  # 5 minutes

var _save_timer: Timer
var _current_save: SaveGame

func _ready() -> void:
    _save_timer = Timer.new()
    _save_timer.wait_time = AUTO_SAVE_INTERVAL
    _save_timer.timeout.connect(_on_auto_save)
    add_child(_save_timer)
    _save_timer.start()

func _on_auto_save() -> void:
    if _current_save:
        SaveManager.save_game(_current_save)
        print("Auto-saved at ", Time.get_datetime_string_from_system())
```

## Resource Inheritance

### Base Resource

```gdscript
# data/entity_data.gd
class_name EntityData
extends Resource

@export var entity_name: String = ""
@export var max_health: int = 100
@export var move_speed: float = 100.0
@export var sprite: Texture2D

func get_display_name() -> String:
    return entity_name
```

### Derived Resources

```gdscript
# data/enemy_data.gd
class_name EnemyData
extends EntityData

@export var damage: int = 10
@export var experience_reward: int = 50
@export var gold_reward: int = 25
@export var loot_table: Array[Item] = []

func get_display_name() -> String:
    return "[Enemy] " + entity_name

# data/npc_data.gd
class_name NPCData
extends EntityData

@export var dialogue_lines: Array[String] = []
@export var quest_id: String = ""
@export var shop_inventory: Array[Item] = []

func get_display_name() -> String:
    return "[NPC] " + entity_name
```

## Resource Database Pattern

```gdscript
# autoloads/item_database.gd
extends Node

var _items_by_id: Dictionary = {}

func _ready() -> void:
    _load_all_items()

func _load_all_items() -> void:
    var dir := DirAccess.open("res://data/items/")
    if not dir:
        push_error("Failed to open items directory")
        return

    dir.list_dir_begin()
    var file_name := dir.get_next()
    while file_name != "":
        if file_name.ends_with(".tres"):
            var item := load("res://data/items/" + file_name) as Item
            if item:
                var id := file_name.trim_suffix(".tres")
                _items_by_id[id] = item
        file_name = dir.get_next()
    dir.list_dir_end()

    print("Loaded ", _items_by_id.size(), " items")

func get_item(item_id: String) -> Item:
    if item_id in _items_by_id:
        return _items_by_id[item_id].duplicate()
    push_error("Item not found: " + item_id)
    return null

func get_all_items() -> Array[Item]:
    var items: Array[Item] = []
    for item in _items_by_id.values():
        items.append(item.duplicate())
    return items

func get_items_by_type(type: Item.ItemType) -> Array[Item]:
    var items: Array[Item] = []
    for item in _items_by_id.values():
        if item.type == type:
            items.append(item.duplicate())
    return items
```

## Creating Resources in Editor

### Via Script

1. Create GDScript file extending Resource
2. Add `class_name` declaration
3. Add `@export` properties
4. Save script

### Via Inspector

1. In FileSystem dock, right-click folder
2. Select "Create New" → "Resource"
3. Choose your custom resource class
4. Click "Create"
5. Edit properties in Inspector
6. Save as `.tres` file

### Programmatically

```gdscript
func create_weapon(weapon_name: String, damage: int) -> WeaponData:
    var weapon := WeaponData.new()
    weapon.weapon_name = weapon_name
    weapon.damage = damage
    weapon.attack_speed = 1.0
    weapon.durability = 100

    # Optionally save to disk
    ResourceSaver.save(weapon, "user://weapons/%s.tres" % weapon_name)

    return weapon
```

## Best Practices

### Do

```gdscript
# Use resources for data containers
class_name EnemyStats
extends Resource

@export var health: int = 100
@export var damage: int = 10

# Always specify types for @export
@export var items: Array[Item] = []  # Good
@export var items := []  # Bad - no type info

# Use class_name for discoverability
class_name QuestData  # Good - shows in editor dropdown
extends Resource

# Duplicate when you need unique instances
var player_stats := base_stats.duplicate(true)

# Use descriptive names
class_name WeaponData  # Good
class_name Data  # Bad - too generic
```

### Don't

```gdscript
# Don't use resources for behavior
class_name EnemyAI  # Bad - use Node instead
extends Resource

# Don't forget @export - properties won't save
var health: int = 100  # Bad - won't persist to disk

# Don't modify preloaded resources directly
const SWORD := preload("res://items/sword.tres")
SWORD.durability -= 1  # Bad - affects all references!

# Don't ignore ResourceSaver errors
ResourceSaver.save(item, path)  # Bad - no error handling

# Don't use res:// for save files
ResourceSaver.save(save, "res://save.tres")  # Bad - read-only at runtime
ResourceSaver.save(save, "user://save.tres")  # Good - writable directory
```

## File Formats

| Format | Extension | Use Case | Pros | Cons |
|--------|-----------|----------|------|------|
| Text | `.tres` | Development, VCS | Human-readable, mergeable | Larger file size |
| Binary | `.res` | Production, saves | Smaller, faster, secure | Not human-readable |

```gdscript
# Choose format based on build type
func get_save_path() -> String:
    if OS.is_debug_build():
        return "user://save.tres"  # Text for debugging
    else:
        return "user://save.res"  # Binary for release
```

## Common Use Cases

### Configuration Files

```gdscript
class_name GameSettings
extends Resource

@export var master_volume: float = 1.0
@export var music_volume: float = 0.8
@export var sfx_volume: float = 1.0
@export var fullscreen: bool = false
@export var vsync: bool = true
@export var language: String = "en"

func apply_settings() -> void:
    AudioServer.set_bus_volume_db(0, linear_to_db(master_volume))
    AudioServer.set_bus_volume_db(1, linear_to_db(music_volume))
    AudioServer.set_bus_volume_db(2, linear_to_db(sfx_volume))
    DisplayServer.window_set_mode(
        DisplayServer.WINDOW_MODE_FULLSCREEN if fullscreen
        else DisplayServer.WINDOW_MODE_WINDOWED
    )
    DisplayServer.window_set_vsync_mode(
        DisplayServer.VSYNC_ENABLED if vsync
        else DisplayServer.VSYNC_DISABLED
    )
```

### Scriptable Objects

```gdscript
# Like Unity's ScriptableObjects
class_name WaveData
extends Resource

@export var wave_number: int = 1
@export var enemy_types: Array[EnemyData] = []
@export var spawn_counts: Array[int] = []
@export var spawn_interval: float = 2.0
@export var boss_wave: bool = false

func get_total_enemies() -> int:
    var total := 0
    for count in spawn_counts:
        total += count
    return total
```

### Save Data Migration

```gdscript
# Handle version changes
class_name SaveGame
extends Resource

const CURRENT_VERSION := 2

@export var version: int = CURRENT_VERSION
@export var player_data: Dictionary = {}

static func load_and_migrate(path: String) -> SaveGame:
    var save := ResourceLoader.load(path, "", ResourceLoader.CACHE_MODE_IGNORE) as SaveGame
    if not save:
        return SaveGame.new()

    # Migrate old versions
    match save.version:
        1:
            save._migrate_v1_to_v2()
            save.version = 2

    return save

func _migrate_v1_to_v2() -> void:
    # Example: Convert old health system to new one
    if "hp" in player_data:
        player_data["health"] = player_data["hp"]
        player_data.erase("hp")
```

## Security Considerations

```gdscript
# Resources can execute code - validate before loading
func load_safe_resource(path: String) -> Resource:
    # Only load from trusted directories
    if not path.begins_with("res://data/") and not path.begins_with("user://"):
        push_error("Untrusted resource path: " + path)
        return null

    # Verify file exists
    if not FileAccess.file_exists(path):
        push_error("Resource not found: " + path)
        return null

    return load(path)

# Use binary format in release to prevent casual editing
func save_secure(resource: Resource, name: String) -> void:
    var extension := ".tres" if OS.is_debug_build() else ".res"
    var path := "user://saves/%s%s" % [name, extension]
    ResourceSaver.save(resource, path)
```

## Common Pitfalls

### Shared Resource Modification

```gdscript
# Problem: All enemies share same stats
const BASE_ENEMY := preload("res://data/enemy_base.tres")

func spawn_enemy() -> Enemy:
    var enemy := Enemy.new()
    enemy.stats = BASE_ENEMY  # Bad - shared reference!
    enemy.stats.health = 50  # Modifies BASE_ENEMY!
    return enemy

# Solution: Duplicate the resource
func spawn_enemy() -> Enemy:
    var enemy := Enemy.new()
    enemy.stats = BASE_ENEMY.duplicate()  # Good - unique copy
    enemy.stats.health = 50
    return enemy
```

### Missing @export

```gdscript
# Problem: Property doesn't save to disk
class_name PlayerData
extends Resource

var gold: int = 100  # Won't be saved!

# Solution: Add @export
class_name PlayerData
extends Resource

@export var gold: int = 100  # Will be saved
```

### Cache Issues

```gdscript
# Problem: Loading old data after save
func test_save_load() -> void:
    var data := PlayerData.new()
    data.gold = 1000
    ResourceSaver.save(data, "user://test.tres")

    var loaded := load("user://test.tres") as PlayerData  # May load cached version!
    print(loaded.gold)  # Might be old value

# Solution: Disable cache when loading saves
func test_save_load() -> void:
    var data := PlayerData.new()
    data.gold = 1000
    ResourceSaver.save(data, "user://test.tres")

    var loaded := ResourceLoader.load(
        "user://test.tres",
        "",
        ResourceLoader.CACHE_MODE_IGNORE
    ) as PlayerData
    print(loaded.gold)  # Always fresh from disk
```

## Related Patterns

- [Autoloads](autoloads.md) - Database managers as singletons
- [Signals](signals.md) - Notify when resources change
- [Save/Load](save-load.md) - Persistence patterns using resources
