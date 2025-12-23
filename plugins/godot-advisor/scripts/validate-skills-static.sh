#!/bin/bash
# Static validation for Godot skill reference files
# Fast checks before agent validation - runs in < 1 second
# Usage: ./validate-skills-static.sh [file_or_directory]

set -e

ERRORS=0
WARNINGS=0
TARGET="${1:-.claude/skills/godot/reference}"

# Colors for output
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
NC='\033[0m' # No Color

log_error() {
    echo -e "${RED}ERROR:${NC} $1"
    ERRORS=$((ERRORS + 1))
}

log_warning() {
    echo -e "${YELLOW}WARNING:${NC} $1"
    WARNINGS=$((WARNINGS + 1))
}

log_success() {
    echo -e "${GREEN}OK:${NC} $1"
}

echo "=== Skill Static Validation ==="
echo "Target: $TARGET"
echo ""

# Find all markdown files
if [ -d "$TARGET" ]; then
    FILES=$(find "$TARGET" -name "*.md" -type f)
else
    FILES="$TARGET"
fi

for file in $FILES; do
    # Skip if file doesn't exist
    [ -f "$file" ] || continue

    # 1. Check YAML frontmatter exists
    if ! head -1 "$file" | grep -q "^---$"; then
        log_error "$file - Missing YAML frontmatter (no opening ---)"
        continue
    fi

    # Check closing ---
    if ! head -20 "$file" | grep -q "^---$" | head -2 | tail -1; then
        # Just verify there's at least one more --- in first 20 lines
        frontmatter_end=$(head -20 "$file" | grep -n "^---$" | wc -l)
        if [ "$frontmatter_end" -lt 2 ]; then
            log_error "$file - Incomplete YAML frontmatter (no closing ---)"
            continue
        fi
    fi

    # 2. Check for class: key in node references
    if echo "$file" | grep -q "reference/nodes/"; then
        if ! head -10 "$file" | grep -q "^class:"; then
            log_error "$file - Missing 'class:' key in frontmatter"
        fi
    fi

    # 3. Check for untyped functions in code examples
    if grep -q '```gdscript' "$file" 2>/dev/null; then
        # Look for function definitions without return type annotation
        # Using simpler pattern to avoid regex issues
        untyped=$(grep -A 30 '```gdscript' "$file" 2>/dev/null | grep -E "^func [a-z_]+\(" | grep -v "\->" || true)
        if [ -n "$untyped" ]; then
            log_warning "$file - Possibly untyped function (missing -> ReturnType)"
        fi
    fi

    # 4. Check for deprecated Godot 3.x syntax
    if grep -q "onready var" "$file" 2>/dev/null; then
        log_warning "$file - Uses deprecated 'onready' (use '@onready' for Godot 4.x)"
    fi

    if grep -q "export var" "$file" 2>/dev/null; then
        log_warning "$file - Uses deprecated 'export var' (use '@export' for Godot 4.x)"
    fi

done

echo ""
echo "=== Validation Summary ==="
echo "Errors: $ERRORS"
echo "Warnings: $WARNINGS"

if [ $ERRORS -gt 0 ]; then
    echo -e "${RED}Validation FAILED${NC}"
    exit 1
else
    if [ $WARNINGS -gt 0 ]; then
        echo -e "${YELLOW}Validation PASSED with warnings${NC}"
    else
        echo -e "${GREEN}Validation PASSED${NC}"
    fi
    exit 0
fi
