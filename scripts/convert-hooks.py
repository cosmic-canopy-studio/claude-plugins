#!/usr/bin/env python3
"""
Convert project settings.json hooks to plugin hooks.json format.

Converts:
- $CLAUDE_PROJECT_DIR -> ${CLAUDE_PLUGIN_ROOT}
- .claude/hooks/ -> scripts/

Usage: python3 convert-hooks.py <source-settings.json> <dest-hooks.json>
"""

import json
import sys
from pathlib import Path


def convert_command(command: str) -> str:
    """Convert a hook command from project format to plugin format."""
    # Replace project dir variable with plugin root
    result = command.replace("$CLAUDE_PROJECT_DIR", "${CLAUDE_PLUGIN_ROOT}")
    result = result.replace('"$CLAUDE_PROJECT_DIR"', '"${CLAUDE_PLUGIN_ROOT}"')

    # Replace .claude/hooks/ path with scripts/
    result = result.replace(".claude/hooks/", "scripts/")
    result = result.replace("/.claude/hooks/", "/scripts/")

    return result


def convert_hooks(source_path: str, dest_path: str) -> None:
    """Convert hooks from settings.json to plugin hooks.json format."""
    with open(source_path, "r") as f:
        settings = json.load(f)

    if "hooks" not in settings:
        print(f"No hooks found in {source_path}")
        return

    source_hooks = settings["hooks"]
    converted_hooks = {}

    for event_type, event_hooks in source_hooks.items():
        converted_event_hooks = []

        for hook_group in event_hooks:
            converted_group = {}

            # Copy matcher if present
            if "matcher" in hook_group:
                converted_group["matcher"] = hook_group["matcher"]

            # Convert individual hooks
            if "hooks" in hook_group:
                converted_inner_hooks = []
                for hook in hook_group["hooks"]:
                    converted_hook = dict(hook)

                    if "command" in converted_hook:
                        converted_hook["command"] = convert_command(
                            converted_hook["command"]
                        )

                    # Ensure timeout is reasonable (minimum 1000ms for scripts)
                    if "timeout" in converted_hook:
                        if converted_hook["timeout"] < 1000:
                            converted_hook["timeout"] = 30000  # Default to 30 seconds

                    converted_inner_hooks.append(converted_hook)

                converted_group["hooks"] = converted_inner_hooks

            converted_event_hooks.append(converted_group)

        converted_hooks[event_type] = converted_event_hooks

    # Write output
    output = {"hooks": converted_hooks}

    dest_dir = Path(dest_path).parent
    dest_dir.mkdir(parents=True, exist_ok=True)

    with open(dest_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Converted hooks written to {dest_path}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(
            "Usage: python3 convert-hooks.py <source-settings.json> <dest-hooks.json>"
        )
        sys.exit(1)

    convert_hooks(sys.argv[1], sys.argv[2])
