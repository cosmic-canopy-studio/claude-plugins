# Installation Guide

## Prerequisites

- Claude Code CLI installed
- Access to cosmic-canopy-studio GitHub organization

## Adding the Marketplace

### Option 1: Via Claude Code UI

```shell
/plugin
# Select "Manage Marketplaces"
# Select "Add Marketplace"
# Enter: cosmic-canopy-studio/claude-plugins
```

### Option 2: Via CLI

```shell
claude plugin marketplace add cosmic-canopy-studio/claude-plugins
```

## Installing Plugins

### Interactive Installation

```shell
/plugin
# Select "Browse Plugins"
# Choose a plugin
# Select installation scope
```

### Direct Installation

```shell
# User scope - available in all your projects
claude plugin install <plugin-name>@cosmic-canopy-plugins

# Project scope - committed to git, shared with team
claude plugin install <plugin-name>@cosmic-canopy-plugins --scope project

# Local scope - personal, gitignored
claude plugin install <plugin-name>@cosmic-canopy-plugins --scope local
```

## Scope Recommendations

| Scope | Use When |
|-------|----------|
| `user` | Personal productivity plugins you want everywhere |
| `project` | Team-standardized workflows and conventions |
| `local` | Testing or personal preferences within a team project |

## Verifying Installation

After installing, verify plugins are loaded:

```shell
# Check commands
/help

# Check skills (they appear automatically when relevant)
# Skills trigger based on context

# Check agents
# Available via Task tool
```

## Updating Plugins

```shell
# Uninstall current version
/plugin uninstall <plugin-name>@cosmic-canopy-plugins

# Install latest
/plugin install <plugin-name>@cosmic-canopy-plugins
```

## Troubleshooting

### Plugin not appearing

1. Restart Claude Code after installation
2. Verify marketplace is added: `/plugin` → "Manage Marketplaces"
3. Check installation scope matches your context

### Hooks not firing

1. Ensure plugin with hooks is installed
2. Verify hook scripts have execute permission
3. Check Claude Code logs for hook errors

### Skill not triggering

1. Skills trigger based on `description` keywords
2. Verify the skill's trigger conditions in its SKILL.md
3. Try explicitly mentioning related keywords
