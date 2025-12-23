# 3D Gameplay Dispatcher

Routes to patterns for 3D game development in Godot 4.

## Player Movement

| I want to... | Go to |
|--------------|-------|
| First-person movement | `reference/movement/3d-character.md#fps` |
| Third-person movement | `reference/movement/3d-character.md#tps` |
| Jump and gravity | `reference/movement/3d-character.md#jump` |
| Stairs and slopes | `reference/movement/3d-character.md#slopes` |
| Sprint/run mechanic | `reference/movement/3d-character.md#sprint` |
| Crouch | `reference/movement/3d-character.md#crouch` |

## Camera

| I want to... | Go to |
|--------------|-------|
| First-person camera | `reference/rendering/camera.md#fps-camera` |
| Third-person orbit camera | `reference/rendering/camera.md#orbit` |
| Spring arm for collision | `reference/rendering/camera.md#spring-arm` |
| Mouse look / rotation | `reference/rendering/camera.md#mouse-look` |
| Camera shake | `reference/rendering/camera.md#shake-3d` |

## Collision & Physics

| I want to... | Go to |
|--------------|-------|
| Set up collision shapes | `reference/physics/collision.md#3d-shapes` |
| Configure collision layers | `reference/physics/collision.md#layers` |
| Trigger zones (Area3D) | `reference/physics/areas.md#3d` |
| Raycast for interaction | `reference/physics/raycasting.md#3d` |
| Physics objects | `reference/physics/rigidbody.md#3d` |

## Enemy AI

| I want to... | Go to |
|--------------|-------|
| NavMesh pathfinding | `reference/movement/navigation.md#navmesh` |
| Patrol and chase | `reference/ai/enemy.md#3d-patrol` |
| Line of sight (3D) | `reference/physics/raycasting.md#3d-los` |
| State machine AI | `reference/animation/state-machines.md` |

## Combat

| I want to... | Go to |
|--------------|-------|
| Melee attacks | `reference/physics/hitbox-hurtbox.md#3d` |
| Projectiles/shooting | `reference/physics/projectiles.md#3d` |
| Hitscan weapons | `reference/physics/raycasting.md#hitscan` |
| Health system | `reference/patterns/health-system.md` |

## Animation

| I want to... | Go to |
|--------------|-------|
| Character animation | `reference/animation/animation-player.md#3d` |
| Animation blending | `reference/animation/animation-tree.md#blend-3d` |
| Root motion | `reference/animation/animation-tree.md#root-motion` |
| IK (inverse kinematics) | `reference/animation/ik.md` |

## Rendering

| I want to... | Go to |
|--------------|-------|
| Set up lighting | `reference/rendering/lighting.md` |
| Materials/shaders | `reference/rendering/materials.md` |
| Environment/sky | `reference/rendering/environment.md` |
| Particle effects | `reference/rendering/particles.md#3d` |
| LOD (level of detail) | `reference/rendering/lod.md` |

## Level Design

| I want to... | Go to |
|--------------|-------|
| CSG prototyping | `reference/rendering/csg.md` |
| GridMap for blocky levels | `reference/rendering/gridmap.md` |
| Importing meshes | `reference/rendering/meshes.md#import` |

## Quick Start: Basic FPS Controller

```gdscript
extends CharacterBody3D

@export var speed: float = 5.0
@export var jump_strength: float = 4.5
@export var mouse_sensitivity: float = 0.002

var gravity: float = ProjectSettings.get_setting("physics/3d/default_gravity")

@onready var camera: Camera3D = $Camera3D

func _ready() -> void:
    Input.mouse_mode = Input.MOUSE_MODE_CAPTURED

func _input(event: InputEvent) -> void:
    if event is InputEventMouseMotion:
        rotate_y(-event.relative.x * mouse_sensitivity)
        camera.rotate_x(-event.relative.y * mouse_sensitivity)
        camera.rotation.x = clamp(camera.rotation.x, -PI/2, PI/2)

func _physics_process(delta: float) -> void:
    if not is_on_floor():
        velocity.y -= gravity * delta

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = jump_strength

    var input_dir := Input.get_vector("move_left", "move_right", "move_forward", "move_back")
    var direction := (transform.basis * Vector3(input_dir.x, 0, input_dir.y)).normalized()

    velocity.x = direction.x * speed
    velocity.z = direction.z * speed

    move_and_slide()
```

**Required Input Actions:** `move_left`, `move_right`, `move_forward`, `move_back`, `jump`

**Scene Setup:**
1. CharacterBody3D (root)
2. CollisionShape3D (child) with CapsuleShape3D
3. Camera3D (child) at eye height
