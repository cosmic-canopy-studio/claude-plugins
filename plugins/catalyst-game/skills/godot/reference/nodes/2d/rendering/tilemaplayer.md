---
class: TileMapLayer
category: rendering
complexity: intermediate
godot_version: "4.x"
---

# TileMapLayer

**Inherits:** Node2D < CanvasItem < Node < Object

Node for 2D tile-based maps.

## Description

TileMapLayer is a single-layer tile-based map node that uses a TileSet to create grid-based maps. Unlike the deprecated TileMap node, TileMapLayer represents only one layer - use multiple TileMapLayer nodes for multi-layer maps.

**Important:** All TileMap updates are batched at the end of a frame for performance. Call `update_internals()` to force immediate update if needed.

**Note:** Coordinates are limited to 16-bit signed integers (-32768 to 32767). Tiles outside this range are wrapped when saving.

## Core Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `tile_set` | TileSet | `null` | TileSet containing available tiles |
| `enabled` | bool | `true` | Enable/disable layer completely |
| `tile_map_data` | PackedByteArray | `[]` | Raw tile map data |

## Rendering Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `rendering_quadrant_size` | int | `16` | Quadrant size for rendering batching |
| `y_sort_origin` | int | `0` | Y-sort origin offset for tiles |
| `x_draw_order_reversed` | bool | `false` | Reverse X-axis draw order when Y-sorting |

## Physics Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `collision_enabled` | bool | `true` | Enable collision shapes |
| `physics_quadrant_size` | int | `16` | Quadrant size for physics batching |
| `use_kinematic_bodies` | bool | `false` | Use kinematic bodies for collisions |

## Navigation Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `navigation_enabled` | bool | `true` | Enable navigation regions |

## Occlusion Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `occlusion_enabled` | bool | `true` | Enable light occlusion |

## Debug Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `collision_visibility_mode` | enum | `DEBUG_VISIBILITY_MODE_DEFAULT` | Show/hide collision shapes |
| `navigation_visibility_mode` | enum | `DEBUG_VISIBILITY_MODE_DEFAULT` | Show/hide navigation meshes |

### Debug Visibility Modes

| Constant | Value | Description |
|----------|-------|-------------|
| `DEBUG_VISIBILITY_MODE_DEFAULT` | `0` | Use project debug settings |
| `DEBUG_VISIBILITY_MODE_FORCE_SHOW` | `1` | Always show debug shapes |
| `DEBUG_VISIBILITY_MODE_FORCE_HIDE` | `2` | Always hide debug shapes |

## Essential Methods

### set_cell(coords: Vector2i, source_id: int = -1, atlas_coords: Vector2i = Vector2i(-1, -1), alternative_tile: int = 0)

Sets tile at given coordinates using tile identifiers.

```gdscript
# Set a tile
tile_map.set_cell(Vector2i(0, 0), 0, Vector2i(1, 2))

# Erase a tile (use -1 for any parameter)
tile_map.set_cell(Vector2i(0, 0), -1)
```

**Parameters:**
- `coords`: Grid position
- `source_id`: TileSetSource ID (-1 to erase)
- `atlas_coords`: Atlas coordinates (-1, -1 to erase)
- `alternative_tile`: Alternative tile ID (-1 to erase)

### erase_cell(coords: Vector2i)

Erases the cell at coordinates.

```gdscript
tile_map.erase_cell(Vector2i(5, 3))
```

### get_cell_source_id(coords: Vector2i) -> int

Returns tile source ID at coordinates, or -1 if empty.

### get_cell_atlas_coords(coords: Vector2i) -> Vector2i

Returns tile atlas coordinates, or Vector2i(-1, -1) if empty.

### get_cell_alternative_tile(coords: Vector2i) -> int

Returns alternative tile ID.

### get_cell_tile_data(coords: Vector2i) -> TileData

Returns TileData object for cell, or null if empty or not from TileSetAtlasSource.

```gdscript
func get_tile_custom_data(pos: Vector2i, data_name: String) -> Variant:
    var tile_data: TileData = tile_map.get_cell_tile_data(pos)
    if tile_data:
        return tile_data.get_custom_data(data_name)
    return null
```

### clear()

Clears all cells in the layer.

```gdscript
tile_map.clear()
```

## Coordinate Conversion

### local_to_map(local_position: Vector2) -> Vector2i

Converts local position to map coordinates.

```gdscript
var mouse_pos: Vector2 = get_local_mouse_position()
var cell_coords: Vector2i = tile_map.local_to_map(mouse_pos)
```

### map_to_local(map_position: Vector2i) -> Vector2

Converts map coordinates to centered local position.

```gdscript
var world_pos: Vector2 = tile_map.map_to_local(Vector2i(5, 3))
```

**Note:** Returns cell center, ignoring `TileData.texture_origin`.

## Cell Query Methods

### get_used_cells() -> Array[Vector2i]

Returns array of all non-empty cell coordinates.

```gdscript
var all_cells: Array[Vector2i] = tile_map.get_used_cells()
for coords in all_cells:
    print("Cell at: ", coords)
```

### get_used_cells_by_id(source_id: int = -1, atlas_coords: Vector2i = Vector2i(-1, -1), alternative_tile: int = -1) -> Array[Vector2i]

Returns cells matching given tile identifiers. Use -1 to skip filtering that parameter.

```gdscript
# Find all cells using source 0, atlas coords (2, 3)
var matching_cells: Array[Vector2i] = tile_map.get_used_cells_by_id(0, Vector2i(2, 3))

# Find all cells using source 1 (any atlas coords or alternative)
var source_1_cells: Array[Vector2i] = tile_map.get_used_cells_by_id(1)
```

### get_used_rect() -> Rect2i

Returns rectangle enclosing all used tiles.

```gdscript
var bounds: Rect2i = tile_map.get_used_rect()
print("Map spans from ", bounds.position, " to ", bounds.end)
```

## Neighbor Methods

### get_neighbor_cell(coords: Vector2i, neighbor: TileSet.CellNeighbor) -> Vector2i

Returns neighboring cell coordinates, accounting for tile layout (square/hex/isometric).

```gdscript
# Get cell to the right
var right_cell: Vector2i = tile_map.get_neighbor_cell(
    Vector2i(5, 3),
    TileSet.CELL_NEIGHBOR_RIGHT_SIDE
)
```

### get_surrounding_cells(coords: Vector2i) -> Array[Vector2i]

Returns all cells touching edges (4 for square, 6 for hex).

```gdscript
var neighbors: Array[Vector2i] = tile_map.get_surrounding_cells(Vector2i(5, 3))
for neighbor_pos in neighbors:
    print("Neighbor at: ", neighbor_pos)
```

## Terrain Methods

### set_cells_terrain_connect(cells: Array[Vector2i], terrain_set: int, terrain: int, ignore_empty_terrains: bool = true)

Updates cells to use given terrain, connecting neighbors with same terrain.

```gdscript
# Paint grass terrain on multiple cells
var cells_to_paint: Array[Vector2i] = [Vector2i(0, 0), Vector2i(1, 0), Vector2i(2, 0)]
tile_map.set_cells_terrain_connect(cells_to_paint, 0, 0)  # terrain_set 0, terrain 0
```

### set_cells_terrain_path(path: Array[Vector2i], terrain_set: int, terrain: int, ignore_empty_terrains: bool = true)

Updates cells in path order, connecting successive cells with terrain.

```gdscript
# Create dirt path
var path: Array[Vector2i] = [Vector2i(0, 0), Vector2i(1, 0), Vector2i(2, 0), Vector2i(2, 1)]
tile_map.set_cells_terrain_path(path, 0, 1)  # terrain_set 0, terrain 1 (dirt)
```

**Note:** Requires TileSet with properly configured terrain combinations.

## Pattern Methods

### get_pattern(coords_array: Array[Vector2i]) -> TileMapPattern

Creates TileMapPattern from given cells.

```gdscript
var cells: Array[Vector2i] = [Vector2i(0, 0), Vector2i(1, 0), Vector2i(0, 1)]
var pattern: TileMapPattern = tile_map.get_pattern(cells)
```

### set_pattern(position: Vector2i, pattern: TileMapPattern)

Pastes TileMapPattern at given position.

```gdscript
tile_map.set_pattern(Vector2i(10, 10), saved_pattern)
```

### map_pattern(position_in_tilemap: Vector2i, coords_in_pattern: Vector2i, pattern: TileMapPattern) -> Vector2i

Returns tilemap coordinates for pattern cell when pasted at position.

```gdscript
var final_coords: Vector2i = tile_map.map_pattern(
    Vector2i(10, 10),  # Where pattern will be pasted
    Vector2i(1, 1),    # Cell within pattern
    pattern
)
```

## Update Methods

### update_internals()

Forces immediate TileMapLayer update instead of waiting until end of frame.

```gdscript
# Make changes
tile_map.set_cell(Vector2i(0, 0), 0, Vector2i(1, 1))
tile_map.set_cell(Vector2i(1, 0), 0, Vector2i(1, 1))

# Force update now
tile_map.update_internals()

# Changes are now visible immediately
```

**Warning:** Expensive operation, avoid calling frequently.

### fix_invalid_tiles()

Removes cells with tiles that don't exist in TileSet.

```gdscript
tile_map.fix_invalid_tiles()
```

## Physics Integration

### get_coords_for_body_rid(body: RID) -> Vector2i

Returns coordinates of physics quadrant for given body RID.

```gdscript
func _on_body_entered(body: Node2D) -> void:
    if body is CharacterBody2D:
        var collision: KinematicCollision2D = body.get_last_slide_collision()
        if collision:
            var body_rid: RID = collision.get_collider_rid()
            if tile_map.has_body_rid(body_rid):
                var coords: Vector2i = tile_map.get_coords_for_body_rid(body_rid)
                print("Collided with tile at: ", coords)
```

### has_body_rid(body: RID) -> bool

Returns true if RID belongs to this TileMapLayer.

## Navigation Integration

### get_navigation_map() -> RID

Returns NavigationServer2D navigation map RID.

### set_navigation_map(map: RID)

Sets custom NavigationServer2D navigation map.

```gdscript
# Use custom navigation map
var custom_map: RID = NavigationServer2D.map_create()
tile_map.set_navigation_map(custom_map)
```

## Common Patterns

### Basic Tile Placement

```gdscript
extends Node2D

@onready var tile_map: TileMapLayer = $TileMapLayer

func _ready() -> void:
    # Create simple 5x5 grid
    for x in range(5):
        for y in range(5):
            tile_map.set_cell(Vector2i(x, y), 0, Vector2i(0, 0))
```

### Mouse-Based Tile Editing

```gdscript
func _unhandled_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        var mouse_pos: Vector2 = get_local_mouse_position()
        var coords: Vector2i = tile_map.local_to_map(mouse_pos)

        if event.button_index == MOUSE_BUTTON_LEFT:
            # Place tile
            tile_map.set_cell(coords, 0, Vector2i(0, 0))
        elif event.button_index == MOUSE_BUTTON_RIGHT:
            # Erase tile
            tile_map.erase_cell(coords)
```

### Reading Tile Custom Data

```gdscript
func get_tile_cost(coords: Vector2i) -> int:
    var tile_data: TileData = tile_map.get_cell_tile_data(coords)
    if tile_data:
        return tile_data.get_custom_data("movement_cost")
    return 1  # Default cost
```

### Creating Room from Pattern

```gdscript
# Save a room pattern
var room_cells: Array[Vector2i] = [
    Vector2i(0, 0), Vector2i(1, 0), Vector2i(2, 0),
    Vector2i(0, 1), Vector2i(2, 1),
    Vector2i(0, 2), Vector2i(1, 2), Vector2i(2, 2)
]
var room_pattern: TileMapPattern = tile_map.get_pattern(room_cells)

# Paste room elsewhere
tile_map.set_pattern(Vector2i(10, 5), room_pattern)
```

### Auto-Tiling with Terrain

```gdscript
# Paint connected grass area
var grass_cells: Array[Vector2i] = []
for x in range(5):
    for y in range(5):
        grass_cells.append(Vector2i(x, y))

tile_map.set_cells_terrain_connect(grass_cells, 0, 0)  # Automatically tiles edges
```

## Performance Considerations

### Quadrant Sizes

Quadrants batch similar tiles together:

```gdscript
# Smaller quadrants: better for dynamic changes, more draw calls
tile_map.rendering_quadrant_size = 8

# Larger quadrants: better for static maps, fewer draw calls
tile_map.rendering_quadrant_size = 32

# Physics quadrants affect collision detection
tile_map.physics_quadrant_size = 16
```

### Batch Updates

For many changes, batch them together:

```gdscript
# Bad: Updates after each set_cell
for x in range(100):
    for y in range(100):
        tile_map.set_cell(Vector2i(x, y), 0, Vector2i(0, 0))
        tile_map.update_internals()  # DON'T DO THIS

# Good: Single update at end
for x in range(100):
    for y in range(100):
        tile_map.set_cell(Vector2i(x, y), 0, Vector2i(0, 0))
# Automatic update at end of frame
```

### Y-Sorting

For isometric/top-down games with depth:

```gdscript
tile_map.y_sort_enabled = true
tile_map.y_sort_origin = 0

# For per-tile Y-sort adjustment
tile_map.x_draw_order_reversed = false  # Or true for reversed X order
```

## Runtime Tile Data Updates

Override virtual methods for dynamic tile properties:

```gdscript
extends TileMapLayer

func _use_tile_data_runtime_update(coords: Vector2i) -> bool:
    # Return true for tiles that need runtime updates
    return coords.y == 0  # Example: only first row

func _tile_data_runtime_update(coords: Vector2i, tile_data: TileData) -> void:
    # Modify tile_data properties at runtime
    tile_data.modulate = Color.RED if is_tile_damaged(coords) else Color.WHITE

func mark_tile_damaged(coords: Vector2i) -> void:
    # Notify layer that tile needs update
    notify_runtime_tile_data_update()
```

## Signals

### changed()

Emitted when layer properties or cells change.

```gdscript
func _ready() -> void:
    tile_map.changed.connect(_on_tilemap_changed)

func _on_tilemap_changed() -> void:
    print("TileMap was modified")
```

**Warning:** Can emit very frequently during batch modifications. Use `call_deferred()` for expensive operations.

## Best Practices

1. **Use terrain system** for auto-tiling instead of manual placement
2. **Batch updates** - avoid calling `update_internals()` frequently
3. **Limit runtime updates** - only use `_tile_data_runtime_update()` when necessary
4. **Set max_distance** on navigation if layer is large
5. **Use appropriate quadrant sizes** for your use case
6. **Check tiles exist** before querying to avoid null TileData

## Common Pitfalls

1. **Calling update_internals() in loops** - Very expensive
2. **Not checking tile_data for null** - Can crash
3. **Using wrong coordinate system** - local vs map coords
4. **Forgetting coordinate limits** - ±32768 range
5. **Not waiting for initialization** - Scene tiles initialize after parent

## Multi-Layer Setup

```gdscript
# Use multiple TileMapLayer nodes for layers
var ground_layer: TileMapLayer = $GroundLayer
var objects_layer: TileMapLayer = $ObjectsLayer
var decorations_layer: TileMapLayer = $DecorationsLayer

# All share same TileSet
var shared_tileset: TileSet = preload("res://tilesets/main.tres")
ground_layer.tile_set = shared_tileset
objects_layer.tile_set = shared_tileset
decorations_layer.tile_set = shared_tileset

# Different Z-indices for proper layering
ground_layer.z_index = 0
objects_layer.z_index = 1
decorations_layer.z_index = 2
```

## Related Classes

- **TileSet** - Defines available tiles
- **TileData** - Per-tile properties and metadata
- **TileSetAtlasSource** - Atlas-based tile source
- **TileMapPattern** - Reusable tile patterns
- **TileMap** (deprecated) - Old multi-layer tilemap

## Official Resources

- [Using Tilemaps Tutorial](https://docs.godotengine.org/en/stable/tutorials/2d/using_tilemaps.html)
- [TileSet API](https://docs.godotengine.org/en/stable/classes/class_tileset.html)
- [Demo Projects](https://godotengine.org/asset-library/asset/2727)
