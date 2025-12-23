---
topic: ui-controls
version: 2025.12.19
godot_version: "4.3"
sources:
  - godot-button
  - godot-label
  - godot-line-edit
---

# UI Controls

Common Control nodes for user interfaces.

## Button {#button}

```gdscript
extends Button

func _ready() -> void:
    pressed.connect(_on_pressed)

func _on_pressed() -> void:
    print("Button clicked!")
```

### Button Signals

| Signal | Triggered When |
|--------|----------------|
| `pressed` | Button clicked/activated |
| `button_down` | Button pressed down |
| `button_up` | Button released |
| `toggled(pressed)` | Toggle button state changed |

### Toggle Button

```gdscript
extends Button

func _ready() -> void:
    toggle_mode = true
    toggled.connect(_on_toggled)

func _on_toggled(is_pressed: bool) -> void:
    if is_pressed:
        print("ON")
    else:
        print("OFF")
```

### Button with Icon

```gdscript
func _ready() -> void:
    icon = preload("res://icons/play.png")
    icon_alignment = HORIZONTAL_ALIGNMENT_LEFT
    text = "Play Game"
```

## Label

```gdscript
extends Label

func _ready() -> void:
    text = "Score: 0"
    horizontal_alignment = HORIZONTAL_ALIGNMENT_CENTER

func update_score(score: int) -> void:
    text = "Score: %d" % score
```

### Auto-Sizing

```gdscript
# Fit to text
autowrap_mode = TextServer.AUTOWRAP_OFF
custom_minimum_size = Vector2.ZERO  # Shrink to content

# Fixed width with wrap
autowrap_mode = TextServer.AUTOWRAP_WORD_SMART
custom_minimum_size.x = 200
```

## LineEdit (Text Input) {#line-edit}

```gdscript
extends LineEdit

func _ready() -> void:
    placeholder_text = "Enter name..."
    max_length = 20
    text_submitted.connect(_on_submitted)

func _on_submitted(new_text: String) -> void:
    print("Entered: ", new_text)
```

### LineEdit Signals

| Signal | Triggered When |
|--------|----------------|
| `text_changed(text)` | Text modified |
| `text_submitted(text)` | Enter pressed |

### Password Field

```gdscript
secret = true  # Shows dots instead of characters
```

## Slider {#slider}

```gdscript
extends HSlider  # or VSlider

func _ready() -> void:
    min_value = 0.0
    max_value = 100.0
    value = 50.0
    step = 1.0
    value_changed.connect(_on_value_changed)

func _on_value_changed(new_value: float) -> void:
    print("Slider: ", new_value)
```

### Volume Slider

```gdscript
func _ready() -> void:
    min_value = 0.0
    max_value = 1.0
    step = 0.01
    value = 1.0

func _on_value_changed(linear_volume: float) -> void:
    var bus_idx := AudioServer.get_bus_index("Master")
    AudioServer.set_bus_volume_db(bus_idx, linear_to_db(linear_volume))
```

## OptionButton (Dropdown) {#option-button}

```gdscript
extends OptionButton

func _ready() -> void:
    add_item("Easy", 0)
    add_item("Normal", 1)
    add_item("Hard", 2)
    select(1)  # Select "Normal"
    item_selected.connect(_on_item_selected)

func _on_item_selected(index: int) -> void:
    var difficulty := get_item_id(index)
    print("Selected difficulty: ", difficulty)
```

## CheckBox {#checkbox}

```gdscript
extends CheckBox

func _ready() -> void:
    text = "Enable music"
    button_pressed = true
    toggled.connect(_on_toggled)

func _on_toggled(enabled: bool) -> void:
    AudioManager.set_music_enabled(enabled)
```

## ProgressBar

```gdscript
extends ProgressBar

func _ready() -> void:
    min_value = 0
    max_value = 100
    value = 100
    show_percentage = false

func set_health(current: int, maximum: int) -> void:
    max_value = maximum
    value = current
```

### Animated Progress

```gdscript
func set_value_animated(new_value: float, duration: float = 0.3) -> void:
    var tween := create_tween()
    tween.tween_property(self, "value", new_value, duration)
```

## TextureButton

```gdscript
extends TextureButton

func _ready() -> void:
    texture_normal = preload("res://ui/button_normal.png")
    texture_hover = preload("res://ui/button_hover.png")
    texture_pressed = preload("res://ui/button_pressed.png")
    texture_disabled = preload("res://ui/button_disabled.png")

    pressed.connect(_on_pressed)
```

## RichTextLabel

For formatted text with BBCode:

```gdscript
extends RichTextLabel

func _ready() -> void:
    bbcode_enabled = true
    text = "[color=red]Warning![/color] Health low."

func show_damage(amount: int, is_crit: bool) -> void:
    if is_crit:
        append_text("[shake][color=yellow]CRIT! -%d[/color][/shake]" % amount)
    else:
        append_text("[color=red]-%d[/color]" % amount)
```

### Common BBCode

| Tag | Effect |
|-----|--------|
| `[b]text[/b]` | Bold |
| `[i]text[/i]` | Italic |
| `[color=red]text[/color]` | Color |
| `[font_size=20]text[/font_size]` | Font size |
| `[shake]text[/shake]` | Shake effect |
| `[wave]text[/wave]` | Wave effect |

## Tabs/TabContainer {#tabs}

```gdscript
extends TabContainer

func _ready() -> void:
    tab_changed.connect(_on_tab_changed)

func _on_tab_changed(tab_index: int) -> void:
    print("Switched to tab: ", get_tab_title(tab_index))
```

## Hover Effects {#hover}

```gdscript
extends Button

func _ready() -> void:
    mouse_entered.connect(_on_mouse_entered)
    mouse_exited.connect(_on_mouse_exited)

func _on_mouse_entered() -> void:
    scale = Vector2(1.1, 1.1)

func _on_mouse_exited() -> void:
    scale = Vector2.ONE
```

### Smooth Hover Animation

```gdscript
func _on_mouse_entered() -> void:
    var tween := create_tween()
    tween.tween_property(self, "scale", Vector2(1.1, 1.1), 0.1)

func _on_mouse_exited() -> void:
    var tween := create_tween()
    tween.tween_property(self, "scale", Vector2.ONE, 0.1)
```

## Focus Handling

```gdscript
# Set initial focus
button.grab_focus()

# Focus neighbors (for keyboard/gamepad navigation)
button1.focus_neighbor_bottom = button2.get_path()
button2.focus_neighbor_top = button1.get_path()

# Check focus
if button.has_focus():
    print("Button is focused")
```
