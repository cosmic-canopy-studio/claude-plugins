---
topic: inventory-system
version: 2025.12.21
godot_version: "4.3"
sources:
  - repos/godot_node_essentials/screens/panel_container/drag_drop_inventory_ui
  - repos/godot_node_essentials/screens/button/shop_ui
  - repos/godot_node_essentials/screens/option_button/skill_slots_ui
  - https://dev.to/pdeveloper/godot-4x-drag-and-drop-5g13
  - https://github.com/jlucaso1/drag-drop-inventory
---

# Inventory System

Patterns for item management, drag-and-drop, slots, and stacking in Godot.

## Item Resources {#item-resources}

Define items as custom resources for data-driven design:

```gdscript
# item_resource.gd
extends Resource
class_name ItemResource

@export var item_name: String = ""
@export var icon: Texture2D = null
@export var description: String = ""
@export var max_stack: int = 1
@export var value: int = 0
@export var item_type: ItemType = ItemType.CONSUMABLE

enum ItemType {
    CONSUMABLE,
    EQUIPMENT,
    QUEST,
    MATERIAL
}
```

### Creating Item Resources

```gdscript
# In FileSystem, create .tres files:
# res://items/health_potion.tres
# - Set item_name = "Health Potion"
# - Set icon = preload("res://icons/potion.png")
# - Set max_stack = 99

# Or create programmatically:
var item := ItemResource.new()
item.item_name = "Gold Coin"
item.max_stack = 999
```

## Inventory Slot {#inventory-slot}

Basic slot with TextureRect for visual display:

```gdscript
# inventory_slot.gd
extends PanelContainer
class_name InventorySlot

var item: ItemResource = null
var quantity: int = 0

@onready var texture_rect: TextureRect = %TextureRect
@onready var quantity_label: Label = %QuantityLabel

func set_item(new_item: ItemResource, new_quantity: int = 1) -> void:
    item = new_item
    quantity = new_quantity
    _update_display()

func clear() -> void:
    item = null
    quantity = 0
    _update_display()

func _update_display() -> void:
    if item == null:
        texture_rect.texture = null
        quantity_label.hide()
    else:
        texture_rect.texture = item.icon
        quantity_label.text = str(quantity)
        quantity_label.visible = quantity > 1
```

## Drag and Drop System {#drag-drop}

Use Godot's built-in drag and drop functions with forwarding:

```gdscript
# inventory_ui.gd
extends Control

var _last_dragged_slot: InventorySlot = null

func _ready() -> void:
    # Find all slots and forward drag events
    var slots: Array[InventorySlot] = []
    slots.assign(get_tree().get_nodes_in_group("inventory_slots"))

    for slot in slots:
        slot.set_drag_forwarding(
            _get_drag_data_fw.bind(slot),
            _can_drop_data_fw,
            _drop_data_fw.bind(slot)
        )

func _get_drag_data_fw(_position: Vector2, source_slot: InventorySlot) -> Dictionary:
    if source_slot.item == null:
        return {}

    _last_dragged_slot = source_slot
    var data := {
        "item": source_slot.item,
        "quantity": source_slot.quantity,
        "source_slot": source_slot
    }

    # Create drag preview
    set_drag_preview(_make_preview(source_slot.item.icon))

    # Clear source slot visually (restore on drop cancel)
    source_slot.texture_rect.modulate = Color(1, 1, 1, 0.5)

    return data

func _can_drop_data_fw(_position: Vector2, data: Variant) -> bool:
    return data is Dictionary and data.has("item")

func _drop_data_fw(_position: Vector2, data: Dictionary, target_slot: InventorySlot) -> void:
    var source_slot: InventorySlot = data.source_slot
    source_slot.texture_rect.modulate = Color.WHITE

    # Empty slot: move item
    if target_slot.item == null:
        target_slot.set_item(data.item, data.quantity)
        source_slot.clear()
    # Same item: try to stack
    elif target_slot.item == data.item:
        var space := target_slot.item.max_stack - target_slot.quantity
        var to_add := mini(data.quantity, space)
        target_slot.quantity += to_add
        target_slot._update_display()

        var remaining := data.quantity - to_add
        if remaining > 0:
            source_slot.set_item(data.item, remaining)
        else:
            source_slot.clear()
    # Different item: swap
    else:
        var temp_item := target_slot.item
        var temp_qty := target_slot.quantity

        target_slot.set_item(data.item, data.quantity)
        source_slot.set_item(temp_item, temp_qty)

func _make_preview(texture: Texture2D) -> TextureRect:
    var preview := TextureRect.new()
    preview.texture = texture
    preview.size = Vector2(64, 64)
    preview.expand_mode = TextureRect.EXPAND_FIT_WIDTH_PROPORTIONAL
    preview.stretch_mode = TextureRect.STRETCH_KEEP_ASPECT
    return preview
```

## Drag Recovery {#drag-recovery}

Prevent items from being lost when dragged outside the inventory:

```gdscript
# recovery_panel.gd
extends PanelContainer

signal data_recovered(item_data: Dictionary)

func _can_drop_data(_position: Vector2, data: Variant) -> bool:
    return data is Dictionary and data.has("item")

func _drop_data(_position: Vector2, data: Dictionary) -> void:
    data_recovered.emit(data)
```

### Integration

```gdscript
# inventory_ui.gd
@onready var recovery_panel: PanelContainer = %RecoveryPanel

func _ready() -> void:
    recovery_panel.data_recovered.connect(_on_data_recovered)

func _on_data_recovered(data: Dictionary) -> void:
    # Return item to source slot
    if _last_dragged_slot:
        _last_dragged_slot.set_item(data.item, data.quantity)
        _last_dragged_slot.texture_rect.modulate = Color.WHITE
```

## Item Stacking {#stacking}

### Simple Stack Add

```gdscript
func add_item(item: ItemResource, quantity: int = 1) -> int:
    # Returns remaining quantity that couldn't be added

    # Try to stack with existing slots
    for slot in inventory_slots:
        if slot.item == item and slot.quantity < item.max_stack:
            var space := item.max_stack - slot.quantity
            var to_add := mini(quantity, space)
            slot.quantity += to_add
            slot._update_display()
            quantity -= to_add

            if quantity == 0:
                return 0

    # Add to empty slots
    for slot in inventory_slots:
        if slot.item == null:
            var to_add := mini(quantity, item.max_stack)
            slot.set_item(item, to_add)
            quantity -= to_add

            if quantity == 0:
                return 0

    return quantity  # Couldn't fit all items
```

### Split Stack

```gdscript
func _gui_input(event: InputEvent) -> void:
    if event is InputEventMouseButton and event.pressed:
        # Right-click to split stack
        if event.button_index == MOUSE_BUTTON_RIGHT and quantity > 1:
            var half := ceili(quantity / 2.0)
            quantity -= half
            _update_display()

            # Start dragging the split portion
            var data := {
                "item": item,
                "quantity": half,
                "source_slot": self
            }
            # Start drag with split data
```

## Shop/Trade System {#shop}

Inventory-based commerce system:

```gdscript
# shop_item.gd
extends Button
class_name ShopItem

var item_data: ItemResource = null
var cost: int = 0
var quantity: int = 1

func setup(item: ItemResource, price: int, stock: int) -> void:
    item_data = item
    cost = price
    quantity = stock
    _update_text()

func buy() -> bool:
    if PlayerInventory.gold < cost:
        return false

    if PlayerInventory.add_item(item_data) > 0:
        return false  # Inventory full

    PlayerInventory.gold -= cost
    quantity -= 1

    if quantity <= 0:
        queue_free()
    else:
        _update_text()

    return true

func _update_text() -> void:
    text = "%s - $%d (%d)" % [item_data.item_name, cost, quantity]
```

## Equipment Slots {#equipment}

Type-restricted slots for equipped items:

```gdscript
# equipment_slot.gd
extends InventorySlot
class_name EquipmentSlot

@export var allowed_type: ItemResource.ItemType = ItemResource.ItemType.EQUIPMENT

func _can_drop_data_fw(_position: Vector2, data: Variant) -> bool:
    if not (data is Dictionary and data.has("item")):
        return false

    var item: ItemResource = data.item
    return item.item_type == allowed_type

func _drop_data_fw(_position: Vector2, data: Dictionary, _target_slot: EquipmentSlot) -> void:
    var source_slot: InventorySlot = data.source_slot

    # If slot occupied, swap items
    if item != null:
        var temp_item := item
        var temp_qty := quantity
        set_item(data.item, data.quantity)
        source_slot.set_item(temp_item, temp_qty)
    else:
        set_item(data.item, data.quantity)
        source_slot.clear()

    # Emit signal for equipment changes
    equipment_changed.emit(item)

signal equipment_changed(equipped_item: ItemResource)
```

## Inventory Manager (Singleton) {#manager}

Global inventory state management:

```gdscript
# inventory_manager.gd - Autoload as "PlayerInventory"
extends Node

const MAX_SLOTS := 20

var slots: Array[Dictionary] = []  # {item: ItemResource, quantity: int}
var gold: int = 0

signal inventory_changed
signal item_added(item: ItemResource, quantity: int)
signal item_removed(item: ItemResource, quantity: int)

func _ready() -> void:
    slots.resize(MAX_SLOTS)
    for i in MAX_SLOTS:
        slots[i] = {"item": null, "quantity": 0}

func add_item(item: ItemResource, quantity: int = 1) -> int:
    var remaining := quantity

    # Stack with existing
    for slot in slots:
        if slot.item == item and slot.quantity < item.max_stack:
            var space := item.max_stack - slot.quantity
            var to_add := mini(remaining, space)
            slot.quantity += to_add
            remaining -= to_add

            if remaining == 0:
                break

    # Fill empty slots
    if remaining > 0:
        for slot in slots:
            if slot.item == null:
                var to_add := mini(remaining, item.max_stack)
                slot.item = item
                slot.quantity = to_add
                remaining -= to_add

                if remaining == 0:
                    break

    if remaining < quantity:
        item_added.emit(item, quantity - remaining)
        inventory_changed.emit()

    return remaining

func remove_item(item: ItemResource, quantity: int = 1) -> bool:
    var to_remove := quantity

    for slot in slots:
        if slot.item == item:
            var removed := mini(slot.quantity, to_remove)
            slot.quantity -= removed
            to_remove -= removed

            if slot.quantity == 0:
                slot.item = null

            if to_remove == 0:
                break

    if to_remove == 0:
        item_removed.emit(item, quantity)
        inventory_changed.emit()
        return true

    return false

func has_item(item: ItemResource, quantity: int = 1) -> bool:
    var count := 0
    for slot in slots:
        if slot.item == item:
            count += slot.quantity
            if count >= quantity:
                return true
    return false

func get_item_count(item: ItemResource) -> int:
    var count := 0
    for slot in slots:
        if slot.item == item:
            count += slot.quantity
    return count
```

## UI Refresh Pattern {#refresh}

Keep UI in sync with inventory state:

```gdscript
# inventory_ui.gd
extends Control

@onready var grid: GridContainer = %InventoryGrid

func _ready() -> void:
    PlayerInventory.inventory_changed.connect(_refresh_display)
    _refresh_display()

func _refresh_display() -> void:
    for i in grid.get_child_count():
        var slot_ui: InventorySlot = grid.get_child(i)
        var slot_data := PlayerInventory.slots[i]

        if slot_data.item:
            slot_ui.set_item(slot_data.item, slot_data.quantity)
        else:
            slot_ui.clear()
```

## Tooltips {#tooltips}

Show item information on hover:

```gdscript
# inventory_slot.gd
extends PanelContainer

@onready var tooltip: PanelContainer = %ItemTooltip

func _ready() -> void:
    mouse_entered.connect(_on_mouse_entered)
    mouse_exited.connect(_on_mouse_exited)
    tooltip.hide()

func _on_mouse_entered() -> void:
    if item == null:
        return

    tooltip.get_node("%NameLabel").text = item.item_name
    tooltip.get_node("%DescLabel").text = item.description
    tooltip.get_node("%ValueLabel").text = "Value: %d" % item.value

    tooltip.global_position = get_global_mouse_position() + Vector2(10, 10)
    tooltip.show()

func _on_mouse_exited() -> void:
    tooltip.hide()
```

## Grid-Based Inventory {#grid}

For Tetris-style inventories with variable item sizes:

```gdscript
# grid_inventory.gd
extends Control

# Each item has a grid size (e.g., 1x1, 2x1, 2x2)
class GridItem extends Resource:
    @export var base_item: ItemResource
    @export var grid_width: int = 1
    @export var grid_height: int = 1

var grid_width: int = 10
var grid_height: int = 5
var grid_cells: Array[Array] = []  # 2D array of occupied cells

func _ready() -> void:
    # Initialize grid
    for y in grid_height:
        var row: Array[GridItem] = []
        row.resize(grid_width)
        grid_cells.append(row)

func can_place_item(item: GridItem, grid_x: int, grid_y: int) -> bool:
    # Check if item fits
    if grid_x + item.grid_width > grid_width:
        return false
    if grid_y + item.grid_height > grid_height:
        return false

    # Check if cells are empty
    for y in item.grid_height:
        for x in item.grid_width:
            if grid_cells[grid_y + y][grid_x + x] != null:
                return false

    return true

func place_item(item: GridItem, grid_x: int, grid_y: int) -> bool:
    if not can_place_item(item, grid_x, grid_y):
        return false

    # Occupy cells
    for y in item.grid_height:
        for x in item.grid_width:
            grid_cells[grid_y + y][grid_x + x] = item

    return true
```

## Quick Slots / Hotbar {#quick-slots}

Fast-access slots for frequently used items:

```gdscript
# hotbar.gd
extends HBoxContainer

const SLOT_COUNT := 5

var hotbar_items: Array[ItemResource] = []

func _ready() -> void:
    hotbar_items.resize(SLOT_COUNT)

    for i in SLOT_COUNT:
        var slot := get_child(i) as InventorySlot
        slot.gui_input.connect(_on_slot_input.bind(i))

func _input(event: InputEvent) -> void:
    # Number keys 1-5 use hotbar items
    for i in SLOT_COUNT:
        if event.is_action_pressed("hotbar_%d" % (i + 1)):
            use_hotbar_item(i)

func use_hotbar_item(index: int) -> void:
    var item := hotbar_items[index]
    if item and item.item_type == ItemResource.ItemType.CONSUMABLE:
        # Use consumable
        use_item(item)

        # Remove from inventory
        if PlayerInventory.remove_item(item, 1):
            # Update hotbar display
            _refresh_slot(index)

func _on_slot_input(event: InputEvent, slot_index: int) -> void:
    # Right-click to clear hotbar slot
    if event is InputEventMouseButton:
        if event.button_index == MOUSE_BUTTON_RIGHT and event.pressed:
            hotbar_items[slot_index] = null
            _refresh_slot(slot_index)
```

## Best Practices & Pitfalls

### Do

- Use `set_drag_forwarding()` to centralize drag logic in parent container
- Create recovery panels to prevent item loss from failed drops
- Implement item stacking for stackable items (max_stack > 1)
- Use Resources for item data to enable reusable, data-driven items
- Disconnect from autoload signals (PlayerInventory) in `_exit_tree()`

### Don't

- Don't store inventory state in UI nodes - use a separate data layer
- Don't allow dropping items into invalid slots without validation
- Don't forget to update displays after inventory changes
- Don't hardcode item properties - use Resources instead
- Don't modify dragged item until drop succeeds

### Performance

```gdscript
# BAD: Refreshing entire inventory on every change
func _on_item_changed() -> void:
    for slot in all_slots:
        slot._update_display()

# GOOD: Update only changed slot
func _on_item_changed(slot_index: int) -> void:
    inventory_slots[slot_index]._update_display()
```

## Common Patterns

### Currency System

```gdscript
# Separate currency from items
var gold: int = 0

func add_gold(amount: int) -> void:
    gold += amount
    gold_changed.emit(gold)

func spend_gold(amount: int) -> bool:
    if gold >= amount:
        gold -= amount
        gold_changed.emit(gold)
        return true
    return false
```

### Item Usage

```gdscript
func use_item(item: ItemResource) -> void:
    match item.item_type:
        ItemResource.ItemType.CONSUMABLE:
            apply_consumable_effect(item)
            remove_item(item, 1)
        ItemResource.ItemType.EQUIPMENT:
            equip_item(item)
        _:
            push_warning("Cannot use item type: %s" % item.item_type)
```

## See Also

- [UI Controls](controls.md) - Button, TextureRect, GridContainer
- [Resources](../patterns/resources.md) - Custom Resource types
- [Signals](../patterns/signals.md) - Inventory change notifications
- [Save/Load](../patterns/save-load.md) - Persisting inventory state
