---
topic: shaders
version: 2025.12.21
godot_version: "4.3"
sources:
  - https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html
  - https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html
  - https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html
  - https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html
  - https://docs.godotengine.org/en/stable/tutorials/shaders/visual_shaders.html
---

# Shaders

Custom shader programming for visual effects in Godot.

## What Are Shaders? {#overview}

Shaders are specialized programs that run on the GPU to control how graphics are rendered. They allow fine-grained control over vertex positions, pixel colors, lighting, and other visual effects.

**When to use shaders:**
- Custom visual effects beyond standard materials
- Performance-optimized rendering
- Unique particle behavior
- Special effects (glow, dissolve, outline, distortion)
- Custom 2D/3D materials

## Shader Types {#types}

| Type | Purpose | Use For |
|------|---------|---------|
| **CanvasItem** | 2D rendering | Sprites, UI elements, 2D particles |
| **Spatial** | 3D rendering | 3D objects, materials, meshes |
| **Particle** | Particle systems | Custom particle behavior |
| **Sky** | Sky rendering | Skyboxes, atmospheric effects |
| **Fog** | Volumetric fog | 3D fog effects |

## Basic Shader Structure {#structure}

### CanvasItem Shader (2D)

```gdshader
shader_type canvas_item;

// Uniforms (editable parameters)
uniform vec4 tint_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float speed : hint_range(0.0, 10.0) = 1.0;

// Vertex function (runs per vertex)
void vertex() {
    // Modify vertex position
    VERTEX += vec2(sin(TIME * speed) * 10.0, 0.0);
}

// Fragment function (runs per pixel)
void fragment() {
    // Modify pixel color
    COLOR = texture(TEXTURE, UV) * tint_color;
}
```

### Spatial Shader (3D)

```gdshader
shader_type spatial;

uniform vec4 albedo_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform sampler2D albedo_texture : source_color;
uniform float metallic : hint_range(0.0, 1.0) = 0.0;
uniform float roughness : hint_range(0.0, 1.0) = 0.5;

void vertex() {
    // Modify vertex position (e.g., wave animation)
    VERTEX.y += sin(VERTEX.x * 2.0 + TIME) * 0.1;
}

void fragment() {
    // Set material properties
    ALBEDO = texture(albedo_texture, UV).rgb * albedo_color.rgb;
    METALLIC = metallic;
    ROUGHNESS = roughness;
}
```

## Data Types {#data-types}

### Scalars and Vectors

```gdshader
// Scalars
float a = 1.0;
int b = 5;
bool c = true;

// Vectors
vec2 uv = vec2(0.5, 0.5);           // 2D vector
vec3 color = vec3(1.0, 0.0, 0.0);   // 3D vector (RGB)
vec4 rgba = vec4(1.0, 0.0, 0.0, 1.0); // 4D vector (RGBA)

// Vector construction variations
vec4 v1 = vec4(0.0, 1.0, 2.0, 3.0);              // Individual scalars
vec4 v2 = vec4(vec2(0.0, 1.0), vec2(2.0, 3.0));  // Two vec2s
vec4 v3 = vec4(vec3(0.0, 1.0, 2.0), 3.0);        // vec3 + scalar
vec4 v4 = vec4(0.5);                              // All components same

// Vector swizzling
vec3 rgb = rgba.rgb;   // Get first 3 components
vec3 bgr = rgba.bgr;   // Reorder components
vec3 rrr = rgba.rrr;   // Repeat component
vec2 xy = rgba.xy;     // Use xyzw notation
```

### Matrices

```gdshader
// Matrix types: mat2, mat3, mat4
mat4 identity = mat4(1.0);  // Identity matrix

// Matrix from vectors (column by column)
mat2 m2 = mat2(
    vec2(1.0, 0.0),
    vec2(0.0, 1.0)
);

mat3 m3 = mat3(
    vec3(1.0, 0.0, 0.0),
    vec3(0.0, 1.0, 0.0),
    vec3(0.0, 0.0, 1.0)
);

// Access matrix components
float value = m3[1][2];  // Column 1, row 2
vec3 column = m3[1];     // Get column as vector

// Matrix from another matrix
mat3 basis = mat3(MODEL_MATRIX);
mat4 m4 = mat4(basis);
```

### Samplers (Textures)

```gdshader
uniform sampler2D main_texture : source_color;
uniform sampler2D normal_map : hint_normal;
uniform sampler2D roughness_map : hint_roughness;

void fragment() {
    vec4 tex_color = texture(main_texture, UV);
    vec3 normal = texture(normal_map, UV).rgb;
}
```

## Uniforms {#uniforms}

Uniforms pass values from materials to shaders:

```gdshader
// Basic uniforms
uniform float intensity = 1.0;
uniform vec4 color : source_color = vec4(1.0);
uniform sampler2D texture_name : source_color;

// Uniforms with hints
uniform float speed : hint_range(0.0, 10.0, 0.1) = 1.0;
uniform vec2 offset : hint_range(-1.0, 1.0) = vec2(0.0);

// Texture hints
uniform sampler2D albedo : source_color;
uniform sampler2D normal : hint_normal;
uniform sampler2D roughness : hint_roughness;
uniform sampler2D metallic : hint_metallic;

// Global uniforms (shared across materials)
global uniform float time_scale;

// Instance uniforms (per-object values)
instance uniform vec4 instance_color : source_color;
```

**Note:** Uniforms are read-only in shaders. Vec2/vec3 are padded to vec4 size.

## Built-in Variables {#built-in-variables}

### CanvasItem (2D) Variables

```gdshader
shader_type canvas_item;

void vertex() {
    // VERTEX (vec2): Vertex position in local space
    VERTEX += vec2(10.0, 0.0);

    // UV (vec2): Texture coordinates
    UV *= 2.0;  // Tile texture

    // COLOR (vec4): Vertex color
    COLOR = vec4(1.0, 1.0, 1.0, 1.0);
}

void fragment() {
    // FRAGCOORD (vec2): Pixel position in viewport
    vec2 screen_pos = FRAGCOORD.xy;

    // UV (vec2): Texture coordinates (0,0 to 1,1)
    vec4 tex = texture(TEXTURE, UV);

    // COLOR (vec4): Output pixel color
    COLOR = tex;

    // TIME (float): Elapsed time in seconds
    float anim = sin(TIME * 2.0);

    // TEXTURE (sampler2D): Default texture
    COLOR = texture(TEXTURE, UV);
}
```

### Spatial (3D) Variables

```gdshader
shader_type spatial;

void vertex() {
    // VERTEX (vec3): Vertex position in model space
    VERTEX.y += sin(VERTEX.x + TIME) * 0.1;

    // NORMAL (vec3): Vertex normal
    NORMAL = normalize(NORMAL);

    // UV (vec2): Primary texture coordinates
    UV *= 2.0;

    // UV2 (vec2): Secondary texture coordinates
    UV2 = UV;

    // COLOR (vec4): Vertex color
    COLOR = vec4(1.0);

    // MODEL_MATRIX (mat4): Local to world transform
    vec3 world_pos = (MODEL_MATRIX * vec4(VERTEX, 1.0)).xyz;
}

void fragment() {
    // ALBEDO (vec3): Base color (RGB)
    ALBEDO = vec3(1.0, 0.0, 0.0);

    // ALPHA (float): Transparency
    ALPHA = 1.0;

    // METALLIC (float): Metallic property
    METALLIC = 0.0;

    // ROUGHNESS (float): Roughness property
    ROUGHNESS = 0.5;

    // EMISSION (vec3): Emissive color
    EMISSION = vec3(0.0);

    // NORMAL_MAP (vec3): Normal map modification
    NORMAL_MAP = texture(normal_texture, UV).rgb;

    // UV (vec2): Texture coordinates
    ALBEDO = texture(albedo_texture, UV).rgb;
}
```

### Common Built-ins (All Shaders)

```gdshader
// TIME (float): Elapsed time since shader start
float wave = sin(TIME * 2.0);

// PI (float): Mathematical constant π
float angle = PI * 0.5;
```

## Shader Processor Functions {#processors}

### Vertex Processor

Runs once per vertex (4 times for a quad sprite):

```gdshader
void vertex() {
    // Wave effect
    VERTEX.y += sin(VERTEX.x * 2.0 + TIME) * 10.0;

    // Rotate vertices
    float angle = TIME;
    mat2 rotation = mat2(
        vec2(cos(angle), -sin(angle)),
        vec2(sin(angle), cos(angle))
    );
    VERTEX = rotation * VERTEX;
}
```

### Fragment Processor

Runs once per pixel:

```gdshader
void fragment() {
    // Tint red
    COLOR = texture(TEXTURE, UV);
    COLOR.r *= 1.5;

    // Transparency based on position
    COLOR.a = UV.y;

    // Discard transparent pixels
    if (COLOR.a < 0.1) {
        discard;
    }
}
```

### Light Processor (Advanced)

Custom lighting calculations:

```gdshader
void light() {
    // Custom lighting for 2D/3D
    LIGHT = LIGHT_COLOR * ATTENUATION;
}
```

## Common Shader Effects {#effects}

### Color Tint

```gdshader
shader_type canvas_item;

uniform vec4 tint : source_color = vec4(1.0);

void fragment() {
    COLOR = texture(TEXTURE, UV) * tint;
}
```

### Flash Effect (Hit Feedback)

```gdshader
shader_type canvas_item;

uniform vec4 flash_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float flash_amount : hint_range(0.0, 1.0) = 0.0;

void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    COLOR = mix(tex, flash_color, flash_amount * tex.a);
}
```

### Outline (2D)

```gdshader
shader_type canvas_item;

uniform vec4 outline_color : source_color = vec4(1.0, 1.0, 1.0, 1.0);
uniform float outline_width : hint_range(0.0, 10.0) = 1.0;

void fragment() {
    vec4 col = texture(TEXTURE, UV);
    vec2 pixel_size = 1.0 / vec2(textureSize(TEXTURE, 0));

    float outline = 0.0;
    for(float x = -outline_width; x <= outline_width; x += 1.0) {
        for(float y = -outline_width; y <= outline_width; y += 1.0) {
            vec2 offset = vec2(x, y) * pixel_size;
            outline = max(outline, texture(TEXTURE, UV + offset).a);
        }
    }

    outline *= 1.0 - col.a;
    COLOR = mix(col, outline_color, outline);
}
```

### Dissolve Effect

```gdshader
shader_type canvas_item;

uniform float dissolve_amount : hint_range(0.0, 1.0) = 0.0;
uniform sampler2D dissolve_texture;
uniform vec4 edge_color : source_color = vec4(1.0, 0.5, 0.0, 1.0);
uniform float edge_width : hint_range(0.0, 0.2) = 0.1;

void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    float noise = texture(dissolve_texture, UV).r;

    // Create edge glow
    float edge = smoothstep(dissolve_amount, dissolve_amount + edge_width, noise);
    float edge_mask = edge - smoothstep(dissolve_amount + edge_width,
                                         dissolve_amount + edge_width * 2.0, noise);

    // Dissolve
    float alpha = step(dissolve_amount, noise);
    COLOR = tex;
    COLOR.rgb = mix(COLOR.rgb, edge_color.rgb, edge_mask);
    COLOR.a *= alpha;
}
```

### Glow/Emission

```gdshader
shader_type spatial;

uniform vec4 glow_color : source_color = vec4(1.0, 1.0, 0.0, 1.0);
uniform float glow_strength : hint_range(0.0, 10.0) = 1.0;

void fragment() {
    ALBEDO = vec3(0.1);
    EMISSION = glow_color.rgb * glow_strength;
}
```

### Water Surface (2D)

```gdshader
shader_type canvas_item;

uniform vec2 wave_speed = vec2(0.5, 0.3);
uniform float wave_amplitude : hint_range(0.0, 0.1) = 0.02;
uniform vec4 water_tint : source_color = vec4(0.3, 0.5, 0.8, 0.7);

void fragment() {
    // Distort UVs for wave effect
    vec2 uv = UV;
    uv.x += sin(UV.y * 20.0 + TIME * wave_speed.x) * wave_amplitude;
    uv.y += cos(UV.x * 20.0 + TIME * wave_speed.y) * wave_amplitude;

    vec4 tex = texture(TEXTURE, uv);
    COLOR = tex * water_tint;
}
```

### Sprite Animation (UV Scrolling)

```gdshader
shader_type canvas_item;

uniform vec2 scroll_speed = vec2(0.1, 0.0);

void fragment() {
    vec2 uv = UV + TIME * scroll_speed;
    COLOR = texture(TEXTURE, uv);
}
```

### Pixelation Effect

```gdshader
shader_type canvas_item;

uniform float pixel_size : hint_range(1.0, 32.0) = 8.0;

void fragment() {
    vec2 uv = UV;
    uv = floor(uv * pixel_size) / pixel_size;
    COLOR = texture(TEXTURE, uv);
}
```

### Chromatic Aberration

```gdshader
shader_type canvas_item;

uniform float aberration_strength : hint_range(0.0, 0.1) = 0.01;

void fragment() {
    vec2 offset = vec2(aberration_strength, 0.0);

    float r = texture(TEXTURE, UV + offset).r;
    float g = texture(TEXTURE, UV).g;
    float b = texture(TEXTURE, UV - offset).b;
    float a = texture(TEXTURE, UV).a;

    COLOR = vec4(r, g, b, a);
}
```

## Using Shaders in Code {#usage}

### Assign to Material

```gdscript
# Create shader material
var shader_material := ShaderMaterial.new()
shader_material.shader = preload("res://shaders/my_shader.gdshader")

# Set uniforms
shader_material.set_shader_parameter("tint_color", Color.RED)
shader_material.set_shader_parameter("speed", 2.0)

# Apply to sprite
$Sprite2D.material = shader_material
```

### Modify Uniforms at Runtime

```gdscript
extends Sprite2D

@onready var mat := material as ShaderMaterial

func _ready() -> void:
    # Animate flash effect
    var tween := create_tween()
    tween.tween_method(set_flash, 1.0, 0.0, 0.3)

func set_flash(amount: float) -> void:
    mat.set_shader_parameter("flash_amount", amount)

func take_damage() -> void:
    mat.set_shader_parameter("flash_amount", 1.0)
    var tween := create_tween()
    tween.tween_method(set_flash, 1.0, 0.0, 0.3)
```

### Global Uniforms (Shared Across Materials)

```gdscript
# Set global uniform in code
RenderingServer.global_shader_parameter_set("time_scale", 1.0)
```

```gdshader
// Use in shader
global uniform float time_scale;

void fragment() {
    float adjusted_time = TIME * time_scale;
    // Use adjusted_time for effects
}
```

## VisualShader (Node-Based) {#visual-shader}

VisualShader provides a node-based editor for creating shaders without code:

### When to Use VisualShader

- Prototyping effects quickly
- Learning shader concepts visually
- Building simple effects without GLSL knowledge
- Team members unfamiliar with shader code

### When to Use Code Shaders

- Complex custom logic
- Performance-critical shaders
- Version control (text is easier to diff)
- Reusable shader libraries

### Creating a VisualShader

```gdscript
# Create in code
var visual_shader := VisualShader.new()
visual_shader.set_mode(VisualShader.MODE_CANVAS_ITEM)

var shader_material := ShaderMaterial.new()
shader_material.shader = visual_shader

$Sprite2D.material = shader_material
```

In the editor:
1. Create new ShaderMaterial
2. Click "Shader" → "New VisualShader"
3. Click shader to open VisualShader editor
4. Add nodes and connect them

### Common VisualShader Nodes

| Node Type | Purpose |
|-----------|---------|
| **Input** | UV, Time, Color, Texture |
| **Color** | ColorConstant, ColorOp, Mix |
| **Vector** | VectorCompose, VectorDecompose, VectorOp |
| **Scalar** | FloatConstant, FloatOp, Clamp |
| **Texture** | Texture2D, CubeMap |
| **Transform** | TransformCompose, TransformDecompose |

## Performance Tips {#performance}

### Optimization

```gdshader
// GOOD: Precalculate in vertex shader when possible
varying vec2 offset;

void vertex() {
    offset = VERTEX * 0.5;  // Runs 4 times (quad vertices)
}

void fragment() {
    COLOR = texture(TEXTURE, UV + offset);  // Runs per pixel
}

// BAD: Expensive calculations per pixel
void fragment() {
    vec2 offset = VERTEX * 0.5;  // Calculated for EVERY pixel
    COLOR = texture(TEXTURE, UV + offset);
}
```

### Minimize Texture Samples

```gdshader
// GOOD: Single texture sample
void fragment() {
    vec4 tex = texture(TEXTURE, UV);
    COLOR = tex * 0.5;
    ALPHA = tex.a;
}

// BAD: Multiple samples of same texture
void fragment() {
    COLOR = texture(TEXTURE, UV) * 0.5;
    ALPHA = texture(TEXTURE, UV).a;  // Unnecessary second sample
}
```

### Use Discard Sparingly

```gdshader
// Discard can hurt performance (breaks GPU parallelism)
void fragment() {
    if (COLOR.a < 0.1) {
        discard;  // Use only when necessary
    }
}
```

### Constants Over Uniforms

```gdshader
// Constants are slightly faster (compiled into shader)
const float PI = 3.14159265359;
const vec3 UP = vec3(0.0, 1.0, 0.0);

// Uniforms are for values that change at runtime
uniform float speed = 1.0;
```

## Debugging Shaders {#debugging}

### Visual Debugging

```gdshader
void fragment() {
    // Show UVs as colors
    COLOR.rgb = vec3(UV, 0.0);

    // Show normals as colors (3D)
    // ALBEDO = NORMAL * 0.5 + 0.5;

    // Show time as grayscale
    // COLOR.rgb = vec3(fract(TIME));

    // Isolate channels
    // COLOR.rgb = vec3(COLOR.r, 0.0, 0.0);  // Show only red
}
```

### Common Issues

| Problem | Solution |
|---------|----------|
| Texture looks wrong/repeated | Check UV coordinates are in 0-1 range |
| Shader has no effect | Verify material is assigned to node |
| Colors too dark/bright | Check color values and ensure in valid range |
| Performance drop | Reduce texture samples, simplify calculations |
| Uniform not visible | Check uniform syntax and hints |

## Shader Preprocessing {#preprocessing}

```gdshader
// Conditional compilation
#ifdef USE_NORMAL_MAP
uniform sampler2D normal_map : hint_normal;
#endif

void fragment() {
    #ifdef USE_NORMAL_MAP
    NORMAL_MAP = texture(normal_map, UV).rgb;
    #endif
}

// Define constants
#define MAX_LIGHTS 8
#define PI 3.14159265359
```

## Additional Resources {#resources}

### Official Documentation
- [Shading Language Reference](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/shading_language.html)
- [Introduction to Shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/introduction_to_shaders.html)
- [CanvasItem Shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/canvas_item_shader.html)
- [Spatial Shaders](https://docs.godotengine.org/en/stable/tutorials/shaders/shader_reference/spatial_shader.html)

### Community Resources
- [Godot Shaders](https://godotshaders.com/) - Community shader collection
- [GDQuest Tutorials](https://www.gdquest.com/) - Video tutorials
- [Kodeco Shader Guide](https://www.kodeco.com/43354079-introduction-to-shaders-in-godot-4)
