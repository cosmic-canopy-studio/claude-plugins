---
class: Label
category: nodes/ui/text
description: A control for displaying plain text
godot_version: 4.x
---

# Label

**Inherits:** Control < CanvasItem < Node < Object

A control for displaying plain text.

## Description

A control for displaying plain text. It gives you control over the horizontal and vertical alignment and can wrap the text inside the node's bounding rectangle. It doesn't support bold, italics, or other rich text formatting. For that, use RichTextLabel instead.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `text` | String | "" | The text to display |
| `horizontal_alignment` | HorizontalAlignment | 0 (LEFT) | Controls horizontal text alignment |
| `vertical_alignment` | VerticalAlignment | 0 (TOP) | Controls vertical text alignment |
| `autowrap_mode` | AutowrapMode | 0 (OFF) | Text wrapping mode |
| `clip_text` | bool | false | Clip text horizontally if it exceeds bounds |
| `text_overrun_behavior` | OverrunBehavior | 0 (TRIM_NOTHING) | Clipping behavior when text exceeds bounds |
| `uppercase` | bool | false | Display all text as UPPERCASE |
| `visible_characters` | int | -1 | Number of visible characters (-1 = all) |
| `visible_ratio` | float | 1.0 | Fraction of characters to display |
| `lines_skipped` | int | 0 | Number of lines to skip from start |
| `max_lines_visible` | int | -1 | Maximum number of lines to show |
| `label_settings` | LabelSettings | null | Shared settings resource |
| `language` | String | "" | Language code for line-breaking |
| `ellipsis_char` | String | "…" | Character used for text clipping |

## Key Methods

```gdscript
func get_line_count() -> int
func get_line_height(line: int = -1) -> int
func get_total_character_count() -> int
func get_visible_line_count() -> int
func get_character_bounds(pos: int) -> Rect2
```

## Theme Properties

### Colors
- `font_color`: Default text color (default: Color(1, 1, 1, 1))
- `font_outline_color`: Text outline color (default: Color(0, 0, 0, 1))
- `font_shadow_color`: Shadow effect color (default: Color(0, 0, 0, 0))

### Constants
- `line_spacing`: Additional vertical spacing between lines (default: 3)
- `outline_size`: Text outline size (default: 0)
- `shadow_offset_x`: Horizontal shadow offset (default: 1)
- `shadow_offset_y`: Vertical shadow offset (default: 1)
- `shadow_outline_size`: Shadow outline size (default: 1)

### Font
- `font`: Font resource to use
- `font_size`: Font size

### Styles
- `normal`: Background StyleBox
- `focus`: StyleBox when focused (for assistive apps)

## Usage Example

```gdscript
extends Label

func _ready() -> void:
    # Basic label
    text = "Hello, World!"
    horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    vertical_alignment = VERTICAL_ALIGNMENT_CENTER

    # Wrapping text
    var wrapped_label := Label.new()
    wrapped_label.text = "This is a long text that will wrap within the label's bounds"
    wrapped_label.autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
    wrapped_label.custom_minimum_size = Vector2(200, 0)
    add_sibling(wrapped_label)

    # Animated text reveal
    var animated_label := Label.new()
    animated_label.text = "Revealing text..."
    animated_label.visible_ratio = 0.0
    add_sibling(animated_label)

    var tween := create_tween()
    tween.tween_property(animated_label, "visible_ratio", 1.0, 2.0)

# Update label text dynamically
func set_score(score: int) -> void:
    text = "Score: %d" % score

# Limit visible lines
func show_preview(full_text: String, max_lines: int = 3) -> void:
    text = full_text
    max_lines_visible = max_lines
```

## Advanced Example: Styled Label

```gdscript
extends Label

func _ready() -> void:
    text = "Stylized Label"

    # Custom font
    var custom_font := load("res://fonts/custom_font.ttf")
    add_theme_font_override("font", custom_font)
    add_theme_font_size_override("font_size", 24)

    # Colors
    add_theme_color_override("font_color", Color.GOLD)
    add_theme_color_override("font_outline_color", Color.BLACK)

    # Outline and shadow
    add_theme_constant_override("outline_size", 2)
    add_theme_color_override("font_shadow_color", Color(0, 0, 0, 0.5))
    add_theme_constant_override("shadow_offset_x", 3)
    add_theme_constant_override("shadow_offset_y", 3)

    # Alignment
    horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER
    vertical_alignment = VERTICAL_ALIGNMENT_CENTER
```

## Text Animation Example

```gdscript
extends Label

var full_text: String = "The quick brown fox jumps over the lazy dog."

func _ready() -> void:
    text = full_text
    visible_characters = 0

    # Typewriter effect
    var tween := create_tween()
    tween.tween_property(
        self,
        "visible_characters",
        get_total_character_count(),
        2.0
    )

func animate_color_pulse() -> void:
    var tween := create_tween()
    tween.set_loops()
    tween.tween_property(
        self,
        "modulate",
        Color.RED,
        1.0
    )
    tween.tween_property(
        self,
        "modulate",
        Color.WHITE,
        1.0
    )
```

## LabelSettings Example

```gdscript
# Create reusable label style
var title_settings := LabelSettings.new()
title_settings.font_size = 32
title_settings.font_color = Color.GOLD
title_settings.outline_size = 2
title_settings.outline_color = Color.BLACK

# Apply to multiple labels
var title1 := Label.new()
title1.text = "Title 1"
title1.label_settings = title_settings

var title2 := Label.new()
title2.text = "Title 2"
title2.label_settings = title_settings  # Shared settings
```

## Best Practices

1. **Text Wrapping**: Use `autowrap_mode` instead of manual line breaks for dynamic layouts
2. **Performance**: Prefer `visible_ratio` over `visible_characters` for smoother animations
3. **Alignment**: Set `vertical_alignment` for proper vertical centering in variable-height containers
4. **Shared Styles**: Use `LabelSettings` for consistent styling across multiple labels
5. **Outline Size**: For MSDF fonts, set `FontFile.msdf_pixel_range` to at least 2× `outline_size`

## Common Pitfalls

- Text not wrapping: Ensure `autowrap_mode` is set and label has constrained width
- Text clipped unexpectedly: Check `clip_text`, `text_overrun_behavior`, and `max_lines_visible`
- Invisible text: Verify `font_color` isn't transparent and has sufficient contrast
- Outline cutoff: For MSDF fonts, increase `msdf_pixel_range` relative to `outline_size`
- Using `\n` instead of `autowrap_mode`: Manual breaks don't adapt to size changes
- Forgetting `visible_characters` affects Unicode codepoints, not visual characters

## Related Classes

- RichTextLabel - For rich text formatting (BBCode, images, tables)
- LabelSettings - Shared label styling resource
- Control - Parent class with layout properties
- Font - Font resource for text rendering
