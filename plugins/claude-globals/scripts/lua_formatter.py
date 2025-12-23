#!/usr/bin/env python3
"""
Lua formatter and linter hook for Claude Code.
Automatically runs stylua and luacheck on Lua files.
"""

import json
import os
import subprocess
import sys


def run_stylua(file_path: str) -> bool:
    """Run stylua formatter on a Lua file."""
    if not file_path.endswith(".lua"):
        return True  # Not a Lua file, skip

    if not os.path.exists(file_path):
        return True  # File doesn't exist, skip

    try:
        # Get the project root directory
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

        # Run from project directory to pick up .stylua.toml config
        result = subprocess.run(
            ["stylua", file_path],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Print output if there were any changes
        if result.stdout.strip():
            print(f"✓ StyLua: {result.stdout.strip()}")

        # Check for errors
        if result.returncode != 0:
            print(f"⚠ StyLua warnings:\n{result.stderr}", file=sys.stderr)

        return True

    except subprocess.TimeoutExpired:
        print(f"⚠ StyLua timed out on {file_path}", file=sys.stderr)
        return True  # Don't block on timeout
    except FileNotFoundError:
        print("⚠ uv or stylua not found - skipping formatting", file=sys.stderr)
        return True  # Don't block if stylua isn't installed
    except Exception as e:
        print(f"⚠ Error running stylua: {e}", file=sys.stderr)
        return True  # Don't block on errors


def run_luacheck(file_path: str) -> bool:
    """Run luacheck linter on a Lua file."""
    if not file_path.endswith(".lua"):
        return True  # Not a Lua file, skip

    if not os.path.exists(file_path):
        return True  # File doesn't exist, skip

    try:
        # Get the project root directory
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

        # Run from project directory to pick up .luacheckrc config
        result = subprocess.run(
            ["luacheck", file_path],
            cwd=project_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Only print if there are warnings or errors
        if result.returncode != 0 or result.stdout.strip():
            # Filter out "OK" messages
            output = result.stdout.strip()
            if output and "OK" not in output:
                print(f"⚠ Luacheck: {output}")

        return True

    except subprocess.TimeoutExpired:
        print(f"⚠ Luacheck timed out on {file_path}", file=sys.stderr)
        return True  # Don't block on timeout
    except FileNotFoundError:
        print("⚠ luacheck not found - skipping linting", file=sys.stderr)
        return True  # Don't block if luacheck isn't installed
    except Exception as e:
        print(f"⚠ Error running luacheck: {e}", file=sys.stderr)
        return True  # Don't block on errors


def main():
    """Main entry point."""
    try:
        # Read hook input from stdin
        input_data = json.load(sys.stdin)

        # Extract file path from tool input
        file_path = input_data.get("tool_input", {}).get("file_path", "")

        if not file_path:
            sys.exit(0)  # No file path, nothing to do

        # Run stylua first (format), then luacheck (lint)
        run_stylua(file_path)
        run_luacheck(file_path)

        sys.exit(0)

    except Exception as e:
        print(f"⚠ Hook error: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block Claude on hook errors


if __name__ == "__main__":
    main()
