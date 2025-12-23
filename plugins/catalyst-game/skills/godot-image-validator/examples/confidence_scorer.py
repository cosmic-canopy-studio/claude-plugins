#!/usr/bin/env python3
"""
Confidence Scorer for Godot Image Validator

This module provides confidence calculation and threshold management for image validation
results. It supports multi-aspect confidence scoring, configurable thresholds, and
custom validation rules.
"""

from dataclasses import dataclass
from typing import Dict, Any, List, Callable
from enum import Enum
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ValidationLevel(Enum):
    """Validation levels based on confidence scores"""

    AUTO_ACCEPT = "auto_accept"
    MANUAL_REVIEW_SUGGESTED = "manual_review_suggested"
    MANUAL_REVIEW_REQUIRED = "manual_review_required"
    ERROR = "error"


@dataclass
class ThresholdConfig:
    """Configuration for validation thresholds"""

    auto_accept: float = 0.85  # Minimum confidence for auto-accept
    manual_review_suggested: float = 0.60  # Minimum confidence for suggested review
    manual_review_required: float = 0.30  # Minimum confidence for required review
    error: float = 0.0  # Confidence threshold for errors

    def validate(self):
        """Validate threshold configuration"""
        if not (
            0.0
            <= self.error
            <= self.manual_review_required
            <= self.manual_review_suggested
            <= self.auto_accept
            <= 1.0
        ):
            raise ValueError(
                "Thresholds must be in ascending order: error <= manual_required <= manual_suggested <= auto_accept <= 1.0"
            )

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "auto_accept": self.auto_accept,
            "manual_review_suggested": self.manual_review_suggested,
            "manual_review_required": self.manual_review_required,
            "error": self.error,
        }


@dataclass
class AspectWeights:
    """Configuration for aspect weighting in confidence calculation"""

    content_match: float = 0.4  # Weight for content matching
    quality_assessment: float = 0.3  # Weight for quality assessment
    category_confidence: float = 0.2  # Weight for category confidence
    technical_analysis: float = 0.1  # Weight for technical analysis

    def validate(self):
        """Validate aspect weights"""
        total = (
            self.content_match
            + self.quality_assessment
            + self.category_confidence
            + self.technical_analysis
        )
        if not abs(total - 1.0) < 0.01:  # Allow small floating point errors
            raise ValueError(f"Aspect weights must sum to 1.0, got {total}")

    def to_dict(self) -> Dict[str, float]:
        """Convert to dictionary"""
        return {
            "content_match": self.content_match,
            "quality_assessment": self.quality_assessment,
            "category_confidence": self.category_confidence,
            "technical_analysis": self.technical_analysis,
        }


@dataclass
class ConfidenceBreakdown:
    """Detailed breakdown of confidence calculation"""

    overall_confidence: float
    aspect_scores: Dict[str, float]
    aspect_weights: Dict[str, float]
    weighted_contributions: Dict[str, float]
    validation_level: ValidationLevel
    status_color: str
    recommendations: List[str]


class ConfidenceScorer:
    """Manages confidence calculation and threshold decisions"""

    def __init__(
        self,
        thresholds: ThresholdConfig = None,
        weights: AspectWeights = None,
        debug_mode: bool = False,
    ):
        """
        Initialize confidence scorer

        Args:
            thresholds: Configuration for validation thresholds
            weights: Configuration for aspect weightings
            debug_mode: Enable debug logging
        """
        self.thresholds = thresholds or ThresholdConfig()
        self.weights = weights or AspectWeights()
        self.debug_mode = debug_mode

        if debug_mode:
            logger.setLevel(logging.DEBUG)

        # Validate configurations
        self.thresholds.validate()
        self.weights.validate()

        # Custom rules engine
        self.custom_rules: Dict[str, Callable] = {}

    def calculate_confidence(self, analysis_result: Dict[str, Any]) -> float:
        """
        Calculate overall confidence from multi-aspect analysis

        Args:
            analysis_result: Dictionary containing aspect scores (0.0-1.0)

        Returns:
            float: Overall confidence score (0.0-1.0)
        """
        # Extract aspect scores with defaults
        content_match = self._extract_aspect_score(analysis_result, "content_match")
        quality_assessment = self._extract_aspect_score(
            analysis_result, "quality_assessment"
        )
        category_confidence = self._extract_aspect_score(
            analysis_result, "category_confidence"
        )
        technical_analysis = self._extract_aspect_score(
            analysis_result, "technical_analysis"
        )

        # Calculate weighted sum
        overall_confidence = (
            content_match * self.weights.content_match
            + quality_assessment * self.weights.quality_assessment
            + category_confidence * self.weights.category_confidence
            + technical_analysis * self.weights.technical_analysis
        )

        # Ensure result is within valid range
        confidence = max(0.0, min(1.0, overall_confidence))

        if self.debug_mode:
            aspect_scores = {
                "content_match": content_match,
                "quality_assessment": quality_assessment,
                "category_confidence": category_confidence,
                "technical_analysis": technical_analysis,
            }
            logger.debug("Confidence calculation:")
            logger.debug(f"  Aspect scores: {aspect_scores}")
            logger.debug(f"  Weights: {self.weights.to_dict()}")
            logger.debug(f"  Overall confidence: {confidence:.3f}")

        return confidence

    def get_detailed_breakdown(
        self, analysis_result: Dict[str, Any]
    ) -> ConfidenceBreakdown:
        """
        Get detailed breakdown of confidence calculation

        Args:
            analysis_result: Dictionary containing aspect scores

        Returns:
            ConfidenceBreakdown: Detailed confidence analysis
        """
        # Extract aspect scores
        content_match = self._extract_aspect_score(analysis_result, "content_match")
        quality_assessment = self._extract_aspect_score(
            analysis_result, "quality_assessment"
        )
        category_confidence = self._extract_aspect_score(
            analysis_result, "category_confidence"
        )
        technical_analysis = self._extract_aspect_score(
            analysis_result, "technical_analysis"
        )

        aspect_scores = {
            "content_match": content_match,
            "quality_assessment": quality_assessment,
            "category_confidence": category_confidence,
            "technical_analysis": technical_analysis,
        }

        # Calculate weighted contributions
        weights_dict = self.weights.to_dict()
        weighted_contributions = {
            aspect: score * weights_dict[aspect]
            for aspect, score in aspect_scores.items()
        }

        # Calculate overall confidence
        overall_confidence = sum(weighted_contributions.values())

        # Determine validation level
        validation_level = self.get_validation_level(overall_confidence)

        # Get status color
        status_color = self.get_status_color(validation_level)

        # Generate recommendations
        recommendations = self._generate_recommendations(
            aspect_scores, overall_confidence
        )

        return ConfidenceBreakdown(
            overall_confidence=overall_confidence,
            aspect_scores=aspect_scores,
            aspect_weights=weights_dict,
            weighted_contributions=weighted_contributions,
            validation_level=validation_level,
            status_color=status_color,
            recommendations=recommendations,
        )

    def get_validation_level(self, confidence: float) -> ValidationLevel:
        """
        Determine validation level based on confidence score

        Args:
            confidence: Confidence score (0.0-1.0)

        Returns:
            ValidationLevel: Corresponding validation level
        """
        if confidence >= self.thresholds.auto_accept:
            return ValidationLevel.AUTO_ACCEPT
        elif confidence >= self.thresholds.manual_review_suggested:
            return ValidationLevel.MANUAL_REVIEW_SUGGESTED
        elif confidence >= self.thresholds.manual_review_required:
            return ValidationLevel.MANUAL_REVIEW_REQUIRED
        else:
            return ValidationLevel.ERROR

    def should_require_manual_review(self, confidence: float) -> bool:
        """
        Check if manual review is required for given confidence

        Args:
            confidence: Confidence score (0.0-1.0)

        Returns:
            bool: True if manual review is required
        """
        return confidence < self.thresholds.auto_accept

    def get_status_color(self, validation_level: ValidationLevel) -> str:
        """
        Get color code for validation level

        Args:
            validation_level: The validation level

        Returns:
            str: Hex color code
        """
        color_map = {
            ValidationLevel.AUTO_ACCEPT: "#4CAF50",  # Green
            ValidationLevel.MANUAL_REVIEW_SUGGESTED: "#FFC107",  # Yellow
            ValidationLevel.MANUAL_REVIEW_REQUIRED: "#FF9800",  # Orange
            ValidationLevel.ERROR: "#F44336",  # Red
        }
        return color_map.get(validation_level, "#9E9E9E")  # Gray default

    def apply_custom_rules(
        self, image_path: Path, analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Apply custom validation rules to adjust confidence

        Args:
            image_path: Path to the image file
            analysis_result: Original analysis result

        Returns:
            Dict[str, Any]: Modified analysis result with custom rule adjustments
        """
        modified_result = analysis_result.copy()

        for rule_name, rule_func in self.custom_rules.items():
            try:
                if self.debug_mode:
                    logger.debug(f"Applying custom rule: {rule_name}")

                rule_result = rule_func(image_path, analysis_result)

                # Apply rule adjustments
                if isinstance(rule_result, dict):
                    if "confidence_adjustment" in rule_result:
                        current_confidence = modified_result.get("confidence", 0.0)
                        adjustment = rule_result["confidence_adjustment"]
                        modified_result["confidence"] = max(
                            0.0, min(1.0, current_confidence + adjustment)
                        )

                    if "issues" in rule_result:
                        if "issues" not in modified_result:
                            modified_result["issues"] = []
                        modified_result["issues"].extend(rule_result["issues"])

                    if "categories" in rule_result:
                        modified_result["categories"] = rule_result["categories"]

                if self.debug_mode:
                    logger.debug(f"Rule {rule_name} result: {rule_result}")

            except Exception as e:
                logger.error(f"Custom rule {rule_name} failed: {e}")

        return modified_result

    def add_custom_rule(self, name: str, rule_func: Callable):
        """
        Add a custom validation rule

        Args:
            name: Rule name/identifier
            rule_func: Function that takes (image_path, analysis_result) and returns modifications
        """
        self.custom_rules[name] = rule_func
        logger.info(f"Added custom rule: {name}")

    def remove_custom_rule(self, name: str):
        """
        Remove a custom validation rule

        Args:
            name: Rule name/identifier
        """
        if name in self.custom_rules:
            del self.custom_rules[name]
            logger.info(f"Removed custom rule: {name}")

    def get_custom_rules(self) -> List[str]:
        """
        Get list of custom rule names

        Returns:
            List[str]: List of custom rule names
        """
        return list(self.custom_rules.keys())

    def _extract_aspect_score(
        self, analysis_result: Dict[str, Any], aspect: str
    ) -> float:
        """Extract aspect score with validation"""
        score = analysis_result.get(aspect, 0.0)

        # Validate score range
        if not isinstance(score, (int, float)):
            logger.warning(f"Invalid score type for {aspect}: {type(score)}")
            return 0.0

        if score < 0.0 or score > 1.0:
            logger.warning(f"Score out of range for {aspect}: {score}")
            return max(0.0, min(1.0, score))

        return float(score)

    def _generate_recommendations(
        self, aspect_scores: Dict[str, float], overall_confidence: float
    ) -> List[str]:
        """Generate recommendations based on aspect scores"""
        recommendations = []

        # Content match recommendations
        if aspect_scores["content_match"] < 0.7:
            recommendations.append("Consider improving content clarity or resolution")

        # Quality assessment recommendations
        if aspect_scores["quality_assessment"] < 0.6:
            recommendations.append(
                "Image quality may need improvement (compression, artifacts, etc.)"
            )

        # Category confidence recommendations
        if aspect_scores["category_confidence"] < 0.5:
            recommendations.append(
                "Image category is unclear, consider manual classification"
            )

        # Technical analysis recommendations
        if aspect_scores["technical_analysis"] < 0.6:
            recommendations.append(
                "Technical aspects may need attention (format, size, etc.)"
            )

        # Overall recommendations
        if overall_confidence < 0.5:
            recommendations.append(
                "Manual review strongly recommended due to low overall confidence"
            )
        elif overall_confidence < 0.8:
            recommendations.append("Consider manual review for quality assurance")

        if not recommendations:
            recommendations.append("Image meets quality standards")

        return recommendations

    def update_thresholds(self, **kwargs):
        """
        Update threshold values

        Args:
            **kwargs: Threshold values to update
        """
        for key, value in kwargs.items():
            if hasattr(self.thresholds, key):
                setattr(self.thresholds, key, value)
                logger.info(f"Updated threshold {key} to {value}")
            else:
                logger.warning(f"Unknown threshold: {key}")

        # Validate updated thresholds
        self.thresholds.validate()

    def update_weights(self, **kwargs):
        """
        Update aspect weights

        Args:
            **kwargs: Weight values to update
        """
        for key, value in kwargs.items():
            if hasattr(self.weights, key):
                setattr(self.weights, key, value)
                logger.info(f"Updated weight {key} to {value}")
            else:
                logger.warning(f"Unknown weight: {key}")

        # Validate updated weights
        self.weights.validate()

    def export_config(self) -> Dict[str, Any]:
        """
        Export current configuration

        Returns:
            Dict[str, Any]: Configuration dictionary
        """
        return {
            "thresholds": self.thresholds.to_dict(),
            "weights": self.weights.to_dict(),
            "custom_rules": self.get_custom_rules(),
        }

    def import_config(self, config: Dict[str, Any]):
        """
        Import configuration from dictionary

        Args:
            config: Configuration dictionary
        """
        if "thresholds" in config:
            self.thresholds = ThresholdConfig(**config["thresholds"])
            self.thresholds.validate()

        if "weights" in config:
            self.weights = AspectWeights(**config["weights"])
            self.weights.validate()

        logger.info("Configuration imported successfully")


# Predefined rule factories
def create_pixel_art_rule(min_size_multiple: int = 4) -> Callable:
    """Create rule for pixel art validation"""

    def validate_pixel_art(
        image_path: Path, analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            from PIL import Image

            with Image.open(image_path) as img:
                width, height = img.size

            # Pixel art should have dimensions divisible by specified value
            if width % min_size_multiple != 0 or height % min_size_multiple != 0:
                return {
                    "confidence_adjustment": -0.2,
                    "issues": [
                        f"Pixel dimensions {width}x{height} not divisible by {min_size_multiple}"
                    ],
                }

            return {
                "confidence_adjustment": 0.1
            }  # Bonus for proper pixel art dimensions

        except Exception:
            return {"confidence_adjustment": 0.0}  # No adjustment if can't analyze

    return validate_pixel_art


def create_hd_asset_rule(min_resolution: int = 1024) -> Callable:
    """Create rule for HD asset validation"""

    def validate_hd_asset(
        image_path: Path, analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            from PIL import Image

            with Image.open(image_path) as img:
                width, height = img.size

            min_dimension = min(width, height)

            if min_dimension < min_resolution:
                return {
                    "confidence_adjustment": -0.3,
                    "issues": [
                        f"Minimum dimension {min_dimension} below required {min_resolution}"
                    ],
                }

            return {"confidence_adjustment": 0.1}  # Bonus for meeting HD requirements

        except Exception:
            return {"confidence_adjustment": 0.0}

    return validate_hd_asset


def create_file_size_rule(max_size_mb: int = 10) -> Callable:
    """Create rule for file size validation"""

    def validate_file_size(
        image_path: Path, analysis_result: Dict[str, Any]
    ) -> Dict[str, Any]:
        try:
            file_size_bytes = image_path.stat().st_size
            file_size_mb = file_size_bytes / (1024 * 1024)

            if file_size_mb > max_size_mb:
                return {
                    "confidence_adjustment": -0.1 * (file_size_mb / max_size_mb - 1),
                    "issues": [
                        f"Large file size: {file_size_mb:.1f}MB (recommended < {max_size_mb}MB)"
                    ],
                }

            return {"confidence_adjustment": 0.0}

        except Exception:
            return {"confidence_adjustment": 0.0}

    return validate_file_size


# Example usage
async def main():
    """Example usage of confidence scorer"""
    print("Confidence Scorer Example\n")

    # Create scorer with custom thresholds
    thresholds = ThresholdConfig(
        auto_accept=0.9,  # Stricter auto-accept
        manual_review_suggested=0.7,
        manual_review_required=0.4,
        error=0.1,
    )

    weights = AspectWeights(
        content_match=0.5,  # Emphasize content matching
        quality_assessment=0.3,
        category_confidence=0.15,
        technical_analysis=0.05,
    )

    scorer = ConfidenceScorer(thresholds, weights, debug_mode=True)

    # Add custom rules
    scorer.add_custom_rule("pixel_art", create_pixel_art_rule(4))
    scorer.add_custom_rule("hd_asset", create_hd_asset_rule(1024))
    scorer.add_custom_rule("file_size", create_file_size_rule(5))

    # Test with sample analysis results
    test_cases = [
        {
            "name": "High confidence animation",
            "data": {
                "content_match": 0.95,
                "quality_assessment": 0.9,
                "category_confidence": 0.88,
                "technical_analysis": 0.92,
            },
        },
        {
            "name": "Medium confidence UI element",
            "data": {
                "content_match": 0.7,
                "quality_assessment": 0.6,
                "category_confidence": 0.5,
                "technical_analysis": 0.8,
            },
        },
        {
            "name": "Low confidence asset",
            "data": {
                "content_match": 0.4,
                "quality_assessment": 0.3,
                "category_confidence": 0.2,
                "technical_analysis": 0.5,
            },
        },
    ]

    for test_case in test_cases:
        print(f"\n{test_case['name']}:")
        analysis_data = test_case["data"]

        # Calculate confidence
        confidence = scorer.calculate_confidence(analysis_data)
        validation_level = scorer.get_validation_level(confidence)
        color = scorer.get_status_color(validation_level)

        # Get detailed breakdown
        breakdown = scorer.get_detailed_breakdown(analysis_data)

        print(f"  Overall Confidence: {confidence:.3f}")
        print(f"  Validation Level: {validation_level.value}")
        print(f"  Status Color: {color}")
        print(f"  Aspect Scores: {breakdown.aspect_scores}")
        print(f"  Weighted Contributions: {breakdown.weighted_contributions}")
        print(f"  Recommendations: {breakdown.recommendations}")

    # Test custom rules
    print(f"\nCustom Rules: {scorer.get_custom_rules()}")

    # Export configuration
    config = scorer.export_config()
    print(f"\nConfiguration: {config}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
