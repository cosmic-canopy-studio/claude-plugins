---
name: godot-image-validator
description: Validates game images using AI analysis with confidence scoring and hybrid manual review for low-confidence cases. Supports animations, environments, UI elements, and effects with configurable thresholds.
allowed-tools: Read, Grep, Glob
version: 1.0.0
godot_version: "4.2+"
dependencies: []
tags: [validation, ui, ai, mcp, batch-processing]
category: components
---

# Godot Image Validator

## Overview

Image Validator combines automated AI analysis with user input to validate visual assets in Godot projects. It provides confidence scoring, threshold-based filtering, comprehensive quality checks, and integration with Godot's resource system.

## Key Concepts

- **AI Analysis**: Automated visual assessment using advanced image analysis
- **Confidence Scoring**: Numerical quality ratings (0.0-1.0) for each validation category
- **Threshold Configuration**: Customizable minimum confidence levels for different asset types
- **User Override**: Manual validation overrides for artistic decisions
- **Integration**: Seamless integration with Godot's import and resource systems
- **Batch Processing**: Efficient validation of multiple assets at once

## When to Use

- **Asset Import Validation**: Validate sprites, textures, and UI assets before importing
- **Quality Assurance**: Ensure visual consistency across game assets
- **Batch Asset Review**: Process large asset libraries efficiently
- **Team Collaboration**: Provide clear validation criteria for artists and developers
- **Project Maintenance**: Validate assets during project updates and migrations

## Source Reference

- [Godot Import System Documentation](https://docs.godotengine.org/en/stable/tutorials/assets_pipeline/importing_images.html)
- [Godot Texture2D Resources](https://docs.godotengine.org/en/stable/classes/class_texture2d.html)
- [Godot UI Containers](https://docs.godotengine.org/en/stable/tutorials/ui/ui_containers.html)

## Quick Start

```python
# Basic image validation setup
from pathlib import Path
from godot_image_validator import ImageValidator, ImageValidatorUI

def main():
    # Initialize validator
    validator = ImageValidator()

    # Configure validation thresholds
    validator.confidence_scorer.thresholds.auto_accept = 0.85
    validator.confidence_scorer.thresholds.manual_review = 0.60

    # Initialize UI (optional - for interactive validation)
    ui = ImageValidatorUI(validator)

    # Connect event handlers
    validator.validation_completed.connect(on_validation_completed)
    ui.manual_review_completed.connect(on_manual_review_completed)

    # Start batch validation
    project_path = Path("path/to/godot/project")
    assets = get_project_images(project_path)
    validator.validate_batch(assets)

def get_project_images(project_path: Path) -> list[Path]:
    """Find all image assets in Godot project"""
    image_extensions = {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.exr'}
    assets = []

    for ext in image_extensions:
        assets.extend(project_path.rglob(f'*{ext}'))

    return assets

def on_validation_completed(results: list[ValidationResult]):
    """Process validation results"""
    for result in results:
        if result.confidence >= 0.85:
            auto_accept_result(result)
        else:
            queue_for_manual_review(result)

def on_manual_review_completed(image_path: Path, category: str):
    """Apply user's manual validation decision"""
    apply_category(image_path, category)

if __name__ == "__main__":
    main()
```

## Core Concepts

### Confidence Scoring System

The validator uses a multi-aspect confidence calculation:

```python
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AspectWeights:
    content_match: float = 0.4      # How well image matches expected content
    quality_assessment: float = 0.3  # Technical quality (resolution, compression)
    category_confidence: float = 0.2  # Confidence in suggested category
    technical_analysis: float = 0.1   # Technical requirements (format, size)

def calculate_confidence(analysis_result: Dict[str, Any],
                        weights: AspectWeights = None) -> float:
    """Calculate overall confidence from multi-aspect analysis"""
    if weights is None:
        weights = AspectWeights()

    content_match = analysis_result.get('content_match', 0.0)
    quality_assessment = analysis_result.get('quality_assessment', 0.0)
    category_confidence = analysis_result.get('category_confidence', 0.0)
    technical_analysis = analysis_result.get('technical_analysis', 0.0)

    overall_confidence = (
        content_match * weights.content_match +
        quality_assessment * weights.quality_assessment +
        category_confidence * weights.category_confidence +
        technical_analysis * weights.technical_analysis
    )

    return min(1.0, max(0.0, overall_confidence))
```

### Threshold Levels

- **0.85-1.0**: Auto-accept (green indicator)
- **0.60-0.84**: Manual review suggested (yellow indicator)
- **0.30-0.59**: Manual review required (orange indicator)
- **0.00-0.29**: Error/Invalid (red indicator)

### MCP Tool Integration

```python
import asyncio
from typing import Dict, List, Optional
from mcp_client import MCPClient

async def analyze_image_with_mcp(image_path: Path,
                                categories: List[str] = None) -> AnalysisResult:
    """Analyze image using MCP tools with retry logic"""
    if categories is None:
        categories = ["animations", "environments", "ui_elements", "effects"]

    mcp_client = MCPClient()

    try:
        # Primary analysis tool
        result = await mcp_client.analyze_image(image_path, categories)

        if not result.success:
            # Retry with exponential backoff
            result = await mcp_client.retry_analysis(image_path, categories)

        return result

    except Exception as e:
        logger.error(f"MCP analysis failed for {image_path}: {e}")
        return AnalysisResult.fallback_result(image_path, str(e))
```

## Common Use Cases

### 1. Sprite Animation Validation

```python
async def validate_sprite_sheet(sprite_sheet_path: Path) -> ValidationResult:
    """Validate sprite sheet for animation sequence"""
    validator = AnimationValidator()

    result = await validator.validate_sprite_sheet(sprite_sheet_path)

    if result.confidence >= 0.85:
        print(f"Sprite sheet auto-accepted: {result.issues}")
        return result
    else:
        await queue_for_manual_review(sprite_sheet_path, result)
        return result

def validate_all_sprite_sheets(project_path: Path) -> List[ValidationResult]:
    """Validate all sprite sheets in a project"""
    validator = AnimationValidator()
    sprite_sheets = find_sprite_sheets(project_path)

    return asyncio.run(validator.validate_batch(sprite_sheets))
```

### 2. Environment Asset Tiling Check

```python
async def validate_environment_tile(tile_path: Path) -> TilingResult:
    """Validate environment tile for seamless tiling"""
    validator = EnvironmentValidator()

    tiling_result = await validator.validate_tiling(tile_path)

    if tiling_result.seamless:
        print(f"Tile is seamless: {tiling_result.confidence}")
        return tiling_result
    else:
        await show_tiling_issues(tile_path, tiling_result.issues)
        return tiling_result

def analyze_tiling_batch(tiles_dir: Path) -> Dict[Path, TilingResult]:
    """Analyze multiple tiles for tiling compatibility"""
    validator = EnvironmentValidator()
    tiles = list(tiles_dir.glob("*.png"))

    return asyncio.run(validator.validate_tiling_batch(tiles))
```

### 3. UI Element Resolution Check

```python
async def validate_ui_element(ui_path: Path) -> ResolutionResult:
    """Validate UI element resolution and format"""
    validator = UIValidator()

    resolution_result = await validator.validate_resolution(ui_path)

    if resolution_result.fits_guidelines:
        await approve_ui_asset(ui_path)
        return resolution_result
    else:
        await request_resubmission(ui_path, resolution_result.issues)
        return resolution_result

def validate_ui_asset_pack(ui_pack_path: Path) -> List[ResolutionResult]:
    """Validate entire UI asset pack"""
    validator = UIValidator()
    ui_assets = find_ui_assets(ui_pack_path)

    return asyncio.run(validator.validate_batch(ui_assets))
```

## Advanced Features

### Custom Validation Rules

```python
from typing import Callable, Dict
from dataclasses import dataclass

@dataclass
class ValidationResult:
    message: str
    confidence: float
    issues: List[str] = None

def setup_project_specific_rules():
    """Setup project-specific validation rules"""
    validator = ImageValidator()

    # Pixel art project rules
    def validate_pixel_art(image_path: Path) -> ValidationResult:
        from PIL import Image
        with Image.open(image_path) as img:
            width, height = img.size

        if width % 4 != 0 or height % 4 != 0:
            return ValidationResult(
                message="Size must be multiple of 4 for pixel art",
                confidence=0.5,
                issues=[f"Size {width}x{height} not divisible by 4"]
            )

        return ValidationResult(
            message="Valid pixel art size",
            confidence=0.9,
            issues=[]
        )

    validator.add_custom_rule("pixel_art", validate_pixel_art)

    # HD project rules
    def validate_hd_assets(image_path: Path) -> ValidationResult:
        from PIL import Image
        with Image.open(image_path) as img:
            width, height = img.size

        if width < 1024 or height < 1024:
            return ValidationResult(
                message="Minimum 1024x1024 required for HD assets",
                confidence=0.3,
                issues=[f"Size {width}x{height} below minimum 1024x1024"]
            )

        return ValidationResult(
            message="HD resolution met",
            confidence=0.95,
            issues=[]
        )

    validator.add_custom_rule("hd_assets", validate_hd_assets)

async def process_asset_library(project_path: Path) -> None:
    """Process entire asset library with progress tracking"""
    batch_processor = BatchProcessor()
    assets = get_project_images(project_path)

    # Setup event handlers
    batch_processor.processing_started.connect(show_progress_dialog)
    batch_processor.progress_updated.connect(update_progress)
    batch_processor.item_completed.connect(handle_item_result)
    batch_processor.batch_completed.connect(handle_batch_complete)

    # Process with custom configuration
    config = BatchConfig(
        batch_size=50,
        parallel_processing=True,
        auto_accept_threshold=0.85,
        max_retries=3
    )

    await batch_processor.process_async(assets, config)
```

## Integration Examples

### Integration with Godot Import Pipeline

```python
#!/usr/bin/env python3
"""
Godot Editor Plugin Integration
Run as pre-import script or standalone tool
"""

from pathlib import Path
import json
import subprocess

def validate_godot_project(project_path: Path) -> bool:
    """Validate all assets in a Godot project"""
    validator = ImageValidator()

    # Get all image assets
    assets = get_project_images(project_path)

    # Run validation
    results = asyncio.run(validator.validate_batch(assets))

    # Report results
    failed_assets = [r for r in results if r.confidence < 0.6]

    if failed_assets:
        print(f"Validation failed for {len(failed_assets)} assets:")
        for result in failed_assets:
            print(f"  {result.file_path}: {result.message}")
        return False

    print(f"Successfully validated {len(results)} assets")
    return True

def integrate_with_godot_editor(project_path: Path):
    """Create Godot editor plugin integration"""
    plugin_code = '''
@tool
extends EditorPlugin

var validator_dock: Control

func _enter_tree():
    validator_dock = preload("res://addons/image_validator/ValidatorDock.tscn").instantiate()
    add_control_to_dock(DOCK_SLOT_LEFT_UL, validator_dock)

func validate_selected_assets():
    var selected_files = get_selected_files()
    validator_dock.validate_files(selected_files)
'''

    # Create plugin directory
    plugin_dir = project_path / "addons" / "image_validator"
    plugin_dir.mkdir(parents=True, exist_ok=True)

    # Write plugin file
    plugin_file = plugin_dir / "plugin.gd"
    plugin_file.write_text(plugin_code)

    print(f"Created editor plugin at {plugin_file}")
```

### Integration with Build System

```python
#!/usr/bin/env python3
"""
Pre-build validation script for CI/CD pipelines
"""

import sys
import asyncio
from pathlib import Path

async def validate_before_build(project_path: Path) -> int:
    """Validate critical assets before build"""
    validator = ImageValidator()

    # Get critical game assets
    critical_assets = get_critical_game_assets(project_path)

    if not critical_assets:
        print("No critical assets found")
        return 0

    # Validate with high threshold for critical assets
    results = await validator.validate_batch(
        critical_assets,
        auto_accept_threshold=0.9  # Higher threshold for critical assets
    )

    # Check for failures
    failed_assets = [r for r in results if r.confidence < 0.8]

    if failed_assets:
        print(f"CRITICAL: {len(failed_assets)} critical assets failed validation:")
        for result in failed_assets:
            print(f"  ERROR: {result.file_path}")
            print(f"    {result.message}")
            if result.issues:
                for issue in result.issues:
                    print(f"      - {issue}")

        print("\nBuild FAILED due to critical asset validation errors")
        return 1

    print(f"✓ All {len(results)} critical assets passed validation")
    return 0

def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_build.py <godot_project_path>")
        sys.exit(1)

    project_path = Path(sys.argv[1])
    if not project_path.exists():
        print(f"Project path does not exist: {project_path}")
        sys.exit(1)

    # Run validation
    exit_code = asyncio.run(validate_before_build(project_path))
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
```

## Related Skills

- [godot-file-dialog](./godot-file-dialog.html) - For asset selection and browsing
- [godot-grid-container](./godot-grid-container.html) - For validation results display
- [godot-dialog-system](./godot-dialog-system.html) - For manual review dialogs
- [godot-animation-player](./godot-animation-player.html) - For animation sequence validation

## Performance Considerations

- **Batch Size**: Process 50-100 images per batch for optimal performance
- **Memory Management**: Unload images after validation to prevent memory leaks
- **Async Processing**: Use async/await for MCP tool calls to prevent UI freezing
- **Caching**: Cache validation results to avoid re-analysis of unchanged assets

## Troubleshooting

### Common Issues

1. **MCP Tool Fails**: Ensure network connectivity and MCP server is running
2. **Low Confidence Scores**: Check image quality and format compatibility
3. **UI Not Responsive**: Use async processing and proper signal connections
4. **Memory Issues**: Reduce batch size and ensure proper resource cleanup

### Debug Mode

```gdscript
validator.debug_mode = true
validator.mcp_client.debug_mode = true

# This will log detailed information about:
# - MCP tool calls and responses
# - Confidence scoring calculations
# - Threshold decisions
# - UI interaction events
```