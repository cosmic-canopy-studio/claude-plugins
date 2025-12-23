#!/usr/bin/env python3
"""
Quality gate reminder hook.
Runs on PostToolUse to remind about verification.
"""

import sys
import os
import json

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from state import load_state, save_state

# Tools that should trigger verification reminders
EDIT_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
BASH_BUILD_PATTERNS = ["npm run build", "npm test", "make", "pytest", "cargo"]


def main():
    """Remind about verification after edits."""
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    state = load_state()

    # Track edits that need verification
    if tool_name in EDIT_TOOLS:
        file_path = tool_input.get("file_path", "unknown")

        # Add to pending verification list
        pending = state.get("pending_verification", [])
        if file_path not in pending:
            pending.append(file_path)
            state["pending_verification"] = pending[-10:]  # Keep last 10
            save_state(state)

    # Check if verification just happened
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        is_verification = any(p in command for p in BASH_BUILD_PATTERNS)

        if is_verification:
            # Clear pending verification
            state["pending_verification"] = []
            save_state(state)

    # Remind if many edits without verification
    pending = state.get("pending_verification", [])
    if len(pending) >= 5:
        print(
            f"ℹ️  {len(pending)} files edited without verification. "
            "Consider running tests/build.",
            file=sys.stderr,
        )

    sys.exit(0)


if __name__ == "__main__":
    main()
