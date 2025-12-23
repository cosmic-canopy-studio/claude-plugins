---
class: HBoxContainer
inherits: BoxContainer < Container < Control < CanvasItem < Node < Object
category: UI Containers
---

# HBoxContainer

A container that arranges its child controls horizontally.

## Description

A variant of BoxContainer that can only arrange its child controls horizontally. Child controls are rearranged automatically when their minimum size changes.

## Inheritance Chain

HBoxContainer < BoxContainer < Container < Control < CanvasItem < Node < Object

## Properties

All properties are inherited from BoxContainer:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| alignment | AlignmentMode | `BEGIN` | The alignment mode for child controls |
| vertical | bool | `false` | Automatically set to `false` for HBoxContainer |

## Methods

All methods are inherited from BoxContainer and Container.

## Signals

Inherits all signals from Container and Control.

## Theme Properties

Inherited from BoxContainer:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| separation | int | `4` | The horizontal separation between child controls |

## Usage Example

```gdscript
var hbox: HBoxContainer = HBoxContainer.new()
add_child(hbox)

# Add buttons that will be arranged horizontally
var button1: Button = Button.new()
button1.text = "First"
hbox.add_child(button1)

var button2: Button = Button.new()
button2.text = "Second"
hbox.add_child(button2)

# Customize spacing
hbox.add_theme_constant_override("separation", 10)
```

## Notes

- Only works with Control-based child nodes
- Children are automatically resized based on their minimum size requirements
- Use BoxContainer if you need to switch between horizontal and vertical layouts dynamically

## See Also

- VBoxContainer - Vertical variant
- BoxContainer - Base class with configurable orientation
- GridContainer - For 2D grid layouts
