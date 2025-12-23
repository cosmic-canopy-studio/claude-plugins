---
class: TileMap
category: nodes/2d/rendering
complexity: advanced
tags: [2d, tilemap, tiles, grid, rendering]
deprecated: true
---

# TileMap

**Inherits:** Node2D < CanvasItem < Node < Object

**Deprecated:** Use multiple TileMapLayer nodes instead.

Node for 2D tile-based maps.

## Description

Node for 2D tile-based maps. Tilemaps use a TileSet which contain a list of tiles which are used to create grid-based maps. A TileMap may have several layers, layouting tiles on top of each other.

For performance reasons, all TileMap updates are batched at the end of a frame. To force an update earlier, call `update_internals()`.

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `collision_animatable` | `bool` | `false` | If enabled, syncs collisions to physics tick (for moving platforms) |
| `collision_visibility_mode` | `VisibilityMode` | `0` | Show or hide collision shapes |
| `navigation_visibility_mode` | `VisibilityMode` | `0` | Show or hide navigation meshes |
| `rendering_quadrant_size` | `int` | `16` | TileMap's quadrant size for rendering optimization |
| `tile_set` | `TileSet` | | The TileSet used by this TileMap |

## Methods

| Return | Method |
|--------|--------|
| `void` | `add_layer(to_position: int)` |
| `void` | `clear()` |
| `void` | `clear_layer(layer: int)` |
| `void` | `erase_cell(layer: int, coords: Vector2i)` |
| `void` | `fix_invalid_tiles()` |
| `int` | `get_cell_alternative_tile(layer: int, coords: Vector2i, use_proxies: bool = false)` |
| `Vector2i` | `get_cell_atlas_coords(layer: int, coords: Vector2i, use_proxies: bool = false)` |
| `int` | `get_cell_source_id(layer: int, coords: Vector2i, use_proxies: bool = false)` |
| `TileData` | `get_cell_tile_data(layer: int, coords: Vector2i, use_proxies: bool = false)` |
| `int` | `get_layers_count()` |
| `Vector2i` | `get_neighbor_cell(coords: Vector2i, neighbor: CellNeighbor)` |
| `Array[Vector2i]` | `get_surrounding_cells(coords: Vector2i)` |
| `Array[Vector2i]` | `get_used_cells(layer: int)` |
| `Array[Vector2i]` | `get_used_cells_by_id(layer: int, source_id: int = -1, atlas_coords: Vector2i = Vector2i(-1, -1), alternative_tile: int = -1)` |
| `Rect2i` | `get_used_rect()` |
| `Vector2i` | `local_to_map(local_position: Vector2)` |
| `Vector2` | `map_to_local(map_position: Vector2i)` |
| `void` | `move_layer(layer: int, to_position: int)` |
| `void` | `remove_layer(layer: int)` |
| `void` | `set_cell(layer: int, coords: Vector2i, source_id: int = -1, atlas_coords: Vector2i = Vector2i(-1, -1), alternative_tile: int = 0)` |
| `void` | `set_cells_terrain_connect(layer: int, cells: Array[Vector2i], terrain_set: int, terrain: int, ignore_empty_terrains: bool = true)` |
| `void` | `set_cells_terrain_path(layer: int, path: Array[Vector2i], terrain_set: int, terrain: int, ignore_empty_terrains: bool = true)` |
| `void` | `update_internals()` |

## Signals

- **changed()**: Emitted when the TileSet of this TileMap changes

## Enumerations

### VisibilityMode
- **VISIBILITY_MODE_DEFAULT** (0): Use debug settings to determine visibility
- **VISIBILITY_MODE_FORCE_SHOW** (1): Always show
- **VISIBILITY_MODE_FORCE_HIDE** (2): Always hide

## Quick Examples

### Basic tilemap setup

```gdscript
@onready var tilemap: TileMap = $TileMap

func _ready() -> void:
    # Set a tile at position (0, 0) on layer 0
    tilemap.set_cell(0, Vector2i(0, 0), 0, Vector2i(0, 0))
```

### Place tiles from code

```gdscript
@onready var tilemap: TileMap = $TileMap

func place_tile(map_pos: Vector2i, tile_coords: Vector2i) -> void:
    tilemap.set_cell(0, map_pos, 0, tile_coords)

func remove_tile(map_pos: Vector2i) -> void:
    tilemap.erase_cell(0, map_pos)
```

### Convert between local and map coordinates

```gdscript
@onready var tilemap: TileMap = $TileMap

func _input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        var local_pos: Vector2 = tilemap.to_local(event.position)
        var map_pos: Vector2i = tilemap.local_to_map(local_pos)
        print("Clicked tile: ", map_pos)
```

## Common Patterns

### Get all used tiles

```gdscript
func get_all_tiles(layer: int) -> Array[Vector2i]:
    return $TileMap.get_used_cells(layer)
```

### Check tile at position

```gdscript
func get_tile_data_at(layer: int, map_pos: Vector2i) -> TileData:
    return $TileMap.get_cell_tile_data(layer, map_pos)

func is_tile_occupied(layer: int, map_pos: Vector2i) -> bool:
    return $TileMap.get_cell_source_id(layer, map_pos) != -1
```

### Terrain painting

```gdscript
func paint_terrain(layer: int, cells: Array[Vector2i], terrain_id: int) -> void:
    $TileMap.set_cells_terrain_connect(layer, cells, 0, terrain_id)
```

### Get tile custom data

```gdscript
func get_tile_property(layer: int, map_pos: Vector2i, property_name: String) -> Variant:
    var tile_data: TileData = $TileMap.get_cell_tile_data(layer, map_pos)
    if tile_data:
        return tile_data.get_custom_data(property_name)
    return null
```

### Clear entire layer

```gdscript
func clear_tilemap_layer(layer: int) -> void:
    $TileMap.clear_layer(layer)
```

## Best Practices

- **Deprecated**: Use TileMapLayer nodes instead of TileMap for new projects
- Negative layer indices access layers from the end (-1 = last layer)
- Call `update_internals()` only when necessary (expensive operation)
- Use `get_cell_tile_data()` to access custom tile properties
- Use `local_to_map()` and `map_to_local()` for coordinate conversion
- Enable `collision_animatable` only for moving platform tilemaps
- Use terrain painting methods for natural-looking tile placement
- Quadrant size affects rendering performance (default 16 is usually good)

## Migration Notes

TileMap is deprecated in favor of TileMapLayer nodes. To convert:
1. Open TileMap bottom panel
2. Click toolbox icon (top-right)
3. Choose "Extract TileMap layers as individual TileMapLayer nodes"

## See Also

- [TileMapLayer](tilemaplayer.md) - Replacement for TileMap
- [TileSet](../../resources/tileset.md) - Tile set resource
