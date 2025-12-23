# Godot Image Validator - Implementation Patterns

This document provides comprehensive implementation patterns for the Godot Image Validator, focusing on Python-based analysis with MCP integration, confidence scoring, and UI workflows.

## Core Architecture Patterns

### 1. MCP Client Pattern

The MCP client handles communication with Model Context Protocol servers for AI-powered image analysis.

```python
# examples/mcp_client.py
import asyncio
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class AnalysisResult:
    success: bool
    confidence: float
    categories: List[str]
    issues: List[str]
    metadata: Dict[str, Any]
    error_message: Optional[str] = None

class MCPClient:
    """Client for MCP image analysis tools"""

    def __init__(self, timeout: int = 30):
        self.timeout = timeout
        self.max_retries = 3
        self.retry_delay = 2.0
        self.logger = logging.getLogger(__name__)

    async def analyze_image(self,
                           image_path: Path,
                           categories: List[str] = None) -> AnalysisResult:
        """Analyze image using MCP tools"""
        if categories is None:
            categories = ["animations", "environments", "ui_elements", "effects"]

        try:
            # Primary tool: mcp__zai-mcp-server__analyze_image
            result = await self._call_analyze_image_tool(image_path, categories)

            if not result.success:
                # Retry with exponential backoff
                result = await self._retry_analysis(image_path, categories)

            return result

        except Exception as e:
            self.logger.error(f"MCP analysis failed for {image_path}: {e}")
            return AnalysisResult.fallback_result(image_path, str(e))

    async def _call_analyze_image_tool(self,
                                      image_path: Path,
                                      categories: List[str]) -> AnalysisResult:
        """Call the primary MCP analyze_image tool"""
        try:
            # Tool call implementation would go here
            # This is where you'd integrate with the actual MCP tool

            # Mock implementation for demonstration
            await asyncio.sleep(0.1)  # Simulate network call

            return AnalysisResult(
                success=True,
                confidence=0.85,
                categories=categories[:1],  # Simulated category selection
                issues=[],
                metadata={"tool_used": "mcp__zai-mcp-server__analyze_image"}
            )

        except Exception as e:
            return AnalysisResult(
                success=False,
                confidence=0.0,
                categories=[],
                issues=[f"Tool call failed: {e}"],
                metadata={}
            )

    async def _retry_analysis(self,
                             image_path: Path,
                             categories: List[str]) -> AnalysisResult:
        """Retry analysis with exponential backoff"""
        for attempt in range(self.max_retries):
            try:
                delay = self.retry_delay * (2 ** attempt)
                await asyncio.sleep(delay)

                result = await self._call_analyze_image_tool(image_path, categories)
                if result.success:
                    return result

            except Exception as e:
                self.logger.warning(f"Retry {attempt + 1} failed: {e}")
                continue

        # All retries failed
        return AnalysisResult.fallback_result(image_path, "All retries failed")

# Usage Example
async def main():
    client = MCPClient()
    result = await client.analyze_image(Path("assets/player_sprite.png"))

    if result.success:
        print(f"Analysis successful: {result.categories} (confidence: {result.confidence})")
    else:
        print(f"Analysis failed: {result.error_message}")
```

### 2. Confidence Scoring Pattern

The confidence scorer provides weighted confidence calculation with configurable thresholds.

```python
# examples/confidence_scorer.py
from dataclasses import dataclass, field
from typing import Dict, Any, List
from enum import Enum

class ValidationLevel(Enum):
    AUTO_ACCEPT = "auto_accept"
    MANUAL_REVIEW_SUGGESTED = "manual_review_suggested"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    ERROR = "error"

@dataclass
class ThresholdConfig:
    auto_accept: float = 0.85
    manual_review_suggested: float = 0.60
    manual_review_required: float = 0.30
    error: float = 0.0

@dataclass
class AspectWeights:
    content_match: float = 0.4
    quality_assessment: float = 0.3
    category_confidence: float = 0.2
    technical_analysis: float = 0.1

class ConfidenceScorer:
    """Manages confidence calculation and threshold decisions"""

    def __init__(self, thresholds: ThresholdConfig = None, weights: AspectWeights = None):
        self.thresholds = thresholds or ThresholdConfig()
        self.weights = weights or AspectWeights()

    def calculate_confidence(self, analysis_result: Dict[str, Any]) -> float:
        """Calculate overall confidence from multi-aspect analysis"""
        content_match = analysis_result.get('content_match', 0.0)
        quality_assessment = analysis_result.get('quality_assessment', 0.0)
        category_confidence = analysis_result.get('category_confidence', 0.0)
        technical_analysis = analysis_result.get('technical_analysis', 0.0)

        overall_confidence = (
            content_match * self.weights.content_match +
            quality_assessment * self.weights.quality_assessment +
            category_confidence * self.weights.category_confidence +
            technical_analysis * self.weights.technical_analysis
        )

        return min(1.0, max(0.0, overall_confidence))

    def get_validation_level(self, confidence: float) -> ValidationLevel:
        """Determine validation level based on confidence"""
        if confidence >= self.thresholds.auto_accept:
            return ValidationLevel.AUTO_ACCEPT
        elif confidence >= self.thresholds.manual_review_suggested:
            return ValidationLevel.MANUAL_REVIEW_SUGGESTED
        elif confidence >= self.thresholds.manual_review_required:
            return ValidationLevel.MANUAL_REVIEW_REQUIRED
        else:
            return ValidationLevel.ERROR

    def should_require_manual_review(self, confidence: float) -> bool:
        """Check if manual review is required"""
        return confidence < self.thresholds.auto_accept

    def get_status_color(self, validation_level: ValidationLevel) -> str:
        """Get color code for validation level"""
        color_map = {
            ValidationLevel.AUTO_ACCEPT: "#4CAF50",      # Green
            ValidationLevel.MANUAL_REVIEW_SUGGESTED: "#FFC107",  # Yellow
            ValidationLevel.MANUAL_REVIEW_REQUIRED: "#FF9800",  # Orange
            ValidationLevel.ERROR: "#F44336"      # Red
        }
        return color_map.get(validation_level, "#9E9E9E")  # Gray default

# Advanced Pattern: Custom Rules Engine
class CustomRulesEngine:
    """Engine for applying custom validation rules"""

    def __init__(self):
        self.rules: Dict[str, callable] = {}

    def add_rule(self, name: str, rule_func: callable) -> None:
        """Add a custom validation rule"""
        self.rules[name] = rule_func

    def apply_rules(self, image_path: Path, analysis_result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Apply all custom rules to an image"""
        results = []

        for rule_name, rule_func in self.rules.items():
            try:
                result = rule_func(image_path, analysis_result)
                results.append({
                    "rule": rule_name,
                    "result": result
                })
            except Exception as e:
                results.append({
                    "rule": rule_name,
                    "result": {
                        "success": False,
                        "message": f"Rule execution failed: {e}",
                        "confidence": 0.0
                    }
                })

        return results

# Usage Examples
def setup_pixel_art_rules(scorer: ConfidenceScorer):
    """Setup rules specific to pixel art projects"""
    rules_engine = CustomRulesEngine()

    def validate_pixel_dimensions(image_path: Path, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        from PIL import Image

        try:
            with Image.open(image_path) as img:
                width, height = img.size

            # Pixel art should have dimensions divisible by 4
            if width % 4 != 0 or height % 4 != 0:
                return {
                    "success": False,
                    "message": f"Pixel dimensions {width}x{height} not divisible by 4",
                    "confidence": 0.5
                }

            return {
                "success": True,
                "message": "Valid pixel art dimensions",
                "confidence": 0.95
            }

        except Exception as e:
            return {
                "success": False,
                "message": f"Image analysis failed: {e}",
                "confidence": 0.0
            }

    rules_engine.add_rule("pixel_dimensions", validate_pixel_dimensions)
    return rules_engine
```

### 3. UI Workflow Pattern

The UI workflow provides an interactive interface for manual review using PyQt/PySide.

```python
# examples/image_validator_ui.py
import sys
from pathlib import Path
from typing import List, Optional, Dict, Any
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QGridLayout, QLabel, QPushButton, QListWidget, QListWidgetItem,
    QScrollArea, QFrame, QDialog, QTextEdit, QProgressBar,
    QMessageBox, QSplitter
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QPixmap, QIcon

class ImageCard(QFrame):
    """Card widget displaying an image for validation"""

    selected = pyqtSignal()
    category_chosen = pyqtSignal(str)

    def __init__(self, image_path: Path, validation_result: Dict[str, Any]):
        super().__init__()
        self.image_path = image_path
        self.validation_result = validation_result
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)

        # Image preview
        image_label = QLabel()
        pixmap = QPixmap(str(self.image_path))
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(200, 200, Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(scaled_pixmap)
        else:
            image_label.setText("No Preview")
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        image_label.setMinimumSize(200, 200)
        layout.addWidget(image_label)

        # Confidence indicator
        confidence = self.validation_result.get('confidence', 0.0)
        confidence_label = QLabel(f"Confidence: {confidence:.1%}")

        # Set color based on confidence
        if confidence >= 0.85:
            confidence_label.setStyleSheet("color: #4CAF50; font-weight: bold;")
        elif confidence >= 0.60:
            confidence_label.setStyleSheet("color: #FFC107; font-weight: bold;")
        elif confidence >= 0.30:
            confidence_label.setStyleSheet("color: #FF9800; font-weight: bold;")
        else:
            confidence_label.setStyleSheet("color: #F44336; font-weight: bold;")

        layout.addWidget(confidence_label)

        # File name
        file_label = QLabel(self.image_path.name)
        file_label.setWordWrap(True)
        layout.addWidget(file_label)

        # Status indicator
        status_color = self._get_status_color(confidence)
        self.setStyleSheet(f"QFrame {{ border: 2px solid {status_color}; }}")

    def _get_status_color(self, confidence: float) -> str:
        if confidence >= 0.85:
            return "#4CAF50"  # Green
        elif confidence >= 0.60:
            return "#FFC107"  # Yellow
        elif confidence >= 0.30:
            return "#FF9800"  # Orange
        else:
            return "#F44336"  # Red

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.selected.emit()
        super().mousePressEvent(event)

class ManualReviewDialog(QDialog):
    """Dialog for manual review of low-confidence images"""

    def __init__(self, image_path: Path, suggested_categories: List[str], parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.suggested_categories = suggested_categories
        self.selected_category = None
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle(f"Manual Review - {self.image_path.name}")
        self.setModal(True)
        self.resize(600, 500)

        layout = QVBoxLayout(self)

        # Image preview
        image_label = QLabel()
        pixmap = QPixmap(str(self.image_path))
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(400, 300, Qt.AspectRatioMode.KeepAspectRatio)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(image_label)

        # Category selection
        category_label = QLabel("Select the appropriate category:")
        layout.addWidget(category_label)

        self.category_list = QListWidget()
        for category in self.suggested_categories:
            item = QListWidgetItem(category)
            self.category_list.addItem(item)

        self.category_list.itemDoubleClicked.connect(self.accept_category)
        layout.addWidget(self.category_list)

        # Notes
        notes_label = QLabel("Notes (optional):")
        layout.addWidget(notes_label)

        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        layout.addWidget(self.notes_input)

        # Buttons
        button_layout = QHBoxLayout()

        accept_button = QPushButton("Accept Selection")
        accept_button.clicked.connect(self.accept_category)
        button_layout.addWidget(accept_button)

        reject_button = QPushButton("Reject")
        reject_button.clicked.connect(self.reject)
        button_layout.addWidget(reject_button)

        layout.addLayout(button_layout)

    def accept_category(self):
        selected_items = self.category_list.selectedItems()
        if selected_items:
            self.selected_category = selected_items[0].text()
            self.accept()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a category.")

class ImageValidatorUI(QMainWindow):
    """Main UI for image validation"""

    validation_completed = pyqtSignal(list)
    manual_review_completed = pyqtSignal(str, str)  # image_path, category

    def __init__(self):
        super().__init__()
        self.validation_results = []
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Godot Image Validator")
        self.setGeometry(100, 100, 1200, 800)

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)

        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel - Image grid
        left_panel = self.create_image_panel()
        splitter.addWidget(left_panel)

        # Right panel - Category selection and actions
        right_panel = self.create_control_panel()
        splitter.addWidget(right_panel)

        # Set splitter sizes
        splitter.setSizes([800, 400])

    def create_image_panel(self) -> QWidget:
        """Create the image display panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Progress bar
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # Scrollable image grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        self.image_grid = QWidget()
        self.grid_layout = QGridLayout(self.image_grid)
        scroll_area.setWidget(self.image_grid)

        layout.addWidget(scroll_area)

        return panel

    def create_control_panel(self) -> QWidget:
        """Create the control panel"""
        panel = QWidget()
        layout = QVBoxLayout(panel)

        # Title
        title_label = QLabel("Image Validator")
        title_label.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title_label)

        # Category list
        category_label = QLabel("Categories:")
        layout.addWidget(category_label)

        self.category_list = QListWidget()
        categories = ["animations", "environments", "ui_elements", "effects", "other"]
        for category in categories:
            self.category_list.addItem(category)
        layout.addWidget(self.category_list)

        # Action buttons
        button_layout = QVBoxLayout()

        self.validate_button = QPushButton("Start Validation")
        self.validate_button.clicked.connect(self.start_validation)
        button_layout.addWidget(self.validate_button)

        self.process_review_button = QPushButton("Process Manual Reviews")
        self.process_review_button.clicked.connect(self.process_manual_reviews)
        self.process_review_button.setEnabled(False)
        button_layout.addWidget(self.process_review_button)

        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)
        button_layout.addWidget(self.export_button)

        layout.addLayout(button_layout)

        # Statistics
        layout.addStretch()

        self.stats_label = QLabel("No assets loaded")
        self.stats_label.setStyleSheet("color: #666;")
        layout.addWidget(self.stats_label)

        return panel

    def load_images(self, image_paths: List[Path]):
        """Load images for validation"""
        self.image_paths = image_paths
        self.update_stats()

    def display_validation_results(self, results: List[Dict[str, Any]]):
        """Display validation results in the grid"""
        self.validation_results = results

        # Clear existing grid
        for i in reversed(range(self.grid_layout.count())):
            child = self.grid_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

        # Add image cards
        cols = 4
        for i, result in enumerate(results):
            image_path = result.get('image_path')
            if not image_path:
                continue

            card = ImageCard(image_path, result)
            card.selected.connect(lambda p=image_path: self.select_image(p))

            row = i // cols
            col = i % cols
            self.grid_layout.addWidget(card, row, col)

        self.update_stats()

    def select_image(self, image_path: Path):
        """Handle image selection"""
        # Find the result and show manual review dialog if needed
        for result in self.validation_results:
            if result.get('image_path') == image_path:
                confidence = result.get('confidence', 0.0)
                if confidence < 0.85:
                    self.show_manual_review_dialog(image_path, result)
                break

    def show_manual_review_dialog(self, image_path: Path, result: Dict[str, Any]):
        """Show manual review dialog for low-confidence image"""
        suggested_categories = result.get('categories', ['other'])

        dialog = ManualReviewDialog(image_path, suggested_categories, self)
        if dialog.exec() == QDialog.DialogCode.Accepted:
            category = dialog.selected_category or 'other'
            notes = dialog.notes_input.toPlainText()

            # Emit signal for manual review completion
            self.manual_review_completed.emit(str(image_path), category)

    def update_stats(self):
        """Update statistics display"""
        if hasattr(self, 'validation_results') and self.validation_results:
            total = len(self.validation_results)
            auto_accept = sum(1 for r in self.validation_results if r.get('confidence', 0) >= 0.85)
            manual_review = total - auto_accept

            stats_text = f"Total: {total} | Auto-accept: {auto_accept} | Manual review: {manual_review}"
            self.stats_label.setText(stats_text)
        else:
            self.stats_label.setText("No assets loaded")

# Usage Example
def main():
    app = QApplication(sys.argv)

    # Create main window
    ui = ImageValidatorUI()
    ui.show()

    # Load some test images
    test_images = [
        Path("test_assets/player.png"),
        Path("test_assets/background.jpg"),
        Path("test_assets/ui_button.png")
    ]

    # Mock validation results for demonstration
    mock_results = [
        {
            "image_path": test_images[0],
            "confidence": 0.92,
            "categories": ["animations"]
        },
        {
            "image_path": test_images[1],
            "confidence": 0.75,
            "categories": ["environments"]
        },
        {
            "image_path": test_images[2],
            "confidence": 0.45,
            "categories": ["ui_elements"]
        }
    ]

    ui.load_images(test_images)
    ui.display_validation_results(mock_results)

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
```

### 4. Batch Processing Pattern

The batch processor handles efficient processing of multiple images with progress tracking.

```python
# examples/batch_processor.py
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional
from dataclasses import dataclass
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

@dataclass
class BatchConfig:
    batch_size: int = 50
    parallel_processing: bool = True
    max_workers: int = 4
    auto_accept_threshold: float = 0.85
    timeout_per_image: int = 30

class BatchProcessor:
    """Processes multiple images in batches with progress tracking"""

    def __init__(self, config: BatchConfig = None):
        self.config = config or BatchConfig()
        self.logger = logging.getLogger(__name__)
        self._progress_callbacks = []

    def add_progress_callback(self, callback: Callable[[int, int, str], None]):
        """Add callback for progress updates"""
        self._progress_callbacks.append(callback)

    async def process_batch(self,
                           image_paths: List[Path],
                           validator_func: Callable) -> List[Dict[str, Any]]:
        """Process a batch of images"""
        total_images = len(image_paths)
        results = []

        self.logger.info(f"Starting batch processing of {total_images} images")

        if self.config.parallel_processing:
            results = await self._process_parallel(image_paths, validator_func)
        else:
            results = await self._process_sequential(image_paths, validator_func)

        self.logger.info(f"Batch processing completed: {len(results)} results")
        return results

    async def _process_parallel(self,
                               image_paths: List[Path],
                               validator_func: Callable) -> List[Dict[str, Any]]:
        """Process images in parallel"""
        results = []
        total_images = len(image_paths)
        processed = 0

        # Create batches
        batches = self._create_batches(image_paths)

        for batch_num, batch in enumerate(batches):
            self._notify_progress(processed, total_images, f"Processing batch {batch_num + 1}/{len(batches)}")

            # Process batch in parallel
            batch_tasks = []
            for image_path in batch:
                task = asyncio.create_task(
                    self._process_single_image(image_path, validator_func)
                )
                batch_tasks.append(task)

            # Wait for batch completion
            batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)

            # Handle results
            for result in batch_results:
                if isinstance(result, Exception):
                    self.logger.error(f"Error processing image: {result}")
                    results.append(self._create_error_result(str(result)))
                else:
                    results.append(result)

                processed += 1
                self._notify_progress(processed, total_images, f"Processed {processed}/{total_images} images")

        return results

    async def _process_sequential(self,
                                image_paths: List[Path],
                                validator_func: Callable) -> List[Dict[str, Any]]:
        """Process images sequentially"""
        results = []
        total_images = len(image_paths)

        for i, image_path in enumerate(image_paths):
            self._notify_progress(i, total_images, f"Processing {image_path.name}")

            try:
                result = await self._process_single_image(image_path, validator_func)
                results.append(result)
            except Exception as e:
                self.logger.error(f"Error processing {image_path}: {e}")
                results.append(self._create_error_result(str(e)))

        return results

    async def _process_single_image(self,
                                   image_path: Path,
                                   validator_func: Callable) -> Dict[str, Any]:
        """Process a single image"""
        try:
            result = await validator_func(image_path)
            result['image_path'] = image_path
            return result
        except Exception as e:
            self.logger.error(f"Validation failed for {image_path}: {e}")
            return self._create_error_result(str(e), image_path)

    def _create_batches(self, items: List[Path]) -> List[List[Path]]:
        """Split items into batches"""
        batches = []
        for i in range(0, len(items), self.config.batch_size):
            batch = items[i:i + self.config.batch_size]
            batches.append(batch)
        return batches

    def _create_error_result(self, error_message: str, image_path: Path = None) -> Dict[str, Any]:
        """Create an error result"""
        return {
            "image_path": image_path,
            "success": False,
            "confidence": 0.0,
            "categories": [],
            "issues": [error_message],
            "metadata": {"error": True}
        }

    def _notify_progress(self, current: int, total: int, message: str):
        """Notify progress callbacks"""
        for callback in self._progress_callbacks:
            try:
                callback(current, total, message)
            except Exception as e:
                self.logger.error(f"Progress callback error: {e}")

# Progress tracking with UI integration
class ProgressTracker:
    """Tracks and reports batch processing progress"""

    def __init__(self):
        self.current = 0
        self.total = 0
        self.start_time = None
        self.last_update = None

    def start(self, total: int):
        """Start progress tracking"""
        self.total = total
        self.current = 0
        self.start_time = asyncio.get_event_loop().time()
        self.last_update = self.start_time

    def update(self, current: int, message: str = ""):
        """Update progress"""
        self.current = current
        self.last_update = asyncio.get_event_loop().time()

        if message:
            print(f"Progress: {current}/{self.total} - {message}")

    def get_eta(self) -> float:
        """Get estimated time remaining"""
        if self.current == 0 or not self.start_time:
            return 0.0

        elapsed = self.last_update - self.start_time
        rate = self.current / elapsed if elapsed > 0 else 0
        remaining = self.total - self.current

        return remaining / rate if rate > 0 else 0.0

    def get_progress_percentage(self) -> float:
        """Get progress as percentage"""
        if self.total == 0:
            return 0.0
        return (self.current / self.total) * 100.0

# Usage Example
async def main():
    # Setup batch processor
    config = BatchConfig(
        batch_size=20,
        parallel_processing=True,
        max_workers=4,
        auto_accept_threshold=0.85
    )

    processor = BatchProcessor(config)

    # Setup progress tracking
    progress_tracker = ProgressTracker()

    def progress_update(current: int, total: int, message: str):
        progress_tracker.update(current, message)
        eta = progress_tracker.get_eta()
        percentage = progress_tracker.get_progress_percentage()
        print(f"Progress: {percentage:.1f}% - ETA: {eta:.1f}s - {message}")

    processor.add_progress_callback(progress_update)

    # Mock validation function
    async def mock_validator(image_path: Path) -> Dict[str, Any]:
        await asyncio.sleep(0.1)  # Simulate processing time
        return {
            "success": True,
            "confidence": 0.8,
            "categories": ["animations"],
            "issues": [],
            "metadata": {"processing_time": 0.1}
        }

    # Get test images
    image_paths = list(Path("test_assets").glob("*.png"))

    if not image_paths:
        print("No test images found")
        return

    # Start processing
    progress_tracker.start(len(image_paths))
    results = await processor.process_batch(image_paths, mock_validator)

    # Report results
    successful = sum(1 for r in results if r.get("success", False))
    auto_accepted = sum(1 for r in results if r.get("confidence", 0) >= config.auto_accept_threshold)

    print(f"\nProcessing complete!")
    print(f"Total images: {len(results)}")
    print(f"Successful: {successful}")
    print(f"Auto-accepted: {auto_accepted}")
    print(f"Manual review required: {len(results) - auto_accepted}")

if __name__ == "__main__":
    asyncio.run(main())
```

## Anti-Patterns

### 1. Synchronous MCP Tool Calls
```python
# ANTI-PATTERN: Blocking calls in UI thread
def bad_mcp_usage():
    result = mcp_client.analyze_image_sync(image_path)  # Blocks UI!

# GOOD PATTERN: Async calls with proper await
async def good_mcp_usage():
    result = await mcp_client.analyze_image_async(image_path)  # Non-blocking
```

### 2. No Error Handling
```python
# ANTI-PATTERN: No error handling
def bad_validation():
    result = risky_operation()  # Can crash the application

# GOOD PATTERN: Comprehensive error handling
def good_validation():
    try:
        result = await risky_operation()
        return result
    except Exception as e:
        logger.error(f"Validation failed: {e}")
        return fallback_result()
```

### 3. Memory Leaks in Batch Processing
```python
# ANTI-PATTERN: Loading all images at once
def bad_batch_processing():
    images = [load_image(path) for path in image_paths]  # High memory usage
    # Process images...

# GOOD PATTERN: Stream processing with cleanup
async def good_batch_processing():
    for image_path in image_paths:
        image = load_image(image_path)
        try:
            await process_image(image)
        finally:
            image.close()  # Cleanup
```

## Best Practices

1. **Always use async/await** for MCP tool calls and I/O operations
2. **Implement proper error handling** with fallback mechanisms
3. **Use progress callbacks** for long-running operations
4. **Validate input paths** before processing
5. **Log operations** for debugging and audit trails
6. **Use dataclasses** for structured data handling
7. **Implement retry logic** for network operations
8. **Clean up resources** properly to prevent memory leaks
9. **Use type hints** for better code documentation
10. **Test with mock data** before using real MCP tools