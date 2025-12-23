---
topic: ui-themes
version: 2025.12.21
godot_version: "4.3"
sources:
  - godot_node_essentials/addons/gdquest_theme_utils
  - official-docs
  - community-tutorials
---

# UI Themes

Theme resources provide consistent styling for Control nodes across your UI.

## Quick Start

```gdscript
# Apply theme to entire UI tree
extends Control

func _ready() -> void:
    theme = preload("res://ui/my_theme.tres")
```

## Theme Resource Basics

Create a Theme resource (`.tres`) to define global UI styles:

```gdscript
# Create theme programmatically
var custom_theme := Theme.new()

# Set default font
custom_theme.default_font = preload("res://fonts/game_font.ttf")
custom_theme.default_font_size = 16

# Apply to control
my_control.theme = custom_theme
```

## StyleBox Types

### StyleBoxFlat

Most common - draws solid colors with borders and rounded corners:

```gdscript
var style := StyleBoxFlat.new()
style.bg_color = Color(0.2, 0.16, 0.28)  # Background
style.border_color = Color(0.3, 0.65, 1.0)  # Border
style.border_width_left = 3
style.border_width_top = 3
style.border_width_right = 3
style.border_width_bottom = 3
style.corner_radius_top_left = 8
style.corner_radius_top_right = 8
style.corner_radius_bottom_left = 8
style.corner_radius_bottom_right = 8
style.content_margin_left = 20.0  # Internal padding

# Apply to button
var theme := Theme.new()
theme.set_stylebox("normal", "Button", style)
```

### StyleBoxTexture

Uses textures with 9-slice scaling:

```gdscript
var style := StyleBoxTexture.new()
style.texture = preload("res://ui/button.png")
style.texture_margin_left = 23.0
style.texture_margin_top = 23.0
style.texture_margin_right = 23.0
style.texture_margin_bottom = 36.0
style.region_rect = Rect2(0, 0, 199, 128)
style.modulate_color = Color(0.55, 0.59, 0.76)

# Add padding
style.content_margin_left = 10.0
style.content_margin_right = 10.0
```

### StyleBoxEmpty

Transparent - useful for removing default styling:

```gdscript
var empty_style := StyleBoxEmpty.new()
theme.set_stylebox("panel", "Panel", empty_style)
```

## Theme Overrides

Override theme properties on individual controls without affecting others:

### Color Overrides

```gdscript
extends Button

func _ready() -> void:
    # Change font color
    add_theme_color_override("font_color", Color.WHITE)
    add_theme_color_override("font_hover_color", Color.YELLOW)
    add_theme_color_override("font_pressed_color", Color.GRAY)
```

### Font Overrides

```gdscript
extends Label

func _ready() -> void:
    var custom_font := preload("res://fonts/title.ttf")
    add_theme_font_override("font", custom_font)
    add_theme_font_size_override("font_size", 32)
```

### StyleBox Overrides

```gdscript
extends LineEdit

const STYLE_FOCUS := preload("res://ui/lineedit_focus.tres")
const STYLE_ERROR := preload("res://ui/lineedit_error.tres")

func _ready() -> void:
    text_changed.connect(_on_text_changed)

func _on_text_changed(new_text: String) -> void:
    var is_valid := _validate_email(new_text)
    var style := STYLE_FOCUS if is_valid else STYLE_ERROR
    add_theme_stylebox_override("focus", style)
```

### Constant Overrides

```gdscript
extends MarginContainer

func _ready() -> void:
    # Override margin constants
    add_theme_constant_override("margin_left", 20)
    add_theme_constant_override("margin_right", 20)
    add_theme_constant_override("margin_top", 10)
    add_theme_constant_override("margin_bottom", 10)
```

## Theme Type Variations

Create variations of base Control types for different styles:

### Creating Type Variations

```gdscript
# In theme editor or programmatically
var theme := Theme.new()

# Base Button style
var base_button := StyleBoxFlat.new()
base_button.bg_color = Color.GRAY
theme.set_stylebox("normal", "Button", base_button)

# Confirm Button variation (green)
var confirm_style := StyleBoxFlat.new()
confirm_style.bg_color = Color.GREEN
theme.set_stylebox("normal", "ConfirmButton", confirm_style)
theme.set_type_variation("ConfirmButton", "Button")

# Cancel Button variation (red)
var cancel_style := StyleBoxFlat.new()
cancel_style.bg_color = Color.RED
theme.set_stylebox("normal", "CancelButton", cancel_style)
theme.set_type_variation("CancelButton", "Button")
```

### Applying Type Variations

```gdscript
extends Button

func _ready() -> void:
    # Set in inspector or code
    theme_type_variation = "ConfirmButton"
```

Scene structure:
```
HBoxContainer
├── Button (theme_type_variation = "ConfirmButton")
│   └── text = "Accept"
└── Button (theme_type_variation = "CancelButton")
    └── text = "Cancel"
```

## Getting Theme Properties

```gdscript
extends Control

func _ready() -> void:
    # Get theme color
    var font_color: Color = get_theme_color("font_color", "Label")

    # Get theme font
    var font: Font = get_theme_font("font", "Button")
    var font_size: int = get_theme_font_size("font_size", "Button")

    # Get theme stylebox
    var panel_style: StyleBox = get_theme_stylebox("panel", "Panel")

    # Get theme constant
    var margin: int = get_theme_constant("margin_left", "MarginContainer")

    # Check if theme property exists
    if has_theme_color("font_color", "Label"):
        print("Theme has font_color defined")
```

## Programmatic Theme Creation

```gdscript
# autoloads/theme_manager.gd
extends Node

var game_theme: Theme

func _ready() -> void:
    game_theme = _create_game_theme()

func _create_game_theme() -> Theme:
    var theme := Theme.new()

    # Set default font
    theme.default_font = preload("res://fonts/game_font.ttf")
    theme.default_font_size = 16

    # Button styles
    _setup_button_styles(theme)

    # Panel styles
    _setup_panel_styles(theme)

    # Label colors
    theme.set_color("font_color", "Label", Color.WHITE)

    return theme

func _setup_button_styles(theme: Theme) -> void:
    # Normal state
    var normal := StyleBoxFlat.new()
    normal.bg_color = Color(0.2, 0.2, 0.3)
    normal.corner_radius_top_left = 4
    normal.corner_radius_top_right = 4
    normal.corner_radius_bottom_left = 4
    normal.corner_radius_bottom_right = 4
    normal.content_margin_left = 16.0
    normal.content_margin_right = 16.0
    normal.content_margin_top = 8.0
    normal.content_margin_bottom = 8.0
    theme.set_stylebox("normal", "Button", normal)

    # Hover state
    var hover := normal.duplicate()
    hover.bg_color = Color(0.3, 0.3, 0.4)
    theme.set_stylebox("hover", "Button", hover)

    # Pressed state
    var pressed := normal.duplicate()
    pressed.bg_color = Color(0.15, 0.15, 0.25)
    theme.set_stylebox("pressed", "Button", pressed)

    # Font colors
    theme.set_color("font_color", "Button", Color.WHITE)
    theme.set_color("font_hover_color", "Button", Color(1, 1, 0.8))
    theme.set_color("font_pressed_color", "Button", Color(0.8, 0.8, 0.8))

func _setup_panel_styles(theme: Theme) -> void:
    var panel := StyleBoxFlat.new()
    panel.bg_color = Color(0.1, 0.1, 0.15, 0.9)
    panel.border_color = Color(0.3, 0.3, 0.4)
    panel.border_width_left = 2
    panel.border_width_top = 2
    panel.border_width_right = 2
    panel.border_width_bottom = 2
    panel.corner_radius_top_left = 8
    panel.corner_radius_top_right = 8
    panel.corner_radius_bottom_left = 8
    panel.corner_radius_bottom_right = 8
    theme.set_stylebox("panel", "Panel", panel)
```

## Scaling Themes for Editor

When creating editor plugins, scale theme properties for different editor scales:

```gdscript
extends Control

func _ready() -> void:
    if Engine.is_editor_hint():
        _scale_theme_for_editor()

func _scale_theme_for_editor() -> void:
    var editor_scale := EditorInterface.get_editor_scale()

    # Scale font size
    var font_size: int = get_theme_font_size("font_size")
    add_theme_font_size_override("font_size", font_size * editor_scale)

    # Scale margins
    var margin: int = get_theme_constant("margin_left")
    add_theme_constant_override("margin_left", margin * editor_scale)
```

### Comprehensive Theme Scaling

```gdscript
static func generate_scaled_theme(theme_resource: Theme) -> Theme:
    var new_theme := theme_resource.duplicate(true)
    var editor_scale := EditorInterface.get_editor_scale()

    # Scale font sizes
    new_theme.default_font_size = new_theme.default_font_size * editor_scale
    for theme_type in new_theme.get_font_size_type_list():
        for font_size_property in new_theme.get_font_size_list(theme_type):
            var font_size: int = new_theme.get_font_size(font_size_property, theme_type)
            new_theme.set_font_size(font_size_property, theme_type, font_size * editor_scale)

    # Scale constants (margins, spacing, etc.)
    for theme_type in new_theme.get_constant_type_list():
        for constant in new_theme.get_constant_list(theme_type):
            var constant_value: int = new_theme.get_constant(constant, theme_type)
            new_theme.set_constant(theme_type, constant, constant_value * editor_scale)

    # Scale StyleBox properties
    for stylebox_type in new_theme.get_stylebox_type_list():
        for stylebox_name in new_theme.get_stylebox_list(stylebox_type):
            var stylebox: StyleBox = new_theme.get_stylebox(stylebox_name, stylebox_type)

            if stylebox is StyleBoxFlat:
                # Scale borders
                stylebox.border_width_left *= editor_scale
                stylebox.border_width_right *= editor_scale
                stylebox.border_width_top *= editor_scale
                stylebox.border_width_bottom *= editor_scale

                # Scale corner radius
                stylebox.corner_radius_top_left *= editor_scale
                stylebox.corner_radius_top_right *= editor_scale
                stylebox.corner_radius_bottom_left *= editor_scale
                stylebox.corner_radius_bottom_right *= editor_scale

                # Scale shadow
                stylebox.shadow_offset *= editor_scale
                stylebox.shadow_size *= editor_scale

            if stylebox is StyleBoxFlat or stylebox is StyleBoxTexture:
                # Scale margins
                stylebox.content_margin_left *= editor_scale
                stylebox.content_margin_right *= editor_scale
                stylebox.content_margin_top *= editor_scale
                stylebox.content_margin_bottom *= editor_scale

                stylebox.expand_margin_left *= editor_scale
                stylebox.expand_margin_right *= editor_scale
                stylebox.expand_margin_top *= editor_scale
                stylebox.expand_margin_bottom *= editor_scale

    return new_theme
```

## Common Theme Properties

### Button

| Property Type | Name | Description |
|--------------|------|-------------|
| StyleBox | `normal` | Default appearance |
| StyleBox | `hover` | Mouse hover state |
| StyleBox | `pressed` | Clicked state |
| StyleBox | `disabled` | Disabled appearance |
| StyleBox | `focus` | Keyboard focus outline |
| Color | `font_color` | Default text color |
| Color | `font_hover_color` | Hover text color |
| Color | `font_pressed_color` | Pressed text color |
| Color | `font_disabled_color` | Disabled text color |
| Font | `font` | Text font |
| int | `font_size` | Text size |

### Label

| Property Type | Name | Description |
|--------------|------|-------------|
| Color | `font_color` | Text color |
| Color | `font_shadow_color` | Shadow color |
| Font | `font` | Text font |
| int | `font_size` | Text size |
| int | `line_spacing` | Space between lines |
| int | `shadow_offset_x` | Shadow X offset |
| int | `shadow_offset_y` | Shadow Y offset |

### LineEdit

| Property Type | Name | Description |
|--------------|------|-------------|
| StyleBox | `normal` | Default background |
| StyleBox | `focus` | Focused state |
| StyleBox | `read_only` | Read-only appearance |
| Color | `font_color` | Text color |
| Color | `font_placeholder_color` | Placeholder color |
| Color | `caret_color` | Cursor color |
| Color | `selection_color` | Selection highlight |

### Panel

| Property Type | Name | Description |
|--------------|------|-------------|
| StyleBox | `panel` | Background appearance |

## Best Practices

### Theme Organization

```gdscript
# Good - centralized theme management
res://ui/
├── themes/
│   ├── main_theme.tres
│   ├── styles/
│   │   ├── button_normal.tres
│   │   ├── button_hover.tres
│   │   └── panel_dark.tres
│   └── fonts/
│       ├── title_font.ttf
│       └── body_font.ttf
```

### Avoid Inline Overrides

```gdscript
# Bad - hard to maintain
func _ready() -> void:
    add_theme_color_override("font_color", Color(0.8, 0.2, 0.1))
    add_theme_font_size_override("font_size", 24)

# Good - use theme variations
func _ready() -> void:
    theme_type_variation = "TitleLabel"
```

### Performance: Bulk Theme Overrides

```gdscript
func _ready() -> void:
    # Start bulk override session
    begin_bulk_theme_override()

    # Make multiple changes
    add_theme_color_override("font_color", Color.RED)
    add_theme_font_size_override("font_size", 20)
    add_theme_constant_override("margin_left", 10)

    # End session - theme recompiles once
    end_bulk_theme_override()
```

## Common Pitfalls

### Theme Override Priority

```gdscript
# Theme overrides take precedence over theme resources
# This will NOT change color if override is set:
theme = custom_theme  # Has font_color = WHITE
add_theme_color_override("font_color", Color.RED)  # This wins
```

### Clear Overrides

```gdscript
# Remove specific override
remove_theme_color_override("font_color")

# Or check before getting
if has_theme_color("font_color"):
    var color := get_theme_color("font_color")
```

### Missing Theme Properties

```gdscript
# Bad - may crash if theme missing
var color := get_theme_color("font_color", "Button")

# Good - check first
if has_theme_color("font_color", "Button"):
    var color := get_theme_color("font_color", "Button")
else:
    var color := Color.WHITE  # Fallback
```

## Dynamic Theme Switching

```gdscript
# autoloads/theme_manager.gd
extends Node

var light_theme: Theme = preload("res://ui/themes/light.tres")
var dark_theme: Theme = preload("res://ui/themes/dark.tres")

var current_theme: Theme = dark_theme

signal theme_changed(new_theme: Theme)

func toggle_theme() -> void:
    if current_theme == dark_theme:
        current_theme = light_theme
    else:
        current_theme = dark_theme

    theme_changed.emit(current_theme)

# In UI root
func _ready() -> void:
    ThemeManager.theme_changed.connect(_on_theme_changed)
    theme = ThemeManager.current_theme

func _on_theme_changed(new_theme: Theme) -> void:
    theme = new_theme
```

## Related Patterns

- [UI Controls](controls.md) - Controls that use themes
- [UI Containers](containers.md) - Layout with themed panels
- [Resources](../patterns/resources.md) - Theme as Resource type

## Sources

1. **Official Godot Docs**: [Theme Class](https://docs.godotengine.org/en/stable/classes/class_theme.html)
2. **Official Godot Docs**: [StyleBoxFlat](https://docs.godotengine.org/en/stable/classes/class_styleboxflat.html)
3. **Official Godot Docs**: [StyleBoxTexture](https://docs.godotengine.org/en/stable/classes/class_styleboxtexture.html)
4. **Official Godot Docs**: [Theme Type Variations](https://docs.godotengine.org/en/stable/tutorials/ui/gui_theme_type_variations.html)
5. **Official Godot Docs**: [Using the Theme Editor](https://docs.godotengine.org/en/stable/tutorials/ui/gui_using_theme_editor.html)
6. **Example Repository**: godot_node_essentials - Theme utilities and StyleBox examples
7. **GDQuest**: [Making the Most of the Theme Editor](https://school.gdquest.com/courses/learn_2d_gamedev_godot_4/telling_a_story/all_theme_editor_areas)
