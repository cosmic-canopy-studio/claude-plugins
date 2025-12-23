# Animation Tutorial Patterns

A comprehensive collection of animation patterns extracted from Godot's official animation tutorials. These patterns cover AnimationPlayer setup, AnimationTree state machines, blend spaces, cutout animation rigs, and skeletal deformation.

## AnimationPlayer Setup

### Problem: Creating a basic animation from scratch

**Solution: Basic AnimationPlayer Setup Pattern**

Create a root node with an AnimationPlayer as a child, then add animated sprites/objects below:

```gdscript
# Scene structure:
# Node2D (root)
#   └─ Sprite2D
#   └─ AnimationPlayer

extends Node2D

func _ready() -> void:
    # AnimationPlayer will be selected in editor to access animation panel
    # The animation panel appears at bottom of viewport when AnimationPlayer is selected
    pass
```

**Key points:**
- AnimationPlayer inherits from Node, not Node2D/Node3D, so child nodes don't inherit 2D/3D transforms
- The animation panel provides four main sections: animation controls, tracks listing, timeline, and track controls
- Avoid placing 2D/3D nodes as direct children of AnimationPlayer
- Use AnimationPlayer as a sibling or parent to non-transform nodes

**Source:** Introduction to the animation features

---

### Problem: Setting up keyframes and animation timelines

**Solution: Keyframe and Timeline Setup**

Keyframes define property values at specific times. Two keyframes create smooth interpolation:

```gdscript
# In AnimationPlayer editor:
# 1. Create new animation via "Animation" button
# 2. Select the node you want to animate
# 3. Click convenience buttons (loc, rot, scl) to specify which properties
# 4. Press key button at time=0.0 to create first keyframe
# 5. Move slider to desired end time (e.g., 2.0 seconds)
# 6. Change node property (e.g., position)
# 7. Press key button again to create second keyframe

# Animation length can be set in the timeline controls
# The engine interpolates values between keyframes
```

**Key points:**
- Keyframes are represented as diamond shapes in the timeline
- Animation length defaults to 1 second but is fully customizable
- Values are automatically interpolated between keyframes
- You can animate ANY property visible in the Inspector
- The "Capture" track mode blends the first keyframe with current property values

**Source:** Introduction to the animation features

---

### Problem: Choosing the right interpolation mode for smooth animations

**Solution: Track Interpolation Configuration**

Different interpolation modes produce different animation feels:

```gdscript
# In track settings (right side of animation panel):

# Continuous mode - updates every frame (default)
# Use for smooth property changes over time

# Discrete mode - only updates at keyframes
# Use for sudden value changes (like frame switching)

# Capture mode - blends starting value with animation
# Use when animating objects at unknown starting positions

# Interpolation types:
# - Nearest: Jump to nearest keyframe value
# - Linear: Constant speed between keyframes (robotic feel)
# - Cubic: Slower at keyframes, faster between (natural feel)
# - Linear Angle: Linear with shortest rotation path
# - Cubic Angle: Cubic with shortest rotation path
```

**Key points:**
- Cubic interpolation is standard for character animation (natural motion)
- Linear interpolation produces more mechanical results
- Rotation properties have angle-specific interpolation modes
- Linear Angle prevents rotation interpolation from taking wrong path
- Choose "Continuous" update mode for most animations

**Source:** Introduction to the animation features

---

### Problem: Handling animation looping and forward/backward motion

**Solution: Loop Mode Configuration**

Control how animations behave when looping:

```gdscript
# In track settings:

# Clamp loop interpolation:
# - Animation stops after last keyframe
# - Resets to first keyframe when loop begins
# - Use for animations that should reset to start

# Wrap loop interpolation:
# - Engine calculates values from last keyframe back to first
# - Creates smooth back-and-forth motion
# - Use for bidirectional animations

# Example: 2-second animation extended to 4 seconds with wrap mode
# 0.0s - 2.0s: Move right (keyframes defined)
# 2.0s - 4.0s: Automatically moves back left (calculated)
```

**Key points:**
- Wrap mode automatically creates return path animation
- Clamp mode requires explicit keyframes for all directions
- No keyframe needed at animation end for wrap mode
- Setting animation length controls the full loop period

**Source:** Introduction to the animation features

---

## Animation Properties and Tracks

### Problem: Animating properties beyond transform (position, rotation, scale)

**Solution: Property Track Creation**

Animate any Inspector property by creating property-specific tracks:

```gdscript
# Method 1: Visual keyframing in editor
# Select node while animation panel open
# Look for keyframe button next to any property in Inspector
# Click the button to add keyframe for that property

# Method 2: Animate color, opacity, texture properties
# Use same process as position/rotation
# Works with Sprite2D.modulate for color changes
# Works with CanvasItem.modulate.a for opacity
# Works with Sprite2D.texture for texture swaps

# Example: Color fade animation
# Create property track for "modulate"
# Set first keyframe: Color(1, 1, 1, 1) at t=0.0
# Set second keyframe: Color(1, 1, 1, 0) at t=1.0
# Result: Smooth fade to transparent
```

**Key points:**
- Inspector keyframe buttons appear when animation panel is open
- Any property in the Inspector can be animated
- Visibility, materials, particle parameters can all be animated
- Script variables (if exported) can be animated too
- Each property gets its own track in the timeline

**Source:** Introduction to the animation features

---

### Problem: Setting default poses for proper animation blending

**Solution: RESET Animation Pattern**

Create a RESET animation that defines default property values:

```gdscript
# In AnimationPlayer editor:

# 1. Create new animation named "RESET" (case-sensitive)
# 2. Add tracks for all properties that need default values
# 3. Set a single keyframe at time 0.0 with desired default values
# 4. Don't add more keyframes - RESET should be instantaneous

# In SKILL.md inspector:
# Set AnimationPlayer's "Reset On Save" property to true
# Scene will save with effects of RESET animation applied
# Ensures default pose loads when reopening scene

# RESET animation affects blending calculations
# When blending animations, missing property tracks default to RESET values
# This ensures deterministic and consistent blend results
```

**Key points:**
- RESET animation must be named exactly "RESET" (case-sensitive)
- Only needs single keyframe at time 0.0
- Used as reference when blending animations
- If Reset On Save is enabled, editor state reflects RESET animation
- Essential for proper AnimationTree blending

**Source:** Introduction to the animation features

---

### Problem: Playing sections of long animations using markers

**Solution: Animation Markers Pattern**

Break single animation files into playable sections:

```gdscript
extends Node

@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
    # In editor: right-click above timeline, select "Insert Marker..."
    # Name markers: "attack_start", "attack_end", "walk_start", "walk_end"

    # Play section between markers from code
    animation_player.play_section_with_markers("attack", "attack_start", "attack_end")

    # Play section from start of animation to marker
    animation_player.play_section_with_markers("combo", null, "combo_end")

    # Play section from marker to end of animation
    animation_player.play_section_with_markers("combo", "combo_start", null)

    # Play backwards between markers
    animation_player.play_section_with_markers_backwards("attack", "attack_start", "attack_end")

# To preview markers in editor:
# Shift+Click on two markers to highlight section
# Play buttons then act as if entire animation is that section
```

**Key points:**
- Markers require unique names within animation
- Markers can be color-coded for organization
- Useful when animation file contains multiple actions
- Eliminates need for separate animation files
- Shift+Click in editor to preview marker sections

**Source:** Introduction to the animation features

---

## Call Method Tracks

### Problem: Triggering script functions at specific animation times

**Solution: Method Call Track Pattern**

Execute functions at precise animation keyframes:

```gdscript
extends Node

@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
    # Create method track programmatically
    setup_method_animation()

func setup_method_animation() -> void:
    var animation: Animation = animation_player.get_animation("attack")

    # Add a call method track
    var track_index: int = animation.add_track(Animation.TYPE_METHOD)

    # Set the track path to current node
    animation.track_set_path(track_index, ".")

    # Create method call dictionary
    var method_dict: Dictionary = {
        "method": "on_attack_hit",
        "args": [50, Vector2.RIGHT]  # damage, direction
    }

    # Insert method call at specific time (0.6 seconds)
    animation.track_insert_key(track_index, 0.6, method_dict, 0)

# Called from animation at 0.6 second mark
func on_attack_hit(damage: int, direction: Vector2) -> void:
    # Apply damage in specified direction
    apply_damage(damage, direction)

func apply_damage(damage: int, direction: Vector2) -> void:
    # Handle damage application
    pass
```

**Key points:**
- Method calls execute only at keyframe times
- Method calls won't execute during editor preview (safety feature)
- Arguments must match function signature exactly
- Useful for hit detection, sound triggers, particle effects
- Track path "." refers to node owning the AnimationPlayer

**Source:** Animation Track types

---

## AnimationTree State Machines

### Problem: Blending animations with advanced transitions

**Solution: AnimationTree Setup Pattern**

Use AnimationTree for complex animation blending:

```gdscript
extends Node

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var animation_player: AnimationPlayer = $AnimationPlayer

func _ready() -> void:
    # AnimationTree references animations from AnimationPlayer
    # Set animation_player property in editor to link them

    # Create state machine in animation_tree editor:
    # 1. Set root node to AnimationNodeStateMachine
    # 2. Right-click to add states (one per animation)
    # 3. Connect states with transitions

    # Enable tree processing
    animation_tree.active = true

# To travel between states from code
func _process(delta: float) -> void:
    var state_machine: AnimationNodeStateMachinePlayback = animation_tree["parameters/playback"]

    if Input.is_action_pressed("move_right"):
        # Travel to "run" state with automatic path finding
        state_machine.travel("run")
    elif Input.is_action_pressed("jump"):
        state_machine.travel("jump")
    else:
        state_machine.travel("idle")
```

**Key points:**
- AnimationTree doesn't contain animations - it references AnimationPlayer
- Set animation_player property to link the two nodes
- State machine travels via A* pathfinding algorithm
- travel() requires state machine to already be running
- Active property must be true to enable state machine processing

**Source:** Using AnimationTree

---

### Problem: Configuring automatic state transitions with conditions

**Solution: State Transition with Advance Conditions**

Create automatic transitions between states based on boolean variables:

```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
var is_walking: bool = false
var is_jumping: bool = false

func _process(delta: float) -> void:
    # Update animation variables
    var input_velocity: Vector2 = Vector2.ZERO
    if Input.is_action_pressed("move_right"):
        input_velocity.x += 1
    if Input.is_action_pressed("move_left"):
        input_velocity.x -= 1

    is_walking = input_velocity.length() > 0.0
    is_jumping = Input.is_action_just_pressed("jump")

    velocity = input_velocity * 100.0
    velocity = move_and_slide(velocity)

# In AnimationTree editor:
# 1. Create states: idle, walk, jump
# 2. idle -> walk: Advance Condition = "is_walking"
# 3. walk -> idle: Advance Condition = "!is_walking"  # WON'T WORK!
# 4. This fails because Advance Condition only checks TRUE
```

**Key points:**
- Advance Condition only evaluates if variable is true
- Cannot use NOT operator (!) in Advance Condition
- Must create opposite variables for bidirectional transitions
- This limitation is why Advance Expression was added in Godot 4

**Source:** Using AnimationTree - Advance Condition and Advance Expression

---

### Problem: Flexible state transitions using expressions instead of simple conditions

**Solution: Advance Expression Pattern**

Use full expressions for complex transition logic:

```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
var is_walking: bool = false
var is_jumping: bool = false
var is_falling: bool = false

func _process(delta: float) -> void:
    # Update state variables
    var input_velocity: Vector2 = Vector2.ZERO
    if Input.is_action_pressed("move_right"):
        input_velocity.x += 1

    is_walking = input_velocity.length() > 0.0
    is_jumping = Input.is_action_just_pressed("jump")

    velocity.y += 9.8 * delta
    is_falling = velocity.y > 0.0

    velocity = move_and_slide(velocity)

# In AnimationTree editor:
# Set Advance Expression Base Node to node with above script

# Example transitions with Advance Expression:
# idle -> walk: is_walking
# walk -> idle: !is_walking  # Now works!
# walk -> jump: is_jumping && is_walking
# jump -> fall: !is_jumping && is_falling
# fall -> idle: !is_falling && !is_walking
# fall -> walk: !is_falling && is_walking

# All of these are valid Advance Expression syntax:
# - is_walking
# - is_walking == true
# - is_walking && !is_idle
# - velocity > 0
# - health < max_health
# - player.is_on_floor()
```

**Key points:**
- Advance Expression evaluates any condition like if statements
- Can use logical operators: && (and), || (or), ! (not)
- Can compare numbers, booleans, call methods
- Requires Advance Expression Base Node to be set
- Base node should contain the script with animation variables
- Eliminates need for opposite variable pairs

**Source:** Using AnimationTree - Advance Condition and Advance Expression

---

### Problem: Playing one-shot animations that interrupt normal flow

**Solution: OneShot Node Pattern**

Execute animations once, then return to previous state:

```gdscript
extends Node

@onready var animation_tree: AnimationTree = $AnimationTree

func _process(delta: float) -> void:
    # Request one-shot animation to fire
    if Input.is_action_just_pressed("attack"):
        animation_tree["parameters/OneShot/request"] = AnimationNodeOneShot.ONE_SHOT_REQUEST_FIRE

    # Check if one-shot is active (read-only)
    var is_active: bool = animation_tree["parameters/OneShot/active"]
    if is_active:
        # Character is mid-attack, disable movement input
        pass

    # Abort one-shot if needed
    if Input.is_action_just_pressed("cancel"):
        animation_tree["parameters/OneShot/request"] = AnimationNodeOneShot.ONE_SHOT_REQUEST_ABORT

# In AnimationTree editor:
# 1. Add OneShot node
# 2. Connect animation to its "shot" input port
# 3. Connect OneShot output to main animation flow
# 4. Set blend time for fade in/out effect
# 5. Enable/disable filters to control which tracks blend
```

**Key points:**
- ONE_SHOT_REQUEST_FIRE triggers animation
- ONE_SHOT_REQUEST_ABORT stops animation early
- "active" parameter is read-only, use for state checks
- Blend times control fade in and fade out
- Filters allow selective track blending
- Returns to previous state automatically after finishing

**Source:** Using AnimationTree - OneShot

---

### Problem: Controlling animation playback speed dynamically

**Solution: TimeScale Node Pattern**

Speed up, slow down, or reverse animations at runtime:

```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
var current_speed: float = 1.0

func _process(delta: float) -> void:
    # Normal speed
    animation_tree["parameters/TimeScale/scale"] = current_speed

    # Slow down to 50% speed (slow-mo effect)
    if Input.is_action_pressed("slow_mo"):
        animation_tree["parameters/TimeScale/scale"] = 0.5

    # Double speed for dashing
    if Input.is_action_pressed("dash"):
        animation_tree["parameters/TimeScale/scale"] = 2.0

    # Reverse animation
    if Input.is_action_pressed("reverse"):
        animation_tree["parameters/TimeScale/scale"] = -1.0

    # Pause animation
    if Input.is_action_pressed("pause"):
        animation_tree["parameters/TimeScale/scale"] = 0.0

# In AnimationTree editor:
# 1. Add TimeScale node
# 2. Connect animation to its "in" input port
# 3. TimeScale output goes to next node or Output
```

**Key points:**
- Scale value of 0.0 pauses the animation
- Negative scale values play animation backwards
- Scale < 1.0 slows animation (0.5 = half speed)
- Scale > 1.0 speeds animation (2.0 = double speed)
- Used for time dilation, slow-motion, and reverse playback

**Source:** Using AnimationTree - TimeScale

---

### Problem: Seeking to specific times in animations

**Solution: TimeSeek Node Pattern**

Jump to specific animation timestamps:

```gdscript
extends Node

@onready var animation_tree: AnimationTree = $AnimationTree

func _process(delta: float) -> void:
    # Play animation from beginning
    animation_tree["parameters/TimeSeek/seek_request"] = 0.0

    # Jump to 3 seconds into animation
    animation_tree["parameters/TimeSeek/seek_request"] = 3.0

    # Jump to halfway point (5 second animation)
    animation_tree["parameters/TimeSeek/seek_request"] = 2.5

# In AnimationTree editor:
# 1. Add TimeSeek node
# 2. Connect animation to its "in" input port
# 3. TimeSeek output goes to next node or Output
# 4. Set seek_request to desired time in seconds
```

**Key points:**
- Seek request is measured in seconds (float)
- 0.0 starts animation from beginning
- Seek happens once per frame when value is set
- Useful for preview scrubbing, gameplay sequences
- TimeSeek output synchronizes with input animation

**Source:** Using AnimationTree - TimeSeek

---

## Blend Spaces

### Problem: Blending multiple animations based on a single parameter

**Solution: BlendSpace1D Pattern**

Linear blending between animations on one axis:

```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
var current_speed: float = 0.0

func _process(delta: float) -> void:
    var input_velocity: Vector2 = Vector2.ZERO
    if Input.is_action_pressed("move_right"):
        input_velocity.x += 1.0
    if Input.is_action_pressed("move_left"):
        input_velocity.x -= 1.0

    current_speed = input_velocity.length() * 100.0

    # Blend between idle and run based on speed
    animation_tree["parameters/movement/blend_position"] = current_speed

    velocity = input_velocity * 100.0
    velocity = move_and_slide(velocity)

# In AnimationTree editor:
# 1. Add BlendSpace1D node as root
# 2. Add animation points by right-clicking
# 3. Point 0.0: "idle" animation
# 4. Point 1.0: "walk" animation
# 5. Point 2.0: "run" animation
# 6. Set blend_position parameter from 0.0 to 2.0
# 7. Animations blend smoothly between points
```

**Key points:**
- BlendSpace1D uses single parameter for blending
- Points are positioned on a 1D line
- Animations blend based on blend position
- Smooth interpolation between animation points
- Common for speed-based locomotion blending

**Source:** Using AnimationTree - BlendSpace1D

---

### Problem: Blending animations based on two parameters (direction)

**Solution: BlendSpace2D Pattern**

2D blending for directional animations:

```gdscript
extends CharacterBody2D

@onready var animation_tree: AnimationTree = $AnimationTree
var move_direction: Vector2 = Vector2.ZERO

func _process(delta: float) -> void:
    var input: Vector2 = Vector2.ZERO
    if Input.is_action_pressed("move_right"):
        input.x += 1.0
    if Input.is_action_pressed("move_left"):
        input.x -= 1.0
    if Input.is_action_pressed("move_down"):
        input.y += 1.0
    if Input.is_action_pressed("move_up"):
        input.y -= 1.0

    move_direction = input.normalized()

    # Blend between directional animations
    animation_tree["parameters/movement/blend_position"] = move_direction

    velocity = input * 100.0
    velocity = move_and_slide(velocity)

# In AnimationTree editor:
# 1. Add BlendSpace2D node as root
# 2. Right-click to add animation points
# 3. Position points in 2D space:
#    - (0, -1): walk_forward
#    - (1, 0): walk_right
#    - (-1, 0): walk_left
#    - (0, 1): walk_backward
# 4. Set blend_position to Vector2 value
# 5. Animations blend smoothly between closest triangle

# Change blend mode for different behaviors:
# - Continuous: Smooth interpolation (default, for natural motion)
# - Discrete: Snap between animations (for frame-by-frame art)
# - Carry: Preserve playback position when switching discrete animations
```

**Key points:**
- BlendSpace2D blends between up to 3 animations per triangle
- Triangles generated automatically using Delaunay triangulation
- Blend position uses Vector2 coordinates
- Discrete mode useful for spritesheet animations
- Carry mode maintains frame position during discrete transitions

**Source:** Using AnimationTree - BlendSpace2D

---

## Root Motion

### Problem: Synchronizing animation movement with character controller

**Solution: Root Motion Pattern**

Extract motion from animation bone and apply to character position:

```gdscript
extends CharacterBody3D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var skeleton: Skeleton3D = $Skeleton3D

func _ready() -> void:
    # Set root motion track in AnimationTree editor
    # Select animation_tree.anim_player's animations
    # In animation tracks, select a bone and enable "Root Motion Track"
    # Usually the root/hip bone

    animation_tree.active = true

    # Optional: Use RootMotionView for visual debugging
    # Place in scene to visualize character floor/animation paths

func _physics_process(delta: float) -> void:
    # Get motion delta from animation
    var motion_position: Vector3 = animation_tree.get_root_motion_position()
    var motion_rotation: Quaternion = animation_tree.get_root_motion_rotation()

    # Apply animation motion to character
    velocity = motion_position / delta

    # Optional: Get accumulated motion for movement verification
    var total_position: Vector3 = animation_tree.get_root_motion_position_accumulator()

    # Move the character
    velocity = move_and_slide(velocity)

# In AnimationPlayer animations:
# 1. Set up animation with character bone
# 2. The bone provides motion (walking forward, jumping, etc.)
# 3. Mark this bone as Root Motion Track
# 4. Engine cancels bone's visual movement
# 5. Motion available via get_root_motion_position()
```

**Key points:**
- Root motion extracts movement from animation skeleton
- Animation bone stays in place visually while providing motion data
- Essential for step-aligned walking animations
- Works for position, rotation, and scale
- Accumulator gives total motion since root motion track start
- Recommended for 3D character locomotion

**Source:** Using AnimationTree - Root motion

---

### Problem: Precise skeletal animation alignment with environment

**Solution: Root Motion with T-Pose Setup**

Ensure proper blending with near-midpoint skeleton rest poses:

```gdscript
# When exporting 3D models for root motion:
# 1. Export skeleton in T-pose (arms horizontal)
# 2. This places bones near middle of range of motion
# 3. Blending rotations < 180 degrees from rest pose
# 4. Prevents bones penetrating body during blended animations

# In Godot, after importing:
# - Inspect Skeleton3D bone rest values
# - Should be close to middle of acceptable range
# - Not at extremes of the bone's rotation range

# When using rotation interpolation for 2D:
# Set rotation track interpolation to "Linear Angle" or "Cubic Angle"
# These prevent rotation > 180 degrees from initial value during blending

# Root motion for large rotations:
# If character needs > 180 degree rotation with blended animations:
# Use Root Motion for rotational component
# RootMotionView shows animation floor path visually
```

**Key points:**
- T-pose exports enable optimal blending
- Bone rest values should be near motion midpoint
- Linear/Cubic Angle prevents incorrect rotation interpolation
- RootMotionView node aids in debugging animation paths
- Especially important for humanoid character rigs

**Source:** Using AnimationTree - For better blending

---

## Cutout Animation

### Problem: Creating a 2D character rig from sprite pieces

**Solution: Cutout Rig Setup Pattern**

Assemble 2D character from individual sprite assets:

```gdscript
# Scene structure for GBot character:
# Node2D (root)
#   ├─ hip (Sprite2D) - root bone
#   ├─ torso (Sprite2D) - child of hip
#   ├─ right_arm (Sprite2D) - child of torso
#   ├─ left_arm (Sprite2D) - child of torso
#   ├─ right_leg (Sprite2D) - child of hip
#   ├─ left_leg (Sprite2D) - child of hip
#   └─ AnimationPlayer

extends Node2D

func _ready() -> void:
    # Hip is typically the root of the skeleton
    # Each body part is a child of its parent bone
    # Rotation of parent automatically affects children

    # Adjust pivot points by modifying Sprite2D.offset
    # For rotation to work correctly around joints
    pass
```

**Key points:**
- Hip is typically the root of 2D skeletons
- Each sprite is a child in the scene hierarchy
- Child transform inheritance automatically creates articulation
- Pivot (offset) must be adjusted for proper rotation points
- Rotation pivot can be set visually with V key while hovering

**Source:** Cutout animation - Setting up the rig

---

### Problem: Controlling depth ordering when skeletal parts overlap

**Solution: RemoteTransform2D for Visual Depth**

Fix z-ordering without breaking skeletal hierarchy:

```gdscript
# Scene hierarchy problem:
# If left arm needs to appear BEHIND hip/torso but IS a child of torso:
# Normal child rendering puts left arm IN FRONT of parent

# Solution: Use RemoteTransform2D

# Scene structure:
# Node2D
#   ├─ hip (Sprite2D)
#   ├─ torso (Sprite2D)
#   │   ├─ remote_arm_l (RemoteTransform2D)
#   │   │   └─ remote_hand_l (RemoteTransform2D)
#   │   ├─ arm_r (Sprite2D)
#   │   └─ hand_r (Sprite2D)
#   ├─ arm_l (Sprite2D) - positioned above hip in tree
#   └─ hand_l (Sprite2D)

extends Node2D

func _ready() -> void:
    # Configure RemoteTransform2D:
    # 1. Create RemoteTransform2D as child of torso
    # 2. Set its Remote Path property to target arm_l node
    # 3. RemoteTransform2D applies its transform to arm_l
    # 4. arm_l stays behind hip (due to tree position)
    # 5. But inherits torso's transforms (via RemoteTransform2D)

    # RemoteTransform2D nodes can be nested
    # This allows complex depth ordering while maintaining hierarchy
    pass
```

**Key points:**
- RemoteTransform2D applies its transform to remote node
- Solves depth ordering without breaking animation hierarchy
- Remote node doesn't inherit parent transforms normally
- Only the RemoteTransform2D's transforms apply
- Can be nested for complex setups
- Alternative: Use Z property of Node2D for depth

**Source:** Cutout animation - RemoteTransform2D node

---

### Problem: Adding bones and inverse kinematics to cutout rigs

**Solution: Skeleton Creation and IK Chains**

Create articulated bones for easier posing:

```gdscript
# Creating bones:
# 1. Select chain of nodes from top to bottom (e.g., arm -> forearm -> hand)
# 2. Open Skeleton menu > Make Bones
# 3. Bones connect parent to child
# 4. Result: visual bones between articulation points

# Create endpoint for last bone:
# In cutout rig, a bone connects node to its parent
# Hand node has no child, so no bone emerges from it
# Solution: Create Marker2D as child of hand
# Then select hand -> marker chain and create bone
# Now hand has visible bone extending to marker

# Setting up IK (Inverse Kinematics):
# IK allows moving extremities while rest of chain adjusts
# Example: Move foot, thigh and shin auto-adjust

# Creating IK chain:
# 1. Select bone chain from endpoint to base (e.g., foot -> shin -> thigh)
# 2. Edit > Make IK Chain
# 3. Base bone turns yellow
# 4. Now drag foot to new position - shin and thigh adjust

# Note: IK chains in Godot work in EDITOR ONLY
# Not available at runtime for procedural animation
# Intended only for easing keyframe creation
```

**Key points:**
- Bones connect parent to child nodes
- Endpoints need children for bones to be created
- IK chains make posing more intuitive
- IK is editor-only feature for animation creation
- Not usable for runtime procedural animation
- Useful for extremities (feet, hands, tail)

**Source:** Cutout animation - Skeletons and IK chains

---

### Problem: Setting rest pose for skeletal rigs

**Solution: Rest Pose Configuration**

Define default pose for skeleton reset:

```gdscript
extends Node2D

func _ready() -> void:
    # Setting rest pose in editor:
    # 1. Position all skeleton nodes in desired rest arrangement
    # 2. Select Skeleton2D node in scene tree
    # 3. Click Skeleton2D button in toolbar
    # 4. Select "Overwrite Rest Pose"
    # 5. All bones record their current positions/rotations

    # After modifying skeleton (add/remove/rename bones):
    # Must update rest pose again

    # Rest pose used for:
    # - Default pose when animations aren't playing
    # - Reference for animation blending
    # - Resetting to neutral state
    pass
```

**Key points:**
- Rest pose must be set after creating skeleton
- Rest pose is snapshot of bone positions/rotations
- Must be reset if skeleton structure changes
- Used as reference for animation blending
- Warnings appear on bones without rest pose

**Source:** Cutout animation - Completing the skeleton

---

## 2D Skeletal Animation

### Problem: Creating smooth skeletal deformation for 2D characters

**Solution: Polygon2D with Skeleton Binding**

Deform polygons based on skeletal movement:

```gdscript
# Process:
# 1. Create Polygon2D nodes for each character piece
# 2. Assign texture with character sprites
# 3. Open UV dialog, go to Points mode
# 4. Draw polygon around desired sprite piece
# 5. Duplicate polygon, rename, repeat for other pieces
# 6. Create Skeleton2D with Bone2D hierarchy
# 7. Assign Skeleton2D to each Polygon2D

# In polygon editor:
extends Node2D

func setup_skeletal_polygon() -> void:
    # Get polygon and skeleton
    var polygon: Polygon2D = $BodyPart
    var skeleton: Skeleton2D = $Skeleton2D

    # Assign skeleton to polygon
    # (Done in editor via Skeleton property)

    # Sync bones from skeleton to polygon
    # Open UV dialog > Bones section > "Sync Bones to Polygon"
    # This creates bone list in polygon matching skeleton

    # Paint bone weights
    # In Bones section of UV editor:
    # - Select bone
    # - Paint vertices white (full influence) or gray (partial)
    # - Black vertices unaffected by bone
```

**Key points:**
- Polygon2D deforms based on bound Skeleton2D
- Bones must be synced from skeleton to polygon
- Weight painting controls how much each bone affects vertices
- Multiple bones can influence single vertex (weight distribution)
- Only animate bones, not polygons, for deformation

**Source:** 2D skeletons - Deforming the polygons

---

### Problem: Fixing unexpected polygon bending during animation

**Solution: Internal Vertices for Deformation Control**

Add extra vertices to guide polygon bending:

```gdscript
extends Node2D

func add_internal_vertices() -> void:
    # Problem: Godot generates internal triangles for polygon
    # These triangles don't always bend as expected

    # Solution: Add internal vertices in bending regions

    # In polygon UV editor:
    # 1. Go to Points section
    # 2. Add vertices inside polygon where bending occurs
    #    (e.g., elbow region, waist, knee, etc.)
    # 3. Go to Polygon section
    # 4. Redraw polygon with added internal vertices
    # 5. Create finer triangulation by including internal points
    # 6. Return to Bones section
    # 7. Paint weights for internal vertices too

    # Result: Better control over deformation
    # Geometry follows bone movement more naturally
```

**Key points:**
- Internal vertices guide triangle generation
- Added in regions expecting deformation
- Must re-draw polygon with new vertices
- New vertices require weight painting
- Reduces distortion during animation
- Experiment to find optimal vertex placement

**Source:** 2D skeletons - Internal vertices

---

## Animation Tips

### Problem: Setting keyframes selectively for overlapping animations

**Solution: Property Toggle Pattern**

Control which properties get keyframed:

```gdscript
# In animation editor toolbar:
# Three toggle buttons: "loc", "rot", "scl"
# These determine which properties keyframes include

# Example: Overlapping animations
# Scenario: Node has scale animation 0.0-1.0s
#           Want to add rotation animation 0.5-1.5s

# Process:
# 1. Select node
# 2. Toggle OFF: "loc", "scl"
# 3. Toggle ON: "rot"
# 4. Press key at 0.5s to create first rotation keyframe
# 5. Modify rotation
# 6. Press key at 1.5s to create second rotation keyframe
# 7. Result: Scale animation unaffected, rotation added cleanly

# Key icon in toolbar applies keyframes for all toggled properties
extends Node2D

func _ready() -> void:
    # For cutout animation:
    # Most nodes only need rotation changes
    # Toggle "rot" on, "loc" and "scl" off
    # Avoids creating unwanted position/scale tracks
    pass
```

**Key points:**
- Toggles control which property types get keyframed
- Prevents disrupting existing animation tracks
- Useful for layering animations on same node
- Cutout animation typically uses only rotation
- loc (location), rot (rotation), scl (scale) toggles

**Source:** Cutout animation - Setting keyframes and excluding properties

---

### Problem: Creating a rest pose for cutout character

**Solution: Rest Pose Animation**

Store default character arrangement:

```gdscript
extends Node2D

func create_rest_pose() -> void:
    # In AnimationPlayer editor:

    # 1. Position all character parts in resting arrangement
    # 2. Create new animation, name it "rest"
    # 3. Select all body part nodes (box select)
    # 4. Toggle all buttons ON: "loc", "rot", "scl"
    # 5. Press key button (at any time)
    # 6. Result: Single keyframe storing entire rest pose

    # Usage: Play "rest" animation to return to default pose
    # Useful when returning from complex animations

    # Can also use as reference for animation preview
    pass
```

**Key points:**
- Rest pose is snapshot of entire rig position
- Single keyframe at time 0.0
- Can be recalled anytime
- Useful after complex animation sequences
- Documents intended character silhouette

**Source:** Cutout animation - Creating a rest pose

---

### Problem: Applying easing curves to multiple keyframes at once

**Solution: Batch Easing Curve Application**

Set same easing for multiple keys simultaneously:

```gdscript
extends Node2D

func apply_easing_to_animation() -> void:
    # In animation editor:

    # 1. Select multiple keyframes on timeline
    #    (Click first, Shift+Click others, or box select)
    # 2. Click pencil icon in bottom right of animation panel
    #    (Opens transition/easing editor)
    # 3. Click desired curve (e.g., ease-out)
    # 4. All selected keys get same easing applied

    # Common easing curves:
    # - Linear: constant speed
    # - Ease In: slow start, fast end
    # - Ease Out: fast start, slow end
    # - Ease In-Out: slow start and end

    # Result: Consistent motion feel across multiple properties
    pass
```

**Key points:**
- Easing affects how property changes between keyframes
- Batch application saves time on complex animations
- Pencil icon opens easing curve editor
- Box select or Shift+Click to select multiple keys
- Easing applied per keyframe (affects outgoing motion)

**Source:** Cutout animation - Setting easing curves for multiple keys

---

## Best Practices

### Problem: Ensuring consistent animation blending in AnimationTree

**Solution: Complete Property Tracks for Blending**

Make sure all blended animations have consistent tracks:

```gdscript
extends Node3D

@onready var animation_tree: AnimationTree = $AnimationTree
@onready var animation_player: AnimationPlayer = $AnimationPlayer

func setup_animations_for_blending() -> void:
    # Problem: Blending animation A (has position track)
    #          with animation B (no position track)
    # Result: Inconsistent blend - B defaults to Vector3(0,0,0)

    # Solution: Use RESET animation as reference

    # Create RESET animation with all property tracks:
    # 1. Add track for every property used in any blended animation
    # 2. Set first keyframe at time 0.0 with appropriate default
    # 3. Don't add more keyframes - RESET is instantaneous

    # Example for character movement:
    var reset_animation: Animation = animation_player.get_animation("RESET")

    # RESET should have tracks for:
    # - position (with value like Vector3.ZERO)
    # - rotation (with value like Quaternion.IDENTITY)
    # - any blend-space parameters used

    # Now when blending:
    # - Animation without position track uses RESET position
    # - Blending is deterministic and consistent
    # - Animation produces same result regardless of parameter state
    pass
```

**Key points:**
- RESET animation defines default values for missing tracks
- Missing properties default to RESET track values
- Ensures reproducible blending results
- Critical for animation parameter blending
- RESET should have all properties used in any animation

**Source:** Using AnimationTree - For better blending

---

### Problem: Preventing texture and material glitches during animations

**Solution: Discrete Track Mode for Texture Changes**

Switch between discrete property values without interpolation:

```gdscript
extends Node2D

@onready var animation_player: AnimationPlayer = $AnimationPlayer

func create_spritesheet_animation() -> void:
    # Scenario: Animating between different sprite frames
    # Problem: Linear interpolation between frame 1 and frame 2
    #          Creates blurry in-between state

    # Solution: Use Discrete update mode for texture track

    # In animation editor:
    # 1. Add track for "texture" property
    # 2. Create keyframes with different textures
    # 3. Open track settings (right side)
    # 4. Set Update Mode to "Discrete"
    # 5. Result: Texture snaps from one frame to next
    #            No interpolation blur

    # Works for any property where interpolation doesn't make sense:
    # - Textures/sprite frames
    # - Boolean flags
    # - Enum values
    # - Material changes
    pass
```

**Key points:**
- Discrete mode updates only at keyframes
- No interpolation between values
- Use for properties that can't blend smoothly
- Prevents visual glitches with textures
- Common in sprite animation workflows

**Source:** Introduction to the animation features - Track settings

---

## Quick Reference

### AnimationPlayer Node Setup
- Place as sibling to animated nodes (not parent of 2D/3D nodes)
- Open animation panel by selecting AnimationPlayer
- Create animations via "Animation" dropdown

### Common Track Types
- Property Track: Animate any Inspector property
- Method Track: Call functions at specific times
- Bezier Track: Animate with curve control
- Audio Track: Play sounds on timeline
- Animation Playback: Sequence other AnimationPlayers

### AnimationTree Root Nodes
- AnimationNodeBlendTree: Graph of blend nodes
- AnimationNodeStateMachine: State-based animation control
- AnimationNodeBlendSpace1D: Linear 1D blending
- AnimationNodeBlendSpace2D: 2D directional blending
- AnimationNodeAnimation: Simple single animation playback

### Key Properties
- animation_tree.active: Enable/disable state machine
- animation_tree["parameters/path"]: Read/write animation variables
- state_machine.travel("state_name"): Change states with pathfinding
- animation_player.play("animation_name"): Play animation

### Cutout Animation Workflow
1. Create Sprite2D for each body part
2. Arrange in scene hierarchy (parent = parent joint)
3. Adjust pivots (offset) for rotation points
4. Use RemoteTransform2D for z-order fixes
5. Create AnimationPlayer
6. Keyframe node positions/rotations in animation editor

### Skeletal Deformation Workflow
1. Create Skeleton2D with Bone2D hierarchy
2. Create Polygon2D for each deformable piece
3. Assign Skeleton2D to polygon
4. Sync bones in polygon editor
5. Paint bone weights on polygon vertices
6. Add internal vertices for better bending
7. Animate bones (not polygons)

---

## Sources

All patterns extracted from official Godot documentation:
- [Introduction to the animation features](https://docs.godotengine.org/en/stable/tutorials/animation/introduction.html)
- [Using AnimationTree](https://docs.godotengine.org/en/stable/tutorials/animation/animation_tree.html)
- [Animation Track types](https://docs.godotengine.org/en/stable/tutorials/animation/animation_track_types.html)
- [Cutout animation](https://docs.godotengine.org/en/stable/tutorials/animation/cutout_animation.html)
- [2D skeletons](https://docs.godotengine.org/en/stable/tutorials/animation/2d_skeletons.html)
