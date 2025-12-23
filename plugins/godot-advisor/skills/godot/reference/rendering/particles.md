---
topic: particles
version: 2025.12.21
godot_version: "4.3"
sources:
  - "https://docs.godotengine.org/en/stable/classes/class_gpuparticles2d.html"
  - "https://docs.godotengine.org/en/stable/classes/class_gpuparticles3d.html"
  - "https://docs.godotengine.org/en/stable/classes/class_cpuparticles2d.html"
  - "https://docs.godotengine.org/en/stable/tutorials/3d/particles/index.html"
  - "repos/godot_node_essentials/screens/gpu_particles_2d/"
  - "repos/godot_node_essentials/common/2d/explosion_effect_2d/"
  - "repos/godot_node_essentials/common/3d/collision_particles_3d/"
status: complete
---

# Particle Systems

GPU and CPU particle systems for creating visual effects like explosions, trails, smoke, fire, and ambient effects in Godot 4.

## Quick Start

```gdscript
# Toggle particle emission
@onready var particles: GPUParticles2D = $GPUParticles2D

func _ready() -> void:
    particles.emitting = true

# One-shot effect (e.g., explosion)
@onready var explosion: GPUParticles2D = $ExplosionGPUParticles2D

func explode() -> void:
    explosion.one_shot = true
    explosion.emitting = true
```

## GPU vs CPU Particles

### GPUParticles2D / GPUParticles3D

**When to use:**
- High particle counts (100s to 1000s)
- Continuous effects (smoke, fire, ambient)
- Complex physics (attractors, collisions)
- Trail effects

**Properties:**
- Rendered on GPU for maximum performance
- Uses `ParticleProcessMaterial` for physics
- Supports sub-emitters and trails
- Amount: typically 16-1000+ particles

**Limitations:**
- Cannot read particle state from code
- Requires GPU support
- More complex setup

### CPUParticles2D / CPUParticles3D

**When to use:**
- Simple effects with few particles (< 100)
- Need particle state access in code
- Targeting low-end hardware
- Prototyping (simpler setup)

**Properties:**
- Rendered on CPU
- Built-in physics properties (no material needed)
- Can query individual particle positions
- Amount: typically 8-100 particles

**Performance:**
- Lower overhead for small counts
- Scales poorly with particle count
- Better for mobile/web

## Common Patterns

### Continuous Emission

For looping effects like thrusters, smoke, or ambient particles:

```gdscript
# Trail effect behind moving object
extends Sprite2D

@onready var trail_left: GPUParticles2D = %TrailLeftGPUParticles2D
@onready var trail_right: GPUParticles2D = %TrailRightGPUParticles2D

func _unhandled_input(_event: InputEvent) -> void:
    # Toggle trails based on input
    var is_moving: bool = Input.is_action_pressed("move_up")
    trail_left.emitting = is_moving
    trail_right.emitting = is_moving
```

**Scene Setup (2D):**
```
ShipPlayer (Sprite2D)
├── TrailLeftGPUParticles2D
│   ├── amount: 20
│   ├── lifetime: 0.5
│   ├── trail_enabled: true
│   └── process_material: ParticleProcessMaterial
└── TrailRightGPUParticles2D
```

### One-Shot Effects

For explosions, impacts, and event-triggered effects:

```gdscript
# Explosion on click/impact
extends Node2D

@export var explosion_scene: PackedScene

func create_explosion(at_position: Vector2) -> void:
    var explosion: Node2D = explosion_scene.instantiate()
    explosion.global_position = at_position
    add_child(explosion)
    # Explosion auto-frees after animation completes
```

**Explosion Scene Structure:**
```
ExplosionEffect2D (Node2D)
├── SmokeGPUParticles2D
│   ├── amount: 16
│   ├── lifetime: 3.0
│   ├── one_shot: false (controlled by animation)
│   ├── explosiveness: 0.6
│   └── preprocess: 0.6
├── FireTrailGPUParticles2D
│   ├── amount: 20
│   ├── lifetime: 0.5
│   ├── trail_enabled: true
│   └── randomness: 0.5
├── FireBurstGPUParticles2D
│   ├── amount: 64
│   ├── lifetime: 0.5
│   ├── explosiveness: 0.3
│   └── randomness: 1.0
├── SparkleGPUParticles2D
│   ├── amount: 32
│   ├── explosiveness: 0.2
│   └── randomness: 1.0
└── AnimationPlayer
    └── explode animation (calls queue_free at end)
```

**Animation-controlled emission:**
```gdscript
# AnimationPlayer controls emitting property
# Track: "SmokeGPUParticles2D:emitting"
# 0.0s: true
# 0.5s: false
# 3.0s: calls queue_free() on parent
```

### Charging/Building Effects

Particles that intensify over time:

```gdscript
# Charging laser effect
@onready var charging_particles: GPUParticles2D = $ChargingGPUParticles2D
@onready var animation_player: AnimationPlayer = $AnimationPlayer

func start_charging() -> void:
    charging_particles.emitting = true
    animation_player.play("charge")
    # Animation tweens speed_scale: 0.5 → 4.0 over 2 seconds
    # Animation tweens self_modulate: (1,1,1,1) → (1.5,1.5,1.5,1)

func release_charge() -> void:
    charging_particles.emitting = false
    fire_weapon()
```

### Landing/Impact Dust

Event-triggered particle spawn:

```gdscript
extends CharacterBody2D

@onready var dust_puff_spawner: Spawner2D = $DustPuffSpawner2D
var _was_on_floor: bool = false

func _physics_process(delta: float) -> void:
    # ... movement code ...
    move_and_slide()

    # Detect landing
    if is_on_floor() and not _was_on_floor:
        dust_puff_spawner.spawn()

    _was_on_floor = is_on_floor()
```

**Spawner pattern:**
```gdscript
# Reusable spawner node
class_name Spawner2D extends Node2D

@export var scene_to_spawn: PackedScene

func spawn() -> Node:
    if not scene_to_spawn:
        return null

    var instance: Node = scene_to_spawn.instantiate()
    if instance is Node2D:
        instance.global_position = global_position
    get_tree().current_scene.add_child(instance)
    return instance
```

### Collision Particles (3D)

Spawn particles at impact points:

```gdscript
# 3D collision impact
extends RigidBody3D

@export var collision_particles_scene: PackedScene

func _on_body_entered(body: Node) -> void:
    var particles: GPUParticles3D = collision_particles_scene.instantiate()
    particles.global_position = global_position
    particles.emitting = true
    get_tree().current_scene.add_child(particles)
```

**CollisionParticles3D setup:**
```
CollisionGPUParticles3D
├── emitting: false
├── amount: 10
├── lifetime: 0.25
├── one_shot: true
├── process_material: ParticleProcessMaterial
│   ├── direction: Vector3(0, 0, -1)
│   ├── spread: 22.0
│   ├── initial_velocity: 2.7 - 3.3
│   ├── gravity: Vector3(0, -5, 0)
│   └── scale_curve: (fade over lifetime)
└── draw_pass_1: QuadMesh with StandardMaterial3D
    ├── transparency: enabled
    ├── blend_mode: additive
    ├── billboard_mode: particles
    └── vertex_color_use_as_albedo: true
```

## ParticleProcessMaterial Configuration

The `process_material` defines particle physics and appearance.

### Key Properties

| Property | Type | Description |
|----------|------|-------------|
| `emission_shape` | int | 0=Point, 1=Sphere, 2=Box, 3=Points, 4=Directed Points |
| `emission_sphere_radius` | float | Radius for sphere emission |
| `emission_box_extents` | Vector3 | Size for box emission |
| `particle_flag_disable_z` | bool | 2D mode (particles stay in XY plane) |
| `spread` | float | Angle spread in degrees (0-180) |
| `initial_velocity_min/max` | float | Starting speed range |
| `gravity` | Vector3 | Gravity force (Vector3.ZERO for no gravity) |
| `angular_velocity_min/max` | float | Rotation speed range |
| `damping_min/max` | float | Deceleration over time |
| `scale_min/max` | float | Size range at spawn |
| `scale_curve` | CurveTexture | Size over lifetime |
| `color` | Color | Base color multiplier |
| `color_ramp` | GradientTexture1D | Color over lifetime |

### Common Configurations

**Explosion smoke:**
```gdscript
# Create in scene or code
var material := ParticleProcessMaterial.new()
material.emission_shape = ParticleProcessMaterial.EMISSION_SHAPE_SPHERE
material.emission_sphere_radius = 40.0
material.spread = 180.0
material.initial_velocity_min = 5.0
material.initial_velocity_max = 40.0
material.gravity = Vector3.ZERO
material.damping_min = 20.0
material.damping_max = 40.0
material.scale_min = 0.5
material.scale_max = 2.6
# Set scale_curve and color_ramp via resources
```

**Fire burst:**
```gdscript
var material := ParticleProcessMaterial.new()
material.particle_flag_disable_z = true  # 2D mode
material.spread = 180.0
material.initial_velocity_min = 50.0
material.initial_velocity_max = 200.0
material.angular_velocity_min = 60.0
material.angular_velocity_max = 80.0
material.gravity = Vector3.ZERO
material.damping_min = 80.0
material.damping_max = 100.0
material.scale_min = 0.8
material.scale_max = 1.4
```

**Radial sparkles:**
```gdscript
var material := ParticleProcessMaterial.new()
material.emission_sphere_radius = 50.0
material.spread = 180.0
material.gravity = Vector3.ZERO
material.radial_accel_min = 160.0  # Push outward
material.radial_accel_max = 250.0
material.tangential_accel_min = 100.0  # Circular motion
material.tangential_accel_max = 100.0
material.scale_min = 0.1
material.scale_max = 0.3
```

**Charging effect (inward pull):**
```gdscript
var material := ParticleProcessMaterial.new()
material.particle_flag_disable_z = true
material.emission_sphere_radius = 60.0
material.gravity = Vector3.ZERO
material.radial_accel_min = -80.0  # Negative = pull inward
material.radial_accel_max = -60.0
material.scale_min = 0.3
material.scale_max = 0.8
```

## Advanced Features

### Trails

Create motion trails behind particles:

```gdscript
@onready var trail_particles: GPUParticles2D = $TrailGPUParticles2D

func _ready() -> void:
    trail_particles.trail_enabled = true
    trail_particles.trail_lifetime = 0.3  # Trail duration
    # Increase amount for smoother trails
```

**Scene setup:**
```
GPUParticles2D
├── amount: 20
├── lifetime: 0.5
├── trail_enabled: true
├── trail_lifetime: 0.3
├── process_material: ParticleProcessMaterial
│   ├── initial_velocity: 400-1000
│   ├── tangential_accel: 1000
│   └── damping: 1500
└── texture: smooth gradient sprite
```

### Speed Control

Adjust particle speed at runtime:

```gdscript
@onready var particles: GPUParticles2D = $GPUParticles2D

func speed_up() -> void:
    particles.speed_scale = 2.0  # 2x faster

func slow_down() -> void:
    particles.speed_scale = 0.5  # 2x slower

func pause() -> void:
    particles.speed_scale = 0.0  # Frozen
```

### Explosiveness vs Randomness

Control particle spawn timing:

```gdscript
# Explosiveness: 0.0-1.0
# 0.0 = steady stream over lifetime
# 1.0 = all particles spawn immediately
particles.explosiveness = 0.6  # Burst-like

# Randomness: 0.0-1.0
# 0.0 = uniform particle timing
# 1.0 = random particle timing
particles.randomness = 1.0  # Chaotic
```

**Common combinations:**
- Fire/smoke: `explosiveness=0.3, randomness=1.0`
- Explosion: `explosiveness=0.6, randomness=0.5`
- Steady stream: `explosiveness=0.0, randomness=0.2`
- Burst: `explosiveness=1.0, randomness=0.0`

### Preprocess

Start particles mid-cycle for instant visual:

```gdscript
# Smoke that appears already dispersed
particles.preprocess = 0.6  # Simulates 60% of lifetime

func _ready() -> void:
    particles.emitting = true
    # Particles appear already spread out
```

### Local vs Global Coordinates

```gdscript
# Local coordinates (default): particles move with parent
particles.local_coords = true
# Use for: ship trails, character effects

# Global coordinates: particles stay in world space
particles.local_coords = false
# Use for: explosions, environmental effects
```

### Modulation

Adjust brightness and color:

```gdscript
# Brighten particles
particles.modulate = Color(1.2, 1.2, 1.2, 1.0)

# Self-modulate (doesn't affect children)
particles.self_modulate = Color(1.5, 1.5, 1.5, 1.0)

# Animate with Tween
var tween := create_tween()
tween.tween_property(particles, "self_modulate", Color(2.0, 2.0, 2.0, 1.0), 1.0)
```

## 3D-Specific Features

### Draw Passes

3D particles use meshes instead of textures:

```gdscript
@onready var particles_3d: GPUParticles3D = $GPUParticles3D

func _ready() -> void:
    # Create mesh for particles
    var quad_mesh := QuadMesh.new()
    quad_mesh.size = Vector2(0.1, 0.1)

    # Create material
    var material := StandardMaterial3D.new()
    material.transparency = BaseMaterial3D.TRANSPARENCY_ALPHA
    material.blend_mode = BaseMaterial3D.BLEND_MODE_ADD
    material.shading_mode = BaseMaterial3D.SHADING_MODE_UNSHADED
    material.billboard_mode = BaseMaterial3D.BILLBOARD_PARTICLES
    material.vertex_color_use_as_albedo = true
    material.albedo_color = Color(4, 4, 4, 1)  # HDR brightness

    quad_mesh.material = material
    particles_3d.draw_pass_1 = quad_mesh
```

**Billboard modes:**
- `BILLBOARD_DISABLED`: No billboarding (mesh orientation)
- `BILLBOARD_ENABLED`: Face camera
- `BILLBOARD_PARTICLES`: Face camera, Y-axis locked to particle direction
- `BILLBOARD_FIXED_Y`: Face camera, Y-axis always up

### Visibility AABB

3D particles require bounding box for culling:

```gdscript
# Expand if particles escape default bounds
particles_3d.visibility_aabb = AABB(Vector3(-10, -10, -10), Vector2(20, 20, 20))

# Auto-generate from current particles
particles_3d.capture_aabb()  # Call after emitting for a while
```

## Best Practices & Pitfalls

### Managing One-Shot Particles

**Don't:**
```gdscript
# Creates memory leak - particles never freed
func explode() -> void:
    var explosion: GPUParticles2D = explosion_scene.instantiate()
    add_child(explosion)
    explosion.emitting = true
    # Particles stay in scene forever!
```

**Do:**
```gdscript
# AnimationPlayer calls queue_free after emission
# explosion.tscn:
# AnimationPlayer with "explode" animation
# - Track 0: Sets emitting = true at 0.0s, false at 0.5s
# - Track 1: Calls queue_free() at 3.0s (after lifetime)

func explode() -> void:
    var explosion: Node2D = explosion_scene.instantiate()
    add_child(explosion)
    # AnimationPlayer autoplay handles everything
```

**Alternative with code:**
```gdscript
func explode() -> void:
    var explosion: GPUParticles2D = explosion_scene.instantiate()
    add_child(explosion)
    explosion.emitting = true
    explosion.finished.connect(explosion.queue_free)
```

### Performance Optimization

**Use appropriate counts:**
- Small effects: 8-16 particles
- Medium effects: 32-64 particles
- Large effects: 100-200 particles
- Massive effects: 500-1000+ particles

**Reduce draw calls:**
```gdscript
# Bad: Many small particle systems
for i in 10:
    var smoke: GPUParticles2D = smoke_scene.instantiate()
    add_child(smoke)

# Good: One system with higher amount
var smoke: GPUParticles2D = smoke_scene.instantiate()
smoke.amount = 100  # Instead of 10 systems with 10 each
add_child(smoke)
```

**Disable when off-screen:**
```gdscript
extends GPUParticles2D

func _on_visible_on_screen_notifier_2d_screen_exited() -> void:
    emitting = false

func _on_visible_on_screen_notifier_2d_screen_entered() -> void:
    emitting = true
```

### Common Mistakes

**Forgetting to set texture:**
```gdscript
# Particles won't appear without texture (2D) or draw_pass (3D)
particles.texture = preload("res://effects/particle.png")
```

**Wrong coordinate space:**
```gdscript
# Explosion particles that move with deleted object
particles.local_coords = true  # Wrong!
particles.local_coords = false # Correct - stays at explosion point
```

**Lifetime too short:**
```gdscript
# Particles disappear before visible
particles.lifetime = 0.1  # Too short
particles.lifetime = 0.5  # Better for quick effects
particles.lifetime = 2.0  # Better for lingering smoke
```

**Z-index issues (2D):**
```gdscript
# Particles behind sprites
particles.z_index = 1      # Render above most objects
particles.z_as_relative = false  # Absolute z-index
```

### Debugging Particles

**View particle bounds:**
```gdscript
# In editor: Debug > Visible Collision Shapes
# Shows emission shapes and particle AABB
```

**Test emission shapes:**
```gdscript
# Temporarily increase lifetime to see full spread
particles.lifetime = 5.0  # Was 0.5
```

**Verify material:**
```gdscript
if particles.process_material == null:
    push_warning("Particles missing process_material!")
```

## Properties Quick Reference

### GPUParticles2D / GPUParticles3D

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `emitting` | bool | false | Actively spawning particles |
| `amount` | int | 8 | Max particle count |
| `lifetime` | float | 1.0 | Particle duration (seconds) |
| `one_shot` | bool | false | Emit once then stop |
| `preprocess` | float | 0.0 | Pre-simulate time (seconds) |
| `speed_scale` | float | 1.0 | Simulation speed multiplier |
| `explosiveness` | float | 0.0 | Spawn synchronization (0-1) |
| `randomness` | float | 0.0 | Timing randomization (0-1) |
| `fixed_fps` | int | 30 | Simulation framerate |
| `fract_delta` | bool | true | Smooth sub-frame interpolation |
| `interpolate` | bool | true | Interpolate between frames |
| `process_material` | Material | null | Physics/appearance definition |
| `texture` | Texture2D | null | Particle sprite (2D only) |
| `local_coords` | bool | false | Coordinate space (true=local) |
| `draw_order` | int | INDEX | Particle sort order |
| `trail_enabled` | bool | false | Enable motion trails |
| `trail_lifetime` | float | 0.3 | Trail duration |

### GPUParticles3D Only

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `draw_pass_1` | Mesh | null | Primary particle mesh |
| `draw_passes` | int | 1 | Number of meshes (1-4) |
| `visibility_aabb` | AABB | auto | Culling bounding box |

### Signals

| Signal | Description |
|--------|-------------|
| `finished()` | Emitted when one_shot completes |

## Related

- [Camera Reference](camera.md) - Viewport culling for particles
- [Sprites Reference](sprites.md) - Creating particle textures
- [Shaders Reference](shaders.md) - Custom particle materials
- [Animation Reference](../animation/animation-player.md) - Controlling particle timing
