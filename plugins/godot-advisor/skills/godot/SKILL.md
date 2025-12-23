---
name: godot
description: Unified Godot 4 game development skill system with lookup-based progressive disclosure. Use when building any 2D or 3D game in Godot - routes to specific patterns for movement, physics, UI, audio, animation, and gameplay systems based on what you're building.
allowed-tools: Read, Grep, Glob, Bash
---

# Godot Game Development Skills

## How to Use This System

This skill system uses **progressive disclosure** - start with a dispatcher that routes you to the specific reference you need. Don't search through 120+ individual skills; let the dispatchers guide you.

### Step 1: Choose a Dispatcher

| Building | Dispatcher |
|----------|------------|
| 2D game (platformer, top-down, action) | [dispatchers/2d-gameplay.md](dispatchers/2d-gameplay.md) |
| 3D game (FPS, third-person, adventure) | [dispatchers/3d-gameplay.md](dispatchers/3d-gameplay.md) |
| Menus, HUD, dialogs, inventory | [dispatchers/ui-systems.md](dispatchers/ui-systems.md) |
| Music, sound effects, spatial audio | [dispatchers/audio-systems.md](dispatchers/audio-systems.md) |
| Architecture, patterns, best practices | [dispatchers/game-patterns.md](dispatchers/game-patterns.md) |

### Step 2: Find Your Pattern

Each dispatcher has lookup tables that route "I want to..." questions to specific reference sections.

### Step 3: Load Reference (On Demand)

References are organized by topic cluster in `reference/`:
- `movement/` - Character controllers, platformers, navigation
- `physics/` - Collision, areas, raycasting, rigid bodies
- `rendering/` - Camera, sprites, particles, shaders
- `ui/` - Controls, containers, dialogs, menus
- `audio/` - Players, buses, spatial audio, music systems
- `animation/` - AnimationPlayer, AnimationTree, tweens


## Quick Reference

### Most Common Tasks

| I want to... | Go directly to |
|--------------|----------------|
| Move a player with WASD | `reference/movement/2d-character.md#8-way` |
| Create platformer movement | `reference/movement/2d-character.md#platformer` |
| Make camera follow player | `reference/rendering/camera.md#follow` |
| Add screen shake | `reference/rendering/camera.md#shake` |
| Create health bar | `reference/ui/bars.md#health` |
| Add main menu | `reference/ui/menus.md#main-menu` |
| Play sound effects | `reference/audio/players.md#one-shot` |
| Create state machine | `reference/animation/state-machines.md` |

## Versioning

- **Current Version**: 2025.12.19
- **Godot Version**: 4.3+
- **Changelog**: [changelog/CHANGELOG.md](changelog/CHANGELOG.md)

All patterns are tested against Godot 4.3. Date-based versioning (YYYY.MM.DD) tracks changes to this skill system.

## Index

For programmatic lookup, see [index.yaml](index.yaml) which contains:
- `when_to_use` triggers for each topic
- Keywords for search matching
- Related topics and examples
- Tier classification (core vs detailed)

## Structure

```
godot/
├── SKILL.md              # This file - entry point
├── dispatchers/          # Route by what you're building
├── reference/            # Consolidated knowledge by topic
├── changelog/            # Version history
└── index.yaml            # Searchable metadata
```
