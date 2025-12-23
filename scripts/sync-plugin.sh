#!/bin/bash
# Sync a single plugin from source project to plugin repo
# Usage: ./scripts/sync-plugin.sh <plugin-name> <source-path>
# Example: ./scripts/sync-plugin.sh lb-advisor /home/sam/code/lb_advisor

set -e

PLUGIN_NAME=$1
SOURCE_PATH=$2
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(dirname "$SCRIPT_DIR")"
DEST_PATH="${REPO_ROOT}/plugins/${PLUGIN_NAME}"

if [ -z "$PLUGIN_NAME" ] || [ -z "$SOURCE_PATH" ]; then
    echo "Usage: $0 <plugin-name> <source-path>"
    echo "Example: $0 lb-advisor /home/sam/code/lb_advisor"
    exit 1
fi

if [ ! -d "$SOURCE_PATH/.claude" ]; then
    echo "Error: $SOURCE_PATH/.claude does not exist"
    exit 1
fi

echo "Syncing $PLUGIN_NAME from $SOURCE_PATH..."

# Create destination directories if needed
mkdir -p "$DEST_PATH"/{.claude-plugin,skills,agents}

# Sync skills (always present)
if [ -d "$SOURCE_PATH/.claude/skills" ]; then
    echo "  Syncing skills..."
    rsync -av --delete "$SOURCE_PATH/.claude/skills/" "$DEST_PATH/skills/"
fi

# Sync agents (always present)
if [ -d "$SOURCE_PATH/.claude/agents" ]; then
    echo "  Syncing agents..."
    rsync -av --delete "$SOURCE_PATH/.claude/agents/" "$DEST_PATH/agents/"
fi

# Sync commands (optional)
if [ -d "$SOURCE_PATH/.claude/commands" ]; then
    echo "  Syncing commands..."
    mkdir -p "$DEST_PATH/commands"
    rsync -av --delete "$SOURCE_PATH/.claude/commands/" "$DEST_PATH/commands/"
fi

# Convert hooks if settings.json has hooks
if [ -f "$SOURCE_PATH/.claude/settings.json" ]; then
    if grep -q '"hooks"' "$SOURCE_PATH/.claude/settings.json"; then
        echo "  Converting hooks..."
        mkdir -p "$DEST_PATH/hooks" "$DEST_PATH/scripts"
        python3 "$SCRIPT_DIR/convert-hooks.py" "$SOURCE_PATH/.claude/settings.json" "$DEST_PATH/hooks/hooks.json"

        # Copy hook scripts if they exist
        if [ -d "$SOURCE_PATH/.claude/hooks" ]; then
            for script in "$SOURCE_PATH/.claude/hooks"/*.{py,sh}; do
                if [ -f "$script" ]; then
                    cp "$script" "$DEST_PATH/scripts/"
                fi
            done
            # Copy lib directory if exists
            if [ -d "$SOURCE_PATH/.claude/hooks/lib" ]; then
                cp -r "$SOURCE_PATH/.claude/hooks/lib" "$DEST_PATH/scripts/"
            fi
        fi
    fi
fi

echo "  Done syncing $PLUGIN_NAME"
