---
class: Button
category: nodes/ui/buttons
description: A themed button that can contain text and an icon
godot_version: 4.x
---

# Button

**Inherits:** BaseButton < Control < CanvasItem < Node < Object

A themed button that can contain text and an icon.

## Description

Button is the standard themed button. It can contain text and an icon, and it will display them according to the current Theme.

Buttons do not detect touch input and therefore don't support multitouch, since mouse emulation can only press one button at a given time. Use TouchScreenButton for buttons that trigger gameplay movement or actions.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `alignment` | HorizontalAlignment | 1 (CENTER) | Text alignment policy |
| `autowrap_mode` | AutowrapMode | 0 (OFF) | Text wrapping mode |
| `clip_text` | bool | false | Clip text that exceeds button width |
| `expand_icon` | bool | false | Scale icon to fit button size |
| `flat` | bool | false | Remove button decoration |
| `icon` | Texture2D | null | Button icon texture |
| `icon_alignment` | HorizontalAlignment | 0 (LEFT) | Icon horizontal alignment |
| `language` | String | "" | Language code for text shaping |
| `text` | String | "" | Button's text content |
| `text_direction` | TextDirection | 0 (AUTO) | Base text writing direction |
| `text_overrun_behavior` | OverrunBehavior | 0 (TRIM_NOTHING) | Text clipping behavior |
| `vertical_icon_alignment` | VerticalAlignment | 1 (CENTER) | Icon vertical alignment |

## Inherited Properties (BaseButton)

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `disabled` | bool | false | If true, button is disabled and won't respond to input |
| `button_pressed` | bool | false | If true, button is in pressed state |
| `toggle_mode` | bool | false | If true, button toggles between pressed and unpressed |
| `action_mode` | ActionMode | 1 (RELEASE) | When the button emits pressed signal |
| `keep_pressed_outside` | bool | false | Stay pressed when cursor moves outside |

## Key Methods

```gdscript
# Inherited from BaseButton
func set_pressed_no_signal(pressed: bool) -> void
func is_hovered() -> bool
```

## Signals (from BaseButton)

| Signal | Description |
|--------|-------------|
| `pressed()` | Emitted when the button is pressed (toggled on or clicked) |
| `button_down()` | Emitted when button is pressed down |
| `button_up()` | Emitted when button is released |
| `toggled(toggled_on: bool)` | Emitted when button's toggle state changes |

## Theme Properties

### Colors
- `font_color`: Default text color
- `font_disabled_color`: Text color when disabled
- `font_focus_color`: Text color when focused
- `font_hover_color`: Text color when hovered
- `font_hover_pressed_color`: Text color when hovered and pressed
- `font_pressed_color`: Text color when pressed
- `icon_normal_color`: Default icon modulate color
- `icon_disabled_color`: Icon color when disabled
- `icon_hover_color`: Icon color when hovered
- `icon_pressed_color`: Icon color when pressed

### Constants
- `h_separation`: Space between icon and text (default: 4)
- `icon_max_width`: Maximum icon width (default: 0 = unlimited)
- `outline_size`: Text outline size (default: 0)

### Styles
- `normal`: Default button style
- `hover`: Style when hovered
- `pressed`: Style when pressed
- `disabled`: Style when disabled
- `focus`: Style when focused (overlaid on base style)

## Usage Example

```gdscript
extends Node

func _ready() -> void:
    var button := Button.new()
    button.text = "Click me"
    button.pressed.connect(_on_button_pressed)
    add_child(button)

    # With icon
    var icon_button := Button.new()
    icon_button.text = "Save"
    icon_button.icon = preload("res://icons/save.png")
    icon_button.icon_alignment = HORIZONTAL_ALIGNMENT_RIGHT
    icon_button.pressed.connect(_on_save_pressed)
    add_child(icon_button)

    # Toggle button
    var toggle := Button.new()
    toggle.text = "Mute Sound"
    toggle.toggle_mode = true
    toggle.toggled.connect(_on_mute_toggled)
    add_child(toggle)

    # Flat button
    var flat_btn := Button.new()
    flat_btn.text = "Link"
    flat_btn.flat = true
    add_child(flat_btn)

func _on_button_pressed() -> void:
    print("Button was pressed!")

func _on_save_pressed() -> void:
    print("Saving...")

func _on_mute_toggled(toggled_on: bool) -> void:
    print("Mute: ", toggled_on)
```

## Advanced Example: Custom Styling

```gdscript
extends Button

func _ready() -> void:
    # Create custom theme
    var custom_theme := Theme.new()

    # Create StyleBoxFlat for normal state
    var normal_style := StyleBoxFlat.new()
    normal_style.bg_color = Color(0.2, 0.3, 0.8)
    normal_style.corner_radius_top_left = 10
    normal_style.corner_radius_top_right = 10
    normal_style.corner_radius_bottom_left = 10
    normal_style.corner_radius_bottom_right = 10

    # Hover state
    var hover_style := StyleBoxFlat.new()
    hover_style.bg_color = Color(0.3, 0.4, 0.9)
    hover_style.corner_radius_top_left = 10
    hover_style.corner_radius_top_right = 10
    hover_style.corner_radius_bottom_left = 10
    hover_style.corner_radius_bottom_right = 10

    # Apply styles
    add_theme_stylebox_override("normal", normal_style)
    add_theme_stylebox_override("hover", hover_style)
    add_theme_color_override("font_color", Color.WHITE)
```

## Best Practices

1. **Icon Size**: Use `icon_max_width` to limit icon size, or enable `expand_icon` for scalable icons
2. **Text Overflow**: Set `clip_text = true` or use `text_overrun_behavior` for long text
3. **Toggle Buttons**: Enable `toggle_mode` for on/off states (like checkboxes)
4. **Accessibility**: Always set meaningful `text` even for icon-only buttons
5. **Flat Buttons**: Use `flat = true` for link-style or minimal buttons

## Common Pitfalls

- Icon appears on wrong side: Set both `icon_alignment` and `vertical_icon_alignment`
- Text too long: Enable `autowrap_mode` or `clip_text`
- Button not responding: Check if `disabled = true` or parent is blocking input
- Focus visual missing: Ensure `focus` StyleBox is visible (default is transparent)
- Using `button_pressed` property directly: Use `set_pressed_no_signal()` to avoid triggering signals

## Related Classes

- BaseButton - Parent class with common button functionality
- CheckBox - Button with checkbox appearance
- CheckButton - Toggle button with on/off switch
- LinkButton - Text-only button styled as hyperlink
- TextureButton - Button using textures instead of theme
- TouchScreenButton - Button for touch input (supports multitouch)
