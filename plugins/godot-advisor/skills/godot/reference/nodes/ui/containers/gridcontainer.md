---
class: GridContainer
inherits: Container < Control < CanvasItem < Node < Object
category: UI Containers
---

# GridContainer

A container that arranges its child controls in a grid layout.

## Description

GridContainer arranges its child controls in a grid layout. The number of columns is specified by the `columns` property, whereas the number of rows depends on how many are needed for the child controls. The number of rows and columns is preserved for every size of the container.

**Note:** GridContainer only works with child nodes inheriting from Control. It won't rearrange child nodes inheriting from Node2D.

## Inheritance Chain

GridContainer < Container < Control < CanvasItem < Node < Object

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| columns | int | `1` | The number of columns in the GridContainer |

### Property Details

#### columns
- **Type:** int
- **Default:** `1`
- **Setter:** `set_columns(value: int)`
- **Getter:** `get_columns() -> int`

If modified, GridContainer reorders its Control-derived children to accommodate the new layout.

## Methods

All methods are inherited from Container.

## Signals

Inherits all signals from Container and Control.

## Theme Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| h_separation | int | `4` | The horizontal separation of child nodes |
| v_separation | int | `4` | The vertical separation of child nodes |

## Usage Example

```gdscript
var grid: GridContainer = GridContainer.new()
grid.columns = 3
add_child(grid)

# Add 9 buttons in a 3x3 grid
for i in range(9):
	var button: Button = Button.new()
	button.text = str(i + 1)
	grid.add_child(button)

# Customize spacing
grid.add_theme_constant_override("h_separation", 10)
grid.add_theme_constant_override("v_separation", 10)
```

## Common Patterns

### Inventory Grid
```gdscript
var inventory_grid: GridContainer = GridContainer.new()
inventory_grid.columns = 5  # 5 columns for inventory slots

for i in range(20):  # 20 item slots (4 rows x 5 columns)
	var slot: TextureRect = TextureRect.new()
	slot.custom_minimum_size = Vector2(64, 64)
	inventory_grid.add_child(slot)
```

### Dynamic Grid
```gdscript
func update_grid_columns(new_columns: int) -> void:
	grid_container.columns = new_columns
	# Children are automatically rearranged
```

## Notes

- The number of rows is calculated automatically based on the number of children and columns
- All cells have the same size, determined by the largest child's minimum size
- Children fill the grid left-to-right, top-to-bottom
- Empty cells are not rendered but still take up space

## See Also

- HBoxContainer - For single-row horizontal layouts
- VBoxContainer - For single-column vertical layouts
- Container - Base class for all containers
