#!/bin/bash
# Hook script to format, lint, and type-check GDScript files after Write or Edit
# This script reads JSON input from stdin and validates .gd files

set -e

# Read JSON input from stdin
INPUT=$(cat)

# Extract file path from tool_input
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // empty')

# Exit early if no file path or not a .gd file
if [ -z "$FILE_PATH" ]; then
    exit 0
fi

if [[ ! "$FILE_PATH" == *.gd ]]; then
    exit 0
fi

# Check if file exists
if [ ! -f "$FILE_PATH" ]; then
    exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ERRORS=""

# 1. Format with gdscript-formatter
if command -v gdscript-formatter &> /dev/null; then
    gdscript-formatter "$FILE_PATH" 2>/dev/null || true
    echo "✓ Formatted: $FILE_PATH"
else
    echo "⚠ gdscript-formatter not found" >&2
fi

# 2. Lint with gdlint (style checking)
if command -v gdlint &> /dev/null; then
    LINT_OUTPUT=$(gdlint "$FILE_PATH" 2>&1) || true
    if echo "$LINT_OUTPUT" | grep -q "Success: no problems found"; then
        : # Silent on success
    elif [ -n "$LINT_OUTPUT" ]; then
        echo "⚠ Lint issues:"
        echo "$LINT_OUTPUT" | head -10
    fi
fi

# 3. Static type checking with Godot headless
# Uses a minimal project with strict typing enabled
if command -v godot &> /dev/null; then
    # Create temp directory for type checking
    TYPECHECK_DIR="/tmp/gdscript-typecheck-$$"
    mkdir -p "$TYPECHECK_DIR"

    # Create minimal project.godot with strict typing
    cat > "$TYPECHECK_DIR/project.godot" << 'PROJECTEOF'
config_version=5

[application]
config/name="GDScript Type Checker"

[debug]
gdscript/warnings/untyped_declaration=2
gdscript/warnings/inferred_declaration=1
gdscript/warnings/unsafe_property_access=1
gdscript/warnings/unsafe_method_access=1
gdscript/warnings/unsafe_cast=1
gdscript/warnings/unsafe_call_argument=1
PROJECTEOF

    # Copy script to temp project
    cp "$FILE_PATH" "$TYPECHECK_DIR/script.gd"

    # Run Godot type check
    TYPE_OUTPUT=$(cd "$TYPECHECK_DIR" && godot --headless --path . --check-only --script res://script.gd 2>&1) || true

    # Check for type errors
    if echo "$TYPE_OUTPUT" | grep -q "SCRIPT ERROR"; then
        echo "⚠ Static typing issues:"
        echo "$TYPE_OUTPUT" | grep -E "(SCRIPT ERROR|Parse Error)" | head -10
        ERRORS="typing"
    fi

    # Cleanup
    rm -rf "$TYPECHECK_DIR"
fi

# Report final status
if [ -n "$ERRORS" ]; then
    echo "---"
    echo "Fix typing issues: add explicit types (var x: Type = value)"
fi
