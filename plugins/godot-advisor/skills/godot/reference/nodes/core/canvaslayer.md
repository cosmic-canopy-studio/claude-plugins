---
class: CanvasLayer
category: nodes/core
complexity: intermediate
tags: [2d, ui, layering, rendering, canvas]
---

# CanvasLayer

**Inherits:** Node < Object
**Inherited By:** ParallaxBackground

A node used for independent rendering of objects within a 2D scene.

## Description

CanvasItem-derived nodes that are direct or indirect children of a CanvasLayer will be drawn in that layer. The layer is a numeric index that defines the draw order. The default 2D scene renders with index `0`, so a CanvasLayer with index `-1` will be drawn below, and a CanvasLayer with index `1` will be drawn above. This order will hold regardless of the `CanvasItem.z_index` of the nodes within each layer.

CanvasLayers can be hidden and they can also optionally follow the viewport. This makes them useful for HUDs like health bar overlays (on layers `1` and higher) or backgrounds (on layers `-1` and lower).

## Key Concepts

**Note:** Embedded Windows are placed on layer `1024`. CanvasItems on layers `1025` and higher appear in front of embedded windows.

**Note:** Each CanvasLayer is drawn on one specific Viewport and cannot be shared between multiple Viewports, see `custom_viewport`. When using multiple Viewports, for example in a split-screen game, you need to create an individual CanvasLayer for each Viewport you want it to be drawn on.

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `layer` | `int` | `1` | Layer index for draw order |
| `visible` | `bool` | `true` | If false, CanvasItems under this layer are hidden |
| `offset` | `Vector2` | `Vector2(0, 0)` | The layer's base offset |
| `rotation` | `float` | `0.0` | The layer's rotation in radians |
| `scale` | `Vector2` | `Vector2(1, 1)` | The layer's scale |
| `transform` | `Transform2D` | `Transform2D(1, 0, 0, 1, 0, 0)` | The layer's transform |
| `custom_viewport` | `Node` | | Custom Viewport assigned to the CanvasLayer |
| `follow_viewport_enabled` | `bool` | `false` | If true, layer maintains position in world space |
| `follow_viewport_scale` | `float` | `1.0` | Scales the layer when using follow_viewport_enabled |

## Methods

| Return | Method |
|--------|--------|
| `RID` | `get_canvas()` |
| `Transform2D` | `get_final_transform()` |
| `void` | `show()` |
| `void` | `hide()` |

## Signals

- **visibility_changed()**: Emitted when visibility of the layer is changed

## Property Details

### layer

Layer index for draw order. Lower values are drawn behind higher values.

**Note:** If multiple CanvasLayers have the same layer index, CanvasItem children of one CanvasLayer are drawn behind the CanvasItem children of the other CanvasLayer. Which CanvasLayer is drawn in front is non-deterministic.

**Note:** The layer index should be between `RenderingServer.CANVAS_LAYER_MIN` and `RenderingServer.CANVAS_LAYER_MAX` (inclusive). Any other value will wrap around.

### visible

If `false`, any CanvasItem under this CanvasLayer will be hidden.

Unlike `CanvasItem.visible`, visibility of a CanvasLayer isn't propagated to underlying layers.

### follow_viewport_enabled

If enabled, the CanvasLayer maintains its position in world space. If disabled, the CanvasLayer stays in a fixed position on the screen.

Together with `follow_viewport_scale`, this can be used for a pseudo-3D effect.

### follow_viewport_scale

Scales the layer when using `follow_viewport_enabled`. Layers moving into the foreground should have increasing scales, while layers moving into the background should have decreasing scales.

## Quick Examples

### HUD layer

```gdscript
extends CanvasLayer

func _ready() -> void:
    layer = 1  # Above game world
    offset = Vector2.ZERO
```

### Background layer

```gdscript
extends CanvasLayer

func _ready() -> void:
    layer = -1  # Behind game world
```

### Parallax-like effect with follow viewport

```gdscript
extends CanvasLayer

func _ready() -> void:
    follow_viewport_enabled = true
    follow_viewport_scale = 0.5  # Moves at half speed of camera
```

## Common Patterns

### Screen-space UI (HUD)

```gdscript
# HUD.gd
extends CanvasLayer

@onready var health_bar: ProgressBar = $HealthBar

func _ready() -> void:
    layer = 10  # On top of everything
```

### Pause menu overlay

```gdscript
extends CanvasLayer

func _ready() -> void:
    layer = 100  # Very high layer
    visible = false

func show_pause_menu() -> void:
    visible = true
    get_tree().paused = true

func hide_pause_menu() -> void:
    visible = false
    get_tree().paused = false
```

### Multiple viewport UI

```gdscript
# For split-screen, create separate CanvasLayer for each viewport
@onready var viewport1_ui: CanvasLayer = $Viewport1/UI
@onready var viewport2_ui: CanvasLayer = $Viewport2/UI

func _ready() -> void:
    viewport1_ui.custom_viewport = $Viewport1
    viewport2_ui.custom_viewport = $Viewport2
```

### Transform manipulation

```gdscript
# Offset the entire layer
$CanvasLayer.offset = Vector2(100, 50)

# Rotate the layer
$CanvasLayer.rotation = deg_to_rad(15)

# Scale the layer
$CanvasLayer.scale = Vector2(1.5, 1.5)
```

## Best Practices

- **Layer Organization**: Use negative layers for backgrounds, positive for UI
- **HUD Layers**: Place UI on layers 1+ to appear above game world
- **Windows**: Remember layer 1024 is reserved for embedded windows
- **Viewport Specific**: Create separate CanvasLayers for each viewport in split-screen
- **Visibility**: Use `visible` to show/hide entire UI layers
- **Pseudo-3D**: Use `follow_viewport_enabled` and `follow_viewport_scale` for parallax effects

## Anti-Patterns

- Don't share CanvasLayers between viewports (create separate instances)
- Don't use same layer index for multiple CanvasLayers (draw order is non-deterministic)
- Don't forget layer 1024 is reserved for embedded windows
- Don't modify `z_index` expecting it to override layer order (it doesn't)

## See Also

- [Viewport](viewport.md) - For multi-viewport setups
- [Camera2D](../2d/rendering/camera2d.md) - For camera following
- [ParallaxBackground](../2d/parallaxbackground.md) - For parallax scrolling backgrounds
- [Control](../ui/control.md) - For UI elements in CanvasLayers

## Tutorials

- [Viewport and canvas transforms](https://docs.godotengine.org/en/stable/tutorials/2d/2d_transforms.html)
- [Canvas layers](https://docs.godotengine.org/en/stable/tutorials/2d/canvas_layers.html)
- [2D Dodge The Creeps Demo](https://godotengine.org/asset-library/asset/2712)
