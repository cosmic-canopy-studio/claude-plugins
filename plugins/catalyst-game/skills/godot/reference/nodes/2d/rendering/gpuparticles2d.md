---
class: GPUParticles2D
category: nodes/2d/rendering
complexity: advanced
tags: [2d, particles, effects, rendering, gpu]
---

# GPUParticles2D

**Inherits:** Node2D < CanvasItem < Node < Object

A 2D particle emitter.

## Description

2D particle node used to create a variety of particle systems and effects. GPUParticles2D features an emitter that generates some number of particles at a given rate.

Use the `process_material` property to add a ParticleProcessMaterial to configure particle appearance and behavior. Alternatively, you can add a ShaderMaterial which will be applied to all particles.

2D particles can optionally collide with LightOccluder2D, but they don't collide with PhysicsBody2D nodes.

## Properties

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `amount` | `int` | `8` | The number of particles to emit in one emission cycle |
| `amount_ratio` | `float` | `1.0` | The ratio of particles that should actually be emitted |
| `collision_base_size` | `float` | `1.0` | Multiplier for particle's collision radius |
| `draw_order` | `DrawOrder` | `1` | Particle draw order |
| `emitting` | `bool` | `true` | If `true`, particles are being emitted |
| `explosiveness` | `float` | `0.0` | How rapidly particles in an emission cycle are emitted |
| `fixed_fps` | `int` | `30` | Particle system's frame rate |
| `fract_delta` | `bool` | `true` | If `true`, fractional delta for smoother display |
| `interp_to_end` | `float` | `0.0` | Causes particles to interpolate towards end of lifetime |
| `interpolate` | `bool` | `true` | Enables particle interpolation for smoother movement |
| `lifetime` | `float` | `1.0` | Amount of time each particle will exist (in seconds) |
| `local_coords` | `bool` | `false` | If `true`, particles use parent node's coordinate space |
| `one_shot` | `bool` | `false` | If `true`, only one emission cycle occurs |
| `preprocess` | `float` | `0.0` | Particle system starts as if it had already run for this many seconds |
| `process_material` | `Material` | | Material for processing particles |
| `randomness` | `float` | `0.0` | Emission lifetime randomness ratio |
| `seed` | `int` | `0` | Random seed used by the particle system |
| `speed_scale` | `float` | `1.0` | Particle system's running speed scaling ratio |
| `sub_emitter` | `NodePath` | `NodePath("")` | Path to another GPUParticles2D node used as subemitter |
| `texture` | `Texture2D` | | Particle texture |
| `trail_enabled` | `bool` | `false` | If `true`, enables particle trails |
| `trail_lifetime` | `float` | `0.3` | Amount of time particle's trail should represent |
| `trail_section_subdivisions` | `int` | `4` | Number of subdivisions for trail rendering |
| `trail_sections` | `int` | `8` | Number of sections for trail rendering |
| `use_fixed_seed` | `bool` | `false` | If `true`, particles use the same seed for every simulation |
| `visibility_rect` | `Rect2` | `Rect2(-100, -100, 200, 200)` | Region which needs to be visible for particles to be active |

## Methods

| Return | Method |
|--------|--------|
| `Rect2` | `capture_rect()` |
| `void` | `convert_from_particles(particles: Node)` |
| `void` | `emit_particle(xform: Transform2D, velocity: Vector2, color: Color, custom: Color, flags: int)` |
| `void` | `request_particles_process(process_time: float)` |
| `void` | `restart(keep_seed: bool = false)` |

## Signals

- **finished()**: Emitted when all active particles have finished processing (one_shot only)

## Enumerations

### DrawOrder
- **DRAW_ORDER_INDEX** (0): Particles are drawn in the order emitted
- **DRAW_ORDER_LIFETIME** (1): Particles drawn in order of remaining lifetime (highest first)
- **DRAW_ORDER_REVERSE_LIFETIME** (2): Particles drawn in reverse order of lifetime (lowest first)

### EmitFlags
- **EMIT_FLAG_POSITION** (1): Particle starts at specified position
- **EMIT_FLAG_ROTATION_SCALE** (2): Particle starts with specified rotation and scale
- **EMIT_FLAG_VELOCITY** (4): Particle starts with specified velocity vector
- **EMIT_FLAG_COLOR** (8): Particle starts with specified color
- **EMIT_FLAG_CUSTOM** (16): Particle starts with specified CUSTOM data

## Quick Examples

### Basic particle emitter

```gdscript
@onready var particles: GPUParticles2D = $GPUParticles2D

func _ready() -> void:
    particles.emitting = true
    particles.amount = 100
    particles.lifetime = 2.0
```

### One-shot particle burst

```gdscript
@onready var particles: GPUParticles2D = $GPUParticles2D

func _ready() -> void:
    particles.one_shot = true
    particles.emitting = false
    particles.finished.connect(_on_particles_finished)

func trigger_burst() -> void:
    particles.restart()

func _on_particles_finished() -> void:
    print("Particle burst completed")
```

### Configure particle material

```gdscript
@onready var particles: GPUParticles2D = $GPUParticles2D

func _ready() -> void:
    var material: ParticleProcessMaterial = ParticleProcessMaterial.new()
    material.direction = Vector3(0, -1, 0)
    material.initial_velocity_min = 100.0
    material.initial_velocity_max = 200.0
    material.gravity = Vector3(0, 98, 0)
    particles.process_material = material
```

## Common Patterns

### Explosion effect

```gdscript
func create_explosion(pos: Vector2) -> void:
    var particles: GPUParticles2D = $ExplosionParticles
    particles.global_position = pos
    particles.one_shot = true
    particles.explosiveness = 1.0
    particles.restart()
```

### Continuous emission with speed control

```gdscript
@onready var particles: GPUParticles2D = $GPUParticles2D

func set_particle_speed(speed: float) -> void:
    particles.speed_scale = speed

func pause_particles() -> void:
    particles.speed_scale = 0.0

func resume_particles() -> void:
    particles.speed_scale = 1.0
```

### Trail effect

```gdscript
@onready var particles: GPUParticles2D = $GPUParticles2D

func enable_trail() -> void:
    particles.trail_enabled = true
    particles.trail_lifetime = 0.5
    particles.trail_sections = 12
    particles.trail_section_subdivisions = 4
```

### Particle emission from code

```gdscript
func emit_single_particle(pos: Vector2, vel: Vector2) -> void:
    var xform: Transform2D = Transform2D(0, pos)
    var color: Color = Color.WHITE
    var custom: Color = Color.BLACK  # (rotation, age, animation, lifetime)
    $GPUParticles2D.emit_particle(
        xform,
        vel,
        color,
        custom,
        GPUParticles2D.EMIT_FLAG_POSITION | GPUParticles2D.EMIT_FLAG_VELOCITY
    )
```

### Adjust visibility rect

```gdscript
func auto_fit_visibility_rect() -> void:
    var rect: Rect2 = $GPUParticles2D.capture_rect()
    $GPUParticles2D.visibility_rect = rect
```

## Best Practices

- Use `amount_ratio` to dynamically change particle count without restarting
- Set `visibility_rect` large enough to contain all particles
- Enable `one_shot` for effects that should play once (explosions, impacts)
- Use `local_coords = true` for particles that follow the emitter
- Set `fixed_fps` to balance performance and visual quality
- For expensive effects, use `amount_ratio` instead of changing `amount`
- Preprocess is expensive - use sparingly and with low values
- Use `emit_particle()` for precise particle spawning control
- Call `restart()` for one-shot emitters instead of toggling `emitting`
- Only supported on Forward+ and Mobile rendering methods (not Compatibility)

## Performance Tips

- Lower `amount` for better performance
- Increase `fixed_fps` interval to reduce computation
- Use smaller `visibility_rect` to avoid processing off-screen particles
- Disable `interpolate` if not needed
- Consider using CPUParticles2D for simpler effects

## See Also

- [CPUParticles2D](cpuparticles2d.md) - CPU-based particle system
- [ParticleProcessMaterial](../../resources/particleprocessmaterial.md) - Material for particle processing
