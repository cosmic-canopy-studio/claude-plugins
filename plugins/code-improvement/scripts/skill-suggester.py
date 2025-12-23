#!/usr/bin/env python3
"""
Skill suggestion hook.
Runs on SessionEnd to suggest skills based on patterns.
"""

import sys
import os
from collections import Counter

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from state import load_state, log_learning


def analyze_patterns(patterns: list) -> list:
    """Analyze tool patterns for skill opportunities."""
    suggestions = []

    # Count tool sequences
    tool_sequence = [p.get("tool", "") for p in patterns]

    # Find repeated sequences (potential workflow candidates)
    for i in range(len(tool_sequence) - 2):
        seq = tuple(tool_sequence[i : i + 3])
        # Track 3-tool sequences
        if seq not in [s.get("sequence") for s in suggestions]:
            count = sum(
                1
                for j in range(len(tool_sequence) - 2)
                if tuple(tool_sequence[j : j + 3]) == seq
            )
            if count >= 3:
                suggestions.append(
                    {"type": "workflow", "sequence": seq, "count": count}
                )

    # Find repeated file accesses (potential component focus)
    files = [p.get("file", "") for p in patterns if p.get("file")]
    file_counts = Counter(files)
    for file_path, count in file_counts.most_common(3):
        if count >= 5:
            suggestions.append(
                {"type": "focus_area", "file": file_path, "count": count}
            )

    return suggestions


def main():
    """Suggest skills based on session patterns."""
    state = load_state()

    patterns = state.get("tool_patterns", [])

    if len(patterns) < 10:
        # Not enough data for suggestions
        sys.exit(0)

    suggestions = analyze_patterns(patterns)

    if suggestions:
        print("\n📊 Session Analysis:", file=sys.stderr)

        for s in suggestions[:3]:  # Top 3 suggestions
            if s["type"] == "workflow":
                seq = " → ".join(s["sequence"])
                print(
                    f"  • Workflow pattern ({s['count']}x): {seq}",
                    file=sys.stderr,
                )
            elif s["type"] == "focus_area":
                print(
                    f"  • Focus area ({s['count']}x): {s['file']}",
                    file=sys.stderr,
                )

        print(
            "\nConsider running /analyze-skill-gaps for detailed recommendations.",
            file=sys.stderr,
        )

        # Log for persistent learning
        log_learning(
            {
                "type": "session_suggestions",
                "suggestions": suggestions,
                "tool_count": state.get("tool_count", 0),
            }
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
