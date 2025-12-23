# UI Systems Dispatcher

Routes to patterns for user interface development in Godot 4.

## Menus

| I want to... | Go to |
|--------------|-------|
| Create main menu | `reference/ui/menus.md#main-menu` |
| Pause menu with resume | `reference/ui/menus.md#pause` |
| Settings/options menu | `reference/ui/menus.md#settings` |
| Game over screen | `reference/ui/menus.md#game-over` |
| Level select | `reference/ui/menus.md#level-select` |

## HUD Elements

| I want to... | Go to |
|--------------|-------|
| Health bar | `reference/ui/bars.md#health` |
| Stamina/mana bar | `reference/ui/bars.md#resource` |
| Score display | `reference/ui/hud.md#score` |
| Ammo counter | `reference/ui/hud.md#ammo` |
| Minimap | `reference/ui/hud.md#minimap` |
| Timer/countdown | `reference/ui/hud.md#timer` |

## Dialogs & Popups

| I want to... | Go to |
|--------------|-------|
| Dialog box with text | `reference/ui/dialog.md#basic` |
| Typewriter text effect | `reference/ui/dialog.md#typewriter` |
| Choice dialogs | `reference/ui/dialog.md#choices` |
| Confirmation popup | `reference/ui/dialog.md#confirm` |
| Tooltip on hover | `reference/ui/dialog.md#tooltip` |

## Inventory & Items

| I want to... | Go to |
|--------------|-------|
| Grid inventory | `reference/ui/inventory.md#grid` |
| Drag and drop items | `reference/ui/inventory.md#drag-drop` |
| Item tooltips | `reference/ui/inventory.md#tooltips` |
| Equipment slots | `reference/ui/inventory.md#equipment` |
| Stack items | `reference/ui/inventory.md#stacking` |

## Layout & Containers

| I want to... | Go to |
|--------------|-------|
| Horizontal layout | `reference/ui/containers.md#hbox` |
| Vertical layout | `reference/ui/containers.md#vbox` |
| Grid layout | `reference/ui/containers.md#grid` |
| Center content | `reference/ui/containers.md#center` |
| Responsive scaling | `reference/ui/containers.md#anchors` |
| Margins/padding | `reference/ui/containers.md#margin` |

## Controls

| I want to... | Go to |
|--------------|-------|
| Button with click | `reference/ui/controls.md#button` |
| Text input field | `reference/ui/controls.md#line-edit` |
| Slider | `reference/ui/controls.md#slider` |
| Dropdown/options | `reference/ui/controls.md#option-button` |
| Checkbox | `reference/ui/controls.md#checkbox` |
| Tab container | `reference/ui/controls.md#tabs` |

## Theming & Styling

| I want to... | Go to |
|--------------|-------|
| Custom button style | `reference/ui/themes.md#button-style` |
| Global theme | `reference/ui/themes.md#global` |
| Font customization | `reference/ui/themes.md#fonts` |
| StyleBox for panels | `reference/ui/themes.md#stylebox` |

## Animation

| I want to... | Go to |
|--------------|-------|
| Fade in/out | `reference/animation/tween.md#fade` |
| Slide animation | `reference/animation/tween.md#slide` |
| Button hover effects | `reference/ui/controls.md#hover` |
| Screen transitions | `reference/patterns/scenes.md#transitions` |

## Focus & Navigation

| I want to... | Go to |
|--------------|-------|
| Keyboard navigation | `reference/ui/focus.md#keyboard` |
| Gamepad UI navigation | `reference/ui/focus.md#gamepad` |
| Focus neighbors | `reference/ui/focus.md#neighbors` |
| Default focus | `reference/ui/focus.md#default` |

## Quick Start: Main Menu

```gdscript
extends Control

func _ready() -> void:
    # Focus first button for keyboard/gamepad navigation
    $VBoxContainer/StartButton.grab_focus()

func _on_start_button_pressed() -> void:
    get_tree().change_scene_to_file("res://scenes/game.tscn")

func _on_options_button_pressed() -> void:
    $OptionsPanel.visible = true

func _on_quit_button_pressed() -> void:
    get_tree().quit()
```

**Scene Structure:**
```
Control (root, full rect anchor)
└── VBoxContainer (centered)
    ├── Label (game title)
    ├── StartButton
    ├── OptionsButton
    └── QuitButton
```

## Quick Start: Pause Menu

```gdscript
extends Control

func _ready() -> void:
    visible = false
    process_mode = Node.PROCESS_MODE_WHEN_PAUSED

func _input(event: InputEvent) -> void:
    if event.is_action_pressed("pause"):
        toggle_pause()

func toggle_pause() -> void:
    visible = !visible
    get_tree().paused = visible
    if visible:
        $VBoxContainer/ResumeButton.grab_focus()

func _on_resume_button_pressed() -> void:
    toggle_pause()

func _on_quit_button_pressed() -> void:
    get_tree().paused = false
    get_tree().change_scene_to_file("res://scenes/main_menu.tscn")
```

**Required:** Set `process_mode = PROCESS_MODE_WHEN_PAUSED` on pause menu root.
