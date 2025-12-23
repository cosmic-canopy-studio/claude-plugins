# 2D Gameplay Dispatcher

Routes to patterns for 2D game development in Godot 4.

## Player Movement

| I want to... | Go to |
|--------------|-------|
| Move player with WASD (top-down) | `reference/movement/2d-character.md#8-way` |
| Create platformer with jump | `reference/movement/2d-character.md#platformer` |
| Add wall sliding | `reference/movement/2d-character.md#wall-slide` |
| Implement coyote time | `reference/movement/2d-character.md#coyote-time` |
| Add dash/dodge roll | `reference/movement/2d-character.md#dash` |
| Click-to-move / point-and-click | `reference/movement/navigation.md#click-to-move` |
| Smooth acceleration/deceleration | `reference/movement/2d-character.md#smooth-movement` |

## Camera

| I want to... | Go to |
|--------------|-------|
| Camera follow player | `reference/rendering/camera.md#follow` |
| Smooth camera with limits | `reference/rendering/camera.md#limits` |
| Screen shake on impact | `reference/rendering/camera.md#shake` |
| Zoom in/out | `reference/rendering/camera.md#zoom` |
| Multi-target camera | `reference/rendering/camera.md#multi-target` |

## Collision & Physics

| I want to... | Go to |
|--------------|-------|
| Set up collision shapes | `reference/physics/collision.md#shapes` |
| Configure collision layers | `reference/physics/collision.md#layers` |
| Detect overlaps (pickups, triggers) | `reference/physics/areas.md#body-entered` |
| One-way platforms | `reference/physics/collision.md#one-way` |
| Moving platforms | `reference/physics/collision.md#moving-platforms` |
| Raycast for ground check | `reference/physics/raycasting.md#ground-check` |

## Enemy AI

| I want to... | Go to |
|--------------|-------|
| Patrol between points | `reference/ai/enemy.md#patrol` |
| Chase player when seen | `reference/ai/enemy.md#chase` |
| Attack when in range | `reference/ai/enemy.md#attack` |
| Line of sight detection | `reference/physics/raycasting.md#los` |
| A* pathfinding | `reference/movement/navigation.md#astar` |
| State machine for AI | `reference/animation/state-machines.md` |

## Combat

| I want to... | Go to |
|--------------|-------|
| Hitbox/hurtbox system | `reference/physics/hitbox-hurtbox.md` |
| Health and damage | `reference/patterns/health-system.md` |
| Knockback on hit | `reference/patterns/health-system.md#knockback` |
| Invincibility frames | `reference/patterns/health-system.md#invincibility` |
| Projectiles/bullets | `reference/physics/projectiles.md` |

## Animation

| I want to... | Go to |
|--------------|-------|
| Sprite animations | `reference/rendering/sprites.md#animated` |
| Animation state machine | `reference/animation/state-machines.md` |
| Blend animations | `reference/animation/animation-tree.md#blend` |
| Flip sprite direction | `reference/rendering/sprites.md#flip` |

## Level Design

| I want to... | Go to |
|--------------|-------|
| Create tilemap level | `reference/rendering/tilemap.md` |
| Autotiling setup | `reference/rendering/tilemap.md#autotile` |
| Parallax backgrounds | `reference/rendering/parallax.md` |
| Room transitions | `reference/patterns/scenes.md#transitions` |

## Visual Effects

| I want to... | Go to |
|--------------|-------|
| Particle effects | `reference/rendering/particles.md` |
| Trail effects | `reference/rendering/particles.md#trail` |
| Hit flash/damage flash | `reference/rendering/shaders.md#flash` |
| Outline shader | `reference/rendering/shaders.md#outline` |

## Quick Start: Basic 2D Platformer

```gdscript
extends CharacterBody2D

@export var speed: float = 300.0
@export var jump_strength: float = 500.0
@export var gravity: float = 1200.0

func _physics_process(delta: float) -> void:
    velocity.x = Input.get_axis("move_left", "move_right") * speed
    velocity.y += gravity * delta

    if Input.is_action_just_pressed("jump") and is_on_floor():
        velocity.y = -jump_strength

    move_and_slide()
```

**Required Input Actions:** `move_left`, `move_right`, `jump`

**Scene Setup:**
1. CharacterBody2D (root)
2. CollisionShape2D (child) with CapsuleShape2D
3. Sprite2D or AnimatedSprite2D (child)
