---
class: RayCast2D
category: nodes/2d/physics
complexity: intermediate
tags: [2d, physics, raycast, collision, detection]
last_updated: 2025-12-21
---

# RayCast2D

**Inherits:** Node2D < CanvasItem < Node < Object

A ray in 2D space used to find the first collision object it intersects.

## Description

RayCast2D represents a ray from its origin (node position) to its `target_position` that detects the closest intersecting object along its path. It updates collision information every physics frame and can be configured to ignore specific objects, areas, bodies, or collision layers.

For immediate raycasting or multiple updates per frame, use `force_raycast_update()`. To sweep over a region, use multiple RayCast2D nodes or ShapeCast2D.

## Common Use Cases

- Line-of-sight detection (AI vision)
- Ground detection (platformers)
- Wall detection
- Shooting/projectile hit detection
- Interaction prompts (checking what player is looking at)
- Ledge detection for auto-climb

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | bool | true | Whether collisions are detected |
| `target_position` | Vector2 | Vector2(0, 50) | Ray endpoint relative to node position |
| `collision_mask` | int | 1 | Collision layers to detect |
| `collide_with_bodies` | bool | true | Detect PhysicsBody2D collisions |
| `collide_with_areas` | bool | false | Detect Area2D collisions |
| `exclude_parent` | bool | true | Ignore parent CollisionObject2D |
| `hit_from_inside` | bool | false | Detect when ray starts inside shape |

## Key Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `is_colliding()` | bool | Whether ray is intersecting an object |
| `get_collider()` | Object | First intersecting object (or null) |
| `get_collision_point()` | Vector2 | Global collision point |
| `get_collision_normal()` | Vector2 | Normal of collision surface |
| `force_raycast_update()` | void | Update collision immediately |
| `add_exception(node)` | void | Ignore specific node |
| `clear_exceptions()` | void | Clear exception list |

## Basic Example

```gdscript
extends CharacterBody2D

@onready var ground_check: RayCast2D = $GroundCheck

func _ready() -> void:
    ground_check.target_position = Vector2(0, 10)
    ground_check.enabled = true

func _physics_process(delta: float) -> void:
    var is_on_ground: bool = ground_check.is_colliding()
    if is_on_ground:
        print("Standing on: ", ground_check.get_collider().name)
```

## Line-of-Sight Detection

```gdscript
extends CharacterBody2D

@onready var vision_ray: RayCast2D = $VisionRay

func can_see_player(player: Node2D) -> bool:
    # Point ray toward player
    vision_ray.target_position = to_local(player.global_position)
    vision_ray.force_raycast_update()

    if vision_ray.is_colliding():
        var hit_object: Object = vision_ray.get_collider()
        return hit_object == player

    return false
```

## Wall Detection

```gdscript
extends CharacterBody2D

@onready var wall_ray: RayCast2D = $WallRay

func _ready() -> void:
    wall_ray.target_position = Vector2(32, 0)  # Check right
    wall_ray.collision_mask = 1  # Only detect layer 1 (walls)

func is_facing_wall() -> bool:
    return wall_ray.is_colliding()

func get_wall_normal() -> Vector2:
    if wall_ray.is_colliding():
        return wall_ray.get_collision_normal()
    return Vector2.ZERO
```

## Dynamic Ray Aiming

```gdscript
extends Node2D

@onready var aim_ray: RayCast2D = $AimRay

func aim_at_position(target_pos: Vector2) -> void:
    # Convert global position to local target
    aim_ray.target_position = to_local(target_pos)
    aim_ray.force_raycast_update()

func shoot() -> void:
    if aim_ray.is_colliding():
        var hit_point: Vector2 = aim_ray.get_collision_point()
        var hit_object: Object = aim_ray.get_collider()
        print("Hit ", hit_object.name, " at ", hit_point)
```

## Collision Layer Filtering

```gdscript
extends Node2D

func setup_raycast() -> void:
    var ray := RayCast2D.new()
    add_child(ray)

    # Only detect layers 1 and 3
    ray.collision_mask = 0
    ray.set_collision_mask_value(1, true)  # Enable layer 1
    ray.set_collision_mask_value(3, true)  # Enable layer 3

    ray.target_position = Vector2(100, 0)
```

## Exception Handling

```gdscript
extends CharacterBody2D

@onready var forward_ray: RayCast2D = $ForwardRay

func _ready() -> void:
    # Ignore self and any held objects
    forward_ray.add_exception(self)

    if has_node("HeldItem"):
        forward_ray.add_exception(get_node("HeldItem"))

func clear_held_item_exception() -> void:
    forward_ray.clear_exceptions()
    forward_ray.add_exception(self)  # Re-add self
```

## Ledge Detection

```gdscript
extends CharacterBody2D

@onready var ledge_check: RayCast2D = $LedgeCheck

func _ready() -> void:
    # Position ahead and down from character
    ledge_check.position = Vector2(16, 0)
    ledge_check.target_position = Vector2(0, 32)

func is_at_ledge() -> bool:
    # Returns true if no ground ahead
    return not ledge_check.is_colliding()
```

## Common Patterns

### Ground Slope Detection

```gdscript
func get_ground_angle() -> float:
    if ground_ray.is_colliding():
        var normal: Vector2 = ground_ray.get_collision_normal()
        return normal.angle_to(Vector2.UP)
    return 0.0

func is_ground_too_steep(max_angle: float = deg_to_rad(45)) -> bool:
    return abs(get_ground_angle()) > max_angle
```

### Interactive Object Detection

```gdscript
func check_for_interactable() -> Node:
    if interaction_ray.is_colliding():
        var object: Object = interaction_ray.get_collider()
        if object.has_method("interact"):
            return object as Node
    return null

func interact() -> void:
    var interactable: Node = check_for_interactable()
    if interactable:
        interactable.interact(self)
```

### Collision Shape Identification

```gdscript
func get_hit_shape_owner() -> Node:
    if raycast.is_colliding():
        var collider: Object = raycast.get_collider()
        if collider is CollisionObject2D:
            var target := collider as CollisionObject2D
            var shape_id: int = raycast.get_collider_shape()
            var owner_id: int = target.shape_find_owner(shape_id)
            return target.shape_owner_get_owner(owner_id)
    return null
```

## Best Practices

1. **Call force_raycast_update() for immediate checks**: Default updates only occur during `_physics_process`
2. **Use collision layers wisely**: Filter unnecessary collision checks for performance
3. **Check is_colliding() before accessing results**: Prevents null reference errors
4. **Position rays as child nodes**: Easier to visualize and adjust in editor
5. **Enable debug drawing**: Set "Visible Collision Shapes" in Debug menu during development

## Common Pitfalls

- Forgetting to call `force_raycast_update()` when ray is repositioned mid-frame
- Not checking `is_colliding()` before calling `get_collider()` or related methods
- Using wrong coordinate space (target_position is local, not global)
- Raycasting on wrong layers due to collision_mask misconfiguration
- Parent body blocking raycast (disable with `exclude_parent = true`)
- Expecting raycasts to work in `_ready()` (need physics frame or force update)

## Performance Considerations

- Raycasts are relatively cheap but still cost computation
- Minimize unnecessary raycasts by caching results
- Use `enabled = false` to disable inactive raycasts
- Prefer collision layers over exceptions for filtering
- Consider using ShapeCast2D for wider detection areas

## Related Nodes

- **RayCast3D**: 3D equivalent for 3D games
- **ShapeCast2D**: Sweeps a shape instead of a ray
- **Area2D**: For trigger-based detection instead of raycasting
- **PhysicsRayQueryParameters2D**: For one-shot raycasts via PhysicsDirectSpaceState2D

## Tutorials

- [Ray-casting (Official Godot Docs)](https://docs.godotengine.org/en/stable/tutorials/physics/ray-casting.html)

## Source

Official Godot Documentation: [RayCast2D](https://docs.godotengine.org/en/stable/classes/class_raycast2d.html)
