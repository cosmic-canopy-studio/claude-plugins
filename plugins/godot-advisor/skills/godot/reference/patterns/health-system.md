---
topic: health-system
version: 2025.12.21
godot_version: "4.3"
sources:
  - repos/godot_node_essentials
  - gdquest-library
  - godot-community
---

# Health System

Patterns for implementing health, damage, healing, and death in Godot 4 games.

## Quick Start

```gdscript
# Minimal health component
extends Node
class_name HealthComponent

@export var max_health: float = 100.0

var current_health: float = max_health

func take_damage(amount: float) -> void:
    current_health = max(0.0, current_health - amount)
    if current_health == 0.0:
        die()

func die() -> void:
    get_parent().queue_free()
```

## ProgressBar Health Display

### Basic Implementation

```gdscript
extends CharacterBody2D

@onready var health_bar: ProgressBar = %HealthProgressBar

func _ready() -> void:
    health_bar.max_value = 100.0
    health_bar.value = 100.0

func take_damage(amount: int) -> void:
    var tween := create_tween()
    tween.set_trans(Tween.TRANS_CUBIC)
    tween.set_ease(Tween.EASE_IN_OUT)
    tween.tween_property(health_bar, "value", health_bar.value - amount, 0.5)
    await tween.finished

    if health_bar.value == 0:
        die()

func die() -> void:
    queue_free()
```

### Healing System

```gdscript
extends CharacterBody2D

@onready var health_bar: ProgressBar = %HealthProgressBar

func heal(amount: int) -> void:
    # Prevent healing above max health
    if health_bar.value == health_bar.max_value:
        return

    var tween := create_tween()
    tween.set_trans(Tween.TRANS_CUBIC)
    tween.set_ease(Tween.EASE_OUT)
    tween.tween_property(health_bar, "value", health_bar.value + amount, 0.5)
```

### Dynamic Max Health

```gdscript
extends CharacterBody2D

const MAX_HEALTH: float = 300.0

@onready var health_bar: ProgressBar = %HealthProgressBar

func increase_max_health(amount: int) -> void:
    if health_bar.max_value >= MAX_HEALTH:
        return

    var tween := create_tween()
    tween.set_trans(Tween.TRANS_CUBIC)
    tween.set_ease(Tween.EASE_OUT)
    tween.set_parallel(true)
    tween.tween_property(health_bar, "max_value", health_bar.max_value + amount, 0.5)
    # Also scale the bar width visually
    tween.tween_property(health_bar, "custom_minimum_size:x", (health_bar.max_value + amount) * 5, 0.5)
```

## Hitbox/Hurtbox Pattern

### Hurtbox (Receives Damage)

```gdscript
# Enemy with hurtbox that takes damage
extends CharacterBody2D

@onready var hurt_box: Area2D = %HurtBoxArea2D
@onready var animation_player: AnimationPlayer = %AnimationPlayer
@onready var collision_shape: CollisionShape2D = %CollisionShape2D

func _ready() -> void:
    hurt_box.area_entered.connect(_on_hurt_box_area_entered)

func _on_hurt_box_area_entered(area: Area2D) -> void:
    take_damage()

func take_damage() -> void:
    animation_player.play("die")
    collision_shape.set_deferred("disabled", true)
    hurt_box.set_deferred("monitoring", false)
    set_physics_process(false)
```

### Hitbox (Deals Damage)

```gdscript
# Weapon hitbox using duck-typing
extends Node2D

@onready var hitbox_area: Area2D = %HitBoxArea2D

func _ready() -> void:
    hitbox_area.body_entered.connect(_on_area_body_entered)

func _on_area_body_entered(body: PhysicsBody2D) -> void:
    # Duck-typing: check if entity has take_damage method
    if body.has_method("take_damage"):
        body.take_damage()
```

### Typed Hitbox with Damage Value

```gdscript
# Hitbox as custom class with configurable damage
class_name HitBox2D extends Area2D

@export var damage: int = 10

func _ready() -> void:
    area_entered.connect(_on_area_entered)

func _on_area_entered(area: Area2D) -> void:
    # Check if area is a hurtbox
    if area.has_method("receive_damage"):
        area.receive_damage(damage)
```

### Hurtbox with Damage Processing

```gdscript
# Hurtbox that receives typed damage
class_name HurtBox2D extends Area2D

signal damage_received(amount: int)

func receive_damage(amount: int) -> void:
    damage_received.emit(amount)

    # Process damage in parent
    if get_parent().has_method("take_damage"):
        get_parent().take_damage(amount)
```

## 3D Health Bar (SubViewport)

Display health bar as 3D billboard:

```gdscript
extends CharacterBody3D

@onready var hurt_box: Area3D = %HurtBoxArea3D
@onready var progress_bar: ProgressBar = %ProgressBar
@onready var animation_player: AnimationPlayer = %AnimationPlayer

func _ready() -> void:
    hurt_box.area_entered.connect(_on_hurt_box_area_entered)

func _on_hurt_box_area_entered(area: Area3D) -> void:
    take_damage()

func take_damage() -> void:
    animation_player.play("die")

    var tween := get_tree().create_tween()
    tween.tween_property(progress_bar, "value", 0.0, 1.0)
    tween.parallel().tween_property(progress_bar, "modulate", Color.ROSY_BROWN, 1.0)
    await tween.finished
    await get_tree().create_timer(1.0).timeout
    queue_free()
```

Scene structure:
```
RobotEnemy3D (CharacterBody3D)
├── HurtBoxArea3D (Area3D)
├── SubViewport3D (SubViewport in world space)
│   └── ProgressBar
└── AnimationPlayer
```

## Visual Feedback

### Blink Effect (Invincibility Frames)

```gdscript
# 2D player with damage blink
extends CharacterBody2D

@onready var animation_player: AnimationPlayer = %AnimationPlayer

func take_damage() -> void:
    start_blink()

func start_blink(loop: Animation.LoopMode = Animation.LOOP_NONE) -> void:
    animation_player.get_animation("blink").loop_mode = loop
    animation_player.play("blink")

func stop_blink() -> void:
    animation_player.stop()
    animation_player.seek(0, true)
```

Animation "blink" should toggle sprite visibility or modulate alpha.

### Blood/Hit Particles

```gdscript
# Dummy target with particle effect on hit
extends StaticBody2D

@onready var animation_player: AnimationPlayer = %AnimationPlayer
@onready var blood_particles: GPUParticles2D = %BloodGPUParticles2D

func take_damage(collision: KinematicCollision2D) -> void:
    # Orient particles to impact direction
    blood_particles.rotation = collision.get_normal().angle()
    blood_particles.global_position = collision.get_position()
    blood_particles.emitting = true
    animation_player.play("hurt")
```

## Death Handling

### Simple Death

```gdscript
func take_damage(amount: int) -> void:
    health -= amount
    if health <= 0:
        die()

func die() -> void:
    queue_free()
```

### Death with Animation

```gdscript
func take_damage() -> void:
    if not is_physics_processing():
        return

    set_physics_process(false)
    animation_player.play("die")
    # Animation should call queue_free() at end
```

### Death with Cleanup

```gdscript
func take_damage() -> void:
    animation_player.play("die")

    # Disable collision detection
    collision_shape.set_deferred("disabled", true)
    hurt_box.set_deferred("monitoring", false)
    hit_box.set_deferred("monitoring", false)

    # Visual effects
    smoke_particles.emitting = true

    # Stop processing
    set_physics_process(false)
```

## Collision Detection Patterns

### Area-Based Detection

```gdscript
# Player collision area for pickups and hazards
extends CharacterBody2D

const HealthPickup := preload("health_pickup.gd")
const Asteroid := preload("asteroid.gd")

@onready var collision_area: Area2D = %CollisionArea2D
@onready var health_bar: ProgressBar = %HealthProgressBar

func _ready() -> void:
    collision_area.area_entered.connect(_on_area_entered)
    collision_area.body_entered.connect(_on_body_entered)

func _on_area_entered(area: Area2D) -> void:
    if area is HealthPickup:
        if health_bar.value != health_bar.max_value:
            heal(area.health_given)
            area.pickup()

func _on_body_entered(body: Node) -> void:
    if body is Asteroid:
        take_damage(body.damage)
        body.destroy()
```

### Stomp Mechanic

```gdscript
# Player can stomp enemies
extends CharacterBody2D

@export var stomp_bump_strength: float = 400.0

func _physics_process(delta: float) -> void:
    super(delta)
    check_stomp()

func check_stomp() -> void:
    # Only check when landing
    if not is_landing():
        return

    for index in get_slide_collision_count():
        var collision := get_slide_collision(index)
        var collider := collision.get_collider() as CharacterBody2D

        # Check if we landed on an enemy
        if collider != null and collider.is_in_group("enemy"):
            collider.take_damage()
            velocity.y -= stomp_bump_strength

func is_landing() -> bool:
    return was_in_air and is_on_floor()
```

## Pickups

### Health Pickup

```gdscript
# Health pickup item
extends Area2D

const PLAYER_LAYER: int = 1

@export var health_given: int = 50

@onready var animation_player: AnimationPlayer = %AnimationPlayer

func pickup() -> void:
    # Disable collision
    set_collision_layer_value(PLAYER_LAYER, false)

    # Play collection animation sequence
    animation_player.stop()
    animation_player.queue("collected")
    animation_player.queue("delay")
    animation_player.queue("respawn")

func respawn() -> void:
    set_collision_layer_value(PLAYER_LAYER, true)
    animation_player.play("idle")
```

### Damaging Projectile

```gdscript
# Asteroid projectile that damages on contact
extends RigidBody2D

const PLAYER_LAYER: int = 1

@export var damage: int = 20

var direction: Vector2 = Vector2.ONE
var speed: float = 500.0

@onready var animation_player: AnimationPlayer = %AnimationPlayer

func _ready() -> void:
    body_entered.connect(_on_body_entered)
    set_angular_velocity(2.0)
    set_linear_velocity(direction * speed)

func _on_body_entered(body: Node) -> void:
    destroy()

func destroy() -> void:
    # Disable collision
    set_collision_layer_value(PLAYER_LAYER, false)
    set_collision_mask_value(PLAYER_LAYER, false)

    # Stop movement
    set_deferred("freeze", true)

    # Play destruction animation (should queue_free at end)
    animation_player.play("explode")
```

## Component-Based Architecture

### Health Component

```gdscript
# Reusable health component
class_name HealthComponent extends Node

signal health_changed(new_value: float)
signal health_depleted
signal damage_taken(amount: float)
signal healed(amount: float)

@export var max_health: float = 100.0
@export var start_health: float = -1.0  # -1 means use max_health

var current_health: float = 0.0

func _ready() -> void:
    if start_health < 0:
        current_health = max_health
    else:
        current_health = clamp(start_health, 0.0, max_health)

func take_damage(amount: float) -> void:
    if amount <= 0:
        return

    current_health = max(0.0, current_health - amount)
    damage_taken.emit(amount)
    health_changed.emit(current_health)

    if current_health == 0.0:
        health_depleted.emit()

func heal(amount: float) -> void:
    if amount <= 0:
        return

    var old_health := current_health
    current_health = min(max_health, current_health + amount)

    if current_health > old_health:
        healed.emit(amount)
        health_changed.emit(current_health)

func get_health_percent() -> float:
    return current_health / max_health if max_health > 0 else 0.0

func is_alive() -> bool:
    return current_health > 0.0
```

### Using Health Component

```gdscript
extends CharacterBody2D

@onready var health_component: HealthComponent = %HealthComponent
@onready var health_bar: ProgressBar = %HealthProgressBar

func _ready() -> void:
    health_component.health_changed.connect(_on_health_changed)
    health_component.health_depleted.connect(_on_health_depleted)

    # Initialize UI
    health_bar.max_value = health_component.max_health
    health_bar.value = health_component.current_health

func _on_health_changed(new_value: float) -> void:
    var tween := create_tween()
    tween.tween_property(health_bar, "value", new_value, 0.3)

func _on_health_depleted() -> void:
    die()

func take_damage(amount: float) -> void:
    health_component.take_damage(amount)

func die() -> void:
    queue_free()
```

## Best Practices & Pitfalls

### Use Signals for Decoupling
- Health components should emit signals rather than directly calling methods
- Allows multiple systems to react to health changes (UI, sound, particles)

### Cache Node References
```gdscript
# Good - cache in _ready()
@onready var health_bar: ProgressBar = %HealthProgressBar

# Bad - repeated lookups
func take_damage(amount: int) -> void:
    get_node("UI/HealthBar").value -= amount  # Slow!
```

### Collision Layer Organization
```gdscript
# Define layer constants for clarity
const PLAYER_LAYER: int = 1
const ENEMY_LAYER: int = 2
const HITBOX_LAYER: int = 3
const HURTBOX_LAYER: int = 4

# Hitboxes on layer 3, looking for layer 4 (hurtboxes)
# Hurtboxes on layer 4, looking for layer 3 (hitboxes)
```

### Deferred Collision Changes
```gdscript
# Always use set_deferred for collision changes during physics
collision_shape.set_deferred("disabled", true)
hurt_box.set_deferred("monitoring", false)

# Never do this during physics callbacks:
collision_shape.disabled = true  # May cause errors!
```

### Prevent Multiple Death Calls
```gdscript
func take_damage() -> void:
    if not is_physics_processing():
        return  # Already dead

    set_physics_process(false)
    animation_player.play("die")
```

### Duck-Typing vs Type Checking
```gdscript
# Duck-typing (flexible, works with any object)
if body.has_method("take_damage"):
    body.take_damage()

# Type checking (type-safe, better for large projects)
if body is Enemy:
    body.take_damage()

# Group checking (good for cross-type categories)
if body.is_in_group("damageable"):
    body.take_damage()
```

### Hitbox/Hurtbox Size Design
- **Single-player games**: Make enemy hurtboxes larger than sprites (easier to hit)
- **Competitive games**: Make hitboxes match sprites precisely (fairness)
- **Player hurtboxes**: Slightly smaller than sprite (more forgiving)

### Performance Optimization
- Disable collision monitoring when not needed
- Use object pooling for projectiles instead of constant create/destroy
- Minimize UI updates - use tweens to smooth transitions
- Turn off physics processing on death

## Related Patterns

- [Signals](signals.md) - Event-driven health system architecture
- [Timer](timer.md) - Invincibility frame cooldowns
- [Area2D/Area3D](../nodes/area.md) - Hitbox/hurtbox collision detection
- [ProgressBar](../ui/progress-bar.md) - Visual health display
- [Tween](../animation/tween.md) - Smooth health bar transitions

## Sources

1. **Examples**: [godot_node_essentials](https://github.com/gdquest-demos/godot-node-essentials) - Health bar implementations, hitbox/hurtbox patterns
2. **Official**: [GDQuest - Hitbox/Hurtbox](https://www.gdquest.com/library/hitbox_hurtbox_godot4/) - Hit and hurt box damage handling
3. **Community**: [HealthComponent Gist](https://gist.github.com/viniciusemferreira/28b8c6aff0befbaa0e939b556e432e21) - Reusable health component pattern
4. **Community**: [Godot Forum - Health Systems](https://forum.godotengine.org/t/using-classes-to-implement-a-flexible-damage-and-health-system/49321) - Component-based architecture discussions
