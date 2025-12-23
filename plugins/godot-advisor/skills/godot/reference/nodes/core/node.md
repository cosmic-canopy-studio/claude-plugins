---
class: Node
source: repos/godot-docs/classes/class_node.rst
generated: 2025-12-21
---

# Node

**Inherits:** Object

**Inherited By:** AnimationMixer, AudioStreamPlayer, CanvasItem, CanvasLayer, EditorFileSystem, EditorPlugin, EditorResourcePreview, HTTPRequest, InstancePlaceholder, MissingNode, MultiplayerSpawner, MultiplayerSynchronizer, NavigationAgent2D, NavigationAgent3D, Node3D, ResourcePreloader, ShaderGlobalsOverride, StatusIndicator, Timer, Viewport, WorldEnvironment

Base class for all scene objects.

## Description

Nodes are Godot's building blocks. They can be assigned as the child of another node, resulting in a tree arrangement. A given node can contain any number of nodes as children with the requirement that all siblings (direct children of a node) should have unique names.

A tree of nodes is called a scene. Scenes can be saved to the disk and then instantiated into other scenes. This allows for very high flexibility in the architecture and data model of Godot projects.

**Scene tree:** The SceneTree contains the active tree of nodes. When a node is added to the scene tree, it receives the NOTIFICATION_ENTER_TREE notification and its `_enter_tree()` callback is triggered. Child nodes are always added after their parent node.

**Processing:** Nodes can override the "process" state, so that they receive a callback on each frame requesting them to process. Normal processing (callback `_process()`, toggled with `set_process()`) happens as fast as possible and is dependent on the frame rate. Physics processing (callback `_physics_process()`, toggled with `set_physics_process()`) happens a fixed number of times per second (60 by default).

**Groups:** Nodes can be added to as many groups as you want to be easy to manage. You could create groups like "enemies" or "collectables" for example, depending on your game.

## Properties

| Type | Property | Default |
|------|----------|---------|
| AutoTranslateMode | auto_translate_mode | 0 |
| String | editor_description | "" |
| MultiplayerAPI | multiplayer | |
| StringName | name | |
| Node | owner | |
| PhysicsInterpolationMode | physics_interpolation_mode | 0 |
| ProcessMode | process_mode | 0 |
| int | process_physics_priority | 0 |
| int | process_priority | 0 |
| ProcessThreadGroup | process_thread_group | 0 |
| int | process_thread_group_order | |
| BitField[ProcessThreadMessages] | process_thread_messages | |
| String | scene_file_path | |
| bool | unique_name_in_owner | false |

## Methods

| Return Type | Method |
|-------------|--------|
| void | `_enter_tree()` virtual |
| void | `_exit_tree()` virtual |
| void | `_input(event: InputEvent)` virtual |
| void | `_physics_process(delta: float)` virtual |
| void | `_process(delta: float)` virtual |
| void | `_ready()` virtual |
| void | `_unhandled_input(event: InputEvent)` virtual |
| void | `add_child(node: Node, force_readable_name: bool = false, internal: InternalMode = 0)` |
| void | `add_sibling(sibling: Node, force_readable_name: bool = false)` |
| void | `add_to_group(group: StringName, persistent: bool = false)` |
| Tween | `create_tween()` |
| Node | `duplicate(flags: int = 15)` const |
| Node | `find_child(pattern: String, recursive: bool = true, owned: bool = true)` const |
| Array[Node] | `find_children(pattern: String, type: String = "", recursive: bool = true, owned: bool = true)` const |
| Node | `find_parent(pattern: String)` const |
| Node | `get_child(idx: int, include_internal: bool = false)` const |
| int | `get_child_count(include_internal: bool = false)` const |
| Array[Node] | `get_children(include_internal: bool = false)` const |
| Array[StringName] | `get_groups()` const |
| int | `get_index(include_internal: bool = false)` const |
| Node | `get_node(path: NodePath)` const |
| Node | `get_node_or_null(path: NodePath)` const |
| Node | `get_parent()` const |
| NodePath | `get_path()` const |
| NodePath | `get_path_to(node: Node, use_unique_path: bool = false)` const |
| float | `get_physics_process_delta_time()` const |
| float | `get_process_delta_time()` const |
| SceneTree | `get_tree()` const |
| String | `get_tree_string()` |
| Viewport | `get_viewport()` const |
| Window | `get_window()` const |
| bool | `has_node(path: NodePath)` const |
| bool | `is_ancestor_of(node: Node)` const |
| bool | `is_in_group(group: StringName)` const |
| bool | `is_inside_tree()` const |
| bool | `is_node_ready()` const |
| bool | `is_physics_processing()` const |
| bool | `is_processing()` const |
| bool | `is_processing_input()` const |
| bool | `is_processing_unhandled_input()` const |
| void | `move_child(child_node: Node, to_index: int)` |
| void | `print_tree()` |
| void | `print_tree_pretty()` |
| void | `propagate_call(method: StringName, args: Array = [], parent_first: bool = false)` |
| void | `propagate_notification(what: int)` |
| void | `queue_free()` |
| void | `remove_child(node: Node)` |
| void | `remove_from_group(group: StringName)` |
| void | `reparent(new_parent: Node, keep_global_transform: bool = true)` |
| void | `replace_by(node: Node, keep_groups: bool = false)` |
| void | `request_ready()` |
| Error | `rpc(method: StringName, ...)` vararg |
| Error | `rpc_id(peer_id: int, method: StringName, ...)` vararg |
| void | `set_physics_process(enable: bool)` |
| void | `set_process(enable: bool)` |
| void | `set_process_input(enable: bool)` |
| void | `set_process_unhandled_input(enable: bool)` |

## Signals

- **child_entered_tree**(node: Node)
  - Emitted when the child node enters the SceneTree

- **child_exiting_tree**(node: Node)
  - Emitted when the child node is about to exit the SceneTree

- **child_order_changed**()
  - Emitted when the list of children is changed

- **ready**()
  - Emitted when the node is considered ready, after `_ready()` is called

- **renamed**()
  - Emitted when the node's name is changed, if the node is inside the tree

- **tree_entered**()
  - Emitted when the node enters the tree

- **tree_exited**()
  - Emitted after the node exits the tree and is no longer active

- **tree_exiting**()
  - Emitted when the node is just about to exit the tree

## Key Concepts

### Scene Tree Lifecycle

The order of callbacks when adding nodes to the scene tree:
1. Parent's `_enter_tree()`
2. Children's `_enter_tree()` (in tree order)
3. Children's `_ready()` (reverse order - children first)
4. Parent's `_ready()`

This means children are always ready before their parents, allowing parents to safely access initialized child state.

### Processing Callbacks

- **Normal processing** (`_process(delta)`): Called every frame at variable rate (frame-dependent)
- **Physics processing** (`_physics_process(delta)`): Called at fixed rate (60 Hz by default)

Use `_physics_process()` for physics-related code for deterministic behavior. Use `_process()` for visual updates and frame-dependent logic.

### Input Handling

- `_input(event)`: Receives all input events - can be overkill for most cases
- `_unhandled_input(event)`: Receives events not handled by UI (recommended for game logic)

UI Control nodes handle input first, then `_unhandled_input()` receives what's left.

### Node Ownership

The `owner` property tracks which node "owns" this node in the context of scene instantiation. This is primarily used by the editor but is also useful for tools and serialization.

### Groups

Groups provide a way to tag nodes for batch operations:
- Add: `add_to_group("enemies")`
- Check: `is_in_group("enemies")`
- Remove: `remove_from_group("enemies")`
- Operate: `get_tree().call_group("enemies", "take_damage", 10)`

### Node Paths

Node paths (NodePath) are used to reference other nodes:
- Absolute: `/root/MainScene/Player`
- Relative: `../../Enemy` or `Weapon/Sprite`
- Use `get_node()` or the shorthand `$NodeName`

## Best Practices

- Use `queue_free()` instead of `free()` for safer node deletion (waits until safe point)
- Access child nodes in `_ready()`, not `_init()` or `_enter_tree()` - children may not be ready yet
- Use `_physics_process()` for physics, `_process()` for visuals
- Use `_unhandled_input()` instead of `_input()` for game logic to avoid conflict with UI
- Disable processing when not needed: `set_process(false)` and `set_physics_process(false)`
- Use groups for batch operations on similar nodes (enemies, collectibles, etc.)
- When freeing a node, it automatically frees all its children

## Anti-Patterns

- Don't access child nodes in `_enter_tree()` - they may not be initialized
- Don't use `_process()` for physics calculations - frame rate dependency causes issues
- Don't use `free()` in game logic - use `queue_free()` to avoid crashes
- Don't forget to remove from groups before freeing if you have persistent group references
- Don't use `_input()` for game controls - UI will intercept, use `_unhandled_input()`

## Common Patterns

```gdscript
# Safe node initialization
extends Node2D

@onready var weapon: Weapon = $Weapon  # Safe: assigned after children are ready

func _ready() -> void:
    # All children are ready here
    weapon.set_damage(10)
```

```gdscript
# Group-based enemy management
extends CharacterBody2D

func _ready() -> void:
    add_to_group("enemies")

func take_damage(amount: int) -> void:
    health -= amount
    if health <= 0:
        remove_from_group("enemies")  # Clean up
        queue_free()

# Somewhere else:
# get_tree().call_group("enemies", "take_damage", 5)
```

```gdscript
# Conditional processing
extends Node

var is_active: bool = false

func _ready() -> void:
    set_process(false)  # Start disabled

func activate() -> void:
    is_active = true
    set_process(true)  # Enable only when needed

func deactivate() -> void:
    is_active = false
    set_process(false)  # Save performance

func _process(delta: float) -> void:
    # Only runs when active
    pass
```

```gdscript
# Physics vs visual processing
extends CharacterBody2D

var velocity_visual: Vector2  # Smoothed for display

func _physics_process(delta: float) -> void:
    # Physics: deterministic, fixed timestep
    velocity = calculate_physics_velocity(delta)
    move_and_slide()

func _process(delta: float) -> void:
    # Visuals: smooth interpolation for display
    velocity_visual = velocity_visual.lerp(velocity, 10.0 * delta)
    $Arrow.rotation = velocity_visual.angle()
```

```gdscript
# Safe input handling
extends Node2D

func _unhandled_input(event: InputEvent) -> void:
    # Only receives input not handled by UI
    if event.is_action_pressed("shoot"):
        shoot()
        get_viewport().set_input_as_handled()  # Mark as handled
```

## Performance Considerations

- Nodes with processing enabled (`_process`, `_physics_process`) have a per-frame cost
- Large node hierarchies increase tree traversal costs
- Use `call_deferred()` for operations that should wait until safe (e.g., during physics callbacks)
- Node pooling (reusing nodes instead of create/destroy) can improve performance in particle-heavy games
