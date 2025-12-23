---
class: PanelContainer
inherits: Container < Control < CanvasItem < Node < Object
category: UI Containers
---

# PanelContainer

A container that keeps its child controls within the area of a StyleBox.

## Description

A container that keeps its child controls within the area of a StyleBox. Useful for giving controls an outline or background panel.

## Inheritance Chain

PanelContainer < Container < Control < CanvasItem < Node < Object

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| mouse_filter | MouseFilter | `MOUSE_FILTER_STOP` | Overrides Control's default to stop mouse events |

### Property Details

#### mouse_filter
- **Type:** MouseFilter (enum)
- **Default:** `MOUSE_FILTER_STOP` (overrides Control's default)

Controls how the panel handles mouse input events. By default, PanelContainer stops mouse events from passing through.

## Methods

All methods are inherited from Container.

## Signals

Inherits all signals from Container and Control.

## Theme Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| panel | StyleBox | - | The style of PanelContainer's background |

### Theme Property Details

#### panel
- **Type:** StyleBox

Defines the visual appearance of the panel background. Use StyleBoxFlat for simple colored panels or StyleBoxTexture for textured backgrounds.

## Usage Example

```gdscript
# Basic usage with default theme
var panel: PanelContainer = PanelContainer.new()
add_child(panel)

var label: Label = Label.new()
label.text = "Panel Content"
panel.add_child(label)
```

## Common Patterns

### Custom Panel Style
```gdscript
# Create a panel with custom background color
var panel: PanelContainer = PanelContainer.new()

var stylebox: StyleBoxFlat = StyleBoxFlat.new()
stylebox.bg_color = Color(0.2, 0.3, 0.4, 0.9)
stylebox.border_width_all = 2
stylebox.border_color = Color.WHITE
stylebox.corner_radius_all = 8

panel.add_theme_stylebox_override("panel", stylebox)
add_child(panel)
```

### Dialog Box
```gdscript
var dialog: PanelContainer = PanelContainer.new()
dialog.custom_minimum_size = Vector2(300, 200)

var stylebox: StyleBoxFlat = StyleBoxFlat.new()
stylebox.bg_color = Color(0.15, 0.15, 0.15, 0.95)
stylebox.corner_radius_all = 10
stylebox.content_margin_left = 20
stylebox.content_margin_right = 20
stylebox.content_margin_top = 20
stylebox.content_margin_bottom = 20

dialog.add_theme_stylebox_override("panel", stylebox)

# Add content container
var vbox: VBoxContainer = VBoxContainer.new()
dialog.add_child(vbox)

var title: Label = Label.new()
title.text = "Dialog Title"
vbox.add_child(title)
```

### Tooltip Panel
```gdscript
var tooltip: PanelContainer = PanelContainer.new()
tooltip.mouse_filter = Control.MOUSE_FILTER_IGNORE  # Don't block mouse

var stylebox: StyleBoxFlat = StyleBoxFlat.new()
stylebox.bg_color = Color(0.1, 0.1, 0.1, 0.9)
stylebox.border_width_all = 1
stylebox.border_color = Color(0.8, 0.8, 0.8, 1.0)
stylebox.content_margin_all = 8

tooltip.add_theme_stylebox_override("panel", stylebox)
```

### Card/Item Display
```gdscript
func create_item_card(item_name: String, item_icon: Texture2D) -> PanelContainer:
	var card: PanelContainer = PanelContainer.new()
	card.custom_minimum_size = Vector2(100, 120)

	var stylebox: StyleBoxFlat = StyleBoxFlat.new()
	stylebox.bg_color = Color(0.25, 0.25, 0.3, 1.0)
	stylebox.corner_radius_all = 5
	stylebox.content_margin_all = 10

	card.add_theme_stylebox_override("panel", stylebox)

	var vbox: VBoxContainer = VBoxContainer.new()
	card.add_child(vbox)

	var icon: TextureRect = TextureRect.new()
	icon.texture = item_icon
	icon.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT_CENTERED
	vbox.add_child(icon)

	var label: Label = Label.new()
	label.text = item_name
	label.horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
	vbox.add_child(label)

	return card
```

## Notes

- The StyleBox defines both the background appearance and content margins
- Content margins in the StyleBox determine the padding around children
- By default, blocks mouse events (unlike other containers)
- Commonly used for creating visually distinct UI sections
- Can be nested to create layered panel effects

## See Also

- StyleBoxFlat - For solid color panels with borders
- StyleBoxTexture - For textured/image-based panels
- MarginContainer - For adding margins without background styling
- Panel - Control version without container functionality
