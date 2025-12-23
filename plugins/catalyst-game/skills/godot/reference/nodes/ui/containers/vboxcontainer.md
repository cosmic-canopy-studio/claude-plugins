---
class: VBoxContainer
inherits: BoxContainer < Container < Control < CanvasItem < Node < Object
category: UI Containers
---

# VBoxContainer

A container that arranges its child controls vertically.

## Description

A variant of BoxContainer that can only arrange its child controls vertically. Child controls are rearranged automatically when their minimum size changes.

## Inheritance Chain

VBoxContainer < BoxContainer < Container < Control < CanvasItem < Node < Object

## Properties

All properties are inherited from BoxContainer:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| alignment | AlignmentMode | `BEGIN` | The alignment mode for child controls |
| vertical | bool | `true` | Automatically set to `true` for VBoxContainer |

## Methods

All methods are inherited from BoxContainer and Container.

## Signals

Inherits all signals from Container and Control.

## Theme Properties

Inherited from BoxContainer:

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| separation | int | `4` | The vertical separation between child controls |

## Usage Example

```gdscript
var vbox: VBoxContainer = VBoxContainer.new()
add_child(vbox)

# Add labels that will be stacked vertically
var label1: Label = Label.new()
label1.text = "First Line"
vbox.add_child(label1)

var label2: Label = Label.new()
label2.text = "Second Line"
vbox.add_child(label2)

# Customize spacing
vbox.add_theme_constant_override("separation", 8)
```

## Notes

- Only works with Control-based child nodes
- Children are automatically resized based on their minimum size requirements
- Use BoxContainer if you need to switch between horizontal and vertical layouts dynamically

## See Also

- HBoxContainer - Horizontal variant
- BoxContainer - Base class with configurable orientation
- GridContainer - For 2D grid layouts
