---
topic: save-load
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html
  - https://docs.godotengine.org/en/stable/classes/class_fileaccess.html
  - https://www.gdquest.com/library/cheatsheet_save_systems/
  - https://www.gdquest.com/library/save_game_godot4/
  - https://docs.godotengine.org/en/stable/tutorials/io/binary_serialization_api.html
  - https://docs.godotengine.org/en/stable/classes/class_configfile.html
  - https://docs.escoria-framework.org/en/devel/advanced/load_save.html
---

# Save/Load System

Comprehensive patterns for persisting game data, settings, and player progress in Godot 4.

## Quick Reference

| Method | Best For | File Format | Type Safety | Complexity |
|--------|----------|------------|-------------|-----------|
| FileAccess.store_var() | Simple game saves | Binary | Moderate | Low |
| Resources | Complex structured data | .tres/.res | Excellent | High |
| ConfigFile | Settings/preferences | INI text | Moderate | Low |
| JSON | Web APIs, external tools | JSON text | Low | Moderate |

## File Paths

### user:// Directory

Always save player data to `user://` - it's platform-independent and persists between sessions:

```gdscript
# Save game data
const SAVE_PATH: String = "user://savegame.save"

# Settings file
const SETTINGS_PATH: String = "user://settings.cfg"

# Get actual filesystem path
var data_dir: String = OS.get_user_data_dir()
print(data_dir)  # Windows: C:/Users/[username]/AppData/Roaming/Godot/app_userdata/[project_name]
```

**Platform locations:**
- **Windows:** `%APPDATA%\Godot\app_userdata\[project_name]\`
- **macOS:** `~/Library/Application Support/Godot/app_userdata/[project_name]/`
- **Linux:** `~/.local/share/godot/app_userdata/[project_name]/`

### Opening User Directory

```gdscript
# Open user data folder in file explorer
OS.shell_open(OS.get_user_data_dir())
```

## Method 1: Binary Serialization (FileAccess.store_var)

**Best for:** Simple to moderately complex game saves with native Godot types.

### Save Game Data

```gdscript
func save_game() -> void:
	var save_data: Dictionary = {
		"player_position": Vector2(100, 200),
		"health": 75,
		"inventory": ["sword", "potion", "key"],
		"level": 3,
		"timestamp": Time.get_unix_time_from_system()
	}

	var file: FileAccess = FileAccess.open("user://savegame.save", FileAccess.WRITE)
	if file == null:
		print("Error opening save file: ", FileAccess.get_open_error())
		return

	file.store_var(save_data)
	file.close()
	print("Game saved successfully")
```

### Load Game Data

```gdscript
func load_game() -> Dictionary:
	if not FileAccess.file_exists("user://savegame.save"):
		print("Save file does not exist")
		return {}

	var file: FileAccess = FileAccess.open("user://savegame.save", FileAccess.READ)
	if file == null:
		print("Error opening save file: ", FileAccess.get_open_error())
		return {}

	var save_data: Variant = file.get_var()
	file.close()

	if not save_data is Dictionary:
		print("Invalid save data format")
		return {}

	return save_data as Dictionary
```

### Advantages

- **Native type support:** Vector2, Vector3, Color, Transform2D, etc. saved directly
- **Compact:** Binary format uses less space than text
- **Safe:** Cannot execute code (unlike str2var with objects)
- **Fast:** Efficient serialization/deserialization

### Limitations

- **Not human-readable:** Binary format requires Godot to view
- **No partial updates:** Must read/write entire file

## Method 2: Resource-Based System

**Best for:** Complex, strongly-typed data with editor integration.

### Define Resource Classes

```gdscript
# inventory_item.gd
class_name InventoryItem
extends Resource

@export var item_id: String = ""
@export var quantity: int = 1
@export var durability: float = 100.0
```

```gdscript
# player_save_data.gd
class_name PlayerSaveData
extends Resource

@export var player_name: String = "Player"
@export var health: int = 100
@export var max_health: int = 100
@export var position: Vector2 = Vector2.ZERO
@export var inventory: Array[InventoryItem] = []
@export var unlocked_abilities: Array[String] = []
```

### Save Resources

```gdscript
func save_game_as_resource() -> void:
	var save_data := PlayerSaveData.new()
	save_data.player_name = "Hero"
	save_data.health = 85
	save_data.position = player.global_position

	var sword := InventoryItem.new()
	sword.item_id = "iron_sword"
	sword.quantity = 1
	sword.durability = 75.0
	save_data.inventory.append(sword)

	# Use .tres for development (text, readable)
	# Use .res for release (binary, compact)
	var result: Error = ResourceSaver.save(save_data, "user://savegame.tres")
	if result == OK:
		print("Game saved as resource")
	else:
		print("Error saving resource: ", result)
```

### Load Resources

```gdscript
func load_game_from_resource() -> PlayerSaveData:
	if not ResourceLoader.exists("user://savegame.tres"):
		print("Save file does not exist")
		return null

	var save_data: Resource = ResourceLoader.load("user://savegame.tres")
	if save_data is PlayerSaveData:
		return save_data as PlayerSaveData

	print("Invalid save file format")
	return null
```

### Resource Advantages

- **Type safety:** Full static typing support
- **Editor integration:** Inspect/edit .tres files in editor during development
- **Arrays of resources:** Godot 4 fixed issues from Godot 3
- **Inheritance:** Use Resource inheritance for complex data hierarchies

### File Format Choice

```gdscript
# Development: Use .tres (text format)
ResourceSaver.save(save_data, "user://savegame.tres")
# - Human-readable
# - Version control friendly
# - Easy debugging

# Release: Use .res (binary format)
ResourceSaver.save(save_data, "user://savegame.res")
# - Smaller file size
# - Faster loading
# - Harder to tamper with
```

## Method 3: ConfigFile (INI Format)

**Best for:** Settings, preferences, and simple key-value data.

### Save Settings

```gdscript
func save_settings() -> void:
	var config := ConfigFile.new()

	# Graphics settings
	config.set_value("Graphics", "fullscreen", DisplayServer.window_get_mode() == DisplayServer.WINDOW_MODE_FULLSCREEN)
	config.set_value("Graphics", "resolution", DisplayServer.window_get_size())
	config.set_value("Graphics", "vsync", DisplayServer.window_get_vsync_mode())

	# Audio settings
	config.set_value("Audio", "master_volume", AudioServer.get_bus_volume_db(0))
	config.set_value("Audio", "music_volume", AudioServer.get_bus_volume_db(1))
	config.set_value("Audio", "sfx_volume", AudioServer.get_bus_volume_db(2))

	# Gameplay settings
	config.set_value("Gameplay", "mouse_sensitivity", 2.5)
	config.set_value("Gameplay", "invert_y_axis", false)

	var result: Error = config.save("user://settings.cfg")
	if result != OK:
		print("Error saving settings: ", result)
```

### Load Settings

```gdscript
func load_settings() -> void:
	var config := ConfigFile.new()
	var result: Error = config.load("user://settings.cfg")

	if result != OK:
		print("Settings file not found, using defaults")
		return

	# Load graphics settings with defaults
	var fullscreen: bool = config.get_value("Graphics", "fullscreen", false)
	var resolution: Vector2i = config.get_value("Graphics", "resolution", Vector2i(1280, 720))

	# Apply settings
	if fullscreen:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_FULLSCREEN)
	else:
		DisplayServer.window_set_mode(DisplayServer.WINDOW_MODE_WINDOWED)
		DisplayServer.window_set_size(resolution)

	# Load audio settings
	var master_volume: float = config.get_value("Audio", "master_volume", 0.0)
	AudioServer.set_bus_volume_db(0, master_volume)
```

### ConfigFile Format

Produces human-readable INI files:

```ini
[Graphics]
fullscreen=true
resolution=Vector2i(1920, 1080)
vsync=1

[Audio]
master_volume=0.0
music_volume=-5.0
sfx_volume=-3.0

[Gameplay]
mouse_sensitivity=2.5
invert_y_axis=false
```

### ConfigFile Advantages

- **Human-readable:** Easy to edit in text editor
- **Organized:** Sections group related settings
- **Simple API:** Minimal code required
- **Cross-platform:** Standard INI format

## Method 4: JSON

**Best for:** Web APIs, external tools, cross-application data.

### Save JSON

```gdscript
func save_json() -> void:
	# Note: Convert Godot types to JSON-compatible types
	var resolution: Vector2i = DisplayServer.window_get_size()

	var settings: Dictionary = {
		"version": "1.0.0",
		"graphics": {
			"fullscreen": true,
			"resolution": {
				"x": resolution.x,
				"y": resolution.y
			},
			"vsync": true
		},
		"audio": {
			"master_volume": 1.0,
			"music_volume": 0.7,
			"sfx_volume": 0.8
		},
		"gameplay": {
			"mouse_sensitivity": 2.5,
			"difficulty": "normal"
		}
	}

	var json_string: String = JSON.stringify(settings, "\t")  # Pretty-print with tabs

	var file: FileAccess = FileAccess.open("user://settings.json", FileAccess.WRITE)
	if file == null:
		print("Error opening file: ", FileAccess.get_open_error())
		return

	file.store_string(json_string)
	file.close()
```

### Load JSON

```gdscript
func load_json() -> Dictionary:
	if not FileAccess.file_exists("user://settings.json"):
		return {}

	var file: FileAccess = FileAccess.open("user://settings.json", FileAccess.READ)
	if file == null:
		print("Error opening file: ", FileAccess.get_open_error())
		return {}

	var json_string: String = file.get_as_text()
	file.close()

	var json := JSON.new()
	var parse_result: Error = json.parse(json_string)

	if parse_result != OK:
		print("JSON parse error at line ", json.get_error_line(), ": ", json.get_error_message())
		return {}

	var data: Variant = json.data
	if not data is Dictionary:
		print("JSON data is not a dictionary")
		return {}

	return data as Dictionary
```

### JSON Considerations

**Manual type conversion required:**

```gdscript
# Saving: Convert Godot types to JSON-compatible
var pos: Vector2 = player.position
var json_data: Dictionary = {
	"position": {"x": pos.x, "y": pos.y}  # Vector2 → Dictionary
}

# Loading: Convert back to Godot types
var loaded: Dictionary = load_json()
var pos_dict: Dictionary = loaded.get("position", {})
var position := Vector2(pos_dict.get("x", 0.0), pos_dict.get("y", 0.0))
```

**Advantages:**
- Universal format (web, external tools)
- Human-readable
- Debugging-friendly

**Disadvantages:**
- Verbose (larger file size)
- No native Godot type support
- Manual conversion overhead

## Encryption

Protect save files from casual tampering.

### Encrypted Binary Save

```gdscript
func save_encrypted() -> void:
	var save_data: Dictionary = {
		"player_name": "Hero",
		"gold": 1000,
		"level": 25
	}

	var password: String = "MySecretKey2024"
	var key: PackedByteArray = password.sha256_buffer()

	var file: FileAccess = FileAccess.open_encrypted_with_pass("user://savegame.sav", FileAccess.WRITE, password)
	if file == null:
		print("Error: ", FileAccess.get_open_error())
		return

	file.store_var(save_data)
	file.close()
```

### Load Encrypted Binary

```gdscript
func load_encrypted() -> Dictionary:
	var password: String = "MySecretKey2024"

	var file: FileAccess = FileAccess.open_encrypted_with_pass("user://savegame.sav", FileAccess.READ, password)
	if file == null:
		print("Error: ", FileAccess.get_open_error())
		return {}

	var save_data: Variant = file.get_var()
	file.close()

	return save_data as Dictionary
```

### Encrypted ConfigFile

```gdscript
func save_encrypted_config() -> void:
	var config := ConfigFile.new()
	config.set_value("Player", "high_score", 50000)
	config.set_value("Player", "unlocked_levels", 12)

	var password: String = "MySecretKey2024"
	var key: PackedByteArray = password.sha256_buffer()

	var result: Error = config.save_encrypted_pass("user://progress.dat", password)
	if result != OK:
		print("Encryption error: ", result)
```

```gdscript
func load_encrypted_config() -> void:
	var config := ConfigFile.new()
	var password: String = "MySecretKey2024"

	var result: Error = config.load_encrypted_pass("user://progress.dat", password)
	if result == OK:
		var high_score: int = config.get_value("Player", "high_score", 0)
		print("High score: ", high_score)
	else:
		print("Decryption error: ", result)
```

### Encryption Notes

- **Not military-grade:** Deters casual cheating, not determined hackers
- **Password management:** Hard-code in game or derive from device ID
- **Godot 3 → 4:** Encrypted files from Godot 3 cannot be read in Godot 4
- **Use AES-256:** For stronger encryption, use third-party crypto libraries

## Save Game Versioning

Handle save file format changes across game updates.

### Version-Aware Save Structure

```gdscript
const SAVE_VERSION: String = "1.2.0"

func save_game_versioned() -> void:
	var save_data: Dictionary = {
		"version": SAVE_VERSION,
		"timestamp": Time.get_unix_time_from_system(),
		"player": {
			"name": "Hero",
			"health": 100,
			"position": {"x": 150.0, "y": 200.0}
		},
		"inventory": ["sword", "potion"],
		"game_progress": {
			"current_level": 5,
			"completed_quests": ["tutorial", "first_boss"]
		}
	}

	var file: FileAccess = FileAccess.open("user://savegame.save", FileAccess.WRITE)
	if file:
		file.store_var(save_data)
		file.close()
```

### Migration Strategy

```gdscript
func load_game_versioned() -> Dictionary:
	if not FileAccess.file_exists("user://savegame.save"):
		return {}

	var file: FileAccess = FileAccess.open("user://savegame.save", FileAccess.READ)
	if file == null:
		return {}

	var save_data: Dictionary = file.get_var() as Dictionary
	file.close()

	var save_version: String = save_data.get("version", "1.0.0")

	# Migrate old save formats
	save_data = migrate_save_data(save_data, save_version)

	return save_data

func migrate_save_data(data: Dictionary, from_version: String) -> Dictionary:
	# Apply sequential migrations
	if from_version == "1.0.0":
		data = migrate_1_0_to_1_1(data)
		from_version = "1.1.0"

	if from_version == "1.1.0":
		data = migrate_1_1_to_1_2(data)
		from_version = "1.2.0"

	data["version"] = SAVE_VERSION
	return data

func migrate_1_0_to_1_1(data: Dictionary) -> Dictionary:
	# Version 1.1.0 added inventory system
	if not data.has("inventory"):
		data["inventory"] = []
	return data

func migrate_1_1_to_1_2(data: Dictionary) -> Dictionary:
	# Version 1.2.0 changed position from Vector2 to {x, y} dict
	if data.has("player") and data["player"].has("position"):
		var pos: Variant = data["player"]["position"]
		if pos is Vector2:
			data["player"]["position"] = {
				"x": pos.x,
				"y": pos.y
			}
	return data
```

### Versioning Best Practices

- **Always include version:** Store version string in every save file
- **Sequential migration:** Apply migrations in order (1.0 → 1.1 → 1.2)
- **Default values:** Provide sensible defaults for missing data
- **Test migrations:** Keep old save files for regression testing
- **Backward compatibility window:** Support 2-3 previous versions

## Complete Save Manager Example

```gdscript
# autoloads/save_manager.gd
extends Node

const SAVE_VERSION: String = "1.0.0"
const SAVE_PATH: String = "user://savegame.save"
const SETTINGS_PATH: String = "user://settings.cfg"

var game_data: Dictionary = {}
var settings: ConfigFile = ConfigFile.new()

func _ready() -> void:
	load_settings()

## Save game state to file
func save_game() -> bool:
	var save_data: Dictionary = {
		"version": SAVE_VERSION,
		"timestamp": Time.get_unix_time_from_system(),
		"player": {
			"name": game_data.get("player_name", "Player"),
			"health": game_data.get("health", 100),
			"position": game_data.get("position", Vector2.ZERO),
			"level": game_data.get("level", 1)
		},
		"inventory": game_data.get("inventory", []),
		"progress": game_data.get("progress", {})
	}

	var file: FileAccess = FileAccess.open(SAVE_PATH, FileAccess.WRITE)
	if file == null:
		push_error("Failed to save game: " + str(FileAccess.get_open_error()))
		return false

	file.store_var(save_data)
	file.close()
	print("Game saved successfully")
	return true

## Load game state from file
func load_game() -> bool:
	if not FileAccess.file_exists(SAVE_PATH):
		print("No save file found")
		return false

	var file: FileAccess = FileAccess.open(SAVE_PATH, FileAccess.READ)
	if file == null:
		push_error("Failed to load game: " + str(FileAccess.get_open_error()))
		return false

	var save_data: Variant = file.get_var()
	file.close()

	if not save_data is Dictionary:
		push_error("Invalid save file format")
		return false

	var data: Dictionary = save_data as Dictionary
	var version: String = data.get("version", "1.0.0")

	# Migrate if needed
	if version != SAVE_VERSION:
		print("Migrating save from version ", version, " to ", SAVE_VERSION)
		data = migrate_save_data(data, version)

	# Populate game_data
	var player: Dictionary = data.get("player", {})
	game_data["player_name"] = player.get("name", "Player")
	game_data["health"] = player.get("health", 100)
	game_data["position"] = player.get("position", Vector2.ZERO)
	game_data["level"] = player.get("level", 1)
	game_data["inventory"] = data.get("inventory", [])
	game_data["progress"] = data.get("progress", {})

	print("Game loaded successfully")
	return true

## Save settings to ConfigFile
func save_settings() -> void:
	var result: Error = settings.save(SETTINGS_PATH)
	if result != OK:
		push_error("Failed to save settings: " + str(result))

## Load settings from ConfigFile
func load_settings() -> void:
	var result: Error = settings.load(SETTINGS_PATH)
	if result != OK:
		print("No settings file found, using defaults")
		set_default_settings()

## Set default settings
func set_default_settings() -> void:
	settings.set_value("Graphics", "fullscreen", false)
	settings.set_value("Graphics", "resolution", Vector2i(1280, 720))
	settings.set_value("Audio", "master_volume", 1.0)
	settings.set_value("Audio", "music_volume", 0.8)
	settings.set_value("Audio", "sfx_volume", 1.0)

## Get setting with default fallback
func get_setting(section: String, key: String, default: Variant) -> Variant:
	return settings.get_value(section, key, default)

## Set setting value
func set_setting(section: String, key: String, value: Variant) -> void:
	settings.set_value(section, key, value)

## Delete save file
func delete_save() -> bool:
	if FileAccess.file_exists(SAVE_PATH):
		var result: Error = DirAccess.remove_absolute(SAVE_PATH)
		return result == OK
	return false

## Check if save file exists
func save_exists() -> bool:
	return FileAccess.file_exists(SAVE_PATH)

## Migrate save data to current version
func migrate_save_data(data: Dictionary, from_version: String) -> Dictionary:
	# Add migration logic here as game evolves
	data["version"] = SAVE_VERSION
	return data
```

## Best Practices

### Do

```gdscript
# Always check if file opened successfully
var file: FileAccess = FileAccess.open("user://save.dat", FileAccess.READ)
if file == null:
	print("Error: ", FileAccess.get_open_error())
	return

# Provide default values when loading
var health: int = save_data.get("health", 100)

# Use user:// for all player data
const SAVE_PATH: String = "user://savegame.save"

# Include version information
var save_data: Dictionary = {"version": "1.0.0", "data": {}}

# Close files explicitly (or let them auto-close on scope exit)
file.close()
```

### Don't

```gdscript
# Don't save to res:// (read-only in exported games)
# BAD:
var file: FileAccess = FileAccess.open("res://savegame.save", FileAccess.WRITE)

# Don't ignore errors
# BAD:
var file: FileAccess = FileAccess.open("user://save.dat", FileAccess.READ)
var data = file.get_var()  # Crashes if file is null!

# Don't use str2var() with untrusted data
# BAD (security risk):
var untrusted: String = get_string_from_player()
var result = str2var(untrusted)  # Can execute arbitrary code!

# Don't forget to handle missing data
# BAD:
var health: int = save_data["health"]  # Crashes if key missing
# GOOD:
var health: int = save_data.get("health", 100)
```

## Security Considerations

### Safe Methods

```gdscript
# SAFE: store_var/get_var use safe binary serialization
file.store_var(data)
var loaded = file.get_var()

# SAFE: JSON.parse cannot execute code
var json := JSON.new()
json.parse(json_string)

# SAFE: ConfigFile is text-based key-value storage
config.set_value("Player", "score", 100)
```

### Unsafe Methods

```gdscript
# UNSAFE: str2var can execute code if objects enabled
var result = str2var(untrusted_string)  # Never use with untrusted data!

# UNSAFE: bytes_to_var with allow_objects=true
var result = bytes_to_var(data, true)  # Avoid allow_objects

# SAFER: Use allow_objects=false (default)
var result = bytes_to_var(data, false)  # Safe, values only
```

### Protect Against Tampering

```gdscript
# Use encryption for competitive games
var file: FileAccess = FileAccess.open_encrypted_with_pass(
	"user://highscores.dat",
	FileAccess.WRITE,
	"your_secret_password"
)

# Add checksums for integrity verification
var save_data: Dictionary = {"player": {}, "inventory": []}
var json_string: String = JSON.stringify(save_data)
var checksum: String = json_string.sha256_text()
save_data["_checksum"] = checksum
```

## Performance Tips

### Avoid Frequent Saves

```gdscript
# BAD: Saving every frame
func _process(delta: float) -> void:
	save_game()  # Disk I/O bottleneck!

# GOOD: Save on checkpoints/events
func checkpoint_reached() -> void:
	save_game()

func level_completed() -> void:
	save_game()

func quit_game() -> void:
	save_game()
```

### Partial Updates with ConfigFile

```gdscript
# Update single setting without rewriting everything
func set_volume(bus_name: String, volume: float) -> void:
	settings.set_value("Audio", bus_name, volume)
	settings.save("user://settings.cfg")
```

### Async Loading (for large saves)

```gdscript
# Load save file on separate thread to avoid freezing
func load_game_async() -> void:
	var thread := Thread.new()
	thread.start(_load_game_thread)

func _load_game_thread() -> void:
	var file: FileAccess = FileAccess.open("user://savegame.save", FileAccess.READ)
	if file:
		var data: Variant = file.get_var()
		file.close()

		# Call back to main thread
		call_deferred("_on_game_loaded", data)

func _on_game_loaded(data: Variant) -> void:
	game_data = data as Dictionary
	print("Game loaded asynchronously")
```

## Common Patterns

### Auto-Save

```gdscript
# Save game periodically
var auto_save_timer: Timer

func _ready() -> void:
	auto_save_timer = Timer.new()
	auto_save_timer.wait_time = 300.0  # 5 minutes
	auto_save_timer.timeout.connect(_on_auto_save)
	auto_save_timer.autostart = true
	add_child(auto_save_timer)

func _on_auto_save() -> void:
	save_game()
	print("Auto-save triggered")
```

### Multiple Save Slots

```gdscript
func save_to_slot(slot_index: int) -> void:
	var save_path: String = "user://savegame_%d.save" % slot_index
	var file: FileAccess = FileAccess.open(save_path, FileAccess.WRITE)
	if file:
		file.store_var(game_data)
		file.close()

func load_from_slot(slot_index: int) -> bool:
	var save_path: String = "user://savegame_%d.save" % slot_index
	if not FileAccess.file_exists(save_path):
		return false

	var file: FileAccess = FileAccess.open(save_path, FileAccess.READ)
	if file:
		game_data = file.get_var() as Dictionary
		file.close()
		return true
	return false

func get_save_slot_info(slot_index: int) -> Dictionary:
	var save_path: String = "user://savegame_%d.save" % slot_index
	if not FileAccess.file_exists(save_path):
		return {"exists": false}

	var file: FileAccess = FileAccess.open(save_path, FileAccess.READ)
	if file == null:
		return {"exists": false}

	var data: Dictionary = file.get_var() as Dictionary
	file.close()

	return {
		"exists": true,
		"player_name": data.get("player", {}).get("name", "Unknown"),
		"level": data.get("player", {}).get("level", 1),
		"timestamp": data.get("timestamp", 0),
		"version": data.get("version", "1.0.0")
	}
```

### Cloud Save Integration

```gdscript
# Example structure for Steam Cloud or similar
func sync_cloud_save() -> void:
	# 1. Load local save
	var local_data: Dictionary = load_local_save()
	var local_timestamp: int = local_data.get("timestamp", 0)

	# 2. Load cloud save
	var cloud_data: Dictionary = load_cloud_save()
	var cloud_timestamp: int = cloud_data.get("timestamp", 0)

	# 3. Use newest save
	if cloud_timestamp > local_timestamp:
		print("Using cloud save (newer)")
		game_data = cloud_data
		save_local_save()  # Update local
	elif local_timestamp > cloud_timestamp:
		print("Using local save (newer)")
		game_data = local_data
		upload_cloud_save()  # Update cloud
	else:
		print("Saves are in sync")

func load_local_save() -> Dictionary:
	# Standard FileAccess load
	return {}

func load_cloud_save() -> Dictionary:
	# Platform-specific API (Steam, Epic, etc.)
	return {}

func upload_cloud_save() -> void:
	# Platform-specific API
	pass
```

## Debugging Save Files

### View Binary Save Contents

```gdscript
func debug_print_save() -> void:
	var file: FileAccess = FileAccess.open("user://savegame.save", FileAccess.READ)
	if file:
		var data: Variant = file.get_var()
		file.close()
		print(JSON.stringify(data, "\t"))  # Pretty-print as JSON
```

### Validate Save File Integrity

```gdscript
func validate_save_file() -> bool:
	if not FileAccess.file_exists("user://savegame.save"):
		print("Save file does not exist")
		return false

	var file: FileAccess = FileAccess.open("user://savegame.save", FileAccess.READ)
	if file == null:
		print("Cannot open save file")
		return false

	var data: Variant = file.get_var()
	file.close()

	if not data is Dictionary:
		print("Save file is not a dictionary")
		return false

	var save_data: Dictionary = data as Dictionary

	# Check required keys
	if not save_data.has("version"):
		print("Missing version field")
		return false

	if not save_data.has("player"):
		print("Missing player data")
		return false

	print("Save file is valid")
	return true
```

## Related Patterns

- [Autoloads](autoloads.md) - SaveManager singleton pattern
- [Custom Resources](resources.md) - Resource-based save data structures
- [Signals](signals.md) - Notify systems when save/load completes

## Sources

1. **Official:** [Saving games - Godot Docs](https://docs.godotengine.org/en/stable/tutorials/io/saving_games.html) - Official save/load tutorial
2. **Official:** [FileAccess - Godot API](https://docs.godotengine.org/en/stable/classes/class_fileaccess.html) - FileAccess class reference
3. **Official:** [Binary serialization API - Godot Docs](https://docs.godotengine.org/en/stable/tutorials/io/binary_serialization_api.html) - store_var/get_var details
4. **Official:** [ConfigFile - Godot API](https://docs.godotengine.org/en/stable/classes/class_configfile.html) - ConfigFile class reference
5. **Community:** [Save and Load Cheat Sheet - GDQuest](https://www.gdquest.com/library/cheatsheet_save_systems/) - Comprehensive save system patterns
6. **Community:** [Saving and Loading Games in Godot 4 - GDQuest](https://www.gdquest.com/library/save_game_godot4/) - Resource-based save systems
7. **Community:** [Escoria Load/Save System](https://docs.escoria-framework.org/en/devel/advanced/load_save.html) - Save game versioning patterns
