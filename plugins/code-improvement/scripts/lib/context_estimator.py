#!/usr/bin/env python3
"""
Context window estimation utilities.
"""

from typing import Dict, Any


# Token estimation ratios
TOKENS_PER_WORD = {
    "prose": 1.33,
    "technical": 1.54,
    "code": 2.0,
    "json": 2.5,
}

# Thresholds (percentage of 200K context)
THRESHOLDS = {
    "green": 35,
    "yellow": 50,
    "orange": 60,
    "red": 100,
}


def estimate_tokens(content: str, content_type: str = "prose") -> int:
    """Estimate tokens for given content."""
    words = len(content.split())
    ratio = TOKENS_PER_WORD.get(content_type, 1.33)
    return int(words * ratio)


def estimate_tool_output_tokens(tool_name: str, output: str) -> int:
    """Estimate tokens for tool output based on tool type."""
    # Code-heavy tools get higher ratio
    code_tools = {"Read", "Grep", "Glob", "Bash", "LSP"}
    content_type = "code" if tool_name in code_tools else "prose"
    return estimate_tokens(output, content_type)


def get_zone(percentage: float) -> str:
    """Get context zone based on percentage."""
    if percentage < THRESHOLDS["green"]:
        return "green"
    elif percentage < THRESHOLDS["yellow"]:
        return "yellow"
    elif percentage < THRESHOLDS["orange"]:
        return "orange"
    else:
        return "red"


def get_zone_emoji(zone: str) -> str:
    """Get emoji for zone."""
    return {
        "green": "🟢",
        "yellow": "🟡",
        "orange": "🟠",
        "red": "🔴",
    }.get(zone, "⚪")


def calculate_context_status(
    estimated_tokens: int, context_window: int = 200_000
) -> Dict[str, Any]:
    """Calculate full context status."""
    percentage = (estimated_tokens / context_window) * 100
    zone = get_zone(percentage)

    return {
        "tokens": estimated_tokens,
        "percentage": round(percentage, 1),
        "zone": zone,
        "emoji": get_zone_emoji(zone),
        "remaining": context_window - estimated_tokens,
        "warning": zone in ("yellow", "orange", "red"),
        "critical": zone == "red",
    }


def get_recommendation(status: Dict[str, Any]) -> str:
    """Get recommendation based on context status."""
    zone = status["zone"]

    if zone == "green":
        return "Context healthy. Continue normally."
    elif zone == "yellow":
        return "Context approaching limit. Consider task batching."
    elif zone == "orange":
        return "Context warning. Recommend compacting or handoff."
    else:
        return "CRITICAL: Context near limit. Create handoff and reset."


def format_status_line(
    estimated_tokens: int, tool_count: int, context_window: int = 200_000
) -> str:
    """Format status line for display."""
    status = calculate_context_status(estimated_tokens, context_window)
    return (
        f"{status['emoji']} Context: {status['percentage']:.0f}% "
        f"({estimated_tokens // 1000}K/{context_window // 1000}K) | "
        f"Tools: {tool_count}"
    )
