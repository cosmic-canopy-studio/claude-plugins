---
class: CharacterBody2D
godot_version: "4.3"
sources:
  - local: repos/godot-docs/classes/class_characterbody2d.rst
status: extracted
---

# CharacterBody2D

## Inheritance
PhysicsBody2D < CollisionObject2D < Node2D < CanvasItem < Node < Object

## Description
A 2D physics body specialized for characters moved by script.

CharacterBody2D is a specialized class for physics bodies that are meant to be user-controlled. They are not affected by physics at all, but they affect other physics bodies in their path. They are mainly used to provide high-level API to move objects with wall and slope detection (move_and_slide() method) in addition to the general collision detection provided by PhysicsBody2D.move_and_collide(). This makes it useful for highly configurable physics bodies that must move in specific ways and collide with the world, as is often the case with user-controlled characters.

For game objects that don't require complex movement or collision detection, such as moving platforms, AnimatableBody2D is simpler to configure.

## Properties
| Property | Type | Default | Description |
|----------|------|---------|-------------|
| floor_block_on_wall | bool | true | If true, the body will be able to move on the floor only |
| floor_constant_speed | bool | false | If true, body moves at same speed regardless of slope |
| floor_max_angle | float | 0.7853982 | Maximum angle (radians) where a slope is considered a floor (45°) |
| floor_snap_length | float | 1.0 | Snapping distance to keep body attached to slopes |
| floor_stop_on_slope | bool | true | If true, body won't slide on slopes when standing still |
| max_slides | int | 4 | Maximum number of direction changes before stopping |
| motion_mode | MotionMode | 0 | Defines behavior of move_and_slide() |
| platform_floor_layers | int | 4294967295 | Collision layers for floor platform detection |
| platform_on_leave | PlatformOnLeave | 0 | Behavior when leaving a moving platform |
| platform_wall_layers | int | 0 | Collision layers for wall platform detection |
| safe_margin | float | 0.08 | Extra margin for collision recovery |
| slide_on_ceiling | bool | true | If true, body slides on ceiling during jumps |
| up_direction | Vector2 | Vector2(0, -1) | Vector pointing upwards for floor/ceiling detection |
| velocity | Vector2 | Vector2(0, 0) | Current velocity in pixels per second |
| wall_min_slide_angle | float | 0.2617994 | Minimum angle (radians) for sliding on walls (15°) |

## Methods
| Method | Return | Description |
|--------|--------|-------------|
| apply_floor_snap() | void | Manually apply snap to floor regardless of velocity |
| get_floor_angle(up_direction: Vector2 = Vector2(0, -1)) | float | Returns floor collision angle at last collision point |
| get_floor_normal() | Vector2 | Returns collision normal of floor at last collision point |
| get_last_motion() | Vector2 | Returns last motion applied during move_and_slide() |
| get_last_slide_collision() | KinematicCollision2D | Returns info about latest collision |
| get_platform_velocity() | Vector2 | Returns linear velocity of platform at last collision |
| get_position_delta() | Vector2 | Returns travel (position delta) during last move_and_slide() |
| get_real_velocity() | Vector2 | Returns current real velocity since last move_and_slide() |
| get_slide_collision(slide_idx: int) | KinematicCollision2D | Returns collision info for specific slide index |
| get_slide_collision_count() | int | Returns number of collisions during last move_and_slide() |
| get_wall_normal() | Vector2 | Returns collision normal of wall at last collision point |
| is_on_ceiling() | bool | Returns true if body collided with ceiling |
| is_on_ceiling_only() | bool | Returns true if body collided only with ceiling |
| is_on_floor() | bool | Returns true if body collided with floor |
| is_on_floor_only() | bool | Returns true if body collided only with floor |
| is_on_wall() | bool | Returns true if body collided with wall |
| is_on_wall_only() | bool | Returns true if body collided only with wall |
| move_and_slide() | bool | Moves body based on velocity with sliding collision |

## Enums

### MotionMode
| Value | Name | Description |
|-------|------|-------------|
| 0 | MOTION_MODE_GROUNDED | For platformers - uses floor/ceiling/wall detection with slope handling |
| 1 | MOTION_MODE_FLOATING | For top-down games - all collisions reported as walls, constant speed |

### PlatformOnLeave
| Value | Name | Description |
|-------|------|-------------|
| 0 | PLATFORM_ON_LEAVE_ADD_VELOCITY | Add last platform velocity when leaving |
| 1 | PLATFORM_ON_LEAVE_ADD_UPWARD_VELOCITY | Add platform velocity but ignore downward motion |
| 2 | PLATFORM_ON_LEAVE_DO_NOTHING | Do nothing when leaving platform |

## See Also
- [Official Docs](https://docs.godotengine.org/en/stable/classes/class_characterbody2d.html)
- [Physics Introduction Tutorial](repos/godot-docs/tutorials/physics/physics_introduction.rst)
- [Kinematic Character 2D Tutorial](repos/godot-docs/tutorials/physics/kinematic_character_2d.rst)
- [Using CharacterBody2D Tutorial](repos/godot-docs/tutorials/physics/using_character_body_2d.rst)
