---
class: RayCast3D
category: nodes/3d/physics
complexity: intermediate
tags: [3d, physics, raycast, collision, detection]
last_updated: 2025-12-21
---

# RayCast3D

**Inherits:** Node3D < Node < Object

A ray in 3D space used to find the first collision object it intersects.

## Description

RayCast3D represents a ray from its origin (node position) to its `target_position` that detects the closest intersecting object along its path. It updates collision information every physics frame and can be configured to ignore specific objects, areas, bodies, or collision layers.

For immediate raycasting or multiple updates per frame, use `force_raycast_update()`. To sweep over a region, use multiple RayCast3D nodes or ShapeCast3D.

## Common Use Cases

- Line-of-sight detection (AI vision)
- Ground/ceiling detection
- Wall detection
- Shooting/projectile hit detection
- Interaction prompts (checking what player is looking at)
- Camera collision detection
- Grappling hook attachment points

## Key Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `enabled` | bool | true | Whether collisions are detected |
| `target_position` | Vector3 | Vector3(0, -1, 0) | Ray endpoint relative to node position |
| `collision_mask` | int | 1 | Collision layers to detect |
| `collide_with_bodies` | bool | true | Detect PhysicsBody3D collisions |
| `collide_with_areas` | bool | false | Detect Area3D collisions |
| `exclude_parent` | bool | true | Ignore parent CollisionObject3D |
| `hit_from_inside` | bool | false | Detect when ray starts inside shape |
| `hit_back_faces` | bool | true | Hit backfaces of concave/heightmap shapes |
| `debug_shape_custom_color` | Color | Color(0,0,0,1) | Debug visualization color |
| `debug_shape_thickness` | int | 2 | Debug line thickness (1=line, >1=pyramid) |

## Key Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `is_colliding()` | bool | Whether ray is intersecting an object |
| `get_collider()` | Object | First intersecting object (or null) |
| `get_collision_point()` | Vector3 | Global collision point |
| `get_collision_normal()` | Vector3 | Normal of collision surface |
| `get_collision_face_index()` | int | Face index for ConcavePolygonShape3D |
| `force_raycast_update()` | void | Update collision immediately |
| `add_exception(node)` | void | Ignore specific node |
| `clear_exceptions()` | void | Clear exception list |

## Basic Example

```gdscript
extends CharacterBody3D

@onready var ground_check: RayCast3D = $GroundCheck

func _ready() -> void:
    ground_check.target_position = Vector3(0, -1.1, 0)
    ground_check.enabled = true

func _physics_process(delta: float) -> void:
    var is_on_ground: bool = ground_check.is_colliding()
    if is_on_ground:
        print("Standing on: ", ground_check.get_collider().name)
```

## First-Person Interaction

```gdscript
extends Camera3D

@onready var interaction_ray: RayCast3D = $RayCast3D

func _ready() -> void:
    interaction_ray.target_position = Vector3(0, 0, -2.0)
    interaction_ray.enabled = true

func _process(delta: float) -> void:
    if Input.is_action_just_pressed("interact"):
        if interaction_ray.is_colliding():
            var target: Object = interaction_ray.get_collider()
            if target.has_method("interact"):
                target.interact()
```

## Line-of-Sight Detection

```gdscript
extends Node3D

@onready var vision_ray: RayCast3D = $VisionRay

func can_see_target(target: Node3D) -> bool:
    # Point ray toward target
    vision_ray.target_position = to_local(target.global_position)
    vision_ray.force_raycast_update()

    if vision_ray.is_colliding():
        var hit: Object = vision_ray.get_collider()
        return hit == target

    return false
```

## Shooting Mechanic

```gdscript
extends Node3D

@onready var weapon_ray: RayCast3D = $WeaponRay

func _ready() -> void:
    weapon_ray.target_position = Vector3(0, 0, -100)
    weapon_ray.collision_mask = 6  # Layers 2 and 3

func shoot() -> void:
    weapon_ray.force_raycast_update()

    if weapon_ray.is_colliding():
        var hit_point: Vector3 = weapon_ray.get_collision_point()
        var hit_object: Object = weapon_ray.get_collider()
        var hit_normal: Vector3 = weapon_ray.get_collision_normal()

        # Spawn impact effect
        spawn_impact_effect(hit_point, hit_normal)

        # Apply damage
        if hit_object.has_method("take_damage"):
            hit_object.take_damage(10)

func spawn_impact_effect(pos: Vector3, normal: Vector3) -> void:
    var effect := preload("res://effects/bullet_impact.tscn").instantiate()
    get_tree().root.add_child(effect)
    effect.global_position = pos
    effect.look_at(pos + normal, Vector3.UP)
```

## Camera Collision Detection

```gdscript
extends Camera3D

@onready var camera_ray: RayCast3D = $BackwardRay
@export var min_distance: float = 2.0
@export var max_distance: float = 5.0

func _ready() -> void:
    camera_ray.target_position = Vector3(0, 0, max_distance)

func _physics_process(delta: float) -> void:
    camera_ray.force_raycast_update()

    var target_distance: float = max_distance

    if camera_ray.is_colliding():
        var hit_point: Vector3 = camera_ray.get_collision_point()
        var distance: float = global_position.distance_to(hit_point)
        target_distance = max(distance - 0.5, min_distance)

    position.z = lerp(position.z, target_distance, delta * 10.0)
```

## Collision Layer Filtering

```gdscript
extends Node3D

func setup_raycast() -> void:
    var ray := RayCast3D.new()
    add_child(ray)

    # Only detect layers 1, 3, and 5
    ray.collision_mask = 0
    ray.set_collision_mask_value(1, true)
    ray.set_collision_mask_value(3, true)
    ray.set_collision_mask_value(5, true)

    ray.target_position = Vector3(0, 0, -10)
```

## Exception Handling

```gdscript
extends CharacterBody3D

@onready var forward_ray: RayCast3D = $ForwardRay

func _ready() -> void:
    # Ignore self and equipment
    forward_ray.add_exception(self)

    for child in get_children():
        if child.is_in_group("equipment"):
            forward_ray.add_exception(child)

func equip_item(item: Node3D) -> void:
    forward_ray.add_exception(item)
```

## Ground Normal Detection

```gdscript
extends CharacterBody3D

@onready var ground_ray: RayCast3D = $GroundRay

func get_ground_normal() -> Vector3:
    if ground_ray.is_colliding():
        return ground_ray.get_collision_normal()
    return Vector3.UP

func align_to_ground(delta: float) -> void:
    var ground_normal: Vector3 = get_ground_normal()
    var target_up: Vector3 = ground_normal
    var smooth_up: Vector3 = basis.y.lerp(target_up, delta * 10.0)
    look_at(global_position + basis.z, smooth_up)
```

## Common Patterns

### Slope Detection

```gdscript
func get_ground_angle() -> float:
    if ground_ray.is_colliding():
        var normal: Vector3 = ground_ray.get_collision_normal()
        return normal.angle_to(Vector3.UP)
    return 0.0

func is_slope_walkable(max_angle: float = deg_to_rad(45)) -> bool:
    return get_ground_angle() <= max_angle
```

### Face Index for Mesh Collision

```gdscript
func get_collision_triangle() -> PackedVector3Array:
    if not raycast.is_colliding():
        return PackedVector3Array()

    var face_index: int = raycast.get_collision_face_index()
    if face_index == -1:
        return PackedVector3Array()

    var collider: Object = raycast.get_collider()
    if collider is MeshInstance3D:
        var mesh: ArrayMesh = collider.mesh
        var arrays: Array = mesh.surface_get_arrays(0)
        var vertices: PackedVector3Array = arrays[Mesh.ARRAY_VERTEX]

        # Get triangle vertices
        var i: int = face_index * 3
        return PackedVector3Array([
            vertices[i],
            vertices[i + 1],
            vertices[i + 2]
        ])

    return PackedVector3Array()
```

### Grappling Hook

```gdscript
extends CharacterBody3D

@onready var grapple_ray: RayCast3D = $Camera3D/GrappleRay
var grapple_point: Vector3
var is_grappling: bool = false

func try_grapple() -> void:
    grapple_ray.force_raycast_update()

    if grapple_ray.is_colliding():
        grapple_point = grapple_ray.get_collision_point()
        is_grappling = true

func _physics_process(delta: float) -> void:
    if is_grappling:
        var direction: Vector3 = (grapple_point - global_position).normalized()
        velocity = direction * 20.0

        if global_position.distance_to(grapple_point) < 2.0:
            is_grappling = false
```

## Best Practices

1. **Call force_raycast_update() for immediate checks**: Default updates only occur during `_physics_process`
2. **Use collision layers wisely**: Filter unnecessary collision checks for performance
3. **Check is_colliding() before accessing results**: Prevents null reference errors
4. **Position rays as child nodes**: Easier to visualize and adjust in editor
5. **Enable debug visualization**: Helps visualize raycasts during development
6. **Use appropriate hit_back_faces setting**: Disable for one-sided collision detection

## Common Pitfalls

- Forgetting to call `force_raycast_update()` when ray is repositioned mid-frame
- Not checking `is_colliding()` before calling `get_collider()` or related methods
- Using wrong coordinate space (target_position is local, not global)
- Raycasting on wrong layers due to collision_mask misconfiguration
- Parent body blocking raycast (disable with `exclude_parent = true`)
- Expecting raycasts to work in `_ready()` (need physics frame or force update)
- CSGShape3D/GridMap may not return CollisionObject3D from `get_collider()`

## Performance Considerations

- Raycasts are relatively cheap but still cost computation
- Minimize unnecessary raycasts by caching results
- Use `enabled = false` to disable inactive raycasts
- Prefer collision layers over exceptions for filtering
- Consider using ShapeCast3D for wider detection areas
- Debug shapes (thickness > 1) have minimal performance impact

## Debug Visualization

- Set `debug_shape_custom_color` to customize appearance
- `debug_shape_thickness = 1`: Renders as thin line
- `debug_shape_thickness > 1`: Renders as truncated pyramid
- Enable "Visible Collision Shapes" in Debug menu to see at runtime
- Color highlights when colliding

## Related Nodes

- **RayCast2D**: 2D equivalent for 2D games
- **ShapeCast3D**: Sweeps a shape instead of a ray
- **Area3D**: For trigger-based detection instead of raycasting
- **PhysicsRayQueryParameters3D**: For one-shot raycasts via PhysicsDirectSpaceState3D

## Tutorials

- [Ray-casting (Official Godot Docs)](https://docs.godotengine.org/en/stable/tutorials/physics/ray-casting.html)
- [3D Voxel Demo](https://godotengine.org/asset-library/asset/2755)

## Source

Official Godot Documentation: [RayCast3D](https://docs.godotengine.org/en/stable/classes/class_raycast3d.html)
