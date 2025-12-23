# Godot Image Validator - API Reference

This reference provides detailed API documentation for the Godot Image Validator components, including MCP tools, confidence scoring, and validation workflows.

## Core Classes

### AnalysisResult

Dataclass containing the results of image analysis.

```python
from dataclasses import dataclass
from typing import Dict, List, Optional, Any

@dataclass
class AnalysisResult:
    success: bool
    confidence: float
    categories: List[str]
    issues: List[str]
    metadata: Dict[str, Any]
    error_message: Optional[str] = None

    @classmethod
    def fallback_result(cls, image_path: Path, error_message: str) -> 'AnalysisResult':
        """Create a fallback result for failed analysis"""
        return cls(
            success=False,
            confidence=0.0,
            categories=[],
            issues=[error_message],
            metadata={"fallback": True, "image_path": str(image_path)},
            error_message=error_message
        )
```

### MCPClient

Client for Model Context Protocol (MCP) image analysis tools.

#### Constructor

```python
def __init__(self, timeout: int = 30):
    """
    Initialize MCP client.

    Args:
        timeout: Request timeout in seconds (default: 30)
    """
```

#### Methods

##### analyze_image()

```python
async def analyze_image(self,
                       image_path: Path,
                       categories: List[str] = None) -> AnalysisResult:
    """
    Analyze image using MCP tools.

    Args:
        image_path: Path to the image file
        categories: List of categories to analyze (default: ["animations", "environments", "ui_elements", "effects"])

    Returns:
        AnalysisResult: Analysis results with confidence scoring

    Raises:
        FileNotFoundError: If image file doesn't exist
        ValueError: If image format is not supported
        TimeoutError: If analysis timeout is exceeded
    """
```

**Example:**
```python
client = MCPClient(timeout=60)
result = await client.analyze_image(
    Path("assets/player_sprite.png"),
    categories=["animations", "ui_elements"]
)

if result.success:
    print(f"Categories: {result.categories}")
    print(f"Confidence: {result.confidence:.2%}")
else:
    print(f"Error: {result.error_message}")
```

##### retry_analysis()

```python
async def retry_analysis(self,
                        image_path: Path,
                        categories: List[str]) -> AnalysisResult:
    """
    Retry analysis with exponential backoff.

    Args:
        image_path: Path to the image file
        categories: List of categories to analyze

    Returns:
        AnalysisResult: Analysis results after retry attempts
    """
```

### ConfidenceScorer

Manages confidence calculation and threshold decisions.

#### Constructor

```python
def __init__(self, thresholds: ThresholdConfig = None, weights: AspectWeights = None):
    """
    Initialize confidence scorer.

    Args:
        thresholds: Configuration for validation thresholds
        weights: Configuration for aspect weightings
    """
```

#### Methods

##### calculate_confidence()

```python
def calculate_confidence(self, analysis_result: Dict[str, Any]) -> float:
    """
    Calculate overall confidence from multi-aspect analysis.

    Args:
        analysis_result: Dictionary containing aspect scores (0.0-1.0)

    Returns:
        float: Overall confidence score (0.0-1.0)
    """
```

**Example:**
```python
scorer = ConfidenceScorer()
analysis_data = {
    "content_match": 0.9,
    "quality_assessment": 0.8,
    "category_confidence": 0.85,
    "technical_analysis": 0.95
}

confidence = scorer.calculate_confidence(analysis_data)
print(f"Overall confidence: {confidence:.2%}")  # Output: 87.0%
```

##### get_validation_level()

```python
def get_validation_level(self, confidence: float) -> ValidationLevel:
    """
    Determine validation level based on confidence score.

    Args:
        confidence: Confidence score (0.0-1.0)

    Returns:
        ValidationLevel: Corresponding validation level
    """
```

**Validation Levels:**
- `AUTO_ACCEPT` (≥ 0.85): Asset is automatically accepted
- `MANUAL_REVIEW_SUGGESTED` (0.60-0.84): Manual review suggested
- `MANUAL_REVIEW_REQUIRED` (0.30-0.59): Manual review required
- `ERROR` (< 0.30): Asset rejected

##### should_require_manual_review()

```python
def should_require_manual_review(self, confidence: float) -> bool:
    """
    Check if manual review is required for given confidence.

    Args:
        confidence: Confidence score (0.0-1.0)

    Returns:
        bool: True if manual review is required
    """
```

### ValidationLevel

Enumeration of validation levels.

```python
class ValidationLevel(Enum):
    AUTO_ACCEPT = "auto_accept"
    MANUAL_REVIEW_SUGGESTED = "manual_review_suggested"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    ERROR = "error"
```

### ThresholdConfig

Configuration for validation thresholds.

```python
@dataclass
class ThresholdConfig:
    auto_accept: float = 0.85              # Minimum confidence for auto-accept
    manual_review_suggested: float = 0.60  # Minimum confidence for suggested review
    manual_review_required: float = 0.30  # Minimum confidence for required review
    error: float = 0.0                    # Confidence threshold for errors
```

**Example:**
```python
# Stricter thresholds for critical assets
strict_thresholds = ThresholdConfig(
    auto_accept=0.95,
    manual_review_suggested=0.80,
    manual_review_required=0.60
)

scorer = ConfidenceScorer(thresholds=strict_thresholds)
```

### AspectWeights

Configuration for aspect weighting in confidence calculation.

```python
@dataclass
class AspectWeights:
    content_match: float = 0.4        # Weight for content matching
    quality_assessment: float = 0.3  # Weight for quality assessment
    category_confidence: float = 0.2  # Weight for category confidence
    technical_analysis: float = 0.1   # Weight for technical analysis
```

**Example:**
```python
# Emphasize quality for HD assets
quality_focused_weights = AspectWeights(
    content_match=0.2,
    quality_assessment=0.5,
    category_confidence=0.2,
    technical_analysis=0.1
)
```

### BatchProcessor

Processes multiple images in batches with progress tracking.

#### Constructor

```python
def __init__(self, config: BatchConfig = None):
    """
    Initialize batch processor.

    Args:
        config: Configuration for batch processing
    """
```

#### Methods

##### process_batch()

```python
async def process_batch(self,
                       image_paths: List[Path],
                       validator_func: Callable) -> List[Dict[str, Any]]:
    """
    Process a batch of images.

    Args:
        image_paths: List of image file paths to process
        validator_func: Async function to validate individual images

    Returns:
        List[Dict[str, Any]]: List of validation results

    Raises:
        ValueError: If image_paths is empty
        TypeError: If validator_func is not callable
    """
```

**Example:**
```python
config = BatchConfig(
    batch_size=50,
    parallel_processing=True,
    max_workers=4
)

processor = BatchProcessor(config)

async def validate_image(image_path: Path) -> Dict[str, Any]:
    # Your validation logic here
    return {"success": True, "confidence": 0.9}

results = await processor.process_batch(image_paths, validate_image)
```

##### add_progress_callback()

```python
def add_progress_callback(self, callback: Callable[[int, int, str], None]):
    """
    Add callback for progress updates.

    Args:
        callback: Function called with (current, total, message) parameters
    """
```

### BatchConfig

Configuration for batch processing.

```python
@dataclass
class BatchConfig:
    batch_size: int = 50                    # Images per batch
    parallel_processing: bool = True        # Enable parallel processing
    max_workers: int = 4                    # Maximum parallel workers
    auto_accept_threshold: float = 0.85     # Threshold for auto-accept
    timeout_per_image: int = 30             # Timeout per image (seconds)
```

## MCP Tools Integration

### Available MCP Tools

#### mcp__zai-mcp-server__analyze_image

Primary tool for AI-powered image analysis.

**Parameters:**
- `image_source` (str): Path or URL to the image
- `prompt` (str): Analysis prompt
- `output_format` (str, optional): Desired output format

**Returns:**
```python
{
    "success": bool,
    "confidence": float,
    "categories": List[str],
    "analysis": Dict[str, Any],
    "metadata": Dict[str, Any]
}
```

**Example:**
```python
# Direct MCP tool call
result = await mcp__zai_mcp_server__analyze_image(
    image_source=str(image_path),
    prompt="Analyze this image for game asset categories: animations, environments, UI elements, or effects. Provide confidence scores for each category.",
    output_format="json"
)
```

#### mcp__4_5v_mcp__analyze_image

Fallback tool for remote URL analysis.

**Parameters:**
- `imageSource` (str): Remote URL to the image
- `prompt` (str): Analysis prompt

**Example:**
```python
# Fallback for remote URLs
result = await mcp__4_5v_mcp__analyze_image(
    imageSource="https://example.com/image.png",
    prompt="Analyze this game asset image and classify its type."
)
```

## UI Components

### ImageValidatorUI

Main UI window for image validation.

#### Signals

```python
validation_completed = pyqtSignal(list)          # Emitted when validation completes
manual_review_completed = pyqtSignal(str, str)   # Emitted when manual review completes
```

#### Methods

##### load_images()

```python
def load_images(self, image_paths: List[Path]):
    """
    Load images for validation.

    Args:
        image_paths: List of image file paths
    """
```

##### display_validation_results()

```python
def display_validation_results(self, results: List[Dict[str, Any]]):
    """
    Display validation results in the UI.

    Args:
        results: List of validation results to display
    """
```

### ImageCard

Widget displaying an individual image for validation.

#### Constructor

```python
def __init__(self, image_path: Path, validation_result: Dict[str, Any]):
    """
    Initialize image card.

    Args:
        image_path: Path to the image file
        validation_result: Validation result data
    """
```

#### Signals

```python
selected = pyqtSignal()              # Emitted when card is selected
category_chosen = pyqtSignal(str)    # Emitted when category is chosen
```

### ManualReviewDialog

Dialog for manual review of low-confidence images.

#### Constructor

```python
def __init__(self, image_path: Path, suggested_categories: List[str], parent=None):
    """
    Initialize manual review dialog.

    Args:
        image_path: Path to the image being reviewed
        suggested_categories: List of suggested categories
        parent: Parent widget
    """
```

#### Methods

##### get_selected_category()

```python
def get_selected_category(self) -> Optional[str]:
    """
    Get the user-selected category.

    Returns:
        str or None: Selected category or None if no selection
    """
```

##### get_notes()

```python
def get_notes(self) -> str:
    """
    Get user notes from the dialog.

    Returns:
        str: User notes text
    """
```

## Specialized Validators

### AnimationValidator

Validates sprite sheets and animation sequences.

#### Methods

```python
async def validate_sprite_sheet(self, image_path: Path) -> AnimationResult:
    """
    Validate sprite sheet for animation sequence.

    Args:
        image_path: Path to sprite sheet image

    Returns:
        AnimationResult: Validation results specific to animations
    """

async def validate_frame_consistency(self, frames: List[Path]) -> ConsistencyResult:
    """
    Validate consistency across animation frames.

    Args:
        frames: List of animation frame paths

    Returns:
        ConsistencyResult: Consistency validation results
    """
```

### EnvironmentValidator

Validates environment assets (tiles, backgrounds, props).

#### Methods

```python
async def validate_tiling(self, tile_path: Path) -> TilingResult:
    """
    Validate tile for seamless tiling.

    Args:
        tile_path: Path to tile image

    Returns:
        TilingResult: Tiling validation results
    """

async def validate_perspective(self, asset_path: Path) -> PerspectiveResult:
    """
    Validate asset perspective consistency.

    Args:
        asset_path: Path to environment asset

    Returns:
        PerspectiveResult: Perspective validation results
    """
```

### UIValidator

Validates UI elements (icons, buttons, menus).

#### Methods

```python
async def validate_resolution(self, ui_path: Path) -> ResolutionResult:
    """
    Validate UI element resolution.

    Args:
        ui_path: Path to UI element image

    Returns:
        ResolutionResult: Resolution validation results
    """

async def validate_transparency(self, ui_path: Path) -> TransparencyResult:
    """
    Validate UI element transparency.

    Args:
        ui_path: Path to UI element image

    Returns:
        TransparencyResult: Transparency validation results
    """
```

### EffectsValidator

Validates visual effects (particles, explosions, glows).

#### Methods

```python
async def validate_performance(self, effect_path: Path) -> PerformanceResult:
    """
    Validate effect performance characteristics.

    Args:
        effect_path: Path to effect image

    Returns:
        PerformanceResult: Performance validation results
    """

async def validate_visual_impact(self, effect_path: Path) -> ImpactResult:
    """
    Validate visual impact of effect.

    Args:
        effect_path: Path to effect image

    Returns:
        ImpactResult: Visual impact validation results
    """
```

## Result Data Types

### ValidationResult

```python
@dataclass
class ValidationResult:
    success: bool
    confidence: float
    issues: List[str]
    metadata: Dict[str, Any]
```

### AnimationResult

```python
@dataclass
class AnimationResult(ValidationResult):
    frame_count: int
    frame_size: Tuple[int, int]
    consistency_score: float
    animation_type: str
```

### TilingResult

```python
@dataclass
class TilingResult(ValidationResult):
    seamless: bool
    tile_size: Tuple[int, int]
    pattern_detected: bool
    corner_matching: bool
```

### ResolutionResult

```python
@dataclass
class ResolutionResult(ValidationResult):
    resolution: Tuple[int, int]
    fits_guidelines: bool
    recommended_scale: float
    aspect_ratio: float
```

## Constants

### Default Categories

```python
DEFAULT_CATEGORIES = [
    "animations",
    "environments",
    "ui_elements",
    "effects",
    "other"
]
```

### Supported Formats

```python
SUPPORTED_FORMATS = {
    '.png',    # Portable Network Graphics
    '.jpg',    # JPEG
    '.jpeg',   # JPEG
    '.webp',   # WebP
    '.svg',    # Scalable Vector Graphics
    '.exr',    # OpenEXR
    '.tga',    # Targa
    '.bmp'     # Bitmap
}
```

### Default Thresholds

```python
DEFAULT_THRESHOLDS = ThresholdConfig(
    auto_accept=0.85,
    manual_review_suggested=0.60,
    manual_review_required=0.30,
    error=0.0
)
```

## Error Handling

### Exception Types

```python
class ImageValidationError(Exception):
    """Base exception for image validation errors"""
    pass

class MCPConnectionError(ImageValidationError):
    """Raised when MCP connection fails"""
    pass

class UnsupportedFormatError(ImageValidationError):
    """Raised for unsupported image formats"""
    pass

class ConfidenceThresholdError(ImageValidationError):
    """Raised when confidence is below acceptable threshold"""
    pass
```

### Error Recovery

```python
async def safe_validate_image(image_path: Path, validator) -> ValidationResult:
    """Validate image with comprehensive error handling"""
    try:
        return await validator.validate(image_path)
    except FileNotFoundError:
        return ValidationResult.error("File not found")
    except UnsupportedFormatError:
        return ValidationResult.error("Unsupported format")
    except MCPConnectionError:
        # Retry with fallback validator
        return await fallback_validator.validate(image_path)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return ValidationResult.error(f"Validation failed: {e}")
```

## Performance Considerations

### Memory Management

```python
# Good: Process images in batches to limit memory usage
async def memory_efficient_validation(image_paths: List[Path]):
    batch_size = 50
    for i in range(0, len(image_paths), batch_size):
        batch = image_paths[i:i + batch_size]
        await process_batch(batch)
        # Batch automatically cleaned up after processing
```

### Parallel Processing

```python
# Good: Use semaphore to limit concurrent processing
semaphore = asyncio.Semaphore(4)

async def limited_process_image(image_path: Path):
    async with semaphore:
        return await process_image(image_path)
```

### Caching

```python
# Good: Cache analysis results for unchanged files
from functools import lru_cache
import hashlib

@lru_cache(maxsize=1000)
def get_file_hash(file_path: Path) -> str:
    """Get file hash for caching"""
    with open(file_path, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

async def cached_validate(image_path: Path) -> ValidationResult:
    """Validate with caching"""
    file_hash = get_file_hash(image_path)
    cache_key = f"{image_path}:{file_hash}"

    # Check cache first
    cached_result = cache.get(cache_key)
    if cached_result:
        return cached_result

    # Perform validation
    result = await validate_image(image_path)

    # Cache result
    cache[cache_key] = result
    return result
```