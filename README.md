# Claude Plugins

Cosmic Canopy Studio plugin collection for Claude Code.

## Quick Start

### Add the marketplace

```shell
/plugin marketplace add cosmic-canopy-studio/claude-plugins
```

### Install a plugin

```shell
# User scope (available in all your projects)
claude plugin install tool-buddy@cosmic-canopy-plugins

# Project scope (shared with team via git)
claude plugin install tool-buddy@cosmic-canopy-plugins --scope project
```

## Available Plugins

| Plugin | Description | Skills | Commands | Agents |
|--------|-------------|--------|----------|--------|
| [tool-buddy](./plugins/tool-buddy) | Development workflow with RPI commands | 9 | 10 | 2 |
| [code-improvement](./plugins/code-improvement) | Knowledge pipeline and meta-skills | 22 | 24 | 10 |
| [lb-advisor](./plugins/lb-advisor) | Lacrosse Boss game development | 28 | 4 | 14 |
| [godot-advisor](./plugins/godot-advisor) | Godot game engine workflows | 20 | 9 | 26 |
| [software-architecture](./plugins/software-architecture) | Architecture knowledge extraction | 12 | 0 | 12 |
| [pm-toolkit](./plugins/pm-toolkit) | Project management tools | 11 | 0 | 5 |
| [claude-globals](./plugins/claude-globals) | Shared utility commands | 0 | 5 | 11 |
| [stationeers-companion](./plugins/stationeers-companion) | Stationeers IC assembly | 9 | 0 | 11 |
| [netmon](./plugins/netmon) | Network monitoring | 3 | 0 | 0 |
| [os-advisor](./plugins/os-advisor) | OS guidance | 1 | 1 | 2 |
| [asset-helper](./plugins/asset-helper) | Asset management | 2 | 0 | 7 |
| [catalyst-game](./plugins/catalyst-game) | Catalyst game development | 20 | 0 | 12 |

## Categories

### Workflow
- **tool-buddy** - Core development workflow commands and thinking skills

### Game Development
- **lb-advisor** - Lacrosse Boss specific patterns
- **godot-advisor** - General Godot/GDScript workflows
- **catalyst-game** - Catalyst game patterns
- **stationeers-companion** - Stationeers IC programming

### Meta/Knowledge
- **code-improvement** - Knowledge pipeline, analysis, synthesis
- **software-architecture** - Architecture patterns extraction

### Utilities
- **claude-globals** - Shared commands and agents
- **pm-toolkit** - Project management
- **netmon** - Network monitoring
- **os-advisor** - OS utilities
- **asset-helper** - Asset research

## Team Setup

To automatically install plugins for team members, add to your project's `.claude/settings.json`:

```json
{
  "plugins": {
    "marketplaces": [
      {
        "name": "cosmic-canopy-plugins",
        "source": "cosmic-canopy-studio/claude-plugins"
      }
    ],
    "installed": [
      {
        "name": "tool-buddy",
        "marketplace": "cosmic-canopy-plugins"
      }
    ]
  }
}
```

## License

MIT
