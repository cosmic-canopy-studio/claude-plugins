---
class: LineEdit
category: nodes/ui/text
description: An input field for single-line text
godot_version: 4.x
---

# LineEdit

**Inherits:** Control < CanvasItem < Node < Object

An input field for editing a single line of text.

## Description

LineEdit provides an input field for editing a single line of text.

- When focused using keyboard arrow keys, it gains focus but doesn't enter edit mode
- Click with the mouse to enter edit mode
- Exit edit mode by pressing `ui_text_submit` (Enter) or `ui_cancel` (Escape)
- Check `edit()`, `unedit()`, `is_editing()`, and the `editing_toggled` signal for edit mode control

LineEdit features many built-in shortcuts (Ctrl maps to Cmd on macOS):
- Ctrl+C: Copy
- Ctrl+X: Cut
- Ctrl+V/Y: Paste
- Ctrl+Z: Undo
- Ctrl+Shift+Z: Redo
- Ctrl+U: Delete text from caret to beginning
- Ctrl+K: Delete text from caret to end
- Ctrl+A: Select all

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `text` | String | "" | The text content |
| `placeholder_text` | String | "" | Hint text shown when empty |
| `alignment` | HorizontalAlignment | 0 (LEFT) | Text alignment |
| `max_length` | int | 0 | Maximum character limit (0 = unlimited) |
| `editable` | bool | true | Whether text can be modified |
| `secret` | bool | false | Mask characters (for passwords) |
| `secret_character` | String | "•" | Character used for masking |
| `clear_button_enabled` | bool | false | Show clear button when not empty |
| `caret_column` | int | 0 | Caret position in text |
| `caret_blink` | bool | false | Enable caret blinking |
| `caret_blink_interval` | float | 0.65 | Blink interval in seconds |
| `caret_force_displayed` | bool | false | Always show caret (even unfocused) |
| `select_all_on_focus` | bool | false | Select all text when focused |
| `deselect_on_focus_loss_enabled` | bool | true | Deselect when focus is lost |
| `context_menu_enabled` | bool | true | Enable right-click context menu |
| `virtual_keyboard_enabled` | bool | true | Show virtual keyboard on mobile |
| `virtual_keyboard_type` | VirtualKeyboardType | 0 (DEFAULT) | Type of virtual keyboard |
| `selecting_enabled` | bool | true | Allow text selection |
| `shortcut_keys_enabled` | bool | true | Enable shortcut keys |
| `middle_mouse_paste_enabled` | bool | true | Paste with middle mouse (Linux) |
| `drag_and_drop_selection_enabled` | bool | true | Allow drag-and-drop of selection |
| `right_icon` | Texture2D | null | Icon displayed on right side |
| `flat` | bool | false | Hide decoration |

## Key Methods

```gdscript
# Text manipulation
func clear() -> void
func delete_char_at_caret() -> void
func delete_text(from_column: int, to_column: int) -> void
func insert_text_at_caret(text: String) -> void

# Selection
func select(from: int = 0, to: int = -1) -> void
func select_all() -> void
func deselect() -> void
func get_selected_text() -> String
func get_selection_from_column() -> int
func get_selection_to_column() -> int
func has_selection() -> bool

# Edit mode
func edit() -> void
func unedit() -> void
func is_editing() -> bool

# Undo/redo
func has_undo() -> bool
func has_redo() -> bool

# IME support
func apply_ime() -> void
func cancel_ime() -> void
func has_ime_text() -> bool

# Context menu
func get_menu() -> PopupMenu
func is_menu_visible() -> bool
func menu_option(option: int) -> void
```

## Signals

| Signal | Description |
|--------|-------------|
| `text_changed(new_text: String)` | Emitted when text changes |
| `text_submitted(new_text: String)` | Emitted when user presses Enter |
| `text_change_rejected(rejected_substring: String)` | Emitted when text exceeds max_length |
| `editing_toggled(toggled_on: bool)` | Emitted when edit mode changes |

## Enumerations

### MenuItems
- `MENU_CUT` (0)
- `MENU_COPY` (1)
- `MENU_PASTE` (2)
- `MENU_CLEAR` (3)
- `MENU_SELECT_ALL` (4)
- `MENU_UNDO` (5)
- `MENU_REDO` (6)

### VirtualKeyboardType
- `KEYBOARD_TYPE_DEFAULT` (0)
- `KEYBOARD_TYPE_MULTILINE` (1)
- `KEYBOARD_TYPE_NUMBER` (2)
- `KEYBOARD_TYPE_NUMBER_DECIMAL` (3)
- `KEYBOARD_TYPE_PHONE` (4)
- `KEYBOARD_TYPE_EMAIL_ADDRESS` (5)
- `KEYBOARD_TYPE_PASSWORD` (6)
- `KEYBOARD_TYPE_URL` (7)

## Theme Properties

### Colors
- `font_color`: Default text color
- `font_placeholder_color`: Placeholder text color
- `font_selected_color`: Selected text color
- `font_uneditable_color`: Text color when not editable
- `selection_color`: Selection background color
- `caret_color`: Caret color
- `clear_button_color`: Clear button tint
- `clear_button_color_pressed`: Clear button pressed tint

### Constants
- `minimum_character_width`: Minimum width in 'M' characters (default: 4)
- `caret_width`: Caret width in pixels (default: 1)
- `outline_size`: Text outline size (default: 0)

### Styles
- `normal`: Default background
- `focus`: Background when focused
- `read_only`: Background when not editable

## Usage Example

```gdscript
extends LineEdit

func _ready() -> void:
    placeholder_text = "Enter your name..."
    max_length = 20
    text_submitted.connect(_on_text_submitted)
    text_changed.connect(_on_text_changed)

func _on_text_submitted(new_text: String) -> void:
    print("User entered: ", new_text)
    # Process the input
    clear()

func _on_text_changed(new_text: String) -> void:
    # Real-time validation
    if new_text.length() > 0:
        var first_char := new_text[0]
        if not first_char.is_valid_identifier():
            modulate = Color.RED
        else:
            modulate = Color.WHITE
```

## Password Field Example

```gdscript
extends LineEdit

func _ready() -> void:
    secret = true
    secret_character = "*"
    placeholder_text = "Password"
    virtual_keyboard_type = KEYBOARD_TYPE_PASSWORD
    clear_button_enabled = true
    context_menu_enabled = false  # Disable copy/paste for security
```

## Email/URL Field Example

```gdscript
extends LineEdit

func _ready() -> void:
    placeholder_text = "email@example.com"
    virtual_keyboard_type = KEYBOARD_TYPE_EMAIL_ADDRESS
    text_submitted.connect(_validate_email)

func _validate_email(email: String) -> void:
    var regex := RegEx.new()
    regex.compile("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$")
    if regex.search(email):
        print("Valid email: ", email)
    else:
        print("Invalid email format")
        modulate = Color.RED
```

## Number Input Example

```gdscript
extends LineEdit

func _ready() -> void:
    virtual_keyboard_type = KEYBOARD_TYPE_NUMBER_DECIMAL
    placeholder_text = "0.00"
    text_changed.connect(_filter_numeric)

func _filter_numeric(new_text: String) -> void:
    # Only allow numbers and one decimal point
    var filtered := ""
    var has_decimal := false

    for c in new_text:
        if c.is_valid_int():
            filtered += c
        elif c == "." and not has_decimal:
            filtered += c
            has_decimal = true

    if filtered != new_text:
        text = filtered
        caret_column = filtered.length()
```

## Custom Context Menu Example

```gdscript
extends LineEdit

func _ready() -> void:
    var menu := get_menu()
    # Remove all items after "Redo"
    menu.item_count = menu.get_item_index(MENU_REDO) + 1
    # Add custom item
    menu.add_separator()
    menu.add_item("Insert Date", MENU_MAX + 1)
    menu.id_pressed.connect(_on_menu_item_pressed)

func _on_menu_item_pressed(id: int) -> void:
    if id == MENU_MAX + 1:
        insert_text_at_caret(Time.get_date_string_from_system())
```

## Best Practices

1. **Validation**: Use `text_changed` for real-time validation, `text_submitted` for final validation
2. **Keyboard Types**: Set appropriate `virtual_keyboard_type` for mobile devices
3. **Max Length**: Set `max_length` to prevent excessive input and handle `text_change_rejected`
4. **Passwords**: Use `secret = true` and disable context menu for security
5. **Clear Button**: Enable `clear_button_enabled` for better UX on clearable fields
6. **Placeholders**: Use `placeholder_text` to show format examples

## Common Pitfalls

- Changing `text` property doesn't emit `text_changed` signal
- Not handling `text_change_rejected` when using `max_length`
- Forgetting to disable context menu for password fields
- Using `caret_column` without checking text length (can crash)
- Not calling `deselect()` before programmatic text changes can cause unexpected selection
- Modifying text in `text_changed` can cause infinite loops

## Related Classes

- TextEdit - For multiline text editing
- Control - Parent class with focus management
- PopupMenu - Context menu customization
