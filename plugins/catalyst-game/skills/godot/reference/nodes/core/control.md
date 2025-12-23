---
class: Control
source: repos/godot-docs/classes/class_control.rst
generated: 2025-12-21
---

# Control

**Inherits:** CanvasItem < Node < Object

**Inherited By:** BaseButton, ColorRect, Container, GraphEdit, ItemList, Label, LineEdit, MenuBar, NinePatchRect, Panel, Range, ReferenceRect, RichTextLabel, Separator, TabBar, TextEdit, TextureRect, Tree, VideoStreamPlayer

Base class for all GUI controls. Adapts its position and size based on its parent control.

## Description

Base class for all UI-related nodes. Control features a bounding rectangle that defines its extents, an anchor position relative to its parent control or the current viewport, and offsets relative to the anchor. The offsets update automatically when the node, any of its parents, or the screen size change.

For more information on Godot's UI system, anchors, offsets, and containers, see the related tutorials in the manual. To build flexible UIs, you'll need a mix of UI elements that inherit from Control and Container nodes.

**Note:** Since both Node2D and Control inherit from CanvasItem, they share several concepts from the class such as the `z_index` and `visible` properties.

## User Interface Nodes and Input

Godot propagates input events via viewports. Each Viewport is responsible for propagating InputEvents to their child nodes. As the SceneTree.root is a Window, this already happens automatically for all UI elements in your game.

Input events are propagated through the SceneTree from the root node to all child nodes by calling `Node._input()`. For UI elements specifically, it makes more sense to override the virtual method `_gui_input()`, which filters out unrelated input events, such as by checking z-order, `mouse_filter`, focus, or if the event was inside of the control's bounding box.

Call `accept_event()` so no other node receives the event. Once you accept an input, it becomes handled so `Node._unhandled_input()` will not process it.

Only one Control node can be in focus. Only the node in focus will receive events. To get the focus, call `grab_focus()`. Control nodes lose focus when another node grabs it, or if you hide the node in focus.

Sets `mouse_filter` to MOUSE_FILTER_IGNORE to tell a Control node to ignore mouse or touch events. You'll need it if you place an icon on top of a button.

## Theme Resources

Theme resources change the control's appearance. The theme of a Control node affects all of its direct and indirect children (as long as a chain of controls is uninterrupted). To override some of the theme items, call one of the `add_theme_*_override` methods, like `add_theme_font_override()`. You can also override theme items in the Inspector.

**Note:** Theme items are *not* Object properties. This means you can't access their values using `Object.get()` and `Object.set()`. Instead, use the `get_theme_*` and `add_theme_*_override` methods provided by this class.

## Key Properties

| Type | Property | Default |
|------|----------|---------|
| bool | clip_contents | false |
| CursorShape | default_cursor_shape | 0 |
| FocusMode | focus_mode | 0 |
| NodePath | focus_neighbor_bottom | NodePath("") |
| NodePath | focus_neighbor_left | NodePath("") |
| NodePath | focus_neighbor_right | NodePath("") |
| NodePath | focus_neighbor_top | NodePath("") |
| NodePath | focus_next | NodePath("") |
| NodePath | focus_previous | NodePath("") |
| GrowDirection | grow_horizontal | 1 |
| GrowDirection | grow_vertical | 1 |
| LayoutDirection | layout_direction | 0 |
| LayoutMode | layout_mode | 0 |
| MouseFilter | mouse_filter | 0 |
| bool | mouse_force_pass_scroll_events | true |
| Vector2 | pivot_offset | Vector2(0, 0) |
| Vector2 | position | Vector2(0, 0) |
| Vector2 | size | Vector2(0, 0) |
| Theme | theme | |
| String | theme_type_variation | "" |
| String | tooltip_text | "" |

## Common Methods

| Return Type | Method |
|-------------|--------|
| void | `_gui_input(event: InputEvent)` virtual |
| void | `accept_event()` |
| void | `add_theme_color_override(name: StringName, color: Color)` |
| void | `add_theme_constant_override(name: StringName, constant: int)` |
| void | `add_theme_font_override(name: StringName, font: Font)` |
| void | `add_theme_font_size_override(name: StringName, font_size: int)` |
| void | `add_theme_icon_override(name: StringName, texture: Texture2D)` |
| void | `add_theme_stylebox_override(name: StringName, stylebox: StyleBox)` |
| Color | `get_theme_color(name: StringName, theme_type: StringName = &"")` const |
| int | `get_theme_constant(name: StringName, theme_type: StringName = &"")` const |
| Font | `get_theme_font(name: StringName, theme_type: StringName = &"")` const |
| int | `get_theme_font_size(name: StringName, theme_type: StringName = &"")` const |
| Texture2D | `get_theme_icon(name: StringName, theme_type: StringName = &"")` const |
| StyleBox | `get_theme_stylebox(name: StringName, theme_type: StringName = &"")` const |
| void | `grab_click_focus()` |
| void | `grab_focus()` |
| bool | `has_focus()` const |
| void | `release_focus()` |
| void | `set_anchors_preset(preset: LayoutPreset, keep_offsets: bool = false)` |
| void | `set_offsets_preset(preset: LayoutPreset, resize_mode: LayoutPresetMode = 0, margin: int = 0)` |
| void | `warp_mouse(position: Vector2)` |

## Signals

- **focus_entered**()
  - Emitted when the node gains focus

- **focus_exited**()
  - Emitted when the node loses focus

- **gui_input**(event: InputEvent)
  - Emitted when the node receives an InputEvent

- **minimum_size_changed**()
  - Emitted when the node's minimum size changes

- **mouse_entered**()
  - Emitted when the mouse cursor enters the control's bounding rectangle

- **mouse_exited**()
  - Emitted when the mouse cursor leaves the control's bounding rectangle

- **resized**()
  - Emitted when the control's size changes

- **size_flags_changed**()
  - Emitted when the size flags change

- **theme_changed**()
  - Emitted when the theme changes

## Key Concepts

### Input Handling

- Override `_gui_input()` for UI-specific input handling (automatically filtered)
- Call `accept_event()` to mark input as handled and stop propagation
- Use `mouse_filter` to control whether the control receives mouse events
- Set to MOUSE_FILTER_IGNORE for decorative elements (icons on buttons)

### Focus System

- Only one Control can have focus at a time
- Focused control receives keyboard input
- Use `grab_focus()` to take focus
- Configure focus navigation with `focus_neighbor_*` and `focus_next`/`focus_previous`
- Hide a control to release its focus

### Anchors and Offsets

- Controls adapt position/size based on parent control or viewport
- Anchors define attachment points (0.0 = left/top, 1.0 = right/bottom)
- Offsets are the distance from the anchor points
- Use `set_anchors_preset()` for common layouts (PRESET_FULL_RECT, etc.)

### Theme System

- Themes cascade: parent themes affect children
- Override specific theme items with `add_theme_*_override()` methods
- Theme items are NOT Object properties - use special getters/setters
- Theme changes propagate automatically to children

## Best Practices

- Use `_gui_input()` instead of `_input()` for UI controls - it's automatically filtered
- Call `accept_event()` when you handle an input to prevent it from propagating
- Set `mouse_filter = MOUSE_FILTER_IGNORE` for decorative overlay elements
- Use focus neighbors to create keyboard navigation flows
- Override theme items in code rather than duplicating entire themes
- Let Container nodes handle child sizing - don't fight the layout system

## Anti-Patterns

- Don't use `Object.get()`/`Object.set()` for theme items - they're not properties
- Don't manually position children inside Container nodes - use size flags instead
- Don't override `_input()` for UI controls - use `_gui_input()`
- Don't forget to call `accept_event()` - you'll get event leaks to background nodes

## Common Patterns

```gdscript
# Custom input handling
extends Control

func _gui_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        if event.button_index == MOUSE_BUTTON_LEFT:
            print("Left click at: ", event.position)
            accept_event()  # Stop propagation
```

```gdscript
# Theme customization
extends Button

func _ready() -> void:
    # Override specific theme items
    add_theme_color_override("font_color", Color.RED)
    add_theme_font_size_override("font_size", 24)
```

```gdscript
# Focus management
extends Control

func _ready() -> void:
    # Set up focus neighbors for keyboard navigation
    $Button1.focus_neighbor_right = $Button2.get_path()
    $Button2.focus_neighbor_left = $Button1.get_path()
    $Button2.focus_neighbor_right = $Button3.get_path()

    # Give initial focus
    $Button1.grab_focus()
```

```gdscript
# Mouse filter for overlay icons
extends TextureRect

func _ready() -> void:
    # This icon sits on top of a button but doesn't block clicks
    mouse_filter = Control.MOUSE_FILTER_IGNORE
```

```gdscript
# Anchor presets for responsive UI
extends Control

func _ready() -> void:
    # Fill entire parent
    set_anchors_preset(Control.PRESET_FULL_RECT)

    # Center with fixed size
    set_anchors_preset(Control.PRESET_CENTER)
    size = Vector2(400, 300)
```
