#!/usr/bin/env python3
"""
Godot Image Validator UI

Main PyQt6 user interface for interactive image validation.
Displays images in a grid layout with confidence indicators and provides
manual review workflow for low-confidence images.
"""

import sys
from pathlib import Path
from typing import List, Dict, Any
import json
import asyncio
from datetime import datetime

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from PyQt6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QFrame,
    QDialog,
    QTextEdit,
    QProgressBar,
    QMessageBox,
    QSplitter,
    QFileDialog,
    QStatusBar,
    QToolBar,
    QAction,
    QSpinBox,
    QCheckBox,
    QGroupBox,
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QSettings
from PyQt6.QtGui import QPixmap, QFont, QKeySequence, QShortcut

# Import our modules
try:
    from mcp_client import MCPClient, AnalysisResult
    from confidence_scorer import (
        ConfidenceScorer,
        ThresholdConfig,
        AspectWeights,
        ValidationLevel,
    )
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure you're running from the correct directory")
    sys.exit(1)


class ImageCard(QFrame):
    """Card widget displaying an image for validation"""

    selected = pyqtSignal()
    manual_review_requested = pyqtSignal(Path, Dict[str, Any])

    def __init__(
        self, image_path: Path, validation_result: Dict[str, Any], parent=None
    ):
        super().__init__(parent)
        self.image_path = image_path
        self.validation_result = validation_result
        self.selected_state = False
        self.setup_ui()

    def setup_ui(self):
        """Setup the card UI components"""
        self.setFrameStyle(QFrame.Shape.Box)
        self.setLineWidth(2)
        self.setMinimumSize(220, 280)
        self.setMaximumSize(220, 280)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)

        # Image preview
        self.image_label = QLabel()
        self.image_label.setMinimumSize(200, 150)
        self.image_label.setMaximumSize(200, 150)
        self.image_label.setScaledContents(True)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Load and scale image
        self.load_image_preview()
        layout.addWidget(self.image_label, 0, Qt.AlignmentFlag.AlignCenter)

        # Confidence indicator
        confidence = self.validation_result.get("confidence", 0.0)
        self.confidence_label = QLabel(f"Confidence: {confidence:.1%}")
        self.confidence_label.setFont(QFont("Arial", 9, QFont.Weight.Bold))

        # Set color based on confidence
        color = self.get_confidence_color(confidence)
        self.confidence_label.setStyleSheet(f"color: {color};")
        layout.addWidget(self.confidence_label)

        # File name
        file_label = QLabel(self.image_path.name)
        file_label.setWordWrap(True)
        file_label.setFont(QFont("Arial", 8))
        file_label.setMaximumHeight(30)
        layout.addWidget(file_label)

        # Status indicator (colored border)
        self.update_status_color()

        # Make clickable
        self.setCursor(Qt.CursorShape.PointingHandCursor)

    def load_image_preview(self):
        """Load and scale image preview"""
        try:
            from PIL import Image

            # Check if file exists
            if not self.image_path.exists():
                self.image_label.setText("File Not Found")
                self.image_label.setStyleSheet("color: red;")
                return

            # Load and scale image
            with Image.open(self.image_path) as img:
                img.thumbnail((200, 150))

                # Convert to QPixmap
                if img.mode in ("RGBA", "LA"):
                    # Handle transparency
                    img = img.convert("RGBA")
                    qimg = ImageQt.ImageQt(img)
                    pixmap = QPixmap.fromImage(qimg)
                else:
                    img = img.convert("RGB")
                    qimg = ImageQt.ImageQt(img)
                    pixmap = QPixmap.fromImage(qimg)

                self.image_label.setPixmap(pixmap)

        except ImportError:
            # Fallback if PIL not available
            self.image_label.setText("PIL Required")
            self.image_label.setStyleSheet("color: orange;")
        except Exception as e:
            self.image_label.setText("Load Error")
            self.image_label.setStyleSheet("color: red;")
            print(f"Error loading image {self.image_path}: {e}")

    def get_confidence_color(self, confidence: float) -> str:
        """Get color based on confidence level"""
        if confidence >= 0.85:
            return "#4CAF50"  # Green
        elif confidence >= 0.60:
            return "#FFC107"  # Yellow
        elif confidence >= 0.30:
            return "#FF9800"  # Orange
        else:
            return "#F44336"  # Red

    def update_status_color(self):
        """Update the card border color based on confidence"""
        confidence = self.validation_result.get("confidence", 0.0)
        color = self.get_confidence_color(confidence)
        self.setStyleSheet(
            f"QFrame {{ border: 2px solid {color}; background: white; }}"
        )

        if self.selected_state:
            self.setStyleSheet(
                "QFrame { border: 3px solid #2196F3; background: #E3F2FD; }"
            )

    def mousePressEvent(self, event):
        """Handle mouse click events"""
        if event.button() == Qt.MouseButton.LeftButton:
            self.selected_state = not self.selected_state
            self.update_status_color()
            self.selected.emit()

            # If low confidence, request manual review
            confidence = self.validation_result.get("confidence", 0.0)
            if confidence < 0.85:
                self.manual_review_requested.emit(
                    self.image_path, self.validation_result
                )

        super().mousePressEvent(event)

    def set_selected(self, selected: bool):
        """Set selection state"""
        self.selected_state = selected
        self.update_status_color()


class ManualReviewDialog(QDialog):
    """Dialog for manual review of low-confidence images"""

    review_completed = pyqtSignal(Path, Dict[str, Any])

    def __init__(self, image_path: Path, analysis_result: Dict[str, Any], parent=None):
        super().__init__(parent)
        self.image_path = image_path
        self.analysis_result = analysis_result
        self.selected_categories = set()
        self.notes = ""
        self.setup_ui()

    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle(f"Manual Review - {self.image_path.name}")
        self.setModal(True)
        self.resize(700, 600)

        layout = QVBoxLayout(self)

        # Image preview section
        preview_group = QGroupBox("Image Preview")
        preview_layout = QVBoxLayout(preview_group)

        self.image_label = QLabel()
        self.image_label.setMinimumHeight(300)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setStyleSheet("border: 1px solid #ccc; background: #f9f9f9;")
        self.load_full_image()
        preview_layout.addWidget(self.image_label)

        # File info
        info_label = QLabel(f"File: {self.image_path}")
        info_label.setStyleSheet("font-weight: bold; color: #666;")
        preview_layout.addWidget(info_label)

        layout.addWidget(preview_group)

        # Analysis results section
        if self.analysis_result:
            analysis_group = QGroupBox("AI Analysis")
            analysis_layout = QVBoxLayout(analysis_group)

            confidence = self.analysis_result.get("confidence", 0.0)
            conf_label = QLabel(f"AI Confidence: {confidence:.1%}")
            conf_label.setStyleSheet(
                f"color: {self.get_confidence_color(confidence)}; font-weight: bold;"
            )
            analysis_layout.addWidget(conf_label)

            suggested = self.analysis_result.get("categories", [])
            if suggested:
                suggested_label = QLabel(
                    f"Suggested Categories: {', '.join(suggested)}"
                )
                analysis_layout.addWidget(suggested_label)

            issues = self.analysis_result.get("issues", [])
            if issues:
                issues_label = QLabel("Issues:")
                analysis_layout.addWidget(issues_label)
                for issue in issues:
                    issue_item = QLabel(f"  • {issue}")
                    issue_item.setStyleSheet("color: #f44336;")
                    analysis_layout.addWidget(issue_item)

            layout.addWidget(analysis_group)

        # Category selection
        category_group = QGroupBox("Select Correct Category")
        category_layout = QVBoxLayout(category_group)

        # Standard categories
        self.category_checkboxes = {}
        categories = ["animations", "environments", "ui_elements", "effects", "other"]

        # Create grid for categories
        category_grid = QGridLayout()

        for i, category in enumerate(categories):
            checkbox = QCheckBox(category.replace("_", " ").title())
            if category in suggested:
                checkbox.setChecked(True)
                self.selected_categories.add(category)
            checkbox.toggled.connect(
                lambda checked, c=category: self.on_category_toggled(c, checked)
            )
            self.category_checkboxes[category] = checkbox
            category_grid.addWidget(checkbox, i // 2, i % 2)

        category_layout.addLayout(category_grid)
        layout.addWidget(category_group)

        # Notes section
        notes_group = QGroupBox("Notes (Optional)")
        notes_layout = QVBoxLayout(notes_group)

        self.notes_input = QTextEdit()
        self.notes_input.setMaximumHeight(100)
        self.notes_input.setPlaceholderText("Add any notes about this validation...")
        notes_layout.addWidget(self.notes_input)

        layout.addWidget(notes_group)

        # Navigation buttons (for batch processing)
        nav_layout = QHBoxLayout()

        self.prev_button = QPushButton("← Previous")
        self.prev_button.clicked.connect(self.go_previous)
        nav_layout.addWidget(self.prev_button)

        nav_layout.addStretch()

        self.next_button = QPushButton("Next →")
        self.next_button.clicked.connect(self.go_next)
        nav_layout.addWidget(self.next_button)

        layout.addLayout(nav_layout)

        # Action buttons
        button_layout = QHBoxLayout()

        reject_button = QPushButton("Reject")
        reject_button.setStyleSheet("background: #f44336; color: white;")
        reject_button.clicked.connect(self.reject)
        button_layout.addWidget(reject_button)

        button_layout.addStretch()

        accept_button = QPushButton("Accept")
        accept_button.setStyleSheet("background: #4CAF50; color: white;")
        accept_button.clicked.connect(self.accept)
        button_layout.addWidget(accept_button)

        layout.addLayout(button_layout)

    def load_full_image(self):
        """Load full image for preview"""
        try:
            from PIL import ImageQt

            if self.image_path.exists():
                with Image.open(self.image_path) as img:
                    # Scale to fit dialog width while maintaining aspect ratio
                    max_width = 650
                    if img.width > max_width:
                        ratio = max_width / img.width
                        new_height = int(img.height * ratio)
                        img = img.resize((max_width, new_height))

                    qimg = ImageQt.ImageQt(img)
                    pixmap = QPixmap.fromImage(qimg)
                    self.image_label.setPixmap(pixmap)
            else:
                self.image_label.setText("File not found")
                self.image_label.setStyleSheet("color: red; font-size: 18px;")

        except Exception as e:
            self.image_label.setText(f"Error: {e}")
            self.image_label.setStyleSheet("color: red; font-size: 16px;")

    def get_confidence_color(self, confidence: float) -> str:
        """Get color based on confidence level"""
        if confidence >= 0.85:
            return "#4CAF50"
        elif confidence >= 0.60:
            return "#FFC107"
        elif confidence >= 0.30:
            return "#FF9800"
        else:
            return "#F44336"

    def on_category_toggled(self, category: str, checked: bool):
        """Handle category checkbox toggle"""
        if checked:
            self.selected_categories.add(category)
        else:
            self.selected_categories.discard(category)

    def go_previous(self):
        """Navigate to previous item"""
        self.accept()  # Signal to move to previous
        self.reject()  # But don't save current changes

    def go_next(self):
        """Navigate to next item"""
        self.accept()  # Save and move to next

    def get_result(self) -> Dict[str, Any]:
        """Get the validation result from this dialog"""
        return {
            "image_path": self.image_path,
            "categories": list(self.selected_categories),
            "notes": self.notes_input.toPlainText(),
            "accepted": True,
            "timestamp": datetime.now().isoformat(),
        }

    def accept(self):
        """Accept the validation"""
        self.notes = self.notes_input.toPlainText()
        super().accept()


class ImageValidatorUI(QMainWindow):
    """Main UI for image validation"""

    def __init__(self):
        super().__init__()
        self.settings = QSettings("GodotImageValidator", "UI")

        # Initialize components
        self.mcp_client = MCPClient(debug_mode=False)
        self.confidence_scorer = ConfidenceScorer()

        # State
        self.validation_results = []
        self.image_paths = []
        self.current_review_index = 0
        self.pending_reviews = []

        self.setup_ui()
        self.load_settings()

        # Setup keyboard shortcuts
        self.setup_shortcuts()

    def setup_ui(self):
        """Setup the main UI"""
        self.setWindowTitle("Godot Image Validator")
        self.setGeometry(100, 100, 1200, 800)

        # Create menu bar
        self.create_menu_bar()

        # Create toolbar
        self.create_toolbar()

        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")

        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)

        # Create splitter
        splitter = QSplitter(Qt.Orientation.Horizontal)
        main_layout.addWidget(splitter)

        # Left panel - Image grid
        left_panel = self.create_image_panel()
        splitter.addWidget(left_panel)

        # Right panel - Controls
        right_panel = self.create_control_panel()
        splitter.addWidget(right_panel)

        # Set splitter sizes
        splitter.setSizes([900, 300])

    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = self.menuBar()

        # File menu
        file_menu = menubar.addMenu("File")

        open_action = QAction("Open Images...", self)
        open_action.setShortcut(QKeySequence.StandardKey.Open)
        open_action.triggered.connect(self.open_images)
        file_menu.addAction(open_action)

        file_menu.addSeparator()

        save_action = QAction("Save Results...", self)
        save_action.setShortcut(QKeySequence.StandardKey.Save)
        save_action.triggered.connect(self.save_results)
        file_menu.addAction(save_action)

        load_action = QAction("Load Results...", self)
        load_action.triggered.connect(self.load_results)
        file_menu.addAction(load_action)

        file_menu.addSeparator()

        exit_action = QAction("Exit", self)
        exit_action.setShortcut(QKeySequence.StandardKey.Quit)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Edit menu
        edit_menu = menubar.addMenu("Edit")

        select_all_action = QAction("Select All", self)
        select_all_action.setShortcut(QKeySequence.StandardKey.SelectAll)
        select_all_action.triggered.connect(self.select_all)
        edit_menu.addAction(select_all_action)

        clear_selection_action = QAction("Clear Selection", self)
        clear_selection_action.triggered.connect(self.clear_selection)
        edit_menu.addAction(clear_selection_action)

        # View menu
        view_menu = menubar.addMenu("View")

        zoom_in_action = QAction("Zoom In", self)
        zoom_in_action.setShortcut(QKeySequence.StandardKey.ZoomIn)
        zoom_in_action.triggered.connect(self.zoom_in)
        view_menu.addAction(zoom_in_action)

        zoom_out_action = QAction("Zoom Out", self)
        zoom_out_action.setShortcut(QKeySequence.StandardKey.ZoomOut)
        zoom_out_action.triggered.connect(self.zoom_out)
        view_menu.addAction(zoom_out_action)

        # Tools menu
        tools_menu = menubar.addMenu("Tools")

        settings_action = QAction("Settings...", self)
        settings_action.triggered.connect(self.show_settings)
        tools_menu.addAction(settings_action)

        # Help menu
        help_menu = menubar.addMenu("Help")

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def create_toolbar(self):
        """Create the toolbar"""
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        # Open button
        open_action = QAction("Open", self)
        open_action.triggered.connect(self.open_images)
        toolbar.addAction(open_action)

        toolbar.addSeparator()

        # Validate button
        self.validate_action = QAction("Validate", self)
        self.validate_action.triggered.connect(self.start_validation)
        self.validate_action.setEnabled(False)
        toolbar.addAction(self.validate_action)

        toolbar.addSeparator()

        # Manual review button
        self.review_action = QAction("Manual Review", self)
        self.review_action.triggered.connect(self.start_manual_review)
        self.review_action.setEnabled(False)
        toolbar.addAction(self.review_action)

        # Export button
        self.export_action = QAction("Export", self)
        self.export_action.triggered.connect(self.export_results)
        self.export_action.setEnabled(False)
        toolbar.addAction(self.export_action)

    def setup_shortcuts(self):
        """Setup keyboard shortcuts"""
        # Space for manual review
        space_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Space), self)
        space_shortcut.activated.connect(self.quick_manual_review)

        # Ctrl+A for select all
        ctrl_a_shortcut = QShortcut(QKeySequence("Ctrl+A"), self)
        ctrl_a_shortcut.activated.connect(self.select_all)

        # Escape to deselect
        escape_shortcut = QShortcut(QKeySequence(Qt.Key.Key_Escape), self)
        escape_shortcut.activated.connect(self.clear_selection)

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
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.image_grid = QWidget()
        self.grid_layout = QGridLayout(self.image_grid)
        self.grid_layout.setSpacing(10)
        self.grid_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        scroll_area.setWidget(self.image_grid)

        layout.addWidget(scroll_area)

        return panel

    def create_control_panel(self) -> QWidget:
        """Create the control panel"""
        panel = QWidget()
        panel.setMaximumWidth(300)
        layout = QVBoxLayout(panel)

        # Title
        title_label = QLabel("Image Validator")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        layout.addWidget(title_label)

        layout.addWidget(QLabel(""))  # Spacer

        # Threshold settings
        threshold_group = QGroupBox("Validation Thresholds")
        threshold_layout = QVBoxLayout(threshold_group)

        # Auto-accept threshold
        auto_layout = QHBoxLayout()
        auto_layout.addWidget(QLabel("Auto-Accept:"))
        self.auto_threshold_spin = QSpinBox()
        self.auto_threshold_spin.setRange(0, 100)
        self.auto_threshold_spin.setValue(
            int(self.confidence_scorer.thresholds.auto_accept * 100)
        )
        self.auto_threshold_spin.setSuffix("%")
        self.auto_threshold_spin.valueChanged.connect(self.update_thresholds)
        auto_layout.addWidget(self.auto_threshold_spin)
        threshold_layout.addLayout(auto_layout)

        # Manual review threshold
        manual_layout = QHBoxLayout()
        manual_layout.addWidget(QLabel("Manual Review:"))
        self.manual_threshold_spin = QSpinBox()
        self.manual_threshold_spin.setRange(0, 100)
        self.manual_threshold_spin.setValue(
            int(self.confidence_scorer.thresholds.manual_review_suggested * 100)
        )
        self.manual_threshold_spin.setSuffix("%")
        self.manual_threshold_spin.valueChanged.connect(self.update_thresholds)
        manual_layout.addWidget(self.manual_threshold_spin)
        threshold_layout.addLayout(manual_layout)

        layout.addWidget(threshold_group)

        # Statistics
        layout.addWidget(QLabel(""))  # Spacer

        stats_group = QGroupBox("Statistics")
        stats_layout = QVBoxLayout(stats_group)

        self.stats_label = QLabel("No images loaded")
        self.stats_label.setWordWrap(True)
        stats_layout.addWidget(self.stats_label)

        layout.addWidget(stats_group)

        # Actions
        layout.addWidget(QLabel(""))  # Spacer

        actions_group = QGroupBox("Actions")
        actions_layout = QVBoxLayout(actions_group)

        self.validate_button = QPushButton("Start Validation")
        self.validate_button.clicked.connect(self.start_validation)
        self.validate_button.setEnabled(False)
        actions_layout.addWidget(self.validate_button)

        self.review_button = QPushButton("Process Manual Reviews")
        self.review_button.clicked.connect(self.start_manual_review)
        self.review_button.setEnabled(False)
        actions_layout.addWidget(self.review_button)

        self.export_button = QPushButton("Export Results")
        self.export_button.clicked.connect(self.export_results)
        self.export_button.setEnabled(False)
        actions_layout.addWidget(self.export_button)

        layout.addWidget(actions_group)

        # Add stretch at bottom
        layout.addStretch()

        return panel

    def open_images(self):
        """Open image files dialog"""
        file_dialog = QFileDialog()
        file_paths, _ = file_dialog.getOpenFileNames(
            self,
            "Select Images",
            "",
            "Image Files (*.png *.jpg *.jpeg *.webp *.svg *.exr *.tga *.bmp *.tiff *.tif);;All Files (*)",
        )

        if file_paths:
            self.load_images([Path(p) for p in file_paths])

    def load_images(self, image_paths: List[Path]):
        """Load images for validation"""
        self.image_paths = image_paths
        self.validation_results = []
        self.pending_reviews = []

        # Clear existing grid
        self.clear_image_grid()

        # Update UI
        self.update_stats()
        self.status_bar.showMessage(f"Loaded {len(image_paths)} images")

        # Enable buttons
        self.validate_action.setEnabled(True)
        self.validate_button.setEnabled(True)

    def clear_image_grid(self):
        """Clear the image grid"""
        # Remove all widgets from grid
        for i in reversed(range(self.grid_layout.count())):
            child = self.grid_layout.itemAt(i).widget()
            if child:
                child.setParent(None)

    def start_validation(self):
        """Start the validation process"""
        if not self.image_paths:
            QMessageBox.warning(self, "No Images", "Please load images first.")
            return

        # Show progress
        self.progress_bar.setMaximum(len(self.image_paths))
        self.progress_bar.setValue(0)
        self.progress_bar.setVisible(True)

        # Disable buttons
        self.validate_action.setEnabled(False)
        self.validate_button.setEnabled(False)

        # Start async validation
        self.validate_thread = ValidationThread(
            self.image_paths, self.mcp_client, self.confidence_scorer
        )
        self.validate_thread.progress_updated.connect(self.update_progress)
        self.validate_thread.validation_completed.connect(self.on_validation_completed)
        self.validate_thread.start()

    def update_progress(self, current: int, total: int):
        """Update progress bar"""
        self.progress_bar.setValue(current)
        self.status_bar.showMessage(f"Validating... {current}/{total}")

    def on_validation_completed(self, results: List[Dict[str, Any]]):
        """Handle validation completion"""
        self.validation_results = results
        self.progress_bar.setVisible(False)

        # Find items needing manual review
        auto_accept_threshold = self.confidence_scorer.thresholds.auto_accept
        self.pending_reviews = [
            i
            for i, result in enumerate(results)
            if result.get("confidence", 0.0) < auto_accept_threshold
        ]

        # Display results
        self.display_validation_results()

        # Update UI
        self.update_stats()
        self.status_bar.showMessage(
            f"Validation complete - {len(self.pending_reviews)} need manual review"
        )

        # Enable buttons
        self.validate_action.setEnabled(True)
        self.validate_button.setEnabled(True)
        self.review_action.setEnabled(len(self.pending_reviews) > 0)
        self.review_button.setEnabled(len(self.pending_reviews) > 0)
        self.export_action.setEnabled(True)
        self.export_button.setEnabled(True)

    def display_validation_results(self):
        """Display validation results in the grid"""
        self.clear_image_grid()

        # Add image cards
        cols = 4
        for i, result in enumerate(self.validation_results):
            if i < len(self.image_paths):
                image_path = self.image_paths[i]

                card = ImageCard(image_path, result)
                card.selected.connect(self.on_image_selected)
                card.manual_review_requested.connect(self.show_manual_review_dialog)

                row = i // cols
                col = i % cols
                self.grid_layout.addWidget(card, row, col)

        self.image_grid.update()

    def on_image_selected(self):
        """Handle image selection"""
        # Update statistics
        selected_count = self.count_selected_images()
        if selected_count > 0:
            self.status_bar.showMessage(f"Selected {selected_count} images")
        else:
            self.status_bar.showMessage("Ready")

    def show_manual_review_dialog(self, image_path: Path, result: Dict[str, Any]):
        """Show manual review dialog for an image"""
        dialog = ManualReviewDialog(image_path, result, self)

        if dialog.exec() == QDialog.DialogCode.Accepted:
            # Update result with manual review data
            review_result = dialog.get_result()
            self.apply_manual_review(review_result)

    def start_manual_review(self):
        """Start batch manual review process"""
        if not self.pending_reviews:
            QMessageBox.information(
                self, "No Reviews", "No images require manual review."
            )
            return

        self.current_review_index = 0
        self.show_next_manual_review()

    def show_next_manual_review(self):
        """Show next manual review dialog"""
        if self.current_review_index >= len(self.pending_reviews):
            self.finish_manual_review()
            return

        # Get current review item
        result_index = self.pending_reviews[self.current_review_index]
        image_path = self.image_paths[result_index]
        result = self.validation_results[result_index]

        # Create and show dialog
        dialog = ManualReviewDialog(image_path, result, self)
        dialog.review_completed.connect(self.apply_manual_review)

        # Update previous/next buttons
        dialog.prev_button.setEnabled(self.current_review_index > 0)
        dialog.next_button.setEnabled(
            self.current_review_index < len(self.pending_reviews) - 1
        )

        if dialog.exec() == QDialog.DialogCode.Accepted:
            self.current_review_index += 1
            self.show_next_manual_review()

    def apply_manual_review(self, review_result: Dict[str, Any]):
        """Apply manual review result"""
        # Find and update the validation result
        for i, result in enumerate(self.validation_results):
            if result.get("image_path") == review_result["image_path"]:
                # Update categories
                result["categories"] = review_result["categories"]
                result["manual_review"] = True
                result["review_notes"] = review_result.get("notes", "")
                result["review_timestamp"] = review_result.get("timestamp")

                # Update confidence for manual review
                result["confidence"] = 1.0  # Manual review = full confidence

                # Update the image card
                self.update_image_card(i, result)
                break

    def update_image_card(self, index: int, result: Dict[str, Any]):
        """Update an image card with new result"""
        # Find the card at this grid position
        cols = 4
        item = self.grid_layout.itemAtPosition(index // cols, index % cols)
        if item and item.widget():
            card = item.widget()
            if isinstance(card, ImageCard):
                card.validation_result = result
                card.confidence_label.setText(
                    f"Confidence: {result.get('confidence', 0.0):.1%}"
                )
                card.update_status_color()

    def finish_manual_review(self):
        """Finish manual review process"""
        QMessageBox.information(self, "Complete", "All manual reviews completed!")
        self.update_stats()

    def quick_manual_review(self):
        """Quick manual review for selected images"""
        selected = self.get_selected_images()
        if selected:
            self.start_manual_review()
        else:
            QMessageBox.information(self, "No Selection", "Please select images first.")

    def update_thresholds(self):
        """Update confidence thresholds"""
        self.confidence_scorer.thresholds.auto_accept = (
            self.auto_threshold_spin.value() / 100.0
        )
        self.confidence_scorer.thresholds.manual_review_suggested = (
            self.manual_threshold_spin.value() / 100.0
        )

    def count_selected_images(self) -> int:
        """Count selected images"""
        count = 0
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, ImageCard) and widget.selected_state:
                    count += 1
        return count

    def get_selected_images(self) -> List[int]:
        """Get indices of selected images"""
        selected = []
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, ImageCard) and widget.selected_state:
                    selected.append(i)
        return selected

    def select_all(self):
        """Select all images"""
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, ImageCard):
                    widget.set_selected(True)

    def clear_selection(self):
        """Clear selection"""
        for i in range(self.grid_layout.count()):
            item = self.grid_layout.itemAt(i)
            if item and item.widget():
                widget = item.widget()
                if isinstance(widget, ImageCard):
                    widget.set_selected(False)

    def zoom_in(self):
        """Zoom in images"""
        # TODO: Implement zoom functionality
        self.status_bar.showMessage("Zoom not implemented yet")

    def zoom_out(self):
        """Zoom out images"""
        # TODO: Implement zoom functionality
        self.status_bar.showMessage("Zoom not implemented yet")

    def update_stats(self):
        """Update statistics display"""
        if self.validation_results:
            total = len(self.validation_results)
            auto_accept = sum(
                1
                for r in self.validation_results
                if r.get("confidence", 0)
                >= self.confidence_scorer.thresholds.auto_accept
            )
            manual_review = len(self.pending_reviews)

            stats_text = f"Total: {total}\n"
            stats_text += f"Auto-accepted: {auto_accept}\n"
            stats_text += f"Manual review: {manual_review}"

            self.stats_label.setText(stats_text)
        else:
            self.stats_label.setText("No images loaded")

    def save_results(self):
        """Save validation results"""
        if not self.validation_results:
            QMessageBox.warning(self, "No Results", "No validation results to save.")
            return

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Results",
            f"validation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            "JSON Files (*.json);;CSV Files (*.csv);;All Files (*)",
        )

        if file_path:
            try:
                if file_path.endswith(".csv"):
                    self.save_csv(file_path)
                else:
                    self.save_json(file_path)
                QMessageBox.information(self, "Saved", f"Results saved to {file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to save: {e}")

    def save_json(self, file_path: str):
        """Save results as JSON"""
        data = {
            "timestamp": datetime.now().isoformat(),
            "thresholds": self.confidence_scorer.export_config(),
            "results": [],
        }

        for i, result in enumerate(self.validation_results):
            if i < len(self.image_paths):
                data["results"].append(
                    {
                        "image_path": str(self.image_paths[i]),
                        "confidence": result.get("confidence", 0.0),
                        "categories": result.get("categories", []),
                        "issues": result.get("issues", []),
                        "manual_review": result.get("manual_review", False),
                        "notes": result.get("review_notes", ""),
                    }
                )

        with open(file_path, "w") as f:
            json.dump(data, f, indent=2)

    def save_csv(self, file_path: str):
        """Save results as CSV"""
        import csv

        with open(file_path, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(
                [
                    "Image Path",
                    "Confidence",
                    "Categories",
                    "Issues",
                    "Manual Review",
                    "Notes",
                ]
            )

            for i, result in enumerate(self.validation_results):
                if i < len(self.image_paths):
                    writer.writerow(
                        [
                            str(self.image_paths[i]),
                            f"{result.get('confidence', 0.0):.2%}",
                            ", ".join(result.get("categories", [])),
                            "; ".join(result.get("issues", [])),
                            "Yes" if result.get("manual_review", False) else "No",
                            result.get("review_notes", ""),
                        ]
                    )

    def load_results(self):
        """Load validation results"""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Load Results", "", "JSON Files (*.json);;All Files (*)"
        )

        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)

                # Load configuration
                if "thresholds" in data:
                    config = data["thresholds"]
                    if "thresholds" in config:
                        self.confidence_scorer.import_config(config)
                        self.auto_threshold_spin.setValue(
                            int(self.confidence_scorer.thresholds.auto_accept * 100)
                        )
                        self.manual_threshold_spin.setValue(
                            int(
                                self.confidence_scorer.thresholds.manual_review_suggested
                                * 100
                            )
                        )

                # Load results
                # TODO: Implement result loading and UI update
                QMessageBox.information(
                    self, "Loaded", f"Results loaded from {file_path}"
                )

            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to load: {e}")

    def export_results(self):
        """Export validation results"""
        self.save_results()

    def show_settings(self):
        """Show settings dialog"""
        # TODO: Implement settings dialog
        QMessageBox.information(
            self, "Settings", "Settings dialog not implemented yet."
        )

    def show_about(self):
        """Show about dialog"""
        QMessageBox.about(
            self,
            "About Godot Image Validator",
            """<b>Godot Image Validator</b> v1.0.0<br><br>
            AI-powered image validation tool for Godot projects.<br><br>
            Uses Model Context Protocol (MCP) for image analysis<br>
            with confidence scoring and manual review workflows.<br><br>
            © 2025 Claude Code Skills""",
        )

    def load_settings(self):
        """Load application settings"""
        # Load window geometry
        geometry = self.settings.value("geometry")
        if geometry:
            self.restoreGeometry(geometry)

    def save_settings(self):
        """Save application settings"""
        # Save window geometry
        self.settings.setValue("geometry", self.saveGeometry())

    def closeEvent(self, event):
        """Handle close event"""
        self.save_settings()
        event.accept()


class ValidationThread(QThread):
    """Worker thread for image validation"""

    progress_updated = pyqtSignal(int, int)
    validation_completed = pyqtSignal(list)

    def __init__(self, image_paths: List[Path], mcp_client, confidence_scorer):
        super().__init__()
        self.image_paths = image_paths
        self.mcp_client = mcp_client
        self.confidence_scorer = confidence_scorer
        self.results = []

    def run(self):
        """Run validation in background thread"""
        self.results = []

        # Create event loop for async operations
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

        try:
            for i, image_path in enumerate(self.image_paths):
                # Run async validation
                result = loop.run_until_complete(self.validate_single_image(image_path))
                self.results.append(result)

                # Emit progress
                self.progress_updated.emit(i + 1, len(self.image_paths))

        finally:
            loop.close()

        # Emit completion
        self.validation_completed.emit(self.results)

    async def validate_single_image(self, image_path: Path) -> Dict[str, Any]:
        """Validate a single image"""
        try:
            # Analyze with MCP client
            analysis_result = await self.mcp_client.analyze_image(image_path)

            if analysis_result.success:
                # Calculate confidence
                confidence = self.confidence_scorer.calculate_confidence(
                    {
                        "content_match": analysis_result.confidence,
                        "quality_assessment": analysis_result.confidence * 0.9,
                        "category_confidence": analysis_result.confidence,
                        "technical_analysis": 0.9,
                    }
                )

                # Apply custom rules
                modified_result = self.confidence_scorer.apply_custom_rules(
                    image_path, {"confidence": confidence}
                )

                return {
                    "success": True,
                    "confidence": modified_result.get("confidence", confidence),
                    "categories": analysis_result.categories,
                    "issues": analysis_result.issues,
                    "metadata": analysis_result.metadata,
                }
            else:
                return {
                    "success": False,
                    "confidence": 0.0,
                    "categories": ["other"],
                    "issues": [analysis_result.error_message or "Analysis failed"],
                    "metadata": {},
                }

        except Exception as e:
            return {
                "success": False,
                "confidence": 0.0,
                "categories": ["other"],
                "issues": [str(e)],
                "metadata": {},
            }


# Required import for PIL ImageQt
try:
    from PIL import ImageQt
except ImportError:
    ImageQt = None


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    app.setApplicationName("Godot Image Validator")
    app.setApplicationVersion("1.0.0")

    # Create and show main window
    window = ImageValidatorUI()
    window.show()

    # Handle command line arguments
    if len(sys.argv) > 1:
        # Load images from command line
        image_paths = [Path(p) for p in sys.argv[1:]]
        window.load_images(image_paths)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
