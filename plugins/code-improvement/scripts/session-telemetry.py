#!/usr/bin/env python3
"""
Session telemetry hook.
Runs on PostToolUse to log patterns for learning.
"""

import sys
import os
import json

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from state import load_state, append_to_list, log_learning


def main():
    """Log telemetry for pattern detection."""
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Track tool usage patterns
    state = load_state()

    # Build pattern record
    pattern = {
        "tool": tool_name,
        "input_keys": list(tool_input.keys()) if isinstance(tool_input, dict) else [],
    }

    # Add file context if available
    if isinstance(tool_input, dict):
        if "file_path" in tool_input:
            pattern["file"] = tool_input["file_path"]
        if "pattern" in tool_input:
            pattern["search_pattern"] = tool_input["pattern"]

    # Append to session patterns
    append_to_list("tool_patterns", pattern)

    # Log for persistent learning (sampled - every 10th call)
    if state.get("tool_count", 0) % 10 == 0:
        log_learning(
            {
                "type": "tool_usage",
                "tool": tool_name,
                "session_tool_count": state.get("tool_count", 0),
            }
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
