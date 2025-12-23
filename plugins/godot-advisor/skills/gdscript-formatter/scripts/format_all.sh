#!/bin/bash
# Format all GDScript files in a directory using gdscript-formatter
# Usage: ./format_all.sh [--check] [--safe] [--reorder] [directory]

# Don't use set -e since formatter returns 1 for unformatted files

# Default values
CHECK_MODE=false
SAFE_MODE=false
REORDER_MODE=false
TARGET_DIR="."

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --check)
            CHECK_MODE=true
            shift
            ;;
        --safe)
            SAFE_MODE=true
            shift
            ;;
        --reorder)
            REORDER_MODE=true
            shift
            ;;
        *)
            TARGET_DIR="$1"
            shift
            ;;
    esac
done

# Verify gdscript-formatter is installed
if ! command -v gdscript-formatter &> /dev/null; then
    echo "Error: gdscript-formatter not found in PATH"
    echo "Download from: https://www.gdquest.com/library/gdscript_formatter/"
    exit 1
fi

# Build command arguments
ARGS=""
if [ "$CHECK_MODE" = true ]; then
    ARGS="$ARGS --check"
fi
if [ "$SAFE_MODE" = true ]; then
    ARGS="$ARGS --safe"
fi
if [ "$REORDER_MODE" = true ]; then
    ARGS="$ARGS --reorder-code"
fi

# Find and process all .gd files
FILE_COUNT=0
FAILED_COUNT=0

echo "Scanning for GDScript files in: $TARGET_DIR"

while IFS= read -r -d '' file; do
    ((FILE_COUNT++))
    if [ "$CHECK_MODE" = true ]; then
        echo "Checking: $file"
    else
        echo "Formatting: $file"
    fi

    if ! gdscript-formatter $ARGS "$file" 2>&1; then
        ((FAILED_COUNT++)) || true
        if [ "$CHECK_MODE" = true ]; then
            echo "  -> Needs formatting"
        else
            echo "  -> Failed"
        fi
    fi
done < <(find "$TARGET_DIR" -name "*.gd" -type f -print0)

echo ""
echo "Complete: $FILE_COUNT files processed"

if [ "$CHECK_MODE" = true ] && [ $FAILED_COUNT -gt 0 ]; then
    echo "$FAILED_COUNT files need formatting"
    exit 1
fi

if [ $FAILED_COUNT -gt 0 ]; then
    echo "$FAILED_COUNT files failed"
    exit 1
fi

echo "All files OK"
