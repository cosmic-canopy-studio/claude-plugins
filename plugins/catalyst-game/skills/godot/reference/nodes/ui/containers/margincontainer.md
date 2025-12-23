---
class: MarginContainer
inherits: Container < Control < CanvasItem < Node < Object
category: UI Containers
keywords: padding
---

# MarginContainer

A container that keeps a margin around its child controls.

## Description

MarginContainer adds an adjustable margin on each side of its child controls. The margins are added around all children, not around each individual one. To control the MarginContainer's margins, use the `margin_*` theme properties.

**Note:** The margin sizes are theme overrides, not normal properties. Use `add_theme_constant_override()` to modify them in code.

## Inheritance Chain

MarginContainer < Container < Control < CanvasItem < Node < Object

## Properties

No unique properties. All margins are controlled via theme properties.

## Methods

All methods are inherited from Container.

## Signals

Inherits all signals from Container and Control.

## Theme Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| margin_bottom | int | `0` | Offsets children from the bottom |
| margin_left | int | `0` | Offsets children from the left |
| margin_right | int | `0` | Offsets children from the right |
| margin_top | int | `0` | Offsets children from the top |

### Theme Property Details

All margin properties offset the direct children of the container towards the inside by the specified amount of pixels.

## Usage Example

```gdscript
# Basic usage
var margin: MarginContainer = MarginContainer.new()
add_child(margin)

# Set margins using theme overrides
margin.add_theme_constant_override("margin_top", 20)
margin.add_theme_constant_override("margin_left", 20)
margin.add_theme_constant_override("margin_bottom", 20)
margin.add_theme_constant_override("margin_right", 20)

# Add child control
var label: Label = Label.new()
label.text = "This text has margins around it"
margin.add_child(label)
```

## Common Patterns

### Uniform Margins
```gdscript
func set_uniform_margin(container: MarginContainer, margin_value: int) -> void:
	container.add_theme_constant_override("margin_top", margin_value)
	container.add_theme_constant_override("margin_left", margin_value)
	container.add_theme_constant_override("margin_bottom", margin_value)
	container.add_theme_constant_override("margin_right", margin_value)
```

### Asymmetric Margins
```gdscript
# More padding on top for headers
var header_margin: MarginContainer = MarginContainer.new()
header_margin.add_theme_constant_override("margin_top", 40)
header_margin.add_theme_constant_override("margin_left", 20)
header_margin.add_theme_constant_override("margin_bottom", 10)
header_margin.add_theme_constant_override("margin_right", 20)
```

### Responsive Margins
```gdscript
func update_margins_for_screen_size() -> void:
	var viewport_size: Vector2 = get_viewport().size
	var margin_size: int = int(viewport_size.x * 0.05)  # 5% of screen width

	set_uniform_margin(margin_container, margin_size)
```

## Notes

- Margins apply to all children collectively, not individually
- Unlike padding in other containers, margins are set via theme overrides
- Useful for adding spacing around entire UI sections
- Can be nested to create complex spacing layouts

## See Also

- PanelContainer - Container with styled background
- Container - Base class for all containers
- Control.add_theme_constant_override() - Method to set theme properties
