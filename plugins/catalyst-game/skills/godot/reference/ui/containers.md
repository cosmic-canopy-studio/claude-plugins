---
topic: ui-containers
version: 2025.12.21
godot_version: "4.3"
sources:
  - url: "https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html"
    type: official
    priority: 1
  - url: "https://docs.godotengine.org/en/stable/classes/class_boxcontainer.html"
    type: official
    priority: 1
  - url: "https://docs.godotengine.org/en/stable/classes/class_gridcontainer.html"
    type: official
    priority: 1
  - url: "https://docs.godotengine.org/en/stable/classes/class_margincontainer.html"
    type: official
    priority: 1
  - url: "https://school.gdquest.com/courses/learn_2d_gamedev_godot_4/start_a_dialogue/all_the_containers"
    type: community
    priority: 3
  - path: "repos/godot_node_essentials/screens/box_container/"
    type: example
    priority: 2
  - path: "repos/godot_node_essentials/screens/panel_container/"
    type: example
    priority: 2
status: complete
---

# UI Containers

Containers automatically arrange and resize their child Control nodes. Use containers instead of manual positioning for responsive UIs that adapt to different screen sizes.

## Quick Start

```gdscript
# VBoxContainer - vertical list (e.g., menu buttons)
extends VBoxContainer

@onready var _play_button: Button = %PlayButton
@onready var _quit_button: Button = %QuitButton

func _ready() -> void:
    _play_button.pressed.connect(_on_play_pressed)
    _quit_button.pressed.connect(_on_quit_pressed)

# GridContainer - inventory grid
extends Control

@onready var _grid_container: GridContainer = %GridContainer

func _ready() -> void:
    _grid_container.columns = 4
    var items: Array[TextureRect] = []
    items.assign(_grid_container.find_children("", "TextureRect"))
```

## Container Types

### BoxContainer (HBox/VBox)

Arranges children in a single row or column.

```gdscript
# HBoxContainer - horizontal toolbar
extends Control

@onready var _buttons_h_box_container: HBoxContainer = %ButtonsHBoxContainer

func _ready() -> void:
    # Iterate through buttons in horizontal layout
    for button: Button in _buttons_h_box_container.get_children():
        button.pressed.connect(_on_button_pressed.bind(button.text))

func _on_button_pressed(text: String) -> void:
    print("Button pressed: ", text)
```

**Properties:**
- `alignment: AlignmentMode` - How children align (BEGIN, CENTER, END)
- `vertical: bool` - VBoxContainer uses true, HBoxContainer uses false

**Common Uses:**
- Main menu button lists (VBox)
- Toolbar buttons (HBox)
- Split-screen HUD elements (HBox)

### GridContainer

Arranges children in a grid with a specified number of columns.

```gdscript
# Drag-and-drop inventory
extends Control

@onready var _grid_container: GridContainer = %GridContainer

func _ready() -> void:
    _grid_container.columns = 4  # 4 items per row

    # Find all inventory slots
    var slots: Array[TextureRect] = []
    slots.assign(_grid_container.find_children("", "TextureRect"))

    for slot: TextureRect in slots:
        slot.set_drag_forwarding(
            _get_drag_data.bind(slot),
            _can_drop_data,
            _drop_data.bind(slot)
        )

func _get_drag_data(_position: Vector2, slot: TextureRect) -> Texture2D:
    return slot.texture

func _can_drop_data(_position: Vector2, data: Texture2D) -> bool:
    return data != null

func _drop_data(_position: Vector2, data: Texture2D, slot: TextureRect) -> void:
    slot.texture = data
```

**Properties:**
- `columns: int` - Number of columns (rows auto-calculated from child count)

**How it works:**
- Rows = ceil(child_count / columns)
- Children fill left-to-right, top-to-bottom
- Each column width = widest child in that column
- Each row height = tallest child in that row

**Common Uses:**
- Item inventories
- Skill grids
- Turn-based combat action buttons

### MarginContainer

Adds uniform or custom margins around a single child.

```gdscript
# Main menu with margins
extends MarginContainer

@onready var _quit_button: Button = %QuitButton
@onready var _quit_dialog: ConfirmationDialog = %QuitConfirmationDialog

func _ready() -> void:
    # Set margins programmatically
    add_theme_constant_override("margin_left", 50)
    add_theme_constant_override("margin_right", 50)
    add_theme_constant_override("margin_top", 30)
    add_theme_constant_override("margin_bottom", 30)

    _quit_button.pressed.connect(_quit_dialog.popup)
    _quit_dialog.confirmed.connect(_on_quit_confirmed)

func _on_quit_confirmed() -> void:
    get_tree().quit()
```

**Properties:**
- `margin_left`, `margin_right`, `margin_top`, `margin_bottom` (theme constants)

**Common Uses:**
- Screen-edge padding for main menus
- Dialog window borders
- Consistent spacing around content

### PanelContainer

Wraps children in a stylized panel background (from theme).

```gdscript
# Dialog window with panel background
extends Control

@onready var _label: Label = %Label

func _play_dialog() -> void:
    _label.text = "What does all this do? I don't trust it,\ndon't touch anything."
    _label.visible_ratio = 0.0

    var tween := create_tween()
    tween.tween_property(_label, "visible_ratio", 1.0, 2.0)
```

**Common Uses:**
- Dialog boxes
- HUD panels
- Inventory backgrounds
- Windows and frames

### CenterContainer

Centers all children within its bounds.

```gdscript
extends CenterContainer

func _ready() -> void:
    # Child automatically centered
    # No manual positioning needed
```

**Common Uses:**
- Loading screens
- "Game Over" messages
- Centered dialogs

### ScrollContainer

Provides scrolling for content that exceeds container size.

```gdscript
extends ScrollContainer

func _ready() -> void:
    scroll_horizontal_enabled = false
    scroll_vertical_enabled = true
    # Children automatically scrollable
```

**Properties:**
- `scroll_horizontal_enabled: bool`
- `scroll_vertical_enabled: bool`
- `scroll_horizontal: int` - Current horizontal scroll
- `scroll_vertical: int` - Current vertical scroll

**Common Uses:**
- Chat windows
- Long item lists
- Settings menus
- Credits screens

### FlowContainer (HFlow/VFlow)

Wraps children to next line/column when space runs out (like text wrapping).

```gdscript
extends HFlowContainer

func _ready() -> void:
    # Children wrap horizontally when reaching container width
    # Useful for tag clouds or dynamic button lists
    pass
```

**Common Uses:**
- Tag displays
- Dynamic button groups
- Multi-resolution UI that adapts to screen size

### AspectRatioContainer

Maintains child aspect ratio during resizing.

```gdscript
extends AspectRatioContainer

func _ready() -> void:
    ratio = 16.0 / 9.0  # Widescreen aspect ratio
    stretch_mode = STRETCH_FIT
```

**Properties:**
- `ratio: float` - Width/height ratio (1.0 = square, 1.778 = 16:9)
- `stretch_mode: StretchMode` - How to fit child (FIT, COVER, WIDTH_CONTROLS_HEIGHT, HEIGHT_CONTROLS_WIDTH)

**Common Uses:**
- Video players
- Camera viewports
- Images that must maintain proportions

## Size Flags

Control how children behave within containers.

### Overview

Size flags determine:
1. Should the child fill available space? (FILL)
2. Should the child request extra space? (EXPAND)
3. How to position the child if not filling? (SHRINK_CENTER, SHRINK_END)

### FILL

Child fills the space allocated to it.

```gdscript
extends Control

func _ready() -> void:
    # Fill horizontally within container
    size_flags_horizontal = Control.SIZE_FILL
    # Fill vertically within container
    size_flags_vertical = Control.SIZE_FILL
```

### EXPAND

Child requests additional available space in the container.

```gdscript
extends HBoxContainer

func _ready() -> void:
    # Make all buttons share horizontal space equally
    for button: Button in get_children():
        button.size_flags_horizontal = Control.SIZE_EXPAND | Control.SIZE_FILL
```

**Important:** EXPAND doesn't resize the child - it allocates space. Combine with FILL to actually fill that space.

### EXPAND_FILL (Common Pattern)

```gdscript
# Most common: expand AND fill
button.size_flags_horizontal = Control.SIZE_EXPAND_FILL  # Shorthand for EXPAND | FILL
```

### SHRINK_CENTER

Child uses minimum size and centers within allocated space.

```gdscript
extends Control

func _ready() -> void:
    size_flags_horizontal = Control.SIZE_SHRINK_CENTER
    # Child centers itself, doesn't expand or fill
```

**Note:** Mutually exclusive with FILL and EXPAND.

### SHRINK_END

Child uses minimum size and aligns to end (right/bottom).

```gdscript
extends Control

func _ready() -> void:
    size_flags_horizontal = Control.SIZE_SHRINK_END
    # Child aligns to right edge
```

**Note:** Mutually exclusive with FILL and EXPAND.

### Default Behavior

No flags set = "SHRINK_BEGIN" - child uses minimum size, aligns to start (left/top).

## Separation & Spacing

### Container Separation

```gdscript
extends VBoxContainer

func _ready() -> void:
    # Add spacing between children
    add_theme_constant_override("separation", 10)
```

### BoxContainer add_spacer()

```gdscript
extends HBoxContainer

func _ready() -> void:
    var button1 := Button.new()
    add_child(button1)

    # Add flexible spacer between buttons
    add_spacer(false)  # false = flexible spacer

    var button2 := Button.new()
    add_child(button2)

    # Result: button1 | <---space---> | button2
```

## Common Patterns

### Main Menu Layout

```gdscript
# Structure: MarginContainer > VBoxContainer > Buttons
extends MarginContainer

@onready var _buttons_v_box: VBoxContainer = %ButtonsVBoxContainer

func _ready() -> void:
    # Margins provide screen-edge spacing
    add_theme_constant_override("margin_left", 100)
    add_theme_constant_override("margin_right", 100)
    add_theme_constant_override("margin_top", 80)
    add_theme_constant_override("margin_bottom", 80)

    # VBox arranges buttons vertically
    _buttons_v_box.add_theme_constant_override("separation", 15)

    for button: Button in _buttons_v_box.get_children():
        button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
```

### Split-Screen HUD

```gdscript
# HBoxContainer with two panels
extends Control

var _score: int = 0:
    set(value):
        _score = value
        _score_label.text = "%07d" % _score

@onready var _score_label: Label = %ScoreLabel
@onready var _health_bar: ProgressBar = %HealthProgressBar

func _ready() -> void:
    # Two children in HBox split screen horizontally
    pass
```

### Level Editor Toolbar

```gdscript
extends Node2D

@onready var _buttons_h_box_container: HBoxContainer = %ButtonsHBoxContainer
@onready var _mouse_cursor: Sprite2D = %MouseCursor

enum Modes { ERASE, PAINT }
var _current_mode: Modes = Modes.PAINT

func _ready() -> void:
    # Connect all toolbar buttons
    for button: Button in _buttons_h_box_container.get_children():
        button.pressed.connect(_update_mode.bind(button.text))

func _update_mode(key: String) -> void:
    _current_mode = Modes[key.to_upper()]
```

### Inventory Grid with Drag-Drop

```gdscript
extends Control

var _last_dragged_item: TextureRect

@onready var _grid_container: GridContainer = %GridContainer

func _ready() -> void:
    _grid_container.columns = 4

    var slots: Array[TextureRect] = []
    slots.assign(_grid_container.find_children("", "TextureRect"))

    for slot: TextureRect in slots:
        slot.set_drag_forwarding(
            _get_drag_data.bind(slot),
            _can_drop_data,
            _drop_data.bind(slot)
        )

func _get_drag_data(_position: Vector2, source: TextureRect) -> Texture2D:
    _last_dragged_item = source
    var texture: Texture2D = source.texture
    source.texture = null
    return texture

func _can_drop_data(_position: Vector2, data: Texture2D) -> bool:
    return data != null

func _drop_data(_position: Vector2, data: Texture2D, target: TextureRect) -> void:
    # Swap items if target slot occupied
    if target.texture != null:
        _last_dragged_item.texture = target.texture
    target.texture = data
```

## Best Practices

### Use Containers for Responsive Design

```gdscript
# Bad - hardcoded positions break on different screen sizes
button.position = Vector2(100, 200)

# Good - containers adapt automatically
extends VBoxContainer
# Children auto-positioned
```

### Combine Containers for Complex Layouts

```gdscript
# Structure:
# MarginContainer (screen padding)
#   └─ VBoxContainer (vertical layout)
#       ├─ HBoxContainer (top bar)
#       │   ├─ Label (score)
#       │   └─ ProgressBar (health)
#       └─ GridContainer (main content)
```

### Set Minimum Sizes

```gdscript
extends Button

func _ready() -> void:
    custom_minimum_size = Vector2(200, 50)
    size_flags_horizontal = Control.SIZE_EXPAND_FILL
    # Button expands but never smaller than 200x50
```

### Don't Animate Container Children Directly

```gdscript
# Bad - container overrides child position
var tween := create_tween()
tween.tween_property(child_button, "position", Vector2(100, 0), 1.0)
# Won't work - container resets position

# Good - wrap in Control node
# Structure: Container > Control > Button (animate Control)
var tween := create_tween()
tween.tween_property(wrapper_control, "position", Vector2(100, 0), 1.0)
```

## Common Pitfalls

### EXPAND Without FILL

```gdscript
# Common mistake: expand but not fill
button.size_flags_horizontal = Control.SIZE_EXPAND
# Button requests space but doesn't fill it - appears small

# Fix: combine with FILL
button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
```

### Conflicting Size Flags

```gdscript
# Bad - SHRINK_CENTER conflicts with FILL
control.size_flags_horizontal = Control.SIZE_SHRINK_CENTER | Control.SIZE_FILL
# SHRINK_CENTER will override FILL

# Good - use one or the other
control.size_flags_horizontal = Control.SIZE_SHRINK_CENTER  # Centered, min size
# OR
control.size_flags_horizontal = Control.SIZE_FILL  # Fills space
```

### GridContainer with No Columns Set

```gdscript
# Bad - defaults to 1 column (acts like VBoxContainer)
var grid := GridContainer.new()
add_child(grid)

# Good - set columns
var grid := GridContainer.new()
grid.columns = 4
add_child(grid)
```

### Forgetting ScrollContainer Limits

```gdscript
# ScrollContainer only scrolls if child exceeds container size
# Ensure child has proper minimum size or content
extends ScrollContainer

func _ready() -> void:
    var content := VBoxContainer.new()
    content.custom_minimum_size = Vector2(0, 1000)  # Tall enough to scroll
    add_child(content)
```

## Quick Reference

| Container | Use Case | Key Property |
|-----------|----------|--------------|
| HBoxContainer | Horizontal lists, toolbars | `alignment` |
| VBoxContainer | Vertical menus, lists | `alignment` |
| GridContainer | Inventories, skill grids | `columns` |
| MarginContainer | Screen padding, borders | `margin_*` |
| PanelContainer | Styled backgrounds | Inherits panel theme |
| CenterContainer | Centered content | Auto-centers |
| ScrollContainer | Long content | `scroll_*_enabled` |
| FlowContainer | Wrapping content | Wraps like text |
| AspectRatioContainer | Fixed proportions | `ratio`, `stretch_mode` |

| Size Flag | Effect |
|-----------|--------|
| `SIZE_FILL` | Fill allocated space |
| `SIZE_EXPAND` | Request additional space |
| `SIZE_EXPAND_FILL` | Request space AND fill it |
| `SIZE_SHRINK_CENTER` | Min size, centered |
| `SIZE_SHRINK_END` | Min size, end-aligned |
| None | Min size, start-aligned |

## Related

- [Controls Reference](controls.md) - Base Control node properties
- [Themes Reference](themes.md) - Styling containers
- [Signals Reference](../language/signals.md) - Container event handling
