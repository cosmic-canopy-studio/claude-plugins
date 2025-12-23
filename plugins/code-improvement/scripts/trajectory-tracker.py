#!/usr/bin/env python3
"""
Trajectory tracking hook.
Runs on Stop to detect failure loops.
"""

import sys
import os
import json

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from state import load_state, save_state, log_learning


def main():
    """Track trajectory and detect failure patterns."""
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)

    stop_reason = hook_input.get("stop_reason", "")

    state = load_state()

    # Track consecutive failures
    if stop_reason in ("error", "tool_error", "user_interrupt"):
        state["consecutive_failures"] = state.get("consecutive_failures", 0) + 1
    else:
        # Reset on success
        state["consecutive_failures"] = 0

    save_state(state)

    # Warn on bad trajectory
    failures = state["consecutive_failures"]

    if failures >= 3:
        print(
            "⚠️  Bad trajectory detected: 3+ consecutive failures. "
            "Consider resetting context with /create_handoff.",
            file=sys.stderr,
        )
        # Log for learning
        log_learning(
            {
                "type": "trajectory_warning",
                "failures": failures,
                "stop_reason": stop_reason,
            }
        )

    if failures >= 5:
        print(
            "🛑 CRITICAL: 5+ failures. Fresh context strongly recommended. "
            "Model may be in failure loop.",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
