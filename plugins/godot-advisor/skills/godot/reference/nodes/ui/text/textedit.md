---
class: TextEdit
category: nodes/ui/text
description: A multiline text editor with syntax highlighting support
godot_version: 4.x
---

# TextEdit

**Inherits:** Control < CanvasItem < Node < Object

A multiline text editor.

## Description

A multiline text editor. It has limited facilities for editing code, such as syntax highlighting support. For more advanced code editing, see CodeEdit.

Most viewport, caret, and edit methods contain a `caret_index` argument for multiple caret support:
- `-1` for all carets
- `0` for the main caret
- `> 0` for secondary carets in creation order

Holding Alt while scrolling increases scroll speed by 5×.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `text` | String | "" | The entire text content |
| `placeholder_text` | String | "" | Hint text shown when empty |
| `editable` | bool | true | Whether text can be modified |
| `context_menu_enabled` | bool | true | Enable right-click context menu |
| `shortcut_keys_enabled` | bool | true | Enable keyboard shortcuts |
| `selecting_enabled` | bool | true | Allow text selection |
| `deselect_on_focus_loss_enabled` | bool | true | Deselect when focus is lost |
| `drag_and_drop_selection_enabled` | bool | true | Allow drag-and-drop of selection |
| `virtual_keyboard_enabled` | bool | true | Show virtual keyboard on mobile |
| `middle_mouse_paste_enabled` | bool | true | Paste with middle mouse (Linux) |

### Caret Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `caret_type` | CaretType | 0 (LINE) | Caret appearance (line or block) |
| `caret_blink` | bool | false | Enable caret blinking |
| `caret_blink_interval` | float | 0.65 | Blink interval in seconds |
| `caret_multiple` | bool | true | Enable multiple carets |
| `caret_mid_grapheme` | bool | false | Allow caret inside composite characters |
| `caret_move_on_right_click` | bool | true | Move caret on right-click |

### Display Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `autowrap_mode` | AutowrapMode | 3 (WORD_SMART) | Text wrapping mode |
| `wrap_mode` | LineWrappingMode | 0 (NONE) | Line wrapping mode |
| `scroll_smooth` | bool | false | Enable smooth scrolling |
| `scroll_v_scroll_speed` | float | 80.0 | Vertical scroll speed |
| `scroll_past_end_of_file` | bool | false | Allow scrolling past last line |
| `minimap_draw` | bool | false | Draw code minimap |
| `minimap_width` | int | 80 | Minimap width in pixels |

### Highlighting Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `syntax_highlighter` | SyntaxHighlighter | null | Syntax highlighting resource |
| `highlight_all_occurrences` | bool | false | Highlight all word occurrences |
| `highlight_current_line` | bool | false | Highlight line with caret |
| `draw_tabs` | bool | false | Show tab characters |
| `draw_spaces` | bool | false | Show space characters |
| `draw_control_chars` | bool | false | Show control characters |

### Scroll Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `scroll_horizontal` | int | 0 | Horizontal scroll position |
| `scroll_vertical` | float | 0.0 | Vertical scroll position |
| `scroll_fit_content_height` | bool | false | Fit height to content |
| `scroll_fit_content_width` | bool | false | Fit width to content |

## Key Methods

```gdscript
# Text manipulation
func get_line(line: int) -> String
func set_line(line: int, new_text: String) -> void
func insert_line_at(line: int, text: String) -> void
func remove_line_at(line: int, move_carets_down: bool = true) -> void
func insert_text_at_caret(text: String, caret_index: int = -1) -> void
func insert_text(text: String, line: int, column: int,
                 before_selection_begin: bool = true,
                 before_selection_end: bool = false) -> void
func remove_text(from_line: int, from_column: int,
                 to_line: int, to_column: int) -> void

# Caret management
func get_caret_count() -> int
func add_caret(line: int, column: int) -> int
func remove_caret(caret: int) -> void
func remove_secondary_carets() -> void
func get_caret_line(caret_index: int = 0) -> int
func get_caret_column(caret_index: int = 0) -> int
func set_caret_line(line: int, adjust_viewport: bool = true,
                    can_be_hidden: bool = true, wrap_index: int = 0,
                    caret_index: int = 0) -> void
func set_caret_column(column: int, adjust_viewport: bool = true,
                      caret_index: int = 0) -> void
func merge_overlapping_carets() -> void

# Selection
func select(origin_line: int, origin_column: int,
            caret_line: int, caret_column: int,
            caret_index: int = 0) -> void
func select_all() -> void
func select_word_under_caret(caret_index: int = -1) -> void
func add_selection_for_next_occurrence() -> void
func deselect(caret_index: int = -1) -> void
func delete_selection(caret_index: int = -1) -> void
func has_selection(caret_index: int = -1) -> bool
func get_selected_text(caret_index: int = -1) -> String
func get_selection_from_line(caret_index: int = 0) -> int
func get_selection_from_column(caret_index: int = 0) -> int
func get_selection_to_line(caret_index: int = 0) -> int
func get_selection_to_column(caret_index: int = 0) -> int

# Clipboard operations
func copy(caret_index: int = -1) -> void
func cut(caret_index: int = -1) -> void
func paste(caret_index: int = -1) -> void
func paste_primary_clipboard(caret_index: int = -1) -> void

# Undo/Redo
func undo() -> void
func redo() -> void
func has_undo() -> bool
func has_redo() -> bool
func clear_undo_history() -> void
func begin_complex_operation() -> void
func end_complex_operation() -> void

# Viewport
func adjust_viewport_to_caret(caret_index: int = 0) -> void
func center_viewport_to_caret(caret_index: int = 0) -> void
func get_first_visible_line() -> int
func get_last_full_visible_line() -> int
func get_visible_line_count() -> int

# Line info
func get_line_count() -> int
func get_line_height() -> int
func get_line_width(line: int, wrap_index: int = -1) -> int
func get_line_wrap_count(line: int) -> int
func is_line_wrapped(line: int) -> bool

# Search
func search(text: String, flags: int, from_line: int,
            from_column: int) -> Vector2i
func set_search_text(search_text: String) -> void
func set_search_flags(flags: int) -> void

# Gutters
func add_gutter(at: int = -1) -> void
func remove_gutter(gutter: int) -> void
func get_gutter_count() -> int
func set_gutter_name(gutter: int, name: String) -> void
func set_gutter_type(gutter: int, type: GutterType) -> void
func set_gutter_width(gutter: int, width: int) -> void
func set_gutter_draw(gutter: int, draw: bool) -> void
func set_gutter_clickable(gutter: int, clickable: bool) -> void

# Line background/gutter
func set_line_background_color(line: int, color: Color) -> void
func set_line_gutter_text(line: int, gutter: int, text: String) -> void
func set_line_gutter_icon(line: int, gutter: int, icon: Texture2D) -> void
func set_line_gutter_item_color(line: int, gutter: int, color: Color) -> void
func set_line_gutter_metadata(line: int, gutter: int, metadata: Variant) -> void
```

## Signals

| Signal | Description |
|--------|-------------|
| `text_changed()` | Emitted when text changes |
| `text_set()` | Emitted when clear() is called or text property is set |
| `lines_edited_from(from_line: int, to_line: int)` | Emitted immediately when text changes |
| `caret_changed()` | Emitted when any caret changes position |
| `gutter_added()` | Emitted when a gutter is added |
| `gutter_removed()` | Emitted when a gutter is removed |
| `gutter_clicked(line: int, gutter: int)` | Emitted when a gutter is clicked |

## Enumerations

### CaretType
- `CARET_TYPE_LINE` (0): Vertical line caret
- `CARET_TYPE_BLOCK` (1): Block caret

### LineWrappingMode
- `LINE_WRAPPING_NONE` (0): No line wrapping
- `LINE_WRAPPING_BOUNDARY` (1): Wrap at text boundaries

### SelectionMode
- `SELECTION_MODE_NONE` (0)
- `SELECTION_MODE_SHIFT` (1)
- `SELECTION_MODE_POINTER` (2)
- `SELECTION_MODE_WORD` (3)
- `SELECTION_MODE_LINE` (4)

### GutterType
- `GUTTER_TYPE_STRING` (0): Text gutter
- `GUTTER_TYPE_ICON` (1): Icon gutter
- `GUTTER_TYPE_CUSTOM` (2): Custom draw gutter

## Usage Example

```gdscript
extends TextEdit

func _ready() -> void:
    text = "Hello World\nMultiline text editor"
    syntax_highlighter = preload("res://my_highlighter.gd").new()

    # Enable features
    highlight_current_line = true
    draw_tabs = true
    minimap_draw = true

    # Connect signals
    text_changed.connect(_on_text_changed)
    caret_changed.connect(_on_caret_changed)

func _on_text_changed() -> void:
    print("Text modified")
    print("Line count: ", get_line_count())

func _on_caret_changed() -> void:
    var line := get_caret_line()
    var col := get_caret_column()
    print("Caret at ", line, ":", col)
```

## Code Editor Example

```gdscript
extends TextEdit

func _ready() -> void:
    # Add line numbers gutter
    add_gutter(0)
    set_gutter_name(0, "line_numbers")
    set_gutter_type(0, GUTTER_TYPE_STRING)
    set_gutter_draw(0, true)
    set_gutter_width(0, 40)

    # Update line numbers when text changes
    text_set.connect(_update_line_numbers)
    lines_edited_from.connect(_on_lines_edited)

    # Enable code editor features
    syntax_highlighter = GDScriptSyntaxHighlighter.new()
    highlight_current_line = true
    draw_tabs = true
    draw_spaces = true
    minimap_draw = true

    _update_line_numbers()

func _update_line_numbers() -> void:
    for i in get_line_count():
        set_line_gutter_text(i, 0, str(i + 1))

func _on_lines_edited(from_line: int, to_line: int) -> void:
    _update_line_numbers()
```

## Multiple Carets Example

```gdscript
extends TextEdit

func _ready() -> void:
    text = "Line 1\nLine 2\nLine 3"
    caret_multiple = true

    # Add carets at each line
    for i in get_line_count():
        if i > 0:  # First caret already exists
            add_caret(i, 0)

    # Type on all lines at once
    await get_tree().create_timer(1.0).timeout
    insert_text_at_caret(">> ")  # Inserts on all carets

func find_and_select_all(search_term: String) -> void:
    # Select all occurrences of a word
    remove_secondary_carets()
    deselect()

    var result := search(search_term, 0, 0, 0)
    while result.x != -1:
        var caret_idx := add_caret(result.x, result.y)
        select_word_under_caret(caret_idx)
        result = search(search_term, 0, result.x, result.y + 1)
```

## Search and Replace Example

```gdscript
extends TextEdit

func search_and_replace(find_text: String, replace_text: String) -> void:
    var result := search(find_text, 0, 0, 0)
    var replacements := 0

    begin_complex_operation()  # Group into single undo

    while result.x != -1:
        var line := result.x
        var col := result.y
        remove_text(line, col, line, col + find_text.length())
        insert_text(replace_text, line, col)
        replacements += 1

        # Continue search from after replacement
        result = search(find_text, 0, line, col + replace_text.length())

    end_complex_operation()
    print("Replaced ", replacements, " occurrences")
```

## Best Practices

1. **Multiple Operations**: Use `begin_complex_operation()` / `end_complex_operation()` to group edits into single undo
2. **Caret Index**: Use `-1` for operations on all carets, specific index for individual control
3. **Performance**: For large texts, use `scroll_fit_content_height/width = false` and fixed size
4. **Line Numbers**: Implement gutters for line numbers rather than prepending to text
5. **Syntax Highlighting**: Use SyntaxHighlighter or CodeHighlighter for proper coloring

## Common Pitfalls

- Forgetting to merge overlapping carets after programmatic additions
- Not using `begin_complex_operation()` for multi-step edits (creates too many undo steps)
- Setting `text` property directly loses undo history - use insert/remove methods
- Accessing caret beyond `get_caret_count()` causes errors
- Not handling `lines_edited_from` signal for line-dependent decorations
- Using wrong coordinate system (line/column vs pixel position)

## Related Classes

- CodeEdit - Extended TextEdit with code-specific features
- SyntaxHighlighter - Base class for syntax highlighting
- GDScriptSyntaxHighlighter - Built-in GDScript highlighter
- CodeHighlighter - Simple keyword-based highlighter
- LineEdit - Single-line text input
