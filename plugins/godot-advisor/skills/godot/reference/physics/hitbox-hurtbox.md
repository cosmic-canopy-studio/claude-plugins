---
topic: hitbox-hurtbox
version: 2025.12.21
godot_version: "4.3"
sources:
  - official: https://docs.godotengine.org/en/stable/tutorials/physics/using_area_2d.html
  - community: https://www.gdquest.com/library/hitbox_hurtbox_godot4/
  - examples: repos/godot_node_essentials/screens/area_2d/hurtbox_2d/
  - examples: repos/godot_node_essentials/screens/area_3d/hurtbox_3d/
---

# Hitbox/Hurtbox System

Separation of attack zones (hitboxes) and vulnerable zones (hurtboxes) for combat systems using Area2D/Area3D.

## When to Use

Use hitbox/hurtbox separation for:
- Combat systems with multiple damage zones (headshots, weak points)
- Fighting games with precise frame-based attacks
- Games where attacks and damage are separate concerns
- Any system requiring complex collision filtering

**Simple alternative:** For basic platformer damage (touch = death), use direct body collision instead.

## Core Concept {#concept}

**Hitbox:** The attacking area that deals damage (sword swing, bullet, explosion)
**Hurtbox:** The vulnerable area that receives damage (character body, enemy weak point)

Key principle: Hitboxes detect hurtboxes, not the other way around.

## Collision Layer Setup {#layers}

Standard configuration using layers 1-8:

| Layer | Name | Purpose |
|-------|------|---------|
| 1 | World | Static geometry for movement |
| 2 | Player | Player character body |
| 3 | Enemy | Enemy character body |
| 4 | Player Hurtbox | Where player takes damage |
| 5 | Enemy Hurtbox | Where enemies take damage |
| 6 | Player Hitbox | Player's attacks |
| 7 | Enemy Hitbox | Enemy attacks |

### Hitbox Configuration

```gdscript
# Hitbox (weapon, projectile)
collision_layer = 1 << 5  # Layer 6: Player Hitbox
collision_mask = 1 << 4   # Layer 5: Enemy Hurtbox (what it detects)
monitoring = true         # Actively detecting
monitorable = false       # Others don't detect this
```

### Hurtbox Configuration

```gdscript
# Hurtbox (vulnerable area)
collision_layer = 1 << 3  # Layer 4: Player Hurtbox
collision_mask = 0        # Doesn't detect anything
monitoring = false        # Not actively detecting
monitorable = true        # Can be detected by hitboxes
```

## Basic Implementation {#basic}

### Hurtbox (Receives Damage)

```gdscript
extends Area2D
class_name HurtBox2D

func _ready() -> void:
	collision_layer = 1 << 3  # Player Hurtbox layer
	collision_mask = 0
	monitoring = false
	monitorable = true

	area_entered.connect(_on_area_entered)

func _on_area_entered(hitbox: Area2D) -> void:
	if hitbox == null:
		return

	# Duck-typing: any node with take_damage() can handle damage
	if owner.has_method("take_damage"):
		var damage: int = hitbox.get("damage") if hitbox.has_method("get") else 10
		owner.take_damage(damage)
```

### Hitbox (Deals Damage)

```gdscript
extends Area2D
class_name HitBox2D

@export var damage: int = 10

func _ready() -> void:
	collision_layer = 1 << 5  # Player Hitbox layer
	collision_mask = 1 << 4   # Enemy Hurtbox layer
	monitoring = false  # Disabled until attack starts
	monitorable = false

	body_entered.connect(_on_body_entered)

func activate() -> void:
	monitoring = true

func deactivate() -> void:
	monitoring = false

# Alternative: detect PhysicsBody directly
func _on_body_entered(body: PhysicsBody2D) -> void:
	if body.has_method("take_damage"):
		body.take_damage(damage)
```

## Melee Attack Pattern {#melee}

Weapon with animation-controlled hitbox:

```gdscript
extends Node2D

@export var damage: int = 20

@onready var _hitbox: Area2D = %HitBoxArea2D
@onready var _animation_player: AnimationPlayer = %AnimationPlayer

func _ready() -> void:
	_hitbox.monitoring = false
	_hitbox.body_entered.connect(_on_hitbox_body_entered)

func attack() -> void:
	_animation_player.play("attack")

# Called by animation track
func _enable_hitbox() -> void:
	_hitbox.monitoring = true

# Called by animation track
func _disable_hitbox() -> void:
	_hitbox.monitoring = false

func _on_hitbox_body_entered(body: PhysicsBody2D) -> void:
	if body.has_method("take_damage"):
		body.take_damage(damage)
```

**Animation setup:**
1. Add boolean track for `Area2D:monitoring`
2. Set to `true` during attack frames (e.g., frame 5-10)
3. Set to `false` at animation end
4. Add visual track for weapon visibility

## Character with Hurtbox {#character}

```gdscript
extends CharacterBody2D

@export var max_health: int = 100

var _health: int = max_health

@onready var _hurtbox: Area2D = %HurtBoxArea2D
@onready var _collision: CollisionShape2D = %CollisionShape2D
@onready var _animation_player: AnimationPlayer = %AnimationPlayer

func _ready() -> void:
	_hurtbox.area_entered.connect(_on_hurtbox_area_entered)

func _on_hurtbox_area_entered(hitbox: Area2D) -> void:
	if hitbox.has_method("get_damage"):
		take_damage(hitbox.get_damage())
	elif hitbox.get("damage"):
		take_damage(hitbox.damage)

func take_damage(amount: int) -> void:
	_health -= amount
	_animation_player.play("hit")

	if _health <= 0:
		die()

func die() -> void:
	_animation_player.play("die")
	_collision.set_deferred("disabled", true)
	_hurtbox.set_deferred("monitoring", false)
	_hurtbox.set_deferred("monitorable", false)
	set_physics_process(false)
```

## Projectile Pattern {#projectile}

```gdscript
extends Area2D

@export var damage: int = 15
@export var speed: float = 400.0
@export var lifetime: float = 5.0

var _velocity: Vector2 = Vector2.ZERO

func _ready() -> void:
	collision_layer = 1 << 5  # Player Hitbox
	collision_mask = 1 << 4   # Enemy Hurtbox
	monitoring = true

	body_entered.connect(_on_body_entered)
	area_entered.connect(_on_area_entered)

	# Auto-destroy after lifetime
	get_tree().create_timer(lifetime).timeout.connect(queue_free)

func launch(direction: Vector2) -> void:
	_velocity = direction.normalized() * speed
	rotation = direction.angle()

func _physics_process(delta: float) -> void:
	position += _velocity * delta

func _on_body_entered(body: PhysicsBody2D) -> void:
	if body.has_method("take_damage"):
		body.take_damage(damage)
	queue_free()

func _on_area_entered(area: Area2D) -> void:
	# Hit a hurtbox
	queue_free()
```

## 3D Implementation {#3d}

Identical pattern with Area3D:

```gdscript
extends CharacterBody3D

@export var target: Node3D = null
@export var speed := 3.0

@onready var _hit_box: Area3D = %HitBoxArea3D
@onready var _hurt_box: Area3D = %HurtBoxArea3D
@onready var _collision: CollisionShape3D = %CollisionShape3D
@onready var _animation_player: AnimationPlayer = %AnimationPlayer

func _ready() -> void:
	_hit_box.body_entered.connect(_on_hit_box_body_entered)
	_hurt_box.area_entered.connect(_on_hurt_box_area_entered)

func _on_hit_box_body_entered(body: PhysicsBody3D) -> void:
	if body.has_method("take_damage"):
		body.take_damage(10)

func _on_hurt_box_area_entered(_area: Area3D) -> void:
	take_damage(10)

func take_damage(amount: int) -> void:
	_animation_player.play("die")
	_collision.set_deferred("disabled", true)
	_hurt_box.set_deferred("monitoring", false)
	_hit_box.set_deferred("monitoring", false)
	set_physics_process(false)
```

## Advanced: Multiple Hurtboxes {#multiple}

Different damage zones (head, body, legs):

```gdscript
extends CharacterBody2D

@export var base_health: int = 100

var _health: int = base_health

@onready var _head_hurtbox: Area2D = %HeadHurtBox
@onready var _body_hurtbox: Area2D = %BodyHurtBox

func _ready() -> void:
	_head_hurtbox.area_entered.connect(_on_head_hit)
	_body_hurtbox.area_entered.connect(_on_body_hit)

func _on_head_hit(hitbox: Area2D) -> void:
	var damage: int = hitbox.get("damage") if hitbox.has_method("get") else 10
	take_damage(damage * 2)  # Headshot = 2x damage

func _on_body_hit(hitbox: Area2D) -> void:
	var damage: int = hitbox.get("damage") if hitbox.has_method("get") else 10
	take_damage(damage)

func take_damage(amount: int) -> void:
	_health -= amount
	if _health <= 0:
		die()
```

**Scene structure:**
```
CharacterBody2D
├── Sprite2D
├── CollisionShape2D (for movement)
├── HeadHurtBox (Area2D)
│   └── CollisionShape2D
└── BodyHurtBox (Area2D)
    └── CollisionShape2D
```

## Temporary Invincibility {#invincibility}

Prevent damage stacking:

```gdscript
extends CharacterBody2D

@export var invincibility_duration: float = 0.5

var _health: int = 100
var _is_invincible: bool = false

@onready var _hurtbox: Area2D = %HurtBox

func take_damage(amount: int) -> void:
	if _is_invincible:
		return

	_health -= amount
	_start_invincibility()

	if _health <= 0:
		die()

func _start_invincibility() -> void:
	_is_invincible = true
	_hurtbox.monitorable = false  # Can't be hit

	# Visual feedback
	var tween := create_tween()
	tween.tween_property($Sprite2D, "modulate:a", 0.5, 0.1)
	tween.tween_property($Sprite2D, "modulate:a", 1.0, 0.1)
	tween.set_loops(int(invincibility_duration / 0.2))

	await get_tree().create_timer(invincibility_duration).timeout

	_is_invincible = false
	_hurtbox.monitorable = true
```

## One-Hit Detection {#one-hit}

Ensure hitbox only damages once per attack:

```gdscript
extends Area2D

@export var damage: int = 25

var _hit_bodies: Array[Node] = []

func _ready() -> void:
	body_entered.connect(_on_body_entered)

func reset_hits() -> void:
	_hit_bodies.clear()

func _on_body_entered(body: PhysicsBody2D) -> void:
	# Skip if already hit this attack
	if body in _hit_bodies:
		return

	if body.has_method("take_damage"):
		body.take_damage(damage)
		_hit_bodies.append(body)

# Call from animation at attack start
func _on_attack_started() -> void:
	reset_hits()
	monitoring = true

# Call from animation at attack end
func _on_attack_ended() -> void:
	monitoring = false
```

## Performance Optimization {#performance}

```gdscript
extends Area2D

var _is_active: bool = false

# Enable only when needed
func set_active(active: bool) -> void:
	if _is_active == active:
		return

	_is_active = active
	monitoring = active
	monitorable = active

	# Also disable collision shape for better performance
	if has_node("CollisionShape2D"):
		$CollisionShape2D.disabled = not active

# Example: activate only when enemy is near player
func _on_detection_range_body_entered(body: Node2D) -> void:
	if body.is_in_group("player"):
		set_active(true)

func _on_detection_range_body_exited(body: Node2D) -> void:
	if body.is_in_group("player"):
		set_active(false)
```

## Best Practices & Pitfalls {#best-practices}

**Collision Layer Setup:**
- Always set hitbox `collision_mask` to match hurtbox `collision_layer`
- Use distinct layers for player/enemy hitboxes and hurtboxes
- Disable `monitoring` on hitboxes until attack starts

**Duck-Typing Pattern:**
- Use `has_method("take_damage")` for flexible damage handling
- Allow any scene to respond to damage without inheritance
- Store damage value on hitbox as `@export var damage: int`

**Performance:**
- Disable `monitoring` when hitbox is inactive (not attacking)
- Disable collision shapes entirely for dormant enemies
- Use `set_deferred()` when modifying collision during physics processing

**Common Mistakes:**
- Forgetting to disable hitbox after attack animation
- Not using `set_deferred()` when disabling collision shapes
- Having both hitbox and hurtbox actively monitoring (causes double detection)
- Using same collision layer for different team hitboxes (friendly fire)

**Animation Integration:**
- Add boolean tracks to enable/disable hitbox monitoring
- Sync hitbox timing precisely with visual attack frames
- Reset hit tracking at animation start to prevent duplicate hits

**Godot 4 Migration:**
- Collision layer behavior changed from Godot 3
- Test collision mask/layer interactions carefully
- Use Inspector's layer visualization for debugging

## Related Patterns

- **[Area Triggers](areas.md)** - General Area2D/Area3D usage and signals
- **[Collision Detection](collision.md)** - Collision layers and masks setup
- **[Health System](../patterns/health-system.md)** - Managing entity health and death
- **[Animation Player](../animation/animation-player.md)** - Controlling hitbox timing with animations
