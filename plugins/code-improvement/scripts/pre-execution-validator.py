#!/usr/bin/env python3
"""
Pre-execution validation hook.
Runs on PreToolUse to validate tool parameters.
"""

import sys
import os
import json
import re

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))


# Patterns that should be blocked or warned
DANGEROUS_PATTERNS = [
    (r"rm\s+-rf\s+/(?!\S)", "Dangerous: rm -rf / detected"),
    (r"rm\s+-rf\s+~", "Dangerous: rm -rf ~ detected"),
    (r"rm\s+-rf\s+\$HOME", "Dangerous: rm -rf $HOME detected"),
]

# Secret patterns to check in file writes
SECRET_PATTERNS = [
    (r"api[_-]?key\s*[:=]\s*['\"][^'\"]{20,}['\"]", "Potential API key"),
    (r"sk-[a-zA-Z0-9]{48}", "OpenAI API key"),
    (r"ghp_[a-zA-Z0-9]{36}", "GitHub token"),
    (r"AKIA[0-9A-Z]{16}", "AWS access key"),
]


def validate_bash(command: str) -> tuple:
    """Validate bash command."""
    for pattern, message in DANGEROUS_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            return False, message
    return True, ""


def validate_write(content: str, file_path: str) -> tuple:
    """Validate file write content."""
    # Check for secrets
    for pattern, secret_type in SECRET_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            # Warn but don't block
            print(f"⚠️  Warning: {secret_type} detected in {file_path}", file=sys.stderr)

    # Block writes to sensitive files
    sensitive_files = [".env", "credentials", "secrets", ".npmrc", ".pypirc"]
    if any(s in file_path.lower() for s in sensitive_files):
        print(
            f"⚠️  Writing to sensitive file: {file_path}",
            file=sys.stderr,
        )
        # Don't block, just warn

    return True, ""


def main():
    """Validate tool execution before it happens."""
    # Read hook input from stdin
    try:
        hook_input = json.loads(sys.stdin.read())
    except json.JSONDecodeError:
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Validate based on tool type
    if tool_name == "Bash":
        command = tool_input.get("command", "")
        valid, message = validate_bash(command)
        if not valid:
            print(f"🛑 BLOCKED: {message}", file=sys.stderr)
            sys.exit(2)  # Block operation

    elif tool_name in ("Write", "Edit", "MultiEdit"):
        content = tool_input.get("content", "") or tool_input.get("new_string", "")
        file_path = tool_input.get("file_path", "")
        valid, message = validate_write(content, file_path)
        # Writes are warned but not blocked

    sys.exit(0)  # Allow operation


if __name__ == "__main__":
    main()
