---
class: MeshInstance3D
godot_version: "4.x"
sources:
  - repos/godot-docs/classes/class_meshinstance3d.rst
status: extracted
---

# MeshInstance3D

**Inherits:** GeometryInstance3D < VisualInstance3D < Node3D < Node < Object
**Inherited By:** SoftBody3D

Node that instances meshes into a scenario.

## Description

MeshInstance3D is a node that takes a Mesh resource and adds it to the current scenario by creating an instance of it. This is the class most often used to render 3D geometry and can be used to instance a single Mesh in many places. This allows reusing geometry, which can save on resources. When a Mesh has to be instantiated more than thousands of times at close proximity, consider using a MultiMesh in a MultiMeshInstance3D instead.

## Properties

| Property | Type | Default |
|----------|------|---------|
| mesh | Mesh | |
| skeleton | NodePath | NodePath("..") |
| skin | Skin | |

## Methods

| Return | Method |
|--------|--------|
| ArrayMesh | bake_mesh_from_current_blend_shape_mix(existing: ArrayMesh = null) |
| ArrayMesh | bake_mesh_from_current_skeleton_pose(existing: ArrayMesh = null) |
| void | create_convex_collision(clean: bool = true, simplify: bool = false) |
| void | create_debug_tangents() |
| void | create_multiple_convex_collisions(settings: MeshConvexDecompositionSettings = null) |
| void | create_trimesh_collision() |
| int | find_blend_shape_by_name(name: StringName) |
| Material | get_active_material(surface: int) const |
| int | get_blend_shape_count() const |
| float | get_blend_shape_value(blend_shape_idx: int) const |
| SkinReference | get_skin_reference() const |
| Material | get_surface_override_material(surface: int) const |
| int | get_surface_override_material_count() const |
| void | set_blend_shape_value(blend_shape_idx: int, value: float) |
| void | set_surface_override_material(surface: int, material: Material) |

## Property Details

### mesh

The Mesh resource for the instance.

### skeleton

NodePath to the Skeleton3D associated with the instance.

### skin

The Skin to be used by this instance.

## Method Details

### create_convex_collision()

This helper creates a StaticBody3D child node with a ConvexPolygonShape3D collision shape calculated from the mesh geometry. It's mainly used for testing.

If clean is true (default), duplicate and interior vertices are removed automatically. You can set it to false to make the process faster if not needed.

If simplify is true, the geometry can be further simplified to reduce the number of vertices. Disabled by default.

### create_trimesh_collision()

This helper creates a StaticBody3D child node with a ConcavePolygonShape3D collision shape calculated from the mesh geometry. It's mainly used for testing.

### create_multiple_convex_collisions()

This helper creates a StaticBody3D child node with multiple ConvexPolygonShape3D collision shapes calculated from the mesh geometry via convex decomposition. The convex decomposition operation can be controlled with parameters from the optional settings.

### get_active_material()

Returns the Material that will be used by the Mesh when drawing. This can return the GeometryInstance3D.material_override, the surface override Material defined in this MeshInstance3D, or the surface Material defined in the mesh. For example, if GeometryInstance3D.material_override is used, all surfaces will return the override material.

Returns null if no material is active, including when mesh is null.

### get_surface_override_material() / set_surface_override_material()

Returns/sets the override Material for the specified surface of the Mesh resource.

Note: This returns/sets the Material associated to the MeshInstance3D's Surface Material Override properties, not the material within the Mesh resource. To get/set the material within the Mesh resource, use Mesh.surface_get_material() / Mesh.surface_set_material() instead.

### Blend Shapes

#### get_blend_shape_count()

Returns the number of blend shapes available. Produces an error if mesh is null.

#### get_blend_shape_value() / set_blend_shape_value()

Returns/sets the value of the blend shape at the given blend_shape_idx. Returns 0.0 and produces an error if mesh is null or doesn't have a blend shape at that index.

#### find_blend_shape_by_name()

Returns the index of the blend shape with the given name. Returns -1 if no blend shape with this name exists, including when mesh is null.

### Baking

#### bake_mesh_from_current_blend_shape_mix()

Takes a snapshot from the current ArrayMesh with all blend shapes applied according to their current weights and bakes it to the provided existing mesh. If no existing mesh is provided a new ArrayMesh is created, baked and returned. Mesh surface materials are not copied.

Performance: Mesh data needs to be received from the GPU, stalling the RenderingServer in the process.

#### bake_mesh_from_current_skeleton_pose()

Takes a snapshot of the current animated skeleton pose of the skinned mesh and bakes it to the provided existing mesh. If no existing mesh is provided a new ArrayMesh is created, baked, and returned. Requires a skeleton with a registered skin to work. Blendshapes are ignored. Mesh surface materials are not copied.

Performance: Mesh data needs to be retrieved from the GPU, stalling the RenderingServer in the process.
