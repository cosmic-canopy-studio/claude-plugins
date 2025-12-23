#!/usr/bin/env python3
"""
MCP Client for Godot Image Validator

This module provides client functionality for interacting with Model Context Protocol (MCP)
servers for AI-powered image analysis. It handles retry logic, error handling, and fallback
mechanisms for robust operation.
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
import time

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class AnalysisResult:
    """Result from MCP image analysis"""

    success: bool
    confidence: float
    categories: List[str]
    issues: List[str]
    metadata: Dict[str, Any]
    error_message: Optional[str] = None
    processing_time: float = 0.0

    @classmethod
    def fallback_result(cls, image_path: Path, error_message: str) -> "AnalysisResult":
        """Create a fallback result for failed analysis"""
        return cls(
            success=False,
            confidence=0.0,
            categories=["other"],
            issues=[f"Analysis failed: {error_message}"],
            metadata={
                "fallback": True,
                "image_path": str(image_path),
                "error_type": "fallback",
            },
            error_message=error_message,
        )

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for JSON serialization"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AnalysisResult":
        """Create from dictionary"""
        return cls(**data)


class MCPClient:
    """Client for MCP image analysis tools"""

    def __init__(
        self,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 2.0,
        debug_mode: bool = False,
    ):
        """
        Initialize MCP client

        Args:
            timeout: Request timeout in seconds
            max_retries: Maximum number of retry attempts
            retry_delay: Initial delay between retries (seconds)
            debug_mode: Enable debug logging
        """
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.debug_mode = debug_mode

        if debug_mode:
            logger.setLevel(logging.DEBUG)

        # Track statistics
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "retry_attempts": 0,
            "fallback_used": 0,
        }

    async def analyze_image(
        self,
        image_path: Path,
        categories: List[str] = None,
        analysis_prompt: str = None,
    ) -> AnalysisResult:
        """
        Analyze image using MCP tools

        Args:
            image_path: Path to the image file
            categories: List of categories to analyze
            analysis_prompt: Custom prompt for analysis

        Returns:
            AnalysisResult: Analysis results with confidence scoring

        Raises:
            FileNotFoundError: If image file doesn't exist
            ValueError: If image format is not supported
        """
        start_time = time.time()
        self.stats["total_requests"] += 1

        if not image_path.exists():
            error_msg = f"Image file not found: {image_path}"
            logger.error(error_msg)
            self.stats["failed_requests"] += 1
            return AnalysisResult.fallback_result(image_path, error_msg)

        if not self._is_supported_format(image_path):
            error_msg = f"Unsupported image format: {image_path.suffix}"
            logger.error(error_msg)
            self.stats["failed_requests"] += 1
            return AnalysisResult.fallback_result(image_path, error_msg)

        if categories is None:
            categories = ["animations", "environments", "ui_elements", "effects"]

        if analysis_prompt is None:
            analysis_prompt = self._build_default_prompt(categories)

        try:
            # Primary analysis using MCP tool
            result = await self._call_analyze_image_tool(
                image_path, categories, analysis_prompt
            )

            if not result.success:
                # Retry with exponential backoff
                logger.warning(
                    f"Primary analysis failed for {image_path.name}, attempting retry"
                )
                result = await self._retry_analysis(
                    image_path, categories, analysis_prompt
                )

            processing_time = time.time() - start_time
            result.processing_time = processing_time

            if result.success:
                self.stats["successful_requests"] += 1
                logger.info(
                    f"Analysis completed for {image_path.name} in {processing_time:.2f}s"
                )
            else:
                self.stats["failed_requests"] += 1
                logger.warning(f"Analysis failed for {image_path.name}")

            return result

        except Exception as e:
            error_msg = f"Unexpected error during analysis: {e}"
            logger.error(f"Error analyzing {image_path}: {e}")
            self.stats["failed_requests"] += 1

            processing_time = time.time() - start_time
            return AnalysisResult.fallback_result(image_path, error_msg)

    async def _call_analyze_image_tool(
        self, image_path: Path, categories: List[str], prompt: str
    ) -> AnalysisResult:
        """
        Call the primary MCP analyze_image tool

        This is where the actual MCP tool integration would happen.
        For demonstration purposes, this includes a mock implementation.
        """
        try:
            if self.debug_mode:
                logger.debug(f"Calling MCP analyze_image for {image_path.name}")
                logger.debug(f"Categories: {categories}")
                logger.debug(f"Prompt: {prompt}")

            # TODO: Replace with actual MCP tool call
            # result = await mcp__zai_mcp_server__analyze_image(
            #     image_source=str(image_path),
            #     prompt=prompt,
            #     output_format="json"
            # )

            # Mock implementation for demonstration
            await asyncio.sleep(0.5)  # Simulate network call

            # Generate mock results based on file name and content
            mock_result = await self._generate_mock_analysis(image_path, categories)

            if self.debug_mode:
                logger.debug(f"MCP tool result: {mock_result}")

            return mock_result

        except Exception as e:
            logger.error(f"MCP tool call failed: {e}")
            return AnalysisResult.fallback_result(image_path, f"MCP tool error: {e}")

    async def _retry_analysis(
        self, image_path: Path, categories: List[str], prompt: str
    ) -> AnalysisResult:
        """
        Retry analysis with exponential backoff
        """
        for attempt in range(self.max_retries):
            try:
                delay = self.retry_delay * (2**attempt)
                logger.info(
                    f"Retry attempt {attempt + 1}/{self.max_retries} for {image_path.name} after {delay:.1f}s delay"
                )

                await asyncio.sleep(delay)

                # Try primary tool again
                result = await self._call_analyze_image_tool(
                    image_path, categories, prompt
                )
                if result.success:
                    self.stats["retry_attempts"] += attempt + 1
                    return result

                # Try fallback tool on last retry
                if attempt == self.max_retries - 1:
                    logger.info(f"Trying fallback tool for {image_path.name}")
                    result = await self._call_fallback_tool(
                        image_path, categories, prompt
                    )
                    if result.success:
                        self.stats["fallback_used"] += 1
                        return result

            except Exception as e:
                logger.warning(f"Retry {attempt + 1} failed for {image_path.name}: {e}")
                continue

        # All retries failed
        error_msg = f"All {self.max_retries} retry attempts failed"
        return AnalysisResult.fallback_result(image_path, error_msg)

    async def _call_fallback_tool(
        self, image_path: Path, categories: List[str], prompt: str
    ) -> AnalysisResult:
        """
        Call fallback MCP tool (4_5v_mcp for remote URLs)
        """
        try:
            if self.debug_mode:
                logger.debug(f"Calling fallback MCP tool for {image_path.name}")

            # TODO: Replace with actual fallback MCP tool call
            # result = await mcp__4_5v_mcp__analyze_image(
            #     imageSource=str(image_path),
            #     prompt=prompt
            # )

            # Mock fallback implementation
            await asyncio.sleep(0.3)

            # Fallback gives lower confidence but still provides analysis
            mock_result = await self._generate_mock_analysis(
                image_path, categories, confidence_modifier=0.1
            )

            if self.debug_mode:
                logger.debug(f"Fallback tool result: {mock_result}")

            return mock_result

        except Exception as e:
            logger.error(f"Fallback tool call failed: {e}")
            return AnalysisResult.fallback_result(
                image_path, f"Fallback tool error: {e}"
            )

    async def _generate_mock_analysis(
        self, image_path: Path, categories: List[str], confidence_modifier: float = 0.0
    ) -> AnalysisResult:
        """
        Generate mock analysis results for demonstration
        """
        import hashlib

        # Generate deterministic but varied results based on file hash
        file_hash = hashlib.md5(str(image_path).encode()).hexdigest()
        hash_int = int(file_hash[:8], 16)

        # Select category based on hash
        category_index = hash_int % len(categories)
        primary_category = categories[category_index]

        # Generate confidence based on file characteristics
        base_confidence = 0.5 + (hash_int % 50) / 100.0
        confidence = min(1.0, base_confidence + confidence_modifier)

        # Generate mock issues based on file characteristics
        issues = []
        file_size = image_path.stat().st_size if image_path.exists() else 0

        if file_size > 10 * 1024 * 1024:  # > 10MB
            issues.append("Large file size may impact performance")
        elif file_size < 1024:  # < 1KB
            issues.append("Very small file size, may be low quality")

        if "texture" in image_path.name.lower() and image_path.suffix.lower() != ".png":
            issues.append("Texture should use PNG format for better quality")

        if "ui" in image_path.name.lower() and confidence < 0.7:
            issues.append("UI element may need higher resolution")

        metadata = {
            "file_size": file_size,
            "file_extension": image_path.suffix,
            "analysis_timestamp": time.time(),
            "mock_analysis": True,
            "hash_seed": hash_int,
        }

        return AnalysisResult(
            success=True,
            confidence=confidence,
            categories=[primary_category],
            issues=issues,
            metadata=metadata,
        )

    def _build_default_prompt(self, categories: List[str]) -> str:
        """Build default analysis prompt"""
        categories_str = ", ".join(categories)
        return f"""Analyze this game asset image and classify it into one of these categories: {categories_str}.

Provide:
1. Primary category classification
2. Confidence score (0.0-1.0) for the classification
3. Any quality issues or recommendations
4. Technical analysis of the image properties

Focus on game development context and asset quality standards."""

    def _is_supported_format(self, image_path: Path) -> bool:
        """Check if image format is supported"""
        supported_formats = {
            ".png",
            ".jpg",
            ".jpeg",
            ".webp",
            ".svg",
            ".exr",
            ".tga",
            ".bmp",
            ".tiff",
            ".tif",
        }
        return image_path.suffix.lower() in supported_formats

    def get_statistics(self) -> Dict[str, Any]:
        """Get client usage statistics"""
        if self.stats["total_requests"] > 0:
            success_rate = (
                self.stats["successful_requests"] / self.stats["total_requests"]
            ) * 100
        else:
            success_rate = 0.0

        return {**self.stats, "success_rate_percent": round(success_rate, 2)}

    def reset_statistics(self):
        """Reset usage statistics"""
        self.stats = {
            "total_requests": 0,
            "successful_requests": 0,
            "failed_requests": 0,
            "retry_attempts": 0,
            "fallback_used": 0,
        }


# Example usage and testing
async def main():
    """Example usage of MCP client"""
    client = MCPClient(debug_mode=True)

    # Test with some sample images
    test_images = [
        Path("test_assets/player_sprite.png"),
        Path("test_assets/background.jpg"),
        Path("test_assets/ui_button.png"),
        Path("test_assets/particle_effect.png"),
    ]

    print("Starting image analysis with MCP client...\n")

    for image_path in test_images:
        if image_path.exists():
            print(f"Analyzing: {image_path.name}")
            result = await client.analyze_image(
                image_path,
                categories=["animations", "environments", "ui_elements", "effects"],
            )

            print(f"  Success: {result.success}")
            print(f"  Confidence: {result.confidence:.2%}")
            print(f"  Categories: {result.categories}")
            if result.issues:
                print(f"  Issues: {result.issues}")
            print(f"  Processing Time: {result.processing_time:.2f}s")
            print()
        else:
            print(f"Skipping {image_path.name} (file not found)")

    # Print statistics
    stats = client.get_statistics()
    print("Analysis Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")


if __name__ == "__main__":
    # Create test directory if it doesn't exist
    test_dir = Path("test_assets")
    test_dir.mkdir(exist_ok=True)

    # Run example
    asyncio.run(main())
