#!/bin/bash
# Sync all plugins from source projects
# Run from the claude-plugins repo root

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== Syncing all plugins ==="
echo ""

# Define source mappings: plugin-name -> source-path
declare -A PLUGINS=(
    ["tool-buddy"]="/home/sam/code/tool-buddy"
    ["code-improvement"]="/home/sam/code/code_improvement"
    ["lb-advisor"]="/home/sam/code/lb_advisor"
    ["godot-advisor"]="/home/sam/code/godot_advisor"
    ["software-architecture"]="/home/sam/code/software_architecture"
)

for plugin in "${!PLUGINS[@]}"; do
    source_path="${PLUGINS[$plugin]}"
    echo "=== $plugin ==="
    "$SCRIPT_DIR/sync-plugin.sh" "$plugin" "$source_path"
    echo ""
done

echo "=== All plugins synced ==="
