---
class: Control
category: nodes/ui
description: Base class for all GUI controls with anchors and layout management
godot_version: 4.x
---

# Control

**Inherits:** CanvasItem < Node < Object

Base class for all GUI controls. Adapts its position and size based on its parent control.

## Description

Base class for all UI-related nodes. Control features a bounding rectangle that defines its extents, an anchor position relative to its parent control or the current viewport, and offsets relative to the anchor. The offsets update automatically when the node, any of its parents, or the screen size change.

Godot propagates input events via viewports. Input events are propagated through the SceneTree from the root node to all child nodes. For UI elements specifically, override the virtual method `_gui_input()` which filters out unrelated input events.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `anchor_bottom` | float | 0.0 | Bottom anchor position (0.0 to 1.0) |
| `anchor_left` | float | 0.0 | Left anchor position (0.0 to 1.0) |
| `anchor_right` | float | 0.0 | Right anchor position (0.0 to 1.0) |
| `anchor_top` | float | 0.0 | Top anchor position (0.0 to 1.0) |
| `custom_minimum_size` | Vector2 | Vector2(0, 0) | Minimum size for the control |
| `focus_mode` | FocusMode | 0 | How the control responds to focus |
| `global_position` | Vector2 | - | Global position in the canvas |
| `layout_direction` | LayoutDirection | 0 | Text and control layout direction |
| `mouse_default_cursor_shape` | CursorShape | 0 | Default cursor shape when hovering |
| `mouse_filter` | MouseFilter | 0 | How the control filters mouse events |
| `offset_bottom` | float | 0.0 | Bottom offset from anchor |
| `offset_left` | float | 0.0 | Left offset from anchor |
| `offset_right` | float | 0.0 | Right offset from anchor |
| `offset_top` | float | 0.0 | Top offset from anchor |
| `pivot_offset` | Vector2 | Vector2(0, 0) | Rotation and scaling pivot point |
| `position` | Vector2 | Vector2(0, 0) | Control's position |
| `rotation` | float | 0.0 | Rotation in radians |
| `scale` | Vector2 | Vector2(1, 1) | Control's scale |
| `size` | Vector2 | Vector2(0, 0) | Control's size |
| `size_flags_horizontal` | SizeFlags | 1 | Horizontal sizing flags |
| `size_flags_vertical` | SizeFlags | 1 | Vertical sizing flags |
| `theme` | Theme | null | Theme resource override |
| `tooltip_text` | String | "" | Tooltip text when hovering |

## Key Methods

```gdscript
# Virtual methods
func _gui_input(event: InputEvent) -> void
func _get_minimum_size() -> Vector2
func _has_point(point: Vector2) -> bool

# Focus management
func grab_focus() -> void
func has_focus() -> bool
func release_focus() -> void

# Layout and positioning
func get_combined_minimum_size() -> Vector2
func get_global_rect() -> Rect2
func get_rect() -> Rect2
func set_anchor(side: Side, anchor: float, keep_offset: bool = false,
                 push_opposite_anchor: bool = true) -> void
func set_anchors_preset(preset: LayoutPreset, keep_offsets: bool = false) -> void
func set_position(position: Vector2, keep_offsets: bool = false) -> void
func set_size(size: Vector2, keep_offsets: bool = false) -> void

# Theme management
func add_theme_color_override(name: StringName, color: Color) -> void
func add_theme_font_override(name: StringName, font: Font) -> void
func add_theme_stylebox_override(name: StringName, stylebox: StyleBox) -> void
func get_theme_color(name: StringName, theme_type: StringName = "") -> Color
func get_theme_font(name: StringName, theme_type: StringName = "") -> Font
func get_theme_stylebox(name: StringName, theme_type: StringName = "") -> StyleBox

# Input handling
func accept_event() -> void
func get_cursor_shape(position: Vector2 = Vector2(0, 0)) -> CursorShape
```

## Signals

| Signal | Description |
|--------|-------------|
| `focus_entered()` | Emitted when the node gains focus |
| `focus_exited()` | Emitted when the node loses focus |
| `gui_input(event: InputEvent)` | Emitted when the node receives an InputEvent |
| `minimum_size_changed()` | Emitted when the node's minimum size changes |
| `mouse_entered()` | Emitted when the mouse cursor enters the control's area |
| `mouse_exited()` | Emitted when the mouse cursor leaves the control's area |
| `resized()` | Emitted when the control changes size |
| `theme_changed()` | Emitted when the theme changes |

## Enumerations

### FocusMode
- `FOCUS_NONE` (0): Control cannot gain focus
- `FOCUS_CLICK` (1): Control gains focus when clicked
- `FOCUS_ALL` (2): Control gains focus when clicked or navigated to

### MouseFilter
- `MOUSE_FILTER_STOP` (0): Control stops mouse events
- `MOUSE_FILTER_PASS` (1): Control passes mouse events to parent
- `MOUSE_FILTER_IGNORE` (2): Control ignores all mouse events

### LayoutPreset
- `PRESET_TOP_LEFT` (0)
- `PRESET_TOP_RIGHT` (1)
- `PRESET_BOTTOM_LEFT` (2)
- `PRESET_BOTTOM_RIGHT` (3)
- `PRESET_CENTER_LEFT` (4)
- `PRESET_CENTER_TOP` (5)
- `PRESET_CENTER_RIGHT` (6)
- `PRESET_CENTER_BOTTOM` (7)
- `PRESET_CENTER` (8)
- `PRESET_LEFT_WIDE` (9)
- `PRESET_TOP_WIDE` (10)
- `PRESET_RIGHT_WIDE` (11)
- `PRESET_BOTTOM_WIDE` (12)
- `PRESET_VCENTER_WIDE` (13)
- `PRESET_HCENTER_WIDE` (14)
- `PRESET_FULL_RECT` (15)

## Usage Example

```gdscript
extends Control

func _ready() -> void:
    # Set up anchors for full rect
    set_anchors_preset(PRESET_FULL_RECT)

    # Override theme
    add_theme_color_override("font_color", Color.RED)

    # Connect signals
    mouse_entered.connect(_on_mouse_entered)
    resized.connect(_on_resized)

func _gui_input(event: InputEvent) -> void:
    if event is InputEventMouseButton:
        if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
            print("Clicked at: ", event.position)
            accept_event()  # Prevent further processing

func _on_mouse_entered() -> void:
    mouse_default_cursor_shape = CURSOR_POINTING_HAND

func _on_resized() -> void:
    print("New size: ", size)
```

## Best Practices

1. **Anchor Management**: Use anchors for responsive layouts that adapt to different screen sizes
2. **Theme Overrides**: Prefer theme overrides over direct property modification for consistent styling
3. **Input Handling**: Call `accept_event()` after handling input to prevent event propagation
4. **Focus**: Set appropriate `focus_mode` for keyboard/controller navigation
5. **Mouse Filter**: Use `MOUSE_FILTER_IGNORE` for decorative elements that shouldn't block input

## Common Pitfalls

- Not calling `accept_event()` can cause input to propagate to nodes behind
- Forgetting to set `mouse_filter` on overlapping controls
- Mixing absolute positioning with anchors can cause layout issues
- Theme items are NOT Object properties - use theme methods, not get/set

## Related Classes

- Container - Base for layout containers
- CanvasItem - Parent class with drawing methods
- Theme - Controls visual appearance
