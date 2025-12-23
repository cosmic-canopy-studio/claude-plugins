#!/bin/bash
# Pre-commit hook: Architectural review for staged GDScript files

echo "🏗️  Running architectural review..."

# Get list of staged GDScript files
STAGED_FILES=$(git diff --cached --name-only '*.gd' 2>/dev/null)

if [ -z "$STAGED_FILES" ]; then
    echo "No GDScript files staged for architectural review"
    exit 0
fi

# Convert to absolute paths for the architectural reviewer
REPO_ROOT=$(git rev-parse --show-toplevel)
ABSOLUTE_FILES=""

for file in $STAGED_FILES; do
    ABSOLUTE_FILES="$ABSOLUTE_FILES $REPO_ROOT/$file"
done

# Run architectural review on staged files
cd /home/sam/code/lb_advisor
python3 tools/architectural_reviewer.py --files "$ABSOLUTE_FILES" --format console

# Exit with architectural reviewer exit code
ARCH_EXIT=$?

if [ $ARCH_EXIT -ne 0 ]; then
    echo ""
    echo "❌ Architectural review failed. Critical architectural issues found."
    echo ""
    echo "Address the critical issues before committing. For details:"
    echo "  /architecture-review --files '$STAGED_FILES'"
    echo ""
    exit 1
fi

echo "✅ Architectural review passed!"