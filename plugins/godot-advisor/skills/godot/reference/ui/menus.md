---
topic: menus
version: 2025.12.21
godot_version: "4.3"
sources:
  - godot_node_essentials: screens/box_container/main_menu_ui/main_menu_ui.gd
  - godot_node_essentials: screens/button/animated_button_ui/animated_button_ui.gd
  - godot_node_essentials: screens/button/weapon_select_2d/weapon_select_2d.gd
  - godot_node_essentials: screens/sub_viewport/graphics_settings_3d/settings_ui.gd
  - godot_node_essentials: screens/option_button/difficulty_settings_ui/difficulty_settings_ui.gd
  - official_docs: https://docs.godotengine.org/en/stable/tutorials/ui/gui_navigation.html
  - official_docs: https://docs.godotengine.org/en/stable/classes/class_control.html
---

# Menus

Comprehensive patterns for main menus, pause menus, settings screens, and focus navigation in Godot 4.

## Main Menu Pattern {#main-menu}

### Basic Main Menu

```gdscript
# scenes/main_menu.gd
extends Control

@onready var play_button: Button = %PlayButton
@onready var options_button: Button = %OptionsButton
@onready var quit_button: Button = %QuitButton
@onready var quit_dialog: ConfirmationDialog = %QuitConfirmationDialog

func _ready() -> void:
    # Connect button signals
    play_button.pressed.connect(_on_play_pressed)
    options_button.pressed.connect(_on_options_pressed)
    quit_button.pressed.connect(_show_quit_confirmation)

    # Connect dialog signals
    quit_dialog.confirmed.connect(_on_quit_confirmed)

    # Set initial focus for keyboard/gamepad navigation
    play_button.grab_focus()

func _on_play_pressed() -> void:
    _disable_all_buttons()
    GameManager.start_game()

func _on_options_pressed() -> void:
    _disable_all_buttons()
    get_tree().change_scene_to_file("res://scenes/settings_menu.tscn")

func _show_quit_confirmation() -> void:
    quit_dialog.popup_centered()

func _on_quit_confirmed() -> void:
    get_tree().quit()

func _disable_all_buttons() -> void:
    play_button.disabled = true
    options_button.disabled = true
    quit_button.disabled = true
```

### Confirmation Dialog

```gdscript
# Use built-in ConfirmationDialog for quit confirmation
@onready var quit_dialog: ConfirmationDialog = %QuitConfirmationDialog

func _ready() -> void:
    quit_button.pressed.connect(quit_dialog.popup_centered)
    quit_dialog.confirmed.connect(func() -> void:
        get_tree().quit()
    )

    # Optional: customize dialog text
    quit_dialog.dialog_text = "Are you sure you want to quit?"
    quit_dialog.ok_button_text = "Quit"
    quit_dialog.cancel_button_text = "Cancel"
```

## Focus Navigation {#focus-navigation}

### Setting Initial Focus

Every UI scene needs initial focus for keyboard/gamepad navigation:

```gdscript
func _ready() -> void:
    # Method 1: Direct call (most common)
    first_button.grab_focus()

    # Method 2: Deferred (if UI not ready immediately)
    first_button.grab_focus.call_deferred()

    # Method 3: After waiting for layout
    await get_tree().process_frame
    menu_buttons[0].grab_focus()
```

### Tracking Focus Changes

```gdscript
@onready var menu_buttons: Array[Button] = [
    %PlayButton,
    %OptionsButton,
    %ExtrasButton,
    %ExitButton
]

func _ready() -> void:
    for button in menu_buttons:
        # Mouse hover triggers focus (unifies mouse + keyboard)
        button.mouse_entered.connect(button.grab_focus)

        # Track when button gains focus
        button.focus_entered.connect(_on_button_focused.bind(button))

        # Track when button loses focus
        button.focus_exited.connect(_on_button_unfocused.bind(button))

    menu_buttons[0].grab_focus()

func _on_button_focused(button: Button) -> void:
    # Animate selector, play sound, etc.
    selector_sprite.global_position = button.global_position

func _on_button_unfocused(button: Button) -> void:
    # Reset button appearance
    button.scale = Vector2.ONE
```

### Animated Focus Indicator

```gdscript
@onready var selector_2d: Sprite2D = %Selector2D
@onready var menu_buttons: Array[Button] = [%PlayButton, %OptionsButton, %ExitButton]

func _ready() -> void:
    for button in menu_buttons:
        button.mouse_entered.connect(button.grab_focus)
        button.focus_entered.connect(_move_selector.bind(button))
        button.focus_exited.connect(_unfocus_button.bind(button))
        button.pivot_offset = button.size / 2

    await get_tree().process_frame
    menu_buttons[0].grab_focus()

func _move_selector(button: Button) -> void:
    var tween := create_tween().set_parallel(true)

    # Move selector sprite to button
    tween.tween_property(selector_2d, "position", button.global_position, 0.15)\
        .set_trans(Tween.TRANS_QUAD)\
        .set_ease(Tween.EASE_OUT)

    # Scale up button slightly
    tween.tween_property(button, "scale", Vector2.ONE * 1.1, 0.3)\
        .set_trans(Tween.TRANS_CUBIC)\
        .set_ease(Tween.EASE_OUT)

func _unfocus_button(button: Button) -> void:
    var tween := create_tween()
    tween.tween_property(button, "scale", Vector2.ONE, 0.4)\
        .set_trans(Tween.TRANS_CUBIC)\
        .set_ease(Tween.EASE_IN)
```

### Focus Modes

Control nodes have three focus modes:

| Mode | Constant | Behavior |
|------|----------|----------|
| None | `FOCUS_NONE` | Cannot be focused (e.g., Label, Panel) |
| Click | `FOCUS_CLICK` | Focus only on mouse click |
| All | `FOCUS_ALL` | Focus on click OR keyboard navigation (default for buttons) |

```gdscript
# Set focus mode in code
button.focus_mode = Control.FOCUS_ALL

# Disable focus temporarily
button.focus_mode = Control.FOCUS_NONE
button.disabled = true
```

### Custom Focus Order

Override default navigation order:

```gdscript
# In editor: Inspector > Focus > Neighbor Left/Right/Up/Down/Next/Previous
# Or in code:
func _ready() -> void:
    button1.focus_neighbor_right = button2.get_path()
    button2.focus_neighbor_left = button1.get_path()
    button2.focus_neighbor_down = button3.get_path()
```

## Pause Menu Pattern {#pause-menu}

### Basic Pause Menu

```gdscript
# scenes/pause_menu.gd
extends CanvasLayer

@onready var pause_panel: PanelContainer = %PausePanel
@onready var resume_button: Button = %ResumeButton
@onready var settings_button: Button = %SettingsButton
@onready var quit_button: Button = %QuitButton

var is_paused: bool = false

func _ready() -> void:
    pause_panel.visible = false
    process_mode = Node.PROCESS_MODE_ALWAYS

    resume_button.pressed.connect(_on_resume_pressed)
    settings_button.pressed.connect(_on_settings_pressed)
    quit_button.pressed.connect(_on_quit_pressed)

func _input(event: InputEvent) -> void:
    if event.is_action_pressed("ui_cancel"):
        _toggle_pause()

func _toggle_pause() -> void:
    is_paused = !is_paused
    get_tree().paused = is_paused
    pause_panel.visible = is_paused

    if is_paused:
        resume_button.grab_focus()

func _on_resume_pressed() -> void:
    _toggle_pause()

func _on_settings_pressed() -> void:
    # Show settings overlay
    pass

func _on_quit_pressed() -> void:
    get_tree().paused = false
    get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
```

### Pause with Process Mode

The pause menu node needs `PROCESS_MODE_ALWAYS` to remain interactive:

```gdscript
func _ready() -> void:
    # Allow this node to process even when tree is paused
    process_mode = Node.PROCESS_MODE_ALWAYS
```

Scene structure:
```
PauseMenu (CanvasLayer, layer=100, process_mode=ALWAYS)
├── PausePanel (PanelContainer)
│   └── VBoxContainer
│       ├── ResumeButton
│       ├── SettingsButton
│       └── QuitButton
```

## Settings Menu Pattern {#settings-menu}

### Graphics Settings

```gdscript
# scenes/settings_menu.gd
extends PanelContainer

@onready var resolution_option: OptionButton = %ResolutionOptionButton
@onready var shadow_quality_slider: Slider = %ShadowQualityHSlider
@onready var msaa_option: OptionButton = %MSAAOptionButton
@onready var fxaa_toggle: Button = %FXAAToggleButton
@onready var reset_button: Button = %ResetButton

@onready var _sub_viewport: SubViewport = %SubViewport
@onready var _start_shadow_atlas_size := _sub_viewport.positional_shadow_atlas_size

func _ready() -> void:
    # Connect settings controls
    resolution_option.item_selected.connect(_set_resolution)
    shadow_quality_slider.value_changed.connect(_set_shadow_quality)
    msaa_option.item_selected.connect(_set_msaa)
    fxaa_toggle.toggled.connect(_set_fxaa)
    reset_button.pressed.connect(_reset_to_defaults)

    # Configure slider range
    shadow_quality_slider.max_value = RenderingServer.SHADOW_QUALITY_MAX - 1

    # Populate resolution dropdown
    _populate_resolutions()

func _populate_resolutions() -> void:
    for index in range(1, 5):
        var resolution := _sub_viewport.size / index
        var text := "%dx%d" % [resolution.x, resolution.y]
        resolution_option.add_item(text, index)

func _set_resolution(index: int) -> void:
    var scale := index + 1
    get_viewport().size = DisplayServer.screen_get_size() / scale

func _set_shadow_quality(value: int) -> void:
    _sub_viewport.positional_shadow_atlas_size = _start_shadow_atlas_size if value >= 0 else 0
    value = maxi(0, value)

    # For spot/omni lights
    RenderingServer.positional_soft_shadow_filter_set_quality(value)

    # For directional lights
    RenderingServer.directional_soft_shadow_filter_set_quality(value)

func _set_msaa(level: int) -> void:
    _sub_viewport.msaa_3d = level

func _set_fxaa(enabled: bool) -> void:
    _sub_viewport.screen_space_aa = Viewport.SCREEN_SPACE_AA_FXAA if enabled else Viewport.SCREEN_SPACE_AA_DISABLED

func _reset_to_defaults() -> void:
    shadow_quality_slider.value = 0
    fxaa_toggle.button_pressed = false
    resolution_option.select(0)
    _set_resolution(0)
    msaa_option.select(0)
    _set_msaa(0)
```

### Difficulty Settings with OptionButton

```gdscript
extends Control

# Map difficulty keys to display settings
var _difficulty_map := {
    easy = {text = "x1", modulate = Color.WHITE},
    medium = {text = "x2", modulate = Color.TOMATO},
    hard = {text = "x4", modulate = Color.RED},
}

@onready var stats_label: Label = %StatsLabel
@onready var difficulty_option: OptionButton = %DifficultyOptionButton

func _ready() -> void:
    difficulty_option.item_selected.connect(_on_difficulty_changed)
    _on_difficulty_changed(difficulty_option.selected)

func _on_difficulty_changed(index: int) -> void:
    var key := difficulty_option.get_item_text(index).to_lower()
    var settings: Dictionary = _difficulty_map.get(key, {})

    # Apply all properties from settings dict to label
    for prop: String in settings:
        stats_label.set(prop, settings[prop])
```

## Radio Buttons with ButtonGroup {#button-group}

Use ButtonGroup to create mutually exclusive buttons (radio buttons):

```gdscript
# Create ButtonGroup resource (save as weapon_select_group.tres)
# Or create in code:
@export var button_group: ButtonGroup = null

@onready var _player: CharacterBody2D = $Player

var _weapons_list: Array[PackedScene] = [
    preload("res://weapons/rocket_weapon.tscn"),
    preload("res://weapons/gatling_weapon.tscn"),
    preload("res://weapons/bomb_weapon.tscn"),
]

func _ready() -> void:
    if button_group == null:
        return

    # Listen for any button in group being pressed
    button_group.pressed.connect(_on_weapon_button_pressed)

    # Press first button by default
    button_group.get_buttons().front().button_pressed = true

func _on_weapon_button_pressed(button: BaseButton) -> void:
    # Get button's index in the group
    var weapon_idx := button_group.get_buttons().find(button)

    # Match index to weapon scene
    var weapon: Node2D = _weapons_list[weapon_idx].instantiate()

    # Switch player's weapon
    _player.change_weapon(weapon)
```

In the scene tree:
```
WeaponSelectUI
├── RocketButton (toggle_mode=true, button_group=weapon_select_group.tres)
├── GatlingButton (toggle_mode=true, button_group=weapon_select_group.tres)
└── BombButton (toggle_mode=true, button_group=weapon_select_group.tres)
```

## Button State Management {#button-states}

### Disable Buttons During Cooldown

```gdscript
@onready var action_buttons: Array[TextureButton] = [
    %AttackButton,
    %DefendButton,
    %ItemButton
]

@onready var progress_bar: ProgressBar = %ProgressBar

func _on_action_button_pressed(button: TextureButton) -> void:
    _set_buttons_disabled(true)

    # Show cooldown progress
    var cooldown_tween := create_tween()
    progress_bar.value = 100
    cooldown_tween.tween_property(progress_bar, "value", 0.0, 2.0)

    # Re-enable buttons after cooldown
    cooldown_tween.tween_callback(_set_buttons_disabled.bind(false))

func _set_buttons_disabled(is_disabled: bool) -> void:
    for button in action_buttons:
        button.disabled = is_disabled
        button.focus_mode = Control.FOCUS_NONE if is_disabled else Control.FOCUS_ALL

    # Grab focus on first button when re-enabled
    if not is_disabled:
        action_buttons[0].grab_focus()
```

### Conditional Button Enabling

```gdscript
# Shop example - enable/disable based on player currency
var player_cash: int = 100

@onready var grid_container: GridContainer = %GridContainer

func _update_shop_items() -> void:
    for shop_item: Button in grid_container.get_children():
        # Disable if player can't afford it
        shop_item.disabled = player_cash < shop_item.cost

func _on_item_purchased(cost: int) -> void:
    player_cash -= cost
    _update_shop_items()
```

## Animated Button Press {#animated-press}

```gdscript
func _ready() -> void:
    for button in menu_buttons:
        button.pressed.connect(_animate_button_press.bind(button))
        button.pivot_offset = button.size / 2

func _animate_button_press(button: Button) -> void:
    button.rotation_degrees = 30

    var tween := create_tween().set_parallel(true)

    # Animate selector moving off-screen
    tween.tween_property(selector_sprite, "offset", Vector2(-128, 57), 0.5)\
        .from(Vector2(0, 57))\
        .set_trans(Tween.TRANS_ELASTIC)\
        .set_ease(Tween.EASE_OUT)

    # Shrink button
    tween.tween_property(button, "scale", Vector2.ZERO, 0.5)\
        .set_trans(Tween.TRANS_ELASTIC)

    # Reset rotation
    tween.tween_property(button, "rotation", 0.0, 0.5)\
        .set_trans(Tween.TRANS_ELASTIC)\
        .set_ease(Tween.EASE_OUT)

    # Restore button scale after delay
    tween.tween_property(button, "scale", Vector2.ONE, 0.3)\
        .set_trans(Tween.TRANS_BOUNCE)\
        .set_ease(Tween.EASE_OUT)\
        .set_delay(0.75)
```

## Scene Transitions from Menus {#scene-transitions}

### With GameManager Autoload

```gdscript
# autoloads/game_manager.gd
extends Node

enum GameState { MENU, PLAYING, PAUSED, GAME_OVER }

var current_state: GameState = GameState.MENU

signal state_changed(new_state: GameState)

func start_game() -> void:
    current_state = GameState.PLAYING
    state_changed.emit(current_state)
    get_tree().change_scene_to_file("res://scenes/game.tscn")

func return_to_menu() -> void:
    current_state = GameState.MENU
    state_changed.emit(current_state)
    get_tree().change_scene_to_file("res://scenes/main_menu.tscn")

func quit_game() -> void:
    get_tree().quit()
```

### Menu Button Connections

```gdscript
# main_menu.gd
func _on_play_pressed() -> void:
    _disable_all_buttons()
    GameManager.start_game()

func _on_practice_pressed() -> void:
    _disable_all_buttons()
    GameManager.go_to_practice()

func _on_quit_pressed() -> void:
    GameManager.quit_game()
```

## Best Practices {#best-practices}

### Always Set Initial Focus

```gdscript
# GOOD
func _ready() -> void:
    first_button.grab_focus()

# BAD - keyboard/gamepad navigation won't work
func _ready() -> void:
    # No grab_focus() call
    pass
```

### Prevent Double-Click During Scene Changes

```gdscript
func _on_play_pressed() -> void:
    # Disable ALL buttons before changing scene
    play_button.disabled = true
    options_button.disabled = true
    quit_button.disabled = true
    GameManager.start_game()
```

### Use Process Mode for Pause Menus

```gdscript
# Pause menu must process during pause
func _ready() -> void:
    process_mode = Node.PROCESS_MODE_ALWAYS
```

### Unify Mouse and Keyboard Navigation

```gdscript
func _ready() -> void:
    for button in menu_buttons:
        # Mouse hover automatically grabs focus
        button.mouse_entered.connect(button.grab_focus)
```

### Store Settings Persistently

```gdscript
# Save settings to file
func _save_settings() -> void:
    var config := ConfigFile.new()
    config.set_value("graphics", "resolution", current_resolution)
    config.set_value("graphics", "shadows", shadow_quality)
    config.save("user://settings.cfg")

# Load settings on startup
func _load_settings() -> void:
    var config := ConfigFile.new()
    var err := config.load("user://settings.cfg")
    if err == OK:
        resolution_option.select(config.get_value("graphics", "resolution", 0))
        shadow_slider.value = config.get_value("graphics", "shadows", 2)
```

## Common Pitfalls

### Forgetting to Wait for Scene Ready

```gdscript
# BAD - buttons might not exist yet
func _ready() -> void:
    menu_buttons[0].grab_focus()

# GOOD - wait for scene to be fully ready
func _ready() -> void:
    await get_tree().process_frame
    menu_buttons[0].grab_focus()
```

### Not Cleaning Up Button Groups

```gdscript
# When removing buttons dynamically
func _remove_button(button: Button) -> void:
    if button.button_group:
        button.button_group = null  # Remove from group first
    button.queue_free()
```

### Hardcoded Focus Neighbors Break with Layout Changes

```gdscript
# BAD - breaks if you reorder buttons in editor
button1.focus_neighbor_down = NodePath("../Button2")

# GOOD - connect focus dynamically based on actual layout
func _ready() -> void:
    var buttons := get_children()
    for i in range(buttons.size() - 1):
        buttons[i].focus_neighbor_down = buttons[i + 1].get_path()
        buttons[i + 1].focus_neighbor_up = buttons[i].get_path()
```

## Related

- [Scene Transitions](../patterns/scene-transitions.md) - GameManager autoload pattern
- [Controls](controls.md) - Button, Label, and other UI nodes
- [Containers](containers.md) - VBoxContainer for menu layouts
- [Dialog](dialog.md) - ConfirmationDialog and custom popups
- [Input](../patterns/input.md) - Handling ui_cancel for pause menus
- [Tween](../animation/tween.md) - Animating menu elements
