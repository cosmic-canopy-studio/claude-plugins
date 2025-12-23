#!/usr/bin/env python3
"""
Context monitoring hook.
Runs on PostToolUse to track context usage.
"""

import sys
import os
import json

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from state import load_state, save_state
from context_estimator import (
    estimate_tool_output_tokens,
    calculate_context_status,
    get_recommendation,
)


def main():
    """Monitor context usage after tool execution."""
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)  # Allow operation if input is malformed

    tool_name = hook_input.get("tool_name", "")
    tool_output = hook_input.get("tool_output", "")

    # Update state
    state = load_state()

    # Increment tool count
    state["tool_count"] = state.get("tool_count", 0) + 1

    # Estimate tokens from this tool output
    output_tokens = estimate_tool_output_tokens(tool_name, str(tool_output))
    state["estimated_tokens"] = state.get("estimated_tokens", 3000) + output_tokens
    state["last_tool"] = tool_name

    save_state(state)

    # Check thresholds and warn if needed
    status = calculate_context_status(state["estimated_tokens"])

    if status["critical"]:
        print(f"⚠️  CRITICAL: {get_recommendation(status)}", file=sys.stderr)
    elif status["zone"] == "orange":
        # Only warn once per zone transition
        if "orange_warned" not in state.get("warnings_issued", []):
            print(f"⚠️  {get_recommendation(status)}", file=sys.stderr)
            state["warnings_issued"] = state.get("warnings_issued", []) + [
                "orange_warned"
            ]
            save_state(state)
    elif status["zone"] == "yellow":
        if "yellow_warned" not in state.get("warnings_issued", []):
            print(f"ℹ️  {get_recommendation(status)}", file=sys.stderr)
            state["warnings_issued"] = state.get("warnings_issued", []) + [
                "yellow_warned"
            ]
            save_state(state)

    sys.exit(0)  # Always allow operation


if __name__ == "__main__":
    main()
