---
class: CenterContainer
category: nodes/ui/containers
complexity: basic
tags: [ui, container, layout, centering]
last_updated: 2025-12-21
---

# CenterContainer

**Inherits:** Container < Control < CanvasItem < Node < Object

A container that keeps all child controls centered at their minimum size.

## Description

CenterContainer is a simple layout container that centers all of its children in its bounding rectangle. Children are sized to their minimum size and positioned in the center of the container. This is one of the simplest containers in Godot's UI system.

## Common Use Cases

- Centering single UI elements
- Title screens with centered logo
- Centered dialog boxes
- Loading screens with centered spinner
- Menu items that need to be centered
- Centered notification messages

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `use_top_left` | bool | false | Centers relative to top-left instead of center |

## Basic Example

```gdscript
extends Control

func _ready() -> void:
    var center := CenterContainer.new()
    add_child(center)

    var label := Label.new()
    label.text = "Centered Text"
    center.add_child(label)
```

## Centered Loading Screen

```gdscript
extends CenterContainer

@onready var loading_label: Label = $LoadingLabel
@onready var spinner: TextureRect = $Spinner

func show_loading(message: String = "Loading...") -> void:
    loading_label.text = message
    visible = true

    # Animate spinner
    var tween := create_tween().set_loops()
    tween.tween_property(spinner, "rotation", TAU, 1.0)

func hide_loading() -> void:
    visible = false
```

## Centered Dialog

```gdscript
extends Control

func create_centered_dialog(title: String, message: String) -> void:
    var center := CenterContainer.new()
    center.custom_minimum_size = size  # Fill parent
    add_child(center)

    var panel := PanelContainer.new()
    center.add_child(panel)

    var vbox := VBoxContainer.new()
    panel.add_child(vbox)

    var title_label := Label.new()
    title_label.text = title
    title_label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    vbox.add_child(title_label)

    var message_label := Label.new()
    message_label.text = message
    vbox.add_child(message_label)
```

## Nested Centering

```gdscript
extends Control

func _ready() -> void:
    # Horizontal centering
    var h_center := CenterContainer.new()
    h_center.custom_minimum_size = Vector2(400, 0)
    add_child(h_center)

    # Vertical centering
    var v_center := CenterContainer.new()
    v_center.custom_minimum_size = Vector2(0, 300)
    h_center.add_child(v_center)

    # Centered button
    var button := Button.new()
    button.text = "Centered Button"
    v_center.add_child(button)
```

## Title Screen Pattern

```gdscript
extends Control

func setup_title_screen() -> void:
    var center := CenterContainer.new()
    center.anchor_right = 1.0
    center.anchor_bottom = 1.0
    add_child(center)

    var vbox := VBoxContainer.new()
    vbox.add_theme_constant_override("separation", 20)
    center.add_child(vbox)

    # Logo
    var logo := TextureRect.new()
    logo.texture = preload("res://assets/logo.png")
    logo.stretch_mode = TextureRect.STRETCH_KEEP_CENTERED
    vbox.add_child(logo)

    # Menu buttons
    for option in ["New Game", "Continue", "Settings", "Quit"]:
        var button := Button.new()
        button.text = option
        button.custom_minimum_size = Vector2(200, 50)
        vbox.add_child(button)
```

## Dynamic Content Centering

```gdscript
extends CenterContainer

func display_message(text: String, duration: float = 3.0) -> void:
    var label := Label.new()
    label.text = text
    label.add_theme_font_size_override("font_size", 24)
    add_child(label)

    await get_tree().create_timer(duration).timeout
    label.queue_free()
```

## Common Patterns

### Centered Modal Overlay

```gdscript
func create_modal_overlay() -> CenterContainer:
    var overlay := ColorRect.new()
    overlay.color = Color(0, 0, 0, 0.7)
    overlay.anchor_right = 1.0
    overlay.anchor_bottom = 1.0
    add_child(overlay)

    var center := CenterContainer.new()
    center.anchor_right = 1.0
    center.anchor_bottom = 1.0
    overlay.add_child(center)

    return center
```

### Centered Notification

```gdscript
func show_notification(message: String) -> void:
    var center := CenterContainer.new()
    center.anchor_right = 1.0
    center.anchor_bottom = 0.2
    add_child(center)

    var panel := PanelContainer.new()
    center.add_child(panel)

    var label := Label.new()
    label.text = message
    label.add_theme_constant_override("margin_left", 20)
    label.add_theme_constant_override("margin_right", 20)
    panel.add_child(label)

    # Fade in/out
    center.modulate.a = 0
    var tween := create_tween()
    tween.tween_property(center, "modulate:a", 1.0, 0.3)
    tween.tween_interval(2.0)
    tween.tween_property(center, "modulate:a", 0.0, 0.3)
    tween.tween_callback(center.queue_free)
```

### Responsive Centered Content

```gdscript
func create_responsive_center() -> void:
    var center := CenterContainer.new()
    center.anchor_right = 1.0
    center.anchor_bottom = 1.0
    add_child(center)

    var content := VBoxContainer.new()
    # Content will grow but stay centered
    content.size_flags_horizontal = Control.SIZE_SHRINK_CENTER
    content.size_flags_vertical = Control.SIZE_SHRINK_CENTER
    center.add_child(content)
```

## Best Practices

1. **Set container size**: CenterContainer needs defined bounds to center within
2. **Use with single child or VBox/HBox**: Works best with one child or a box container
3. **Consider anchors**: Often used with full-screen anchors (1.0, 1.0)
4. **Child minimum size matters**: Children are sized to minimum, not expanded
5. **Combine with margins**: Add margins to child panels for padding from edges

## Common Pitfalls

- Forgetting to set container size (won't center if container has no size)
- Expecting children to fill container (they use minimum size)
- Using with multiple children without a box container (only one child shows properly)
- Not understanding `use_top_left` (rarely needed, usually keep default false)
- Nesting CenterContainers unnecessarily (usually one is enough)

## use_top_left Property

When `use_top_left = true`, the container centers children relative to its top-left corner instead of its center. This is rarely used but can be helpful for specific layout needs.

```gdscript
func demonstrate_top_left() -> void:
    var center := CenterContainer.new()
    center.use_top_left = true
    center.size = Vector2(200, 200)

    var label := Label.new()
    label.text = "Offset from top-left"
    center.add_child(label)
```

## Layout Behavior

- **Children are NOT resized**: They use their minimum size
- **Multiple children overlap**: Only the last child is visible (use VBoxContainer/HBoxContainer for multiple items)
- **Respects child minimum size**: Set `custom_minimum_size` on children to control sizing
- **Anchors don't affect centering**: Centering is automatic regardless of child anchors

## Related Nodes

- **MarginContainer**: Adds margins around children
- **PanelContainer**: Themed background panel with single child
- **VBoxContainer/HBoxContainer**: Stack children vertically/horizontally
- **AspectRatioContainer**: Maintains child aspect ratio
- **Container**: Base class for all containers

## Tutorials

- [Using Containers (Official Godot Docs)](https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html)

## Source

Official Godot Documentation: [CenterContainer](https://docs.godotengine.org/en/stable/classes/class_centercontainer.html)
