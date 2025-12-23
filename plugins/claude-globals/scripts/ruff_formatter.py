#!/usr/bin/env python3
"""
Ruff formatter hook for Claude Code.
Automatically runs ruff check --fix and ruff format on Python files.
"""
import json
import os
import subprocess
import sys


def run_ruff(file_path: str) -> bool:
    """Run ruff on a Python file."""
    if not file_path.endswith(".py"):
        return True  # Not a Python file, skip

    if not os.path.exists(file_path):
        return True  # File doesn't exist, skip

    # Check if file is in tools/ directory (where ruff is configured)
    is_tools_dir = "tools/" in file_path or file_path.startswith("tools/")

    try:
        # Get the project root directory
        project_dir = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())

        # Determine working directory for uv run
        if is_tools_dir:
            # For files in tools/, run from tools/ directory
            work_dir = os.path.join(project_dir, "tools")
            # Make path relative to tools/ if it's in tools/
            if "/tools/" in file_path:
                rel_path = file_path.split("/tools/", 1)[1]
            else:
                rel_path = os.path.basename(file_path)
        else:
            # For other Python files, run from project root
            work_dir = project_dir
            rel_path = os.path.relpath(file_path, project_dir)

        # Run ruff check --fix
        check_result = subprocess.run(
            ["uv", "run", "ruff", "check", rel_path, "--fix"],
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Run ruff format
        format_result = subprocess.run(
            ["uv", "run", "ruff", "format", rel_path],
            cwd=work_dir,
            capture_output=True,
            text=True,
            timeout=30,
        )

        # Print output if there were any changes
        if check_result.stdout.strip():
            print(f"✓ Ruff check: {check_result.stdout.strip()}")
        if format_result.stdout.strip():
            print(f"✓ Ruff format: {format_result.stdout.strip()}")

        # Check for errors
        if check_result.returncode != 0 and "fixed" not in check_result.stdout.lower():
            print(f"⚠ Ruff check warnings:\n{check_result.stderr}", file=sys.stderr)
        if format_result.returncode != 0:
            print(f"⚠ Ruff format warnings:\n{format_result.stderr}", file=sys.stderr)

        return True

    except subprocess.TimeoutExpired:
        print(f"⚠ Ruff timed out on {file_path}", file=sys.stderr)
        return True  # Don't block on timeout
    except FileNotFoundError:
        print("⚠ uv or ruff not found - skipping formatting", file=sys.stderr)
        return True  # Don't block if ruff isn't installed
    except Exception as e:
        print(f"⚠ Error running ruff: {e}", file=sys.stderr)
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

        # Run ruff on the file
        success = run_ruff(file_path)

        sys.exit(0 if success else 1)

    except Exception as e:
        print(f"⚠ Hook error: {e}", file=sys.stderr)
        sys.exit(0)  # Don't block Claude on hook errors


if __name__ == "__main__":
    main()
