---
class: GPUParticles3D
godot_version: "4.x"
sources:
  - repos/godot-docs/classes/class_gpuparticles3d.rst
status: extracted
---

# GPUParticles3D

**Inherits:** GeometryInstance3D < VisualInstance3D < Node3D < Node < Object

A 3D particle emitter.

## Description

3D particle node used to create a variety of particle systems and effects. GPUParticles3D features an emitter that generates some number of particles at a given rate.

Use process_material to add a ParticleProcessMaterial to configure particle appearance and behavior. Alternatively, you can add a ShaderMaterial which will be applied to all particles.

## Signals

- **finished()** - Emitted when all active particles have finished processing. To immediately restart the emission cycle, call restart(). This signal is never emitted when one_shot is disabled, as particles will be emitted and processed continuously.

## Properties

| Property | Type | Default |
|----------|------|---------|
| amount | int | 8 |
| amount_ratio | float | 1.0 |
| collision_base_size | float | 0.01 |
| draw_order | DrawOrder | 0 |
| draw_pass_1 | Mesh | |
| draw_pass_2 | Mesh | |
| draw_pass_3 | Mesh | |
| draw_pass_4 | Mesh | |
| draw_passes | int | 1 |
| draw_skin | Skin | |
| emitting | bool | true |
| explosiveness | float | 0.0 |
| fixed_fps | int | 30 |
| fract_delta | bool | true |
| interp_to_end | float | 0.0 |
| interpolate | bool | true |
| lifetime | float | 1.0 |
| local_coords | bool | false |
| one_shot | bool | false |
| preprocess | float | 0.0 |
| process_material | Material | |
| randomness | float | 0.0 |
| seed | int | 0 |
| speed_scale | float | 1.0 |
| sub_emitter | NodePath | NodePath("") |
| trail_enabled | bool | false |
| trail_lifetime | float | 0.3 |
| transform_align | TransformAlign | 0 |
| use_fixed_seed | bool | false |
| visibility_aabb | AABB | AABB(-4, -4, -4, 8, 8, 8) |

## Methods

| Return | Method |
|--------|--------|
| AABB | capture_aabb() const |
| void | convert_from_particles(particles: Node) |
| void | emit_particle(xform: Transform3D, velocity: Vector3, color: Color, custom: Color, flags: int) |
| Mesh | get_draw_pass_mesh(pass: int) const |
| void | request_particles_process(process_time: float) |
| void | restart(keep_seed: bool = false) |
| void | set_draw_pass_mesh(pass: int, mesh: Mesh) |

## Constants

**MAX_DRAW_PASSES** = 4 - Maximum number of draw passes supported.

## Enumerations

### DrawOrder

- **DRAW_ORDER_INDEX** = 0 - Particles are drawn in the order emitted. Only option that supports motion vectors for effects like TAA.
- **DRAW_ORDER_LIFETIME** = 1 - Particles are drawn in order of remaining lifetime. The particle with the highest lifetime is drawn at the front.
- **DRAW_ORDER_REVERSE_LIFETIME** = 2 - Particles are drawn in reverse order of remaining lifetime. The particle with the lowest lifetime is drawn at the front.
- **DRAW_ORDER_VIEW_DEPTH** = 3 - Particles are drawn in order of depth.

### EmitFlags

- **EMIT_FLAG_POSITION** = 1 - Particle starts at the specified position.
- **EMIT_FLAG_ROTATION_SCALE** = 2 - Particle starts with specified rotation and scale.
- **EMIT_FLAG_VELOCITY** = 4 - Particle starts with the specified velocity vector, which defines the emission direction and speed.
- **EMIT_FLAG_COLOR** = 8 - Particle starts with specified color.
- **EMIT_FLAG_CUSTOM** = 16 - Particle starts with specified CUSTOM data.

### TransformAlign

- **TRANSFORM_ALIGN_DISABLED** = 0
- **TRANSFORM_ALIGN_Z_BILLBOARD** = 1
- **TRANSFORM_ALIGN_Y_TO_VELOCITY** = 2
- **TRANSFORM_ALIGN_Z_BILLBOARD_Y_TO_VELOCITY** = 3

## Property Details

### amount / amount_ratio

The number of particles to emit in one emission cycle. The effective emission rate is `(amount * amount_ratio) / lifetime` particles per second.

Note: Changing amount will cause the particle system to restart. To avoid this, change amount_ratio instead.

amount_ratio can be used to create effects that make the number of emitted particles vary over time without restarting the system. However, reducing amount_ratio has no performance benefit, since resources need to be allocated and processed for the total amount of particles regardless of the ratio.

### lifetime

The amount of time each particle will exist (in seconds). The effective emission rate is `(amount * amount_ratio) / lifetime` particles per second.

### one_shot

If true, only the number of particles equal to amount will be emitted.

### emitting

If true, particles are being emitted. emitting can be used to start and stop particles from emitting. However, if one_shot is true setting emitting to true will not restart the emission cycle unless all active particles have finished processing. Use the finished signal to be notified once all active particles finish processing.

Tip: If your one_shot emitter needs to immediately restart emitting particles once finished signal is received, consider calling restart() instead of setting emitting.

### explosiveness

Time ratio between each emission. If 0, particles are emitted continuously. If 1, all particles are emitted simultaneously.

### randomness

Emission randomness ratio.

### local_coords

If true, particles use the parent node's coordinate space (known as local coordinates). This will cause particles to move and rotate along the GPUParticles3D node (and its parents) when it is moved or rotated. If false, particles use global coordinates; they will not move or rotate along the GPUParticles3D node (and its parents) when it is moved or rotated.

### process_material

Material for processing particles. Can be a ParticleProcessMaterial or a ShaderMaterial.

### draw_passes / draw_pass_1-4

The number of draw passes when rendering particles. Each draw pass uses a mesh specified by the corresponding draw_pass_N property.

### visibility_aabb

The AABB that determines the node's region which needs to be visible on screen for the particle system to be active. Particle collisions and attraction will only occur within this area.

Grow the box if particles suddenly appear/disappear when the node enters/exits the screen. The AABB can be grown via code or with the Particles → Generate AABB editor tool.

### speed_scale

Speed scaling ratio. A value of 0 can be used to pause the particles.

### fixed_fps / interpolate / fract_delta

The particle system's frame rate is fixed to a value. For example, changing the value to 2 will make the particles render at 2 frames per second. Note this does not slow down the simulation of the particle system itself.

interpolate enables particle interpolation, which makes the particle movement smoother when their fixed_fps is lower than the screen refresh rate.

fract_delta results in fractional delta calculation which has a smoother particles display effect.

### preprocess

Amount of time to preprocess the particles before animation starts. Lets you start the animation some time after particles have started emitting.

Note: This can be very expensive if set to a high number as it requires running the particle shader a number of times equal to the fixed_fps (or 30, if fixed_fps is 0) for every second.

### trail_enabled / trail_lifetime

If true, enables particle trails using a mesh skinning system. Designed to work with RibbonTrailMesh and TubeTrailMesh.

Note: BaseMaterial3D.use_particle_trails must also be enabled on the particle mesh's material.

### sub_emitter

Path to another GPUParticles3D node that will be used as a subemitter. Subemitters can be used to achieve effects such as fireworks, sparks on collision, bubbles popping into water drops, and more.

Note: When sub_emitter is set, the target GPUParticles3D node will no longer emit particles on its own.

## Method Details

### restart()

Restarts the particle emission cycle, clearing existing particles. To avoid particles vanishing from the viewport, wait for the finished signal before calling.

Note: The finished signal is only emitted by one_shot emitters.

If keep_seed is true, the current random seed will be preserved. Useful for seeking and playback.

### emit_particle()

Emits a single particle. Whether xform, velocity, color and custom are applied depends on the value of flags. See EmitFlags.

The default ParticleProcessMaterial will overwrite color and use the contents of custom as (rotation, age, animation, lifetime).

Note: emit_particle() is only supported on the Forward+ and Mobile rendering methods, not Compatibility.

### capture_aabb()

Returns the axis-aligned bounding box that contains all the particles that are active in the current frame.

### convert_from_particles()

Sets this node's properties to match a given CPUParticles3D node.
