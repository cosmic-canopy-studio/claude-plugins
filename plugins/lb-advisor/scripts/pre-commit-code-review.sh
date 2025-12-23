#!/bin/bash
# Pre-commit hook: Run code review on staged GDScript files

echo "🔍 Running pre-commit code review..."

# Get list of staged GDScript files
STAGED_FILES=$(git diff --cached --name-only '*.gd' 2>/dev/null)

if [ -z "$STAGED_FILES" ]; then
    echo "No GDScript files staged for review"
    exit 0
fi

# Run code review on staged files
cd /home/sam/code/lb_advisor
python tools/code_review.py --paths $STAGED_FILES

# Exit with code review exit code
REVIEW_EXIT=$?

if [ $REVIEW_EXIT -ne 0 ]; then
    echo ""
    echo "❌ Code review failed. Please fix issues before committing."
    echo "Run '/code-review --paths $STAGED_FILES' to see details."
    exit 1
fi

echo "✅ Code review passed!"