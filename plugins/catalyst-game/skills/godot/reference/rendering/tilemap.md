---
topic: tilemap
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/4.3/classes/class_tilemaplayer.html
  - https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html
  - https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.html
  - https://github.com/dandeliondino/godot-4-tileset-terrains-docs
  - godot_node_essentials (tile_map_layer demos)
---

# TileMap & TileSet

TileMap patterns for creating tile-based levels in Godot 4.3+.

## Architecture Changes in Godot 4.3

**Important:** In Godot 4.3, the old `TileMap` node is deprecated. Use **`TileMapLayer`** instead.

- **Old approach:** Single TileMap node with multiple layers inside
- **New approach:** Multiple TileMapLayer nodes, one per layer
- **Migration:** Open TileMap bottom panel with node selected, click toolbox icon to convert

### Why TileMapLayer?

```gdscript
# Scene structure (Godot 4.3+)
Level (Node2D)
├─ GroundTileMapLayer (TileMapLayer)      # Terrain layer
├─ ObjectsTileMapLayer (TileMapLayer)      # Props and items
└─ HazardsTileMapLayer (TileMapLayer)      # Dangerous tiles
```

Each layer can have different:
- Z-index for rendering order
- Collision layers/masks
- Y-sort settings for isometric
- Modulation/visibility

## Basic Cell Manipulation {#cells}

### Setting Tiles

```gdscript
@onready var tile_map_layer: TileMapLayer = %TileMapLayer

func place_tile() -> void:
    # Set cell: (map_position, source_id, atlas_coords)
    var map_pos := Vector2i(5, 10)
    var source_id := 0  # Atlas source ID (usually 0)
    var atlas_coords := Vector2i(0, 0)  # Tile position in atlas

    tile_map_layer.set_cell(map_pos, source_id, atlas_coords)

func erase_tile() -> void:
    # Erase by calling set_cell with only position
    var map_pos := Vector2i(5, 10)
    tile_map_layer.set_cell(map_pos)
```

### Reading Tiles

```gdscript
func check_tile_at_position(world_pos: Vector2) -> void:
    # Convert world position to map coordinates
    var map_pos := tile_map_layer.local_to_map(world_pos)

    # Get source ID (-1 if empty)
    var source_id := tile_map_layer.get_cell_source_id(map_pos)

    if source_id == -1:
        print("Empty tile")
        return

    # Get atlas coordinates
    var atlas_coords := tile_map_layer.get_cell_atlas_coords(map_pos)
    print("Tile at ", atlas_coords, " from source ", source_id)

    # Get custom tile data
    var tile_data := tile_map_layer.get_cell_tile_data(map_pos)
    if tile_data:
        var custom_value: Variant = tile_data.get_custom_data("property_name")
```

## Coordinate Conversion {#coordinates}

```gdscript
func coordinate_examples() -> void:
    # World position → Map position
    var mouse_pos := get_global_mouse_position()
    var map_pos := tile_map_layer.local_to_map(mouse_pos)

    # Map position → World position (tile center)
    var world_pos := tile_map_layer.map_to_local(map_pos)

    # Snap to grid (for placing units)
    var snapped_pos := tile_map_layer.map_to_local(
        tile_map_layer.local_to_map(position)
    )
```

### Tile-Snapped Unit Placement

```gdscript
extends Node2D

@export var unit_scene: PackedScene = null

enum { UNIT_PREVIEW_TILE = 0, EMPTY_TILE = -1 }

var preview_cursor_map_position := Vector2i.ZERO

@onready var tile_map_layer: TileMapLayer = %TileMapLayer


func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        _update_tile_map_preview(event.position)

    if event.is_action_pressed("click"):
        _create_unit_at(event.position)


func _create_unit_at(coordinates: Vector2) -> void:
    # Snap input coordinates to the TileMapLayer
    var map_position := tile_map_layer.local_to_map(coordinates)
    var tile := tile_map_layer.get_cell_source_id(map_position)

    # Only place if preview cursor is here
    if tile != UNIT_PREVIEW_TILE:
        return

    var new_unit := unit_scene.instantiate()
    add_child(new_unit)
    # Get world position from map, offset by half tile size
    new_unit.position = tile_map_layer.map_to_local(map_position) - tile_map_layer.tile_set.tile_size / 2.0


func _update_tile_map_preview(coordinates: Vector2) -> void:
    # Clear previous cursor position
    tile_map_layer.set_cell(preview_cursor_map_position)

    # Convert to map coordinates
    var map_position := tile_map_layer.local_to_map(coordinates)

    # Don't show preview over existing tiles
    if tile_map_layer.get_cell_source_id(map_position) != EMPTY_TILE:
        return

    # Show preview
    preview_cursor_map_position = map_position
    tile_map_layer.set_cell(preview_cursor_map_position, UNIT_PREVIEW_TILE, Vector2i.ZERO)
```

## Terrain Sets (Autotiling) {#terrains}

Terrain sets automatically connect tiles based on their neighbors, creating organic shapes for grass, water, platforms, etc.

### Configuring Terrain in TileSet

1. Select TileSet resource in Inspector
2. Under "Terrain Sets", add a terrain set element
3. Add terrain element to the set
4. For each tile in the atlas, assign terrain and configure peering bits

```gdscript
# Terrain sets are configured in the TileSet resource editor
# Each tile stores which terrain it belongs to and how it connects to neighbors
# The engine automatically selects the correct tile variant when painting
```

### Painting with Terrains

```gdscript
# In editor: Use terrain painting mode in TileMap editor
# Terrain tiles automatically adjust based on neighbors

# Programmatic terrain (Godot 4.3+)
func place_terrain_tile() -> void:
    # Note: Direct terrain placement requires using set_cell() with specific
    # atlas coordinates. The terrain system is primarily designed for editor use.
    # For procedural generation, use terrain autotiler plugins or set_cells_terrain_connect()

    # Get terrain set from TileSet
    var terrain_set := 0
    var terrain := 0

    # Set cell and let terrains auto-connect
    tile_map_layer.set_cells_terrain_connect(
        [Vector2i(0, 0), Vector2i(1, 0), Vector2i(2, 0)],
        terrain_set,
        terrain
    )
```

### Deterministic Terrain Generation

For procedural generation or multiplayer, use plugins like **Terrain Autotiler** or **Better Terrain** for consistent results. The built-in terrain system may produce different variations on different runs.

## Custom Tile Data {#custom-data}

Add custom metadata to tiles for gameplay logic (footstep sounds, damage, movement cost, etc.).

### Configuring Custom Data in TileSet

1. Select TileSet resource
2. Add custom data layer: Name it (e.g., "footstep", "damage", "move_cost")
3. Choose type: String, int, float, bool, Color, etc.
4. For each tile, set the custom data value in the TileSet editor

### Reading Custom Data

```gdscript
extends AudioStreamPlayer

@export var step_distance := 160.0

var _step_measure := 0.0

@onready var _player: CharacterBody2D = get_parent()
@onready var _tile_map_layer: TileMapLayer = %BaseTileMapLayer


func _physics_process(delta: float) -> void:
    _step_measure += _player.velocity.length() * delta
    if _step_measure > step_distance:
        _step_measure = 0.0
        _play_footstep()


func _play_footstep() -> void:
    var tile_coordinate := _tile_map_layer.local_to_map(_player.position)
    var tile_data := _tile_map_layer.get_cell_tile_data(tile_coordinate)

    if tile_data:
        var footstep_sound: AudioStream = tile_data.get_custom_data("footstep")
        if footstep_sound:
            stream = footstep_sound
            play()
```

### Hazard Detection

```gdscript
extends AstronautPlayer2D

@onready var _hurt_box_area: Area2D = %HurtBoxArea2D
@onready var _explosion_animation_player: AnimationPlayer = %ExplosionAnimationPlayer


func _ready() -> void:
    _hurt_box_area.body_entered.connect(_on_hurt_box_area_body_entered)


func _on_hurt_box_area_body_entered(body: Node) -> void:
    # Check if tile is in hazard group
    if body is TileMapLayer and body.is_in_group("hazard"):
        _explosion_animation_player.queue("explode")
```

## Procedural Tile Generation {#procedural}

### Randomizing Tiles

```gdscript
extends Node2D

enum Tiles {
    EMPTY_TILE = -1,
    CHANCE_TILE = 0,
    SOLID_TILE = 1,
    DECOR_SOLID = 2,
    DECOR_CEILING1 = 3,
    DECOR_CEILING2 = 4
}

const SOLID_TILE_TYPES := [Tiles.SOLID_TILE, Tiles.DECOR_SOLID]

@onready var tilemap: TileMap = $TileMap
@onready var tiles: TileSet = tilemap.tile_set


func _ready() -> void:
    randomize()
    randomize_chance_tiles()
    add_random_wall_decorations()
    for tile_type: int in SOLID_TILE_TYPES:
        add_random_ceiling_decorations(tile_type)


func randomize_chance_tiles() -> void:
    # Get all cells of a specific type
    for cell: Vector2i in tilemap.get_used_cells(Tiles.CHANCE_TILE):
        var cell_type: int = Tiles.SOLID_TILE if randf() < 0.25 else Tiles.EMPTY_TILE
        tilemap.set_cellv(cell, cell_type)


func add_random_wall_decorations() -> void:
    for cell: Vector2i in tilemap.get_used_cells(Tiles.SOLID_TILE):
        if randf() < 0.1:  # 10% chance
            tilemap.set_cellv(cell, Tiles.DECOR_SOLID)


func add_random_ceiling_decorations(tile_type: int) -> void:
    for cell: Vector2i in tilemap.get_used_cells(tile_type):
        var cell_below := cell + Vector2i.DOWN

        if tilemap.get_cellv(cell_below) != Tiles.EMPTY_TILE:
            continue

        var random_chance := randf()
        if random_chance < 0.1:
            tilemap.set_cellv(cell_below, Tiles.DECOR_CEILING1)
        elif random_chance < 0.2:
            tilemap.set_cellv(cell_below, Tiles.DECOR_CEILING2)
```

## Isometric TileMaps {#isometric}

### Isometric Factor Calculation

```gdscript
extends CharacterBody2D

const SPEED := 640.0

var _isometric_factor := Vector2.ZERO

@onready var ground_objects_tile_map_layer: TileMapLayer = %GroundObjectsTileMapLayer


func _ready() -> void:
    # Calculate width:height ratio from tile size
    var tile_size := ground_objects_tile_map_layer.tile_set.tile_size
    _isometric_factor = Vector2(
        1.0,
        tile_size.y / float(tile_size.x)
    )


func _physics_process(_delta: float) -> void:
    var input_direction := Input.get_vector(
        "move_left", "move_right", "move_up", "move_down"
    )

    # Adjust velocity by isometric factor
    velocity = _isometric_factor * input_direction * SPEED
    move_and_slide()
```

### Multi-Layer Tile Swapping

```gdscript
const TILE_ATLAS_COORDS := {
    door_south_closed = Vector2i(5, 0),
    door_south_opened = Vector2i(1, 1),
    door_west_closed = Vector2i(7, 0),
    door_west_opened = Vector2i(3, 1),
    switch_closed = Vector2i(4, 3),
    switch_opened = Vector2i(0, 3),
}

var _is_switch_pressed := false

@onready var ground_switch_tile_map_layer: TileMapLayer = %GroundSwitchTileMapLayer
@onready var ground_objects_tile_map_layer: TileMapLayer = %GroundObjectsTileMapLayer
@onready var floor_objects_tile_map_layer: TileMapLayer = %UpperObjectsTileMapLayer

# Store tile configurations for state-based swapping
@onready var _toggle_tiles := [
    {
        "node": ground_switch_tile_map_layer,
        false: [
            { atlas_coords = TILE_ATLAS_COORDS.switch_closed },
        ],
        true: [
            { atlas_coords = TILE_ATLAS_COORDS.switch_opened },
        ],
    },
    {
        "node": ground_objects_tile_map_layer,
        false: [
            { map_coords = Vector2i(-12, -14), atlas_coords = TILE_ATLAS_COORDS.door_south_closed },
            { map_coords = Vector2i(-5, -11), atlas_coords = TILE_ATLAS_COORDS.door_west_closed },
        ],
        true: [
            { map_coords = Vector2i(-12, -14), atlas_coords = TILE_ATLAS_COORDS.door_south_opened },
            { map_coords = Vector2i(-5, -11), atlas_coords = TILE_ATLAS_COORDS.door_west_opened },
        ],
    },
]


func toggle_switch() -> void:
    _is_switch_pressed = not _is_switch_pressed
    var switch_map_coords := ground_objects_tile_map_layer.local_to_map(global_position)

    # Iterate through tile configuration
    for dict: Dictionary in _toggle_tiles:
        for arguments: Dictionary in dict[_is_switch_pressed]:
            var tile_map_layer: TileMapLayer = dict.node
            var map_coords: Vector2i = arguments.get("map_coords", switch_map_coords)

            # Set cell: source_id=0 (first atlas), atlas_coords from dictionary
            tile_map_layer.set_cell(map_coords, 0, arguments.atlas_coords)
```

## Physics & Collision {#physics}

### Configuring Collision in TileSet

1. Select TileSet resource
2. Add physics layer
3. For each tile, draw collision polygons in the TileSet editor
4. TileMapLayer automatically creates static collision bodies

```gdscript
# Collision is automatically handled by TileMapLayer
# Configure collision layers/masks in TileMapLayer Inspector:

@export_flags_2d_physics var collision_layer := 1
@export_flags_2d_physics var collision_mask := 1

# Access TileSet properties
func get_tile_size() -> Vector2i:
    return tile_map_layer.tile_set.tile_size
```

### One-Way Platforms

Configure in TileSet physics layer:
- Enable "One Way Collision"
- Set "One Way Collision Margin"

## Light Occlusion {#occlusion}

TileSet supports light occlusion polygons for 2D lighting.

1. Add occlusion layer to TileSet
2. Draw occlusion polygons for tiles
3. Add Light2D or DirectionalLight2D to scene
4. Tiles automatically cast shadows

```gdscript
# Occlusion configured in TileSet editor
# No code required - works automatically with Light2D nodes
```

## Navigation {#navigation}

TileSet supports navigation polygons for pathfinding.

1. Add navigation layer to TileSet
2. Draw navigation polygons for walkable tiles
3. Add NavigationRegion2D to scene
4. Bake navigation mesh

```gdscript
# Navigation configured in TileSet editor
# Use with NavigationAgent2D for pathfinding
```

## Common Patterns

### Tile Lookup Dictionary

```gdscript
# Use enums or constants for tile identification
enum TileType {
    EMPTY = -1,
    GRASS = 0,
    DIRT = 1,
    STONE = 2,
}

const TILE_ATLAS_POSITIONS := {
    TileType.GRASS: Vector2i(0, 0),
    TileType.DIRT: Vector2i(1, 0),
    TileType.STONE: Vector2i(2, 0),
}

func place_tile_by_type(type: TileType, map_pos: Vector2i) -> void:
    if type == TileType.EMPTY:
        tile_map_layer.set_cell(map_pos)
    else:
        tile_map_layer.set_cell(map_pos, 0, TILE_ATLAS_POSITIONS[type])
```

### Mouse Hover Preview

```gdscript
var _hovered_tile := Vector2i(-1, -1)

func _process(_delta: float) -> void:
    var mouse_pos := get_global_mouse_position()
    var map_pos := tile_map_layer.local_to_map(mouse_pos)

    if map_pos != _hovered_tile:
        # Clear old highlight
        if _hovered_tile != Vector2i(-1, -1):
            tile_map_layer.set_cell(_hovered_tile)

        # Show new highlight
        _hovered_tile = map_pos
        tile_map_layer.set_cell(_hovered_tile, 0, Vector2i(3, 3))  # Highlight tile
```

### Flood Fill Algorithm

```gdscript
func flood_fill(start_pos: Vector2i, fill_tile: Vector2i) -> void:
    var target_tile := tile_map_layer.get_cell_source_id(start_pos)
    if target_tile == -1:
        return

    var queue: Array[Vector2i] = [start_pos]
    var visited := {}

    while queue.size() > 0:
        var current := queue.pop_front()

        if current in visited:
            continue
        visited[current] = true

        if tile_map_layer.get_cell_source_id(current) != target_tile:
            continue

        # Fill current tile
        tile_map_layer.set_cell(current, 0, fill_tile)

        # Add neighbors
        queue.append(current + Vector2i.RIGHT)
        queue.append(current + Vector2i.LEFT)
        queue.append(current + Vector2i.UP)
        queue.append(current + Vector2i.DOWN)
```

## Best Practices & Pitfalls

### Do's

- Use TileMapLayer (Godot 4.3+), not deprecated TileMap
- Use separate layers for ground, objects, hazards (easier to manage)
- Enable Y-sort on TileMapLayer for isometric/top-down games
- Use custom data for gameplay properties (sounds, damage, cost)
- Configure collision/occlusion/navigation in TileSet, not code
- Use terrain sets for organic shapes (grass, water, platforms)

### Don'ts

- Don't mix TileMap and TileMapLayer in the same project
- Don't forget to set source_id (usually 0) when calling set_cell()
- Don't rely on built-in terrains for deterministic procedural generation (use plugins)
- Don't manually calculate tile atlas positions - use constants or enums
- Don't create collision shapes in code - configure in TileSet editor

### Performance

- TileMapLayer collision is static by default (very efficient)
- Use `get_used_cells()` instead of iterating all possible positions
- For large procedural maps, generate in chunks
- Clear unused tiles with `set_cell(pos)` to reduce memory

## Related Patterns

- [Collision Detection](/home/sam/code/godot_advisor/.claude/skills/godot/reference/physics/collision.md) - Physics layers and masks
- [2D Character Movement](/home/sam/code/godot_advisor/.claude/skills/godot/reference/movement/2d-character.md) - Interacting with tilemap collision
- [Navigation](/home/sam/code/godot_advisor/.claude/skills/godot/reference/movement/navigation.md) - Pathfinding with navigation layers
- [Resources](/home/sam/code/godot_advisor/.claude/skills/godot/reference/patterns/resources.md) - TileSet as resource

## Migration from Godot 4.2 to 4.3

```gdscript
# OLD (Godot 4.2 and earlier)
var tilemap := TileMap.new()
tilemap.set_cell(0, Vector2i(5, 5), 0, Vector2i(1, 1))  # layer, pos, source, atlas
#           ↑ layer parameter

# NEW (Godot 4.3+)
var tilemap_layer := TileMapLayer.new()
tilemap_layer.set_cell(Vector2i(5, 5), 0, Vector2i(1, 1))  # pos, source, atlas
#                       ↑ no layer - each TileMapLayer is its own layer

# Convert existing TileMap:
# 1. Select TileMap node in scene tree
# 2. Open TileMap editor (bottom panel)
# 3. Click toolbox icon → "Convert to TileMapLayer nodes"
```

## Additional Resources

- [TileMapLayer Class Reference](https://docs.godotengine.org/en/4.3/classes/class_tilemaplayer.html)
- [Using TileMaps Tutorial](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html)
- [Using TileSets Tutorial](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilesets.html)
- [Godot 4 TileSet Terrains Documentation](https://github.com/dandeliondino/godot-4-tileset-terrains-docs)
- [Terrain Autotiler Plugin](https://github.com/dandeliondino/terrain-autotiler)
