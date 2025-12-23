---
topic: ui-tutorials
version: 2025.12.21
godot_version: "4.3"
sources:
  - url: "https://docs.godotengine.org/en/stable/tutorials/ui/gui_containers.html"
    type: official
    priority: 1
  - url: "https://docs.godotengine.org/en/stable/tutorials/ui/size_and_anchors.html"
    type: official
    priority: 1
  - url: "https://docs.godotengine.org/en/stable/tutorials/ui/custom_gui_controls.html"
    type: official
    priority: 1
  - url: "https://docs.godotengine.org/en/stable/tutorials/ui/gui_skinning.html"
    type: official
    priority: 1
  - url: "https://docs.godotengine.org/en/stable/tutorials/ui/gui_theme_type_variations.html"
    type: official
    priority: 1
status: complete
---

# UI Tutorial Patterns

Patterns extracted from Godot Engine UI tutorial documentation covering containers, sizing, custom controls, and theming.

## Container Layout Patterns

### Problem: Need responsive layout that adapts to different screen sizes

**Solution: Use Containers instead of manual positioning**

Containers automatically arrange and resize child Control nodes. They're essential for responsive UIs.

```gdscript
extends Control

# Bad - hardcoded positions break on different screen sizes
func _ready_bad() -> void:
    var button := Button.new()
    button.position = Vector2(100, 200)
    button.size = Vector2(100, 50)
    add_child(button)

# Good - use containers for automatic layout
@onready var _button_container: VBoxContainer = %ButtonsContainer

func _ready() -> void:
    # Children automatically positioned and sized
    for button: Button in _button_container.get_children():
        button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        button.size_flags_vertical = Control.SIZE_EXPAND_FILL
```

**Key points:**
- Containers control positioning; manual position changes are ignored or invalidated on resize
- Nested containers create complex layouts that adapt seamlessly
- Never animate container children directly (use wrapper Control nodes)

### Problem: Need to arrange items horizontally or vertically

**Solution: Use BoxContainer (HBoxContainer or VBoxContainer)**

Box containers arrange children in a single row or column with automatic spacing.

```gdscript
# HBoxContainer - horizontal toolbar layout
extends Control

@onready var _toolbar: HBoxContainer = %ToolbarHBox

func _ready() -> void:
    # HBox arranges buttons left-to-right
    _toolbar.add_theme_constant_override("separation", 10)

    for button: Button in _toolbar.get_children():
        button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        button.pressed.connect(_on_button_pressed.bind(button.name))

# VBoxContainer - vertical menu
extends Control

@onready var _menu: VBoxContainer = %MenuVBox

func _ready() -> void:
    # VBox arranges buttons top-to-bottom
    _menu.add_theme_constant_override("separation", 15)

    for button: Button in _menu.get_children():
        button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
```

**Key points:**
- HBoxContainer expands children vertically but arranges horizontally
- VBoxContainer expands children horizontally but arranges vertically
- Use `separation` theme constant for spacing between children
- `alignment` property controls BEGIN, CENTER, or END positioning

### Problem: Need to create a grid layout (inventory, skill grid, turn-based actions)

**Solution: Use GridContainer with columns property**

Grid containers arrange children in a specified number of columns, with rows calculated automatically.

```gdscript
# Inventory grid (4 items per row)
extends Control

@onready var _inventory_grid: GridContainer = %InventoryGrid

func _ready() -> void:
    _inventory_grid.columns = 4

    # Each row will have 4 items, height auto-calculated
    # Rows = ceil(child_count / columns)
    # Each column width = widest child in that column
    # Each row height = tallest child in that row

    var slots: Array[TextureRect] = []
    slots.assign(_inventory_grid.find_children("", "TextureRect"))

    for slot: TextureRect in slots:
        slot.custom_minimum_size = Vector2(64, 64)
        slot.set_drag_forwarding(
            _get_drag_data.bind(slot),
            _can_drop_data,
            _drop_data.bind(slot)
        )

func _get_drag_data(_position: Vector2, source: TextureRect) -> Texture2D:
    var texture: Texture2D = source.texture
    source.texture = null
    return texture

func _can_drop_data(_position: Vector2, data: Texture2D) -> bool:
    return data != null

func _drop_data(_position: Vector2, data: Texture2D, target: TextureRect) -> void:
    target.texture = data
```

**Key points:**
- Must set `columns` property; defaults to 1 column if not set
- Children fill left-to-right, top-to-bottom
- GridContainer automatically calculates row count
- Perfect for inventories, skill grids, game boards

### Problem: Need padding around UI content or panel styling

**Solution: Use MarginContainer for spacing, PanelContainer for backgrounds**

MarginContainer adds uniform padding around content. PanelContainer adds a styled background.

```gdscript
# Main menu with margins and panel styling
extends Control

@onready var _main_container: MarginContainer = %MainMarginContainer
@onready var _panel: PanelContainer = %DialogPanel

func _ready() -> void:
    # MarginContainer - add padding
    _main_container.add_theme_constant_override("margin_left", 100)
    _main_container.add_theme_constant_override("margin_right", 100)
    _main_container.add_theme_constant_override("margin_top", 80)
    _main_container.add_theme_constant_override("margin_bottom", 80)

    # PanelContainer automatically applies StyleBox from theme
    # and expands child to fill panel area
```

**Key points:**
- MarginContainer accepts margins as theme constants (margin_left, margin_right, margin_top, margin_bottom)
- PanelContainer draws StyleBox from theme, then expands child to fill
- Combine: MarginContainer > VBoxContainer > Content for common layout
- PanelContainer respects StyleBox margins when positioning children

### Problem: Need scrollable content area (chat, inventory list, long menus)

**Solution: Use ScrollContainer with child content**

ScrollContainer adds scrollbars when child exceeds container size.

```gdscript
# Scrollable chat window
extends Control

@onready var _scroll_container: ScrollContainer = %ChatScroll
@onready var _chat_content: VBoxContainer = %ChatMessages

func _ready() -> void:
    _scroll_container.scroll_horizontal_enabled = false
    _scroll_container.scroll_vertical_enabled = true

    # Child (VBoxContainer) will scroll when content exceeds container size
    _chat_content.custom_minimum_size = Vector2(0, 1000)

    # Scroll properties you can control
    _scroll_container.scroll_vertical = 999  # Scroll to bottom
    _scroll_container.scroll_horizontal = 0

func add_message(text: String) -> void:
    var message_label := Label.new()
    message_label.text = text
    message_label.autowrap_mode = TextServer.AUTOWRAP_WORD
    _chat_content.add_child(message_label)

    # Auto-scroll to bottom when new message added
    _scroll_container.scroll_vertical = int(_chat_content.size.y)
```

**Key points:**
- ScrollContainer only scrolls if child exceeds container size
- Set `scroll_vertical_enabled` and `scroll_horizontal_enabled` individually
- Mouse wheel and touch drag automatically supported
- Use VBoxContainer as child for vertical scrolling lists
- Ensure child has proper minimum_size for scrolling to work

### Problem: Need flexible wrapping layout (tag displays, responsive button groups)

**Solution: Use FlowContainer (HFlowContainer or VFlowContainer)**

Flow containers arrange children and wrap to next line/column when space runs out.

```gdscript
# Tag display that wraps to next line
extends Control

@onready var _tag_flow: HFlowContainer = %TagsHFlow

func _ready() -> void:
    # Add tags that wrap like text
    var tags: Array[String] = ["fire", "ice", "lightning", "healing", "buff", "debuff"]

    for tag: String in tags:
        var tag_button := Button.new()
        tag_button.text = tag
        tag_button.custom_minimum_size = Vector2(80, 30)
        _tag_flow.add_child(tag_button)

    # Children automatically wrap when reaching container edge
    # No manual wrapping needed
```

**Key points:**
- HFlowContainer wraps horizontally; VFlowContainer wraps vertically
- Acts like text wrapping - children move to next line/column when space exhausted
- Ideal for responsive UIs that adapt to different screen widths

### Problem: Need centered content in a container

**Solution: Use CenterContainer**

CenterContainer automatically centers all child controls at their minimum size.

```gdscript
# Centered loading screen
extends Control

@onready var _center: CenterContainer = %CenterContainer

func _ready() -> void:
    # Any child added to this container is automatically centered
    # No manual positioning needed
    pass

# Game over screen centered
extends CenterContainer

@onready var _game_over_label: Label = %GameOverLabel

func show_game_over() -> void:
    _game_over_label.text = "GAME OVER"
    visible = true
```

**Key points:**
- Children automatically centered without manual positioning
- Respects child minimum size
- Perfect for splash screens, loading screens, modal dialogs

### Problem: Need to maintain aspect ratio during resize (video player, camera viewport)

**Solution: Use AspectRatioContainer**

Aspect ratio containers automatically scale children to maintain a specific aspect ratio.

```gdscript
# Video player that maintains 16:9 aspect ratio
extends Control

@onready var _aspect_container: AspectRatioContainer = %VideoAspectContainer
@onready var _video_player: VideoPlayer = %VideoPlayer

func _ready() -> void:
    _aspect_container.ratio = 16.0 / 9.0
    _aspect_container.stretch_mode = AspectRatioContainer.STRETCH_FIT

    # Child automatically scales to maintain 16:9 aspect ratio
    # regardless of window size
```

**Key points:**
- `ratio` property sets aspect ratio (width/height)
- `stretch_mode` options: FIT, COVER, WIDTH_CONTROLS_HEIGHT, HEIGHT_CONTROLS_WIDTH
- Perfect for videos, images, camera previews

## Size and Anchors Pattern

### Problem: Need to position UI on specific screen edges (health bar at top, compass at corner)

**Solution: Use Anchors to position relative to screen edges**

Anchors define where control reference points are relative to parent.

```gdscript
# Health bar anchored to top-left
extends Control

@onready var _health_bar: ProgressBar = %HealthBar

func _ready() -> void:
    # Anchor to top-left corner (0.0, 0.0)
    _health_bar.anchor_left = 0.0
    _health_bar.anchor_top = 0.0

    # Offsets are relative to anchor point
    _health_bar.offset_left = 20  # 20 pixels right of left edge
    _health_bar.offset_top = 20   # 20 pixels down from top edge
    _health_bar.size = Vector2(200, 30)

# Compass anchored to top-right corner
extends Control

@onready var _compass: TextureRect = %Compass

func _ready() -> void:
    # Anchor to top-right (1.0, 0.0)
    _compass.anchor_left = 1.0
    _compass.anchor_top = 0.0

    # Negative offset moves left from right edge
    _compass.offset_left = -120  # 120 pixels left of right edge
    _compass.offset_top = 20      # 20 pixels down from top edge
    _compass.size = Vector2(100, 100)
```

**Key points:**
- Anchor values: 0.0 = start (left/top), 1.0 = end (right/bottom), 0.5 = center
- Offset values are pixels relative to anchor point
- Use negative offsets to move in opposite direction of anchor

### Problem: Need responsive UI that adapts to different window sizes

**Solution: Use anchor stretching to fill available space**

Set different anchor values for opposite edges to make control stretch.

```gdscript
# Full-screen panel that stretches with window
extends Control

@onready var _fullscreen_panel: PanelContainer = %FullscreenPanel

func _ready() -> void:
    # Anchor to all four edges of parent
    _fullscreen_panel.anchor_left = 0.0
    _fullscreen_panel.anchor_right = 1.0
    _fullscreen_panel.anchor_top = 0.0
    _fullscreen_panel.anchor_bottom = 1.0

    # Small offsets for margins
    _fullscreen_panel.offset_left = 10
    _fullscreen_panel.offset_right = -10
    _fullscreen_panel.offset_top = 10
    _fullscreen_panel.offset_bottom = -10

    # Panel now stretches to fill window with 10px margin

# Sidebar that fills height but fixed width
extends Control

@onready var _sidebar: PanelContainer = %Sidebar

func _ready() -> void:
    # Full height
    _sidebar.anchor_top = 0.0
    _sidebar.anchor_bottom = 1.0
    _sidebar.offset_top = 0
    _sidebar.offset_bottom = 0

    # Fixed width
    _sidebar.anchor_left = 0.0
    _sidebar.anchor_right = 0.0
    _sidebar.offset_left = 0
    _sidebar.offset_right = 200  # 200 pixels wide
```

**Key points:**
- Different left/right anchors = horizontal stretch
- Different top/bottom anchors = vertical stretch
- Use anchor presets in editor for quick setup
- Containers handle this automatically; anchors useful for manual positioning

### Problem: Need to center a control on its parent

**Solution: Center anchors at 0.5 and use negative offsets**

```gdscript
# Center a texture on screen
extends Control

@onready var _texture_rect: TextureRect = %CenteredTexture

func _ready() -> void:
    _texture_rect.texture = load("res://icon.png")

    # Center point at parent center (0.5, 0.5)
    _texture_rect.anchor_left = 0.5
    _texture_rect.anchor_right = 0.5
    _texture_rect.anchor_top = 0.5
    _texture_rect.anchor_bottom = 0.5

    # Negative offsets position from center
    var texture_size: Vector2 = _texture_rect.texture.get_size()
    _texture_rect.offset_left = -texture_size.x / 2
    _texture_rect.offset_right = texture_size.x / 2
    _texture_rect.offset_top = -texture_size.y / 2
    _texture_rect.offset_bottom = texture_size.y / 2

    # Now texture is perfectly centered
```

**Key points:**
- Anchor left and right at 0.5 centers horizontally
- Anchor top and bottom at 0.5 centers vertically
- Use negative offsets to position from center point

## Size Flags Pattern

### Problem: Button doesn't grow to fill available space in container

**Solution: Use SIZE_EXPAND_FILL flags**

Size flags control how children behave within containers.

```gdscript
# Bad - button stays small
extends HBoxContainer

func _ready() -> void:
    var button := Button.new()
    add_child(button)
    # Button appears small, doesn't use available space

# Good - button expands to fill
extends HBoxContainer

func _ready() -> void:
    var button := Button.new()
    button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    add_child(button)
    # Button now fills available horizontal space
```

**Key points:**
- SIZE_FILL: Child fills allocated space
- SIZE_EXPAND: Child requests additional available space
- SIZE_EXPAND_FILL: Combination of EXPAND and FILL (most common)
- SIZE_SHRINK_CENTER: Min size, centered (no expanding)
- SIZE_SHRINK_END: Min size, right/bottom aligned (no expanding)
- Default (no flags): Min size, left/top aligned

### Problem: Multiple expanding children not sharing space equally

**Solution: Use STRETCH_RATIO on children**

When multiple children have EXPAND, stretch ratio determines space distribution.

```gdscript
# Three buttons sharing horizontal space
extends HBoxContainer

func _ready() -> void:
    var button1 := Button.new()
    button1.text = "1x"
    button1.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    add_child(button1)

    var button2 := Button.new()
    button2.text = "2x"
    button2.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    button2.size_flags_stretch_ratio = 2.0  # Takes 2x space
    add_child(button2)

    var button3 := Button.new()
    button3.text = "1x"
    button3.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    add_child(button3)

    # Result: button1 gets 1/4, button2 gets 2/4, button3 gets 1/4
```

**Key points:**
- Stretch ratio only applies when EXPAND flag is set
- Default ratio is 1.0
- Total space divided by ratio sum: if ratios are 1, 2, 1 (sum=4), each gets (1/4, 2/4, 1/4)

### Problem: Container layout not using full available space

**Solution: Ensure children have proper size flags and minimum size**

```gdscript
# Fix - configure size properly
extends Control

@onready var _container: VBoxContainer = %Container

func _ready() -> void:
    for button: Button in _container.get_children():
        # Must have FILL to fill allocated space
        button.size_flags_vertical = Control.SIZE_FILL

        # Set minimum size to prevent squishing
        button.custom_minimum_size = Vector2(0, 40)

        # Only EXPAND if you want to grow beyond minimum
        button.size_flags_vertical = Control.SIZE_EXPAND_FILL
```

**Key points:**
- EXPAND doesn't actually resize - it allocates space
- Must combine EXPAND with FILL to fill that allocated space
- Set custom_minimum_size to prevent children from being squeezed too small

## Custom GUI Control Pattern

### Problem: Need to draw custom visuals for a control

**Solution: Override _draw() and respect control size**

```gdscript
# Custom circular progress indicator
extends Control

var progress: float = 0.5

func _ready() -> void:
    custom_minimum_size = Vector2(100, 100)
    set_process(true)

func _process(_delta: float) -> void:
    progress = fmod(progress + 0.002, 1.0)
    queue_redraw()  # Trigger _draw() call

func _draw() -> void:
    # Always check size to ensure in-bounds drawing
    var center: Vector2 = size / 2.0
    var radius: float = minf(size.x, size.y) / 2.0 - 2.0

    # Draw background circle
    draw_circle(center, radius, Color.DARK_GRAY)

    # Draw progress arc
    var progress_angle: float = progress * TAU
    draw_set_transform(center)
    draw_colored_polygon([
        Vector2.ZERO,
        Vector2.RIGHT.rotated(0.0) * radius,
        Vector2.RIGHT.rotated(progress_angle) * radius
    ], Color.GREEN)
```

**Key points:**
- Always check `size` property in _draw() to ensure content stays in bounds
- Call `queue_redraw()` to trigger _draw() updates
- Use `custom_minimum_size` to define minimum canvas size
- Don't override size directly; respect container layout

### Problem: Custom control needs to draw focus indicator for keyboard input

**Solution: Check has_focus() in _draw()**

```gdscript
# Custom button that shows focus
extends Control

func _ready() -> void:
    focus_mode = FOCUS_ALL  # Allow focus
    custom_minimum_size = Vector2(100, 50)
    gui_input.connect(_on_gui_input)

func _draw() -> void:
    if has_focus():
        draw_focused()
    else:
        draw_normal()

func draw_normal() -> void:
    draw_rect(Rect2(Vector2.ZERO, size), Color.GRAY)
    var label_text: String = "Normal"
    draw_string(get_theme_font("font"), Vector2(10, 25), label_text)

func draw_focused() -> void:
    draw_rect(Rect2(Vector2.ZERO, size), Color.WHITE)
    draw_rect(Rect2(Vector2.ZERO, size), Color.BLUE, false, 3.0)  # Border
    var label_text: String = "Focused!"
    draw_string(get_theme_font("font"), Vector2(10, 25), label_text, HORIZONTAL_ALIGNMENT_LEFT, -1, 14, Color.BLUE)

func _on_gui_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        print("Custom control clicked!")
```

**Key points:**
- Use `has_focus()` to check current focus state
- Set `focus_mode = FOCUS_ALL` to enable keyboard focus
- Draw focus indicator (highlight, box, etc.) when focused
- Always provide visual feedback for focused controls

### Problem: Custom control should handle size like built-in controls

**Solution: Override _get_minimum_size() or set custom_minimum_size**

```gdscript
# Custom size-aware control
extends Control

class_name CustomLabel

var text: String = "Hello"
var padding: int = 10

func _ready() -> void:
    set_custom_minimum_size()

func _get_minimum_size() -> Vector2:
    # Calculate minimum size based on content
    var font: Font = get_theme_font("font")
    var font_size: int = get_theme_font_size("font_size")

    var text_size: Vector2 = font.get_string_size(text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size)
    return text_size + Vector2(padding * 2, padding * 2)

func _draw() -> void:
    # Draw content respecting minimum size
    draw_rect(Rect2(Vector2.ZERO, size), Color.LIGHT_GRAY)

    var font: Font = get_theme_font("font")
    var font_size: int = get_theme_font_size("font_size")
    var text_pos: Vector2 = Vector2(padding, padding + font_size / 2.0)

    draw_string(font, text_pos, text, HORIZONTAL_ALIGNMENT_LEFT, -1, font_size)
```

**Key points:**
- Override `_get_minimum_size()` for dynamic sizing based on content
- Or use `set_custom_minimum_size(Vector2)` in _ready() for static sizing
- Controls inside containers use minimum size to lay out properly
- Prevents custom controls from being squeezed by other controls

### Problem: Custom control needs to respond to input

**Solution: Override _gui_input() for mouse/focus input**

```gdscript
# Custom slider control
extends Control

var value: float = 0.5
signal value_changed(new_value: float)

func _ready() -> void:
    focus_mode = FOCUS_ALL
    custom_minimum_size = Vector2(200, 30)

func _gui_input(event: InputEvent) -> void:
    # Only responds to input when:
    # - Mouse is over control, OR
    # - Button was pressed over control (captures until release), OR
    # - Control has keyboard/joypad focus

    if event is InputEventMouseButton:
        if event.pressed and event.button_index == MOUSE_BUTTON_LEFT:
            # Calculate slider position from mouse
            var relative_x: float = event.position.x / size.x
            value = clamp(relative_x, 0.0, 1.0)
            value_changed.emit(value)
            queue_redraw()
            get_tree().root.set_input_as_handled()

    elif event is InputEventKey and event.pressed:
        match event.keycode:
            KEY_LEFT:
                value -= 0.1
            KEY_RIGHT:
                value += 0.1
        value = clamp(value, 0.0, 1.0)
        value_changed.emit(value)
        queue_redraw()
        get_tree().root.set_input_as_handled()

func _draw() -> void:
    # Draw slider background
    draw_rect(Rect2(Vector2.ZERO, size), Color.DARK_GRAY)

    # Draw slider handle
    var handle_x: float = value * size.x
    draw_rect(Rect2(Vector2(handle_x - 5, 5), Vector2(10, size.y - 10)), Color.LIGHT_BLUE)
```

**Key points:**
- Only responds to input when conditions are met (mouse over, focus, pressed)
- Call `get_tree().root.set_input_as_handled()` to consume input
- Check `event.button_index == MOUSE_BUTTON_LEFT` for specific mouse button
- Use for interactive custom controls

### Problem: Custom control needs to respond to various control events

**Solution: Override _notification() to handle control notifications**

```gdscript
# Control that reacts to various events
extends Control

func _notification(what: int) -> void:
    match what:
        NOTIFICATION_MOUSE_ENTER:
            modulate = Color.WHITE
            print("Mouse entered control")

        NOTIFICATION_MOUSE_EXIT:
            modulate = Color.GRAY
            print("Mouse left control")

        NOTIFICATION_FOCUS_ENTER:
            queue_redraw()
            print("Control gained focus")

        NOTIFICATION_FOCUS_EXIT:
            queue_redraw()
            print("Control lost focus")

        NOTIFICATION_THEME_CHANGED:
            # Theme was changed; update visuals if needed
            queue_redraw()

        NOTIFICATION_VISIBILITY_CHANGED:
            if is_visible():
                print("Control became visible")
            else:
                print("Control became hidden")

        NOTIFICATION_RESIZED:
            print("Control resized to: ", size)
            queue_redraw()

        NOTIFICATION_MODAL_CLOSE:
            # Modal popup this control belongs to was closed
            print("Modal closed")
```

**Key points:**
- NOTIFICATION_MOUSE_ENTER/EXIT: Track mouse hover
- NOTIFICATION_FOCUS_ENTER/EXIT: Track keyboard focus
- NOTIFICATION_THEME_CHANGED: Redraw if using theme items
- NOTIFICATION_VISIBILITY_CHANGED: React to show/hide
- NOTIFICATION_RESIZED: React to size changes
- NOTIFICATION_MODAL_CLOSE: Handle modal dialogs

## Theme Customization Patterns

### Problem: Need to change colors, fonts, or styling of entire UI

**Solution: Create custom Theme resource and apply to control tree**

```gdscript
# Create theme programmatically
extends Control

func _ready() -> void:
    var custom_theme := Theme.new()

    # Add color items
    custom_theme.set_color("font_color", "Label", Color.WHITE)
    custom_theme.set_color("font_color_disabled", "Label", Color.GRAY)

    # Add font size
    custom_theme.set_font_size("font_size", "Label", 24)

    # Apply theme to this node and all children
    theme = custom_theme
```

**Key points:**
- Theme items: Color, Constant (int), Font, FontSize, Icon, StyleBox
- Theme types: One for each Control class (Button, Label, etc.)
- Apply theme at top of control tree to affect all children
- Children can override with local theme overrides

### Problem: Need different button styles (gray, red, blue variants)

**Solution: Use theme type variations**

Type variations extend a base type, allowing preset variations.

```gdscript
# In editor: Create type variation "BlueButton" based on "Button"
# In code: Apply variation to button

extends Control

@onready var _normal_button: Button = %NormalButton
@onready var _blue_button: Button = %BlueButton
@onready var _red_button: Button = %RedButton

func _ready() -> void:
    # Blue button uses "BlueButton" variation instead of base "Button" type
    _blue_button.theme_type_variation = "BlueButton"

    # Red button uses "RedButton" variation
    _red_button.theme_type_variation = "RedButton"

    # Normal button uses default "Button" type
```

**Key points:**
- Type variations extend a base type (e.g., "BlueButton" extends "Button")
- Variations inherit base properties but can override specific items
- Apply with `theme_type_variation` property
- Keep all variations in project theme for consistency

### Problem: Need to override styling on specific control instance

**Solution: Use local theme overrides on the control**

```gdscript
# Override colors on a specific button
extends Control

@onready var _special_button: Button = %SpecialButton
@onready var _label: Label = %Label

func _ready() -> void:
    # Local override - only affects this button
    _special_button.add_theme_color_override("font_color", Color.YELLOW)
    _special_button.add_theme_color_override("font_focus_color", Color.LIME)

    # Override font size
    _label.add_theme_font_size_override("font_size", 32)

    # Override entire StyleBox for button
    var button_style := StyleBoxFlat.new()
    button_style.bg_color = Color.PURPLE
    button_style.set_border_enabled_all(true)
    button_style.border_color = Color.WHITE
    _special_button.add_theme_stylebox_override("normal", button_style)
```

**Key points:**
- Local overrides take precedence over theme and default theme
- Doesn't affect children or other controls
- Use for one-off styling changes
- Methods: add_theme_*_override(item_name, type, value)

### Problem: Need cascading theme where child inherits parent colors

**Solution: Themes cascade from parent to child in control tree**

```gdscript
# Theme cascade example
extends Control

@onready var _root_panel: PanelContainer = %RootPanel
@onready var _button_in_panel: Button = %ButtonInPanel

func _ready() -> void:
    # Create theme for root
    var root_theme := Theme.new()
    root_theme.set_color("font_color", "Button", Color.WHITE)
    root_theme.set_color("font_color", "Label", Color.WHITE)
    _root_panel.theme = root_theme

    # Button in panel uses root theme
    # Label in panel uses root theme
    # All descendants check theme in this order:
    # 1. Local overrides
    # 2. Their own theme property (if set)
    # 3. Parent theme (cascading up to root)
    # 4. Project theme (gui/theme/custom)
    # 5. Default engine theme
```

**Key points:**
- Theme lookup cascades from child to parents
- Set theme on top-level control to affect entire UI tree
- Each child can override with its own theme
- Local overrides always take precedence

### Problem: Need styling that adapts to different game states (team colors, colorblind modes)

**Solution: Swap theme resource at runtime**

```gdscript
# Dynamic theme switching for teams
extends Control

var _red_team_theme: Theme
var _blue_team_theme: Theme

@onready var _ui_root: Control = %UIRoot

func _ready() -> void:
    # Load team themes
    _red_team_theme = load("res://themes/red_team.tres")
    _blue_team_theme = load("res://themes/blue_team.tres")

    # Start with red team
    set_team(true)

func set_team(is_red: bool) -> void:
    if is_red:
        _ui_root.theme = _red_team_theme
    else:
        _ui_root.theme = _blue_team_theme

    # Entire UI subtree updates to new theme
    # All child controls redrawn with new colors/fonts
```

**Key points:**
- Swap theme resource to completely change UI appearance
- Perfect for team colors, accessibility settings, game modes
- All child controls automatically redraw with new theme
- Theme changes are efficient and responsive

## Complex Layout Patterns

### Problem: Need main menu with title, buttons, and footer

**Solution: Combine MarginContainer > VBoxContainer with spacing**

```gdscript
# Main menu layout
extends MarginContainer

@onready var _menu_vbox: VBoxContainer = %MenuVBoxContainer
@onready var _play_button: Button = %PlayButton
@onready var _settings_button: Button = %SettingsButton
@onready var _quit_button: Button = %QuitButton
@onready var _footer_label: Label = %FooterLabel

func _ready() -> void:
    # MarginContainer - add screen padding
    add_theme_constant_override("margin_left", 100)
    add_theme_constant_override("margin_right", 100)
    add_theme_constant_override("margin_top", 80)
    add_theme_constant_override("margin_bottom", 80)

    # VBoxContainer - arrange vertically
    _menu_vbox.add_theme_constant_override("separation", 20)

    # Configure buttons to expand
    for button: Button in [_play_button, _settings_button, _quit_button]:
        button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
        button.custom_minimum_size = Vector2(0, 60)

    # Add spacer before footer
    _menu_vbox.add_spacer(false)  # Flexible spacer

    # Connect buttons
    _play_button.pressed.connect(_on_play_pressed)
    _settings_button.pressed.connect(_on_settings_pressed)
    _quit_button.pressed.connect(_on_quit_pressed)

func _on_play_pressed() -> void:
    get_tree().change_scene_to_file("res://scenes/game.tscn")

func _on_settings_pressed() -> void:
    print("Settings pressed")

func _on_quit_pressed() -> void:
    get_tree().quit()
```

**Key points:**
- MarginContainer > VBoxContainer is standard for menus
- Use add_spacer(false) for flexible spacing between sections
- Set button minimum height to ensure readable buttons
- SIZE_EXPAND_FILL makes buttons grow with window

### Problem: Need split-screen HUD (health bar left, ammo right)

**Solution: HBoxContainer with spacer between sections**

```gdscript
# Split-screen HUD layout
extends Control

@onready var _hud_container: HBoxContainer = %HUDHBoxContainer
@onready var _health_label: Label = %HealthLabel
@onready var _score_label: Label = %ScoreLabel

func _ready() -> void:
    # Add health on left
    _health_label.text = "Health: 100"

    # Flexible spacer in middle
    var spacer := Control.new()
    spacer.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    _hud_container.add_child(spacer)

    # Add score on right
    _score_label.text = "Score: 0"

func update_health(current: int, maximum: int) -> void:
    _health_label.text = "Health: %d/%d" % [current, maximum]

func update_score(score: int) -> void:
    _score_label.text = "Score: %d" % score
```

**Key points:**
- HBoxContainer for left-right layout
- Use Control node with SIZE_EXPAND_FILL as spacer between elements
- Flexible spacer pushes elements to edges
- Perfect for game HUDs

### Problem: Need complex nested layout (sidebar + main content area)

**Solution: Combine multiple containers**

```gdscript
# Layout: HBox (Sidebar | VBox (Header, Content))
extends Control

@onready var _main_hbox: HBoxContainer = %MainHBoxContainer
@onready var _sidebar: PanelContainer = %Sidebar
@onready var _content_vbox: VBoxContainer = %ContentVBoxContainer
@onready var _header: Control = %Header
@onready var _content_area: Control = %ContentArea

func _ready() -> void:
    # Sidebar on left - fixed width
    _sidebar.custom_minimum_size = Vector2(250, 0)
    _sidebar.size_flags_vertical = Control.SIZE_EXPAND_FILL

    # Content area on right - fills remaining space
    _content_vbox.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    _content_vbox.size_flags_vertical = Control.SIZE_EXPAND_FILL

    # Header fills width, fixed height
    _header.custom_minimum_size = Vector2(0, 80)
    _header.size_flags_horizontal = Control.SIZE_EXPAND_FILL

    # Main content expands to fill
    _content_area.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    _content_area.size_flags_vertical = Control.SIZE_EXPAND_FILL
```

**Key points:**
- Nest containers for complex layouts
- Use custom_minimum_size to fix width/height of sections
- Combine SIZE_EXPAND_FILL to fill remaining space
- Test at different resolutions to ensure responsive

## Anti-Patterns

### Problem: Animating container children directly doesn't work

**Solution: Never animate children inside containers**

```gdscript
# Bad - container repositions child immediately
extends VBoxContainer

func _ready() -> void:
    var button := Button.new()
    add_child(button)

    # Won't work - container overrides position
    var tween := create_tween()
    tween.tween_property(button, "position", Vector2(100, 0), 1.0)

# Good - wrap child in Control, animate wrapper
extends Control

@onready var _container: VBoxContainer = %Container
@onready var _button_wrapper: Control = %ButtonWrapper

func _ready() -> void:
    var button := Button.new()
    _button_wrapper.add_child(button)

    # Animate wrapper instead
    var tween := create_tween()
    tween.tween_property(_button_wrapper, "position", Vector2(100, 0), 1.0)
```

**Key points:**
- Containers override child positions on resize
- Never animate container children directly
- Wrap animatable element in Control node to animate

### Problem: EXPAND flag set but children not filling space

**Solution: Must combine EXPAND with FILL**

```gdscript
# Bad - EXPAND without FILL
extends HBoxContainer

func _ready() -> void:
    var button := Button.new()
    button.size_flags_horizontal = Control.SIZE_EXPAND
    # Button requests space but doesn't fill it - appears small
    add_child(button)

# Good - EXPAND_FILL
extends HBoxContainer

func _ready() -> void:
    var button := Button.new()
    button.size_flags_horizontal = Control.SIZE_EXPAND_FILL
    # Button fills allocated space
    add_child(button)
```

**Key points:**
- EXPAND allocates space but doesn't fill it
- FILL fills allocated space but doesn't request extra
- EXPAND_FILL does both (most common use)

### Problem: GridContainer defaulting to single column layout

**Solution: Always set columns property**

```gdscript
# Bad - defaults to 1 column
var grid := GridContainer.new()
add_child(grid)
# Acts like VBoxContainer instead of grid

# Good - set columns
var grid := GridContainer.new()
grid.columns = 4
add_child(grid)
# Now creates actual 4-column grid
```

**Key points:**
- GridContainer.columns defaults to 1 (acts like VBoxContainer)
- Always explicitly set columns property
- Rows auto-calculated: ceil(child_count / columns)

### Problem: ScrollContainer not scrolling

**Solution: Ensure child exceeds container size**

```gdscript
# Bad - ScrollContainer only scrolls if child exceeds size
extends ScrollContainer

func _ready() -> void:
    var content := VBoxContainer.new()
    add_child(content)
    # Nothing to scroll - content isn't tall enough

# Good - give child sufficient size
extends ScrollContainer

func _ready() -> void:
    scroll_vertical_enabled = true

    var content := VBoxContainer.new()
    content.custom_minimum_size = Vector2(0, 2000)  # Tall enough to scroll
    add_child(content)

    # Now scrolling works
```

**Key points:**
- ScrollContainer only adds scrollbars if child exceeds container size
- Set child custom_minimum_size to ensure content is large enough
- Enable scroll_vertical_enabled and/or scroll_horizontal_enabled

### Problem: Theme items not applying to custom control

**Solution: Access theme items in _draw() with get_theme_*() methods**

```gdscript
# Bad - custom control doesn't use theme
extends Control

func _draw() -> void:
    draw_string(null, Vector2(10, 10), "Text")
    # Hard to customize

# Good - use theme items
extends Control

func _draw() -> void:
    var font: Font = get_theme_font("font")
    var font_size: int = get_theme_font_size("font_size")
    var color: Color = get_theme_color("font_color")

    draw_string(font, Vector2(10, 10), "Text", HORIZONTAL_ALIGNMENT_LEFT, -1, font_size, color)
    # Can be styled with theme
```

**Key points:**
- Use get_theme_color(), get_theme_font(), etc. in custom controls
- Specify theme type (custom name) as second parameter
- Built-in controls automatically use their class name as theme type

## Best Practices

### Always Use Containers for UI Layout

```gdscript
# Good - responsive on any screen size
extends VBoxContainer
# Children auto-arranged, adapt to window resize

# Bad - hardcoded positions
extends Control
func _ready() -> void:
    button.position = Vector2(100, 200)  # Breaks on different resolutions
```

### Set custom_minimum_size on Content

```gdscript
# Good - prevents squishing
extends Control

func _ready() -> void:
    button.custom_minimum_size = Vector2(200, 50)
    # Buttons never smaller than 200x50
    # Containers respect this

# Bad - content squeezed by containers
extends Control

func _ready() -> void:
    button.size = Vector2(200, 50)
    # Ignored by container
```

### Test Layouts at Multiple Resolutions

```gdscript
# In _ready(), print actual sizes to verify layout
extends Control

func _ready() -> void:
    print("Window size: ", get_viewport_rect().size)
    print("Button size: ", button.size)
    print("Container size: ", container.size)

    # Verify layout adapts properly
```

### Document Complex Nested Containers

```gdscript
# Structure: MarginContainer (padding)
#   └─ VBoxContainer (vertical layout)
#       ├─ HBoxContainer (header)
#       │   ├─ Label (title)
#       │   └─ Control (spacer)
#       │   └─ Label (time)
#       └─ TabContainer (main content)

extends Control

func _ready() -> void:
    # Layout tree is complex, document structure
    pass
```

## Related

- [Containers Reference](../ui/containers.md) - Detailed container properties
- [Themes Reference](../ui/themes.md) - Theming system details
- [Controls Reference](../ui/controls.md) - Base Control properties
- [Signals Reference](../patterns/signals.md) - Button and control signals
