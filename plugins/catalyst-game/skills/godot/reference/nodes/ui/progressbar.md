---
class: ProgressBar
category: nodes/ui
complexity: basic
tags: [ui, control, progress, range]
last_updated: 2025-12-21
---

# ProgressBar

**Inherits:** Range < Control < CanvasItem < Node < Object

A control used for visual representation of a percentage.

## Description

ProgressBar is a control that visually represents a percentage value. It shows the fill percentage in the center and can also display indeterminate progress (loading animation). For more advanced fill modes or texture-based progress bars, use TextureProgressBar instead.

## Common Use Cases

- Health/stamina bars in games
- Loading screens
- Download/upload progress indicators
- Skill cooldown timers
- Resource meters (mana, energy, etc.)

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `value` | float | 0.0 | Current value (inherited from Range) |
| `min_value` | float | 0.0 | Minimum value (inherited from Range) |
| `max_value` | float | 100.0 | Maximum value (inherited from Range) |
| `fill_mode` | FillMode | FILL_BEGIN_TO_END | Direction the bar fills |
| `indeterminate` | bool | false | Shows animated loading indicator |
| `show_percentage` | bool | true | Displays percentage text on bar |

## FillMode Enumeration

| Value | Description |
|-------|-------------|
| `FILL_BEGIN_TO_END` | Fills left-to-right (or right-to-left in RTL layouts) |
| `FILL_END_TO_BEGIN` | Fills right-to-left (or left-to-right in RTL layouts) |
| `FILL_TOP_TO_BOTTOM` | Fills from top to bottom |
| `FILL_BOTTOM_TO_TOP` | Fills from bottom to top |

## Basic Example

```gdscript
extends Node

@onready var health_bar: ProgressBar = $HealthBar

func _ready() -> void:
    health_bar.min_value = 0.0
    health_bar.max_value = 100.0
    health_bar.value = 75.0
    health_bar.show_percentage = true

func take_damage(amount: float) -> void:
    health_bar.value = max(0.0, health_bar.value - amount)
```

## Loading Indicator Example

```gdscript
extends Control

@onready var loading_bar: ProgressBar = $LoadingBar

func show_loading() -> void:
    loading_bar.indeterminate = true
    loading_bar.show_percentage = false

func hide_loading() -> void:
    loading_bar.indeterminate = false
```

## Vertical Progress Bar

```gdscript
extends Control

func _ready() -> void:
    var vertical_bar: ProgressBar = $VerticalBar
    vertical_bar.fill_mode = ProgressBar.FILL_BOTTOM_TO_TOP
    vertical_bar.custom_minimum_size = Vector2(32, 200)
```

## Theme Customization

ProgressBar supports extensive theme customization:

**Theme Properties:**
- Colors: `font_color`, `font_outline_color`
- Fonts: `font`, `font_size`
- Styles: `background`, `fill`
- Constants: `outline_size`

```gdscript
func customize_progress_bar(bar: ProgressBar) -> void:
    # Customize appearance via theme overrides
    bar.add_theme_color_override("font_color", Color.WHITE)
    var fill_style := StyleBoxFlat.new()
    fill_style.bg_color = Color.GREEN
    bar.add_theme_stylebox_override("fill", fill_style)
```

## Common Patterns

### Health Bar with Color Change

```gdscript
func update_health_bar(current: float, maximum: float) -> void:
    health_bar.max_value = maximum
    health_bar.value = current

    # Change color based on health percentage
    var fill_style := StyleBoxFlat.new()
    var percentage: float = current / maximum

    if percentage > 0.5:
        fill_style.bg_color = Color.GREEN
    elif percentage > 0.25:
        fill_style.bg_color = Color.YELLOW
    else:
        fill_style.bg_color = Color.RED

    health_bar.add_theme_stylebox_override("fill", fill_style)
```

### Smooth Progress Animation

```gdscript
var target_value: float = 100.0

func _process(delta: float) -> void:
    # Smoothly interpolate to target value
    progress_bar.value = lerp(progress_bar.value, target_value, delta * 5.0)

func set_progress(new_value: float) -> void:
    target_value = clamp(new_value, progress_bar.min_value, progress_bar.max_value)
```

## Best Practices

1. **Use Range signals**: Connect to `value_changed` signal for reactive updates
2. **Clamp values**: Always ensure values stay within min/max bounds
3. **Consider TextureProgressBar**: For radial or custom-shaped progress bars
4. **Hide percentage for small bars**: Disable `show_percentage` for compact UI elements
5. **Use indeterminate mode**: For unknown duration operations

## Common Pitfalls

- Forgetting to set `max_value` when it differs from default 100
- Not clamping values before assignment (can cause display issues)
- Using ProgressBar for radial fills (use TextureProgressBar instead)
- Enabling percentage display on bars too small to read text

## Related Nodes

- **TextureProgressBar**: Texture-based progress with radial/custom fill modes
- **Range**: Base class providing min/max/value functionality
- **Slider**: Interactive Range control for user input
- **SpinBox**: Numeric input with increment/decrement buttons

## Source

Official Godot Documentation: [ProgressBar](https://docs.godotengine.org/en/stable/classes/class_progressbar.html)
