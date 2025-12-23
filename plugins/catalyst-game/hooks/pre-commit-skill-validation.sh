#!/bin/bash
# Pre-commit hook for skill validation
# Runs static checks and prompts for agent validation
#
# Install: ln -sf ../../.claude/hooks/pre-commit-skill-validation.sh .git/hooks/pre-commit

set -e

# Colors
RED='\033[0;31m'
YELLOW='\033[1;33m'
GREEN='\033[0;32m'
CYAN='\033[0;36m'
NC='\033[0m'

# Get modified skill files (staged for commit)
SKILL_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep -E '\.claude/skills/.*\.md$' || true)

if [ -z "$SKILL_FILES" ]; then
    # No skill files modified, skip validation
    exit 0
fi

echo -e "${CYAN}=== Skill Validation Pre-commit Hook ===${NC}"
echo ""
echo "Modified skill files:"
echo "$SKILL_FILES" | while read -r f; do echo "  - $f"; done
echo ""

# Run static validation on modified files
echo -e "${CYAN}Running static validation...${NC}"
VALIDATION_FAILED=0

for file in $SKILL_FILES; do
    if [ -f "$file" ]; then
        if ! .claude/scripts/validate-skills-static.sh "$file" 2>/dev/null; then
            VALIDATION_FAILED=1
        fi
    fi
done

if [ $VALIDATION_FAILED -eq 1 ]; then
    echo ""
    echo -e "${RED}Static validation failed. Please fix errors before committing.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Static checks passed.${NC}"
echo ""

# Count modified files to determine if agent validation is recommended
FILE_COUNT=$(echo "$SKILL_FILES" | wc -l)

if [ "$FILE_COUNT" -gt 3 ]; then
    echo -e "${YELLOW}NOTE: $FILE_COUNT skill files modified.${NC}"
    echo "For comprehensive validation, consider running:"
    echo ""
    echo "  Task skill-validator 'Validate: $SKILL_FILES'"
    echo "  Task skill-auditor 'Audit quality of modified skills'"
    echo ""
fi

# Check if this is a significant change (new files or large modifications)
NEW_FILES=$(git diff --cached --name-only --diff-filter=A | grep -E '\.claude/skills/.*\.md$' || true)
if [ -n "$NEW_FILES" ]; then
    echo -e "${YELLOW}New skill files detected:${NC}"
    echo "$NEW_FILES" | while read -r f; do echo "  - $f"; done
    echo ""
    echo "Recommended: Run skill-validator and skill-auditor before pushing."
    echo ""
fi

# Prompt for confirmation if in interactive mode
if [ -t 0 ]; then
    # Terminal is interactive
    echo -e "${CYAN}Proceed with commit?${NC}"
    echo "  [y] Yes, commit now"
    echo "  [n] No, abort and run agent validation"
    echo ""
    read -p "Choice [Y/n]: " -n 1 -r
    echo ""

    if [[ $REPLY =~ ^[Nn]$ ]]; then
        echo ""
        echo "Commit aborted. Run agent validation:"
        echo "  Task skill-validator 'Validate modified skill files'"
        exit 1
    fi
fi

echo -e "${GREEN}Proceeding with commit.${NC}"
exit 0
