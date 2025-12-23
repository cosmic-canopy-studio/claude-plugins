# GDScript Formatter Reference

## CLI Options

| Option | Description |
|--------|-------------|
| `--check` | Verify formatting without modifying files. Exit code 1 if changes needed. |
| `--safe` | Prevent changes that could alter code meaning. |
| `--reorder-code` | Rearrange code to match GDScript style guide (experimental). |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success (or no formatting needed with --check) |
| 1 | Formatting needed (--check mode) or error |

## Installation Locations

Add the binary to your PATH:

| OS | Common PATH Location |
|----|---------------------|
| Windows | `C:\Windows\System32` or add custom directory to PATH |
| macOS | `~/.local/bin` or `/usr/local/bin` |
| Linux | `~/.local/bin` or `/usr/local/bin` |

## Editor Integration

### Godot Add-on
- Install the official GDScript Formatter plugin
- Keyboard shortcut: `Ctrl+Alt+I`
- Supports format-on-save

### VS Code
- Install "Godot Format" extension
- Format shortcut: `Shift+Alt+F`

### Other Editors
- **Zed**: Install zed-gdscript extension
- **Helix**: Configure in `~/.config/helix/languages.toml`
- **Rider**: Create file watcher in Tools > File Watchers

## Style Guide Ordering (--reorder-code)

Code is reordered in this sequence:
1. `class_name` declaration
2. `extends` statement
3. Signals
4. Enums
5. Constants
6. Exported variables
7. Public variables
8. Private variables (prefixed with `_`)
9. `@onready` variables
10. Built-in virtual methods (`_init`, `_ready`, `_process`, etc.)
11. Public methods
12. Private methods (prefixed with `_`)

## Common Patterns

### CI Pipeline Check
```bash
# Fail CI if any file needs formatting
gdscript-formatter --check $(find . -name "*.gd")
```

### Pre-commit Hook
```bash
#!/bin/bash
# .git/hooks/pre-commit
gdscript-formatter --check $(git diff --cached --name-only --diff-filter=ACM | grep '\.gd$')
```

### Format Changed Files Only
```bash
# Format only staged .gd files
git diff --cached --name-only --diff-filter=ACM | grep '\.gd$' | xargs gdscript-formatter
```
