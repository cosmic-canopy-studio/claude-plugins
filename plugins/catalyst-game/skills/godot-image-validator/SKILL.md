---
name: godot-image-validator
description: Validates game images using AI analysis with confidence scoring. Use when reviewing sprites, textures, or UI assets for quality before importing into Godot projects.
allowed-tools: Read, Grep, Glob
version: 2.0.0
---

# Godot Image Validator

## Overview

Validate visual assets before importing into Godot using Claude's image analysis capabilities.

## When to Use

- Reviewing sprite sheets for animation consistency
- Checking texture tiling and resolution
- Validating UI element sizing
- Quality control during asset import

## Quick Start

When asked to validate an image:

1. Read the image file using the Read tool
2. Analyze visual characteristics
3. Report confidence score (0.0-1.0)
4. Note any issues found

## Confidence Thresholds

| Score | Action | Indicator |
|-------|--------|-----------|
| 0.85-1.0 | Auto-accept | Green |
| 0.60-0.84 | Review suggested | Yellow |
| 0.30-0.59 | Review required | Orange |
| 0.00-0.29 | Likely issues | Red |

## Validation Checks

**Sprite Sheets:**
- Frame consistency (size, alignment)
- Animation flow (smooth transitions)
- Alpha channel quality

**Textures:**
- Seamless tiling edges
- Resolution appropriateness
- Compression artifacts

**UI Elements:**
- Size guidelines for target resolution
- Readable text at target size
- Proper padding and margins

## Example Usage

```
Validate this sprite sheet for our 32x32 pixel art game: path/to/player_walk.png
```

The validator will analyze and report:
- Overall quality confidence
- Frame dimensions and count
- Any alignment or consistency issues
- Recommendations for fixes

## Related Skills

- godot skill for importing validated assets
