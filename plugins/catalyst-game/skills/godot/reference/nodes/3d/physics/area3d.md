---
class: Area3D
version: 2025.12.21
godot_version: "4.3"
sources:
  - repos/godot-docs/classes/class_area3d.rst
---

# Area3D

**Inherits:** CollisionObject3D < Node3D < Node < Object

A region of 3D space that detects other CollisionObject3D's entering or exiting it.

## Description

Area3D is a region of 3D space defined by one or multiple CollisionShape3D or CollisionPolygon3D child nodes. It detects when other CollisionObject3D's enter or exit it, and it also keeps track of which collision objects haven't exited it yet (i.e. which one are overlapping it).

This node can also locally alter or override physics parameters (gravity, damping) and route audio to custom audio buses.

**Note:** Areas and bodies created with PhysicsServer3D might not interact as expected with Area3D's, and might not emit signals or track objects correctly.

**Warning:** Using a ConcavePolygonShape3D inside a CollisionShape3D child of this node may give unexpected results, since this collision shape is hollow. If this is not desired, it has to be split into multiple ConvexPolygonShape3D's or primitive shapes like BoxShape3D, or in some cases it may be replaceable by a CollisionPolygon3D.

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `monitoring` | bool | `true` | If true, area detects bodies/areas entering and exiting |
| `monitorable` | bool | `true` | If true, other areas can detect this area |
| `priority` | int | `0` | Higher priority areas processed first |
| `gravity_space_override` | SpaceOverride | `SPACE_OVERRIDE_DISABLED` | Override mode for gravity |
| `gravity` | float | `9.8` | Gravity intensity (meters per second squared) |
| `gravity_direction` | Vector3 | `Vector3(0, -1, 0)` | Gravity vector (not normalized) |
| `gravity_point` | bool | `false` | If true, gravity calculated from point |
| `gravity_point_center` | Vector3 | `Vector3(0, -1, 0)` | Point of attraction for gravity |
| `gravity_point_unit_distance` | float | `0.0` | Distance at which gravity equals gravity property |
| `linear_damp_space_override` | SpaceOverride | `SPACE_OVERRIDE_DISABLED` | Override mode for linear damping |
| `linear_damp` | float | `0.1` | Rate at which objects stop moving |
| `angular_damp_space_override` | SpaceOverride | `SPACE_OVERRIDE_DISABLED` | Override mode for angular damping |
| `angular_damp` | float | `0.1` | Rate at which objects stop spinning |
| `audio_bus_override` | bool | `false` | If true, area's audio bus overrides default |
| `audio_bus_name` | StringName | `"Master"` | Name of the area's audio bus |
| `reverb_bus_enabled` | bool | `false` | If true, area applies reverb to audio |
| `reverb_bus_name` | StringName | `"Master"` | Name of reverb bus |
| `reverb_bus_amount` | float | `0.0` | Reverb amount (0 to 1, 0.1 precision) |
| `reverb_bus_uniformity` | float | `0.0` | Reverb uniformity (0 to 1, 0.1 precision) |
| `wind_source_path` | NodePath | `NodePath("")` | Node3D for wind direction/origin |
| `wind_force_magnitude` | float | `0.0` | Area-specific wind force magnitude |
| `wind_attenuation_factor` | float | `0.0` | Exponential wind force decrease rate |

## Key Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `get_overlapping_areas()` | Array[Area3D] | Returns list of intersecting Area3D's |
| `get_overlapping_bodies()` | Array[Node3D] | Returns list of intersecting PhysicsBody3D's and GridMap's |
| `has_overlapping_areas()` | bool | Returns true if intersecting any Area3D |
| `has_overlapping_bodies()` | bool | Returns true if intersecting any PhysicsBody3D/GridMap |
| `overlaps_area(area)` | bool | Returns true if given Area3D overlaps this area |
| `overlaps_body(body)` | bool | Returns true if given body overlaps this area |

## Signals

| Signal | Parameters | Description |
|--------|-----------|-------------|
| `area_entered` | area: Area3D | Emitted when Area3D enters this area |
| `area_exited` | area: Area3D | Emitted when Area3D exits this area |
| `area_shape_entered` | area_rid, area, area_shape_index, local_shape_index | Emitted when Shape3D enters |
| `area_shape_exited` | area_rid, area, area_shape_index, local_shape_index | Emitted when Shape3D exits |
| `body_entered` | body: Node3D | Emitted when PhysicsBody3D/GridMap enters |
| `body_exited` | body: Node3D | Emitted when PhysicsBody3D/GridMap exits |
| `body_shape_entered` | body_rid, body, body_shape_index, local_shape_index | Emitted when body Shape3D enters |
| `body_shape_exited` | body_rid, body, body_shape_index, local_shape_index | Emitted when body Shape3D exits |

## Enums

### SpaceOverride

| Constant | Value | Description |
|----------|-------|-------------|
| `SPACE_OVERRIDE_DISABLED` | 0 | Does not affect gravity/damping |
| `SPACE_OVERRIDE_COMBINE` | 1 | Adds values to existing (by priority) |
| `SPACE_OVERRIDE_COMBINE_REPLACE` | 2 | Adds values, ignoring lower priority areas |
| `SPACE_OVERRIDE_REPLACE` | 3 | Replaces all gravity/damping, ignoring lower priority |
| `SPACE_OVERRIDE_REPLACE_COMBINE` | 4 | Replaces so far, keeps calculating rest |

## Basic Detection

```gdscript
extends Area3D

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    body_exited.connect(_on_body_exited)

func _on_body_entered(body: Node3D) -> void:
    if body is CharacterBody3D:
        print("Player entered area")

func _on_body_exited(body: Node3D) -> void:
    if body is CharacterBody3D:
        print("Player exited area")
```

## Custom Gravity Zone

```gdscript
extends Area3D

func _ready() -> void:
    # Override gravity in this area
    gravity_space_override = Area3D.SPACE_OVERRIDE_REPLACE
    gravity = 20.0  # Double gravity
    gravity_direction = Vector3.DOWN
```

## Point Gravity (Planet)

```gdscript
extends Area3D

func _ready() -> void:
    gravity_space_override = Area3D.SPACE_OVERRIDE_REPLACE
    gravity_point = true
    gravity_point_center = Vector3.ZERO  # Local space
    gravity = 9.8
    gravity_point_unit_distance = 100.0  # Planet radius
```

## Get Shape Index from Signal

```gdscript
func _on_body_shape_entered(
    body_rid: RID,
    body: Node3D,
    body_shape_index: int,
    local_shape_index: int
) -> void:
    # Get the CollisionShape3D node from the body
    var body_shape_owner := body.shape_find_owner(body_shape_index)
    var body_shape_node := body.shape_owner_get_owner(body_shape_owner)

    # Get the CollisionShape3D node from this area
    var local_shape_owner := shape_find_owner(local_shape_index)
    var local_shape_node := shape_owner_get_owner(local_shape_owner)

    print("Body shape: ", body_shape_node.name)
    print("Area shape: ", local_shape_node.name)
```

## Notes

- Overlapping body's `collision_layer` must match this area's `collision_mask` for detection
- Collision lists update once per physics frame, not immediately after movement
- Consider using signals instead of polling `get_overlapping_bodies()` for performance
- Wind force only applies to SoftBody3D nodes (not other physics bodies)
- For GridMap detection, MeshLibrary must have collision shapes configured
- Result of overlap tests is not immediate after moving objects
