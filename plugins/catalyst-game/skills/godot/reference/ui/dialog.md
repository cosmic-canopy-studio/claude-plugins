---
topic: dialog-system
version: 2025.12.21
godot_version: "4.3"
sources:
  - repos/godot_node_essentials/screens/nine_patch_rect/stylized_dialog_box_ui/
  - repos/godot_node_essentials/screens/panel_container/fit_to_dialog_ui/
  - repos/godot_node_essentials/screens/label/animated_text_ui/
  - repos/godot_node_essentials/screens/audio_stream_player/dialogues_ui/
  - repos/godot_node_essentials/screens/rich_text_label/custom_bbcode_ui/
  - https://docs.godotengine.org/en/stable/classes/class_richtextlabel.html
  - https://github.com/nathanhoad/godot_dialogue_manager
---

# Dialog System

Create NPC conversations, text boxes, and interactive dialogue for your game.

## Basic Text Box {#text-box}

Simple dialog display with a Label:

```gdscript
extends Control

var lines: Array[String] = [
    "Welcome to the village!",
    "Watch out for monsters in the forest.",
    "Good luck on your journey!",
]

var _current_line: int = 0

@onready var _label: Label = %Label
@onready var _next_button: Button = %NextButton

func _ready() -> void:
    _next_button.pressed.connect(_advance_dialog)
    _show_line(_current_line)

func _show_line(index: int) -> void:
    if index >= lines.size():
        queue_free()  # Close dialog
        return

    _label.text = lines[index]
    _next_button.visible = true

func _advance_dialog() -> void:
    _current_line += 1
    _show_line(_current_line)
```

## Typewriter Effect {#typewriter}

Animate text appearing character by character using Tween and `visible_ratio`:

```gdscript
extends Control

const TEXT_DISPLAY_SPEED: float = 50.0  # Characters per second

var lines: Array[String] = [
    "What does all this do? I don't trust it,\ndon't touch anything.",
    "I found it! There's something under here!",
    "Thanks for the help!",
]

var _tween: Tween = null
var _current_line: int = 0

@onready var _label: Label = %Label
@onready var _next_button: Button = %NextButton

func _ready() -> void:
    _next_button.pressed.connect(_advance_dialog)
    _play_line(_current_line)

func _play_line(index: int) -> void:
    if index >= lines.size():
        queue_free()
        return

    _label.text = lines[index]
    _label.visible_ratio = 0.0
    _next_button.visible = false

    # Calculate duration based on text length
    var duration: float = _label.text.length() / TEXT_DISPLAY_SPEED

    # Animate visible_ratio from 0 to 1
    _tween = create_tween()
    _tween.tween_property(_label, "visible_ratio", 1.0, duration)
    _tween.tween_callback(func() -> void: _next_button.visible = true)

func _advance_dialog() -> void:
    _current_line += 1
    _play_line(_current_line)
```

### Skip to End

Allow players to skip the typewriter animation:

```gdscript
func _unhandled_input(event: InputEvent) -> void:
    if event.is_action_pressed("ui_accept"):
        _try_skip_or_advance()

func _try_skip_or_advance() -> void:
    # If animation is playing, skip to end
    if _tween != null and _tween.is_running():
        _tween.kill()
        _label.visible_ratio = 1.0
        _next_button.visible = true
        return

    # Otherwise advance to next line
    _advance_dialog()
```

## RichTextLabel Dialog {#rich-text}

Use RichTextLabel for formatted text with BBCode:

```gdscript
extends Control

const TEXT_DISPLAY_SPEED: float = 60.0

var lines: Array[String] = [
    "[color=yellow]Quest Updated:[/color] Find the ancient sword",
    "[wave]Magic words appear before you...[/wave]",
    "[shake][color=red]DANGER![/color][/shake] Boss approaching!",
]

var _tween: Tween = null
var _current_line: int = 0

@onready var _rich_text_label: RichTextLabel = %RichTextLabel
@onready var _continue_icon: TextureButton = %ContinueIcon

func _ready() -> void:
    _rich_text_label.bbcode_enabled = true
    _continue_icon.pressed.connect(_advance_dialog)
    _play_line(_current_line)

func _play_line(index: int) -> void:
    if index >= lines.size():
        queue_free()
        return

    _rich_text_label.text = lines[index]
    _rich_text_label.visible_ratio = 0.0
    _continue_icon.visible = false

    var duration: float = _rich_text_label.text.length() / TEXT_DISPLAY_SPEED

    _tween = create_tween()
    _tween.tween_property(_rich_text_label, "visible_ratio", 1.0, duration)
    _tween.tween_callback(_continue_icon.set_visible.bind(true))

func _advance_dialog() -> void:
    _current_line += 1
    _play_line(_current_line)
```

### Common BBCode for Dialog

| Tag | Effect | Example |
|-----|--------|---------|
| `[b]text[/b]` | Bold | `[b]Important![/b]` |
| `[i]text[/i]` | Italic | `[i]whispers[/i]` |
| `[color=red]text[/color]` | Color | `[color=red]Warning[/color]` |
| `[wave]text[/wave]` | Wave effect | `[wave]magical[/wave]` |
| `[shake]text[/shake]` | Shake effect | `[shake]earthquake[/shake]` |
| `[font_size=20]text[/font_size]` | Font size | `[font_size=24]LOUD[/font_size]` |

## Branching Dialogue {#branching}

Present player choices using buttons:

```gdscript
extends Control

class DialogueNode:
    var speaker: String
    var text: String
    var choices: Array[Choice] = []

class Choice:
    var text: String
    var next_node: String

    func _init(choice_text: String, next: String) -> void:
        text = choice_text
        next_node = next

var _nodes: Dictionary = {}
var _current_node: String = "start"

@onready var _speaker_label: Label = %SpeakerLabel
@onready var _text_label: Label = %TextLabel
@onready var _choices_container: VBoxContainer = %ChoicesContainer

func _ready() -> void:
    _setup_dialogue()
    _show_node(_current_node)

func _setup_dialogue() -> void:
    # Create dialogue nodes
    var start := DialogueNode.new()
    start.speaker = "Merchant"
    start.text = "Looking to buy something?"
    start.choices = [
        Choice.new("What do you have for sale?", "shop"),
        Choice.new("Tell me about this town.", "town_info"),
        Choice.new("Goodbye.", "end"),
    ]
    _nodes["start"] = start

    var shop := DialogueNode.new()
    shop.speaker = "Merchant"
    shop.text = "I've got potions, weapons, and armor!"
    shop.choices = [
        Choice.new("I'll take a look. [Open Shop]", "open_shop"),
        Choice.new("Not right now.", "start"),
    ]
    _nodes["shop"] = shop

    var town_info := DialogueNode.new()
    town_info.speaker = "Merchant"
    town_info.text = "This town is known for its skilled blacksmiths."
    town_info.choices = [
        Choice.new("Interesting. What else?", "start"),
    ]
    _nodes["town_info"] = town_info

func _show_node(node_id: String) -> void:
    if node_id == "end":
        queue_free()
        return

    if node_id == "open_shop":
        # Open shop interface
        queue_free()
        return

    var node: DialogueNode = _nodes.get(node_id)
    if node == null:
        push_error("Invalid dialogue node: " + node_id)
        return

    _speaker_label.text = node.speaker
    _text_label.text = node.text

    # Clear existing choice buttons
    for child in _choices_container.get_children():
        child.queue_free()

    # Create new choice buttons
    for choice in node.choices:
        var button := Button.new()
        button.text = choice.text
        button.pressed.connect(_on_choice_selected.bind(choice.next_node))
        _choices_container.add_child(button)

func _on_choice_selected(next_node: String) -> void:
    _current_node = next_node
    _show_node(_current_node)
```

## NPC Portrait {#portrait}

Display character portraits alongside dialogue:

```gdscript
extends Control

class DialogueLine:
    var speaker: String
    var portrait: Texture2D
    var text: String

    func _init(who: String, face: Texture2D, what: String) -> void:
        speaker = who
        portrait = face
        text = what

var lines: Array[DialogueLine] = []
var _current_line: int = 0

@onready var _portrait: TextureRect = %Portrait
@onready var _speaker_label: Label = %SpeakerLabel
@onready var _text_label: Label = %TextLabel
@onready var _next_button: Button = %NextButton

func _ready() -> void:
    # Setup dialogue
    lines = [
        DialogueLine.new("Guard", preload("res://portraits/guard.png"),
            "Halt! What business do you have here?"),
        DialogueLine.new("Hero", preload("res://portraits/hero.png"),
            "I'm looking for the ancient temple."),
        DialogueLine.new("Guard", preload("res://portraits/guard.png"),
            "The temple? That place is dangerous!"),
    ]

    _next_button.pressed.connect(_advance_dialog)
    _show_line(_current_line)

func _show_line(index: int) -> void:
    if index >= lines.size():
        queue_free()
        return

    var line: DialogueLine = lines[index]
    _portrait.texture = line.portrait
    _speaker_label.text = line.speaker
    _text_label.text = line.text

func _advance_dialog() -> void:
    _current_line += 1
    _show_line(_current_line)
```

## Dialog Box Styling {#styling}

### NinePatchRect Background

Use NinePatchRect for scalable dialog boxes:

```gdscript
extends NinePatchRect

func _ready() -> void:
    # Load a nine-patch texture
    texture = preload("res://ui/dialog_box.png")

    # Set patch margins (adjust based on your texture)
    patch_margin_left = 8
    patch_margin_top = 8
    patch_margin_right = 8
    patch_margin_bottom = 8

    # Set size
    custom_minimum_size = Vector2(400, 120)
```

### Auto-Size to Text

Use PanelContainer with Label to auto-size:

```gdscript
extends PanelContainer

@onready var _label: Label = %Label

func show_text(text: String) -> void:
    _label.text = text
    # PanelContainer automatically adjusts to label size
    reset_size()
```

## Audio Integration {#audio}

Play sound effects with dialogue:

```gdscript
extends Control

const TEXT_DISPLAY_SPEED: float = 50.0

var _tween: Tween = null

@onready var _label: Label = %Label
@onready var _typewriter_sound: AudioStreamPlayer = %TypewriterSound
@onready var _next_button: Button = %NextButton

func _ready() -> void:
    _next_button.pressed.connect(_advance_dialog)

func _play_line(text: String) -> void:
    _label.text = text
    _label.visible_ratio = 0.0

    # Play typewriter sound
    _typewriter_sound.play()

    var duration: float = text.length() / TEXT_DISPLAY_SPEED
    _tween = create_tween()
    _tween.tween_property(_label, "visible_ratio", 1.0, duration)
    _tween.tween_callback(_on_line_complete)

func _on_line_complete() -> void:
    _typewriter_sound.stop()
    _next_button.visible = true

func _advance_dialog() -> void:
    # Next line logic...
    pass
```

### Per-Character Sound

Play sound on each character reveal:

```gdscript
var _char_timer: float = 0.0
var _chars_per_sound: int = 2  # Play sound every N characters

func _process(delta: float) -> void:
    if _tween == null or not _tween.is_running():
        return

    var chars_visible: int = int(_label.visible_ratio * _label.text.length())
    var prev_chars: int = int((_label.visible_ratio - delta) * _label.text.length())

    if chars_visible / _chars_per_sound > prev_chars / _chars_per_sound:
        _typewriter_sound.play()
```

## Data-Driven Dialogue {#data-driven}

Store dialogue in JSON for easy editing:

```json
{
  "start": {
    "speaker": "Elder",
    "text": "Welcome, traveler. What brings you here?",
    "choices": [
      { "text": "I seek the ancient artifact.", "next": "quest_start" },
      { "text": "Just passing through.", "next": "goodbye" }
    ]
  },
  "quest_start": {
    "speaker": "Elder",
    "text": "Ah, the artifact! It lies deep in the forest.",
    "choices": [
      { "text": "I'll find it!", "next": "accept_quest" }
    ]
  }
}
```

Loading JSON dialogue:

```gdscript
extends Control

var _dialogue_data: Dictionary = {}
var _current_node: String = "start"

@onready var _speaker_label: Label = %SpeakerLabel
@onready var _text_label: Label = %TextLabel
@onready var _choices_container: VBoxContainer = %ChoicesContainer

func _ready() -> void:
    _load_dialogue()
    _show_node(_current_node)

func _load_dialogue() -> void:
    var file := FileAccess.open("res://dialogue/elder.json", FileAccess.READ)
    if file == null:
        push_error("Failed to load dialogue file")
        return

    var json := JSON.new()
    var parse_result := json.parse(file.get_as_text())
    if parse_result == OK:
        _dialogue_data = json.data
    else:
        push_error("Failed to parse dialogue JSON")

func _show_node(node_id: String) -> void:
    var node: Dictionary = _dialogue_data.get(node_id, {})
    if node.is_empty():
        push_error("Invalid dialogue node: " + node_id)
        return

    _speaker_label.text = node.get("speaker", "")
    _text_label.text = node.get("text", "")

    # Clear existing choices
    for child in _choices_container.get_children():
        child.queue_free()

    # Create choice buttons
    var choices: Array = node.get("choices", [])
    for choice in choices:
        var button := Button.new()
        button.text = choice.get("text", "")
        var next_node: String = choice.get("next", "")
        button.pressed.connect(_on_choice_selected.bind(next_node))
        _choices_container.add_child(button)

func _on_choice_selected(next_node: String) -> void:
    _current_node = next_node
    _show_node(_current_node)
```

## Custom BBCode Effects {#custom-effects}

Create custom RichTextLabel effects for unique dialogue animations:

```gdscript
@tool
class_name RichTextHover extends RichTextEffect

var bbcode := "hover"

func _process_custom_fx(char_fx: CharFXTransform) -> bool:
    var speed: float = char_fx.env.get("speed", 5.0)
    char_fx.offset.y = 5.0 * sin(char_fx.elapsed_time * speed)
    return true
```

Usage:

```gdscript
func _ready() -> void:
    _rich_text_label.install_effect(RichTextHover.new())
    _rich_text_label.text = "[hover]This text hovers![/hover]"
```

## Best Practices {#best-practices}

**Dialog Pacing**
- Use 40-60 characters per second for comfortable reading speed
- Shorter text (< 20 chars) can use faster speeds (80+ cps)
- Allow players to skip typewriter animations

**Input Handling**
- Use both mouse clicks and keyboard for advancing dialogue
- "Accept" action should skip animation OR advance to next line
- Don't block input during animations

**Visual Feedback**
- Show a continue indicator when dialogue is ready to advance
- Hide the indicator during typewriter animation
- Use audio cues for text appearing and advancing

**Performance**
- Kill tweens before creating new ones to prevent memory leaks
- Use `visible_ratio` instead of manually showing characters
- Cache preloaded resources (portraits, sounds)

**Accessibility**
- Support instant text display option (skip all typewriter effects)
- Ensure text is readable (size, contrast, font)
- Provide dialogue history/backlog for reviewing previous lines

## Related Patterns

- [UI Controls](/home/sam/code/godot_advisor/.claude/skills/godot/reference/ui/controls.md) - Button, Label, RichTextLabel basics
- [Containers](/home/sam/code/godot_advisor/.claude/skills/godot/reference/ui/containers.md) - Layout for dialog boxes and choice lists
- [Scene Transitions](/home/sam/code/godot_advisor/docs/references/godot/scene-transitions.md) - Fade in/out for dialogue boxes

## External Resources

**Official Documentation**
- [RichTextLabel - Godot Docs](https://docs.godotengine.org/en/stable/classes/class_richtextlabel.html)
- [RichTextEffect - Godot Docs](https://docs.godotengine.org/en/stable/classes/class_richtexteffect.html)

**Community Addons**
- [Dialogue Manager](https://github.com/nathanhoad/godot_dialogue_manager) - Powerful nonlinear dialogue system addon
- [gd_dialog](https://github.com/QueenChristina/gd_dialog) - Open source dialogue system for RPGs and visual novels
- [Typewriter Label](https://godotengine.org/asset-library/asset/4420) - Asset library typewriter effect node

**Tutorials**
- [How To Build A Dialogue Box In Godot 4 - GameDev Academy](https://gamedevacademy.org/godot-dialogue-box-tutorial/)
- [Building a Dialogue System in Godot - Wayline](https://www.wayline.io/blog/godot-dialogue-system-tutorial)
- [Simple Dialogue System Tutorial - World Eater Games](https://worldeater-dev.itch.io/bittersweet-birthday/devlog/224241/howto-a-simple-dialogue-system-in-godot)
