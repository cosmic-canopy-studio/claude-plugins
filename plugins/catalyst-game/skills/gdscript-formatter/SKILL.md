---
name: gdscript-formatter
description: Format GDScript files using gdscript-formatter. Use when formatting .gd files, checking GDScript style compliance, or reordering code to match the official style guide. Requires gdscript-formatter binary in PATH.
---

# GDScript Formatter

## Plan Mode Behavior

When plan mode is active:
1. **Use --check flag only** - Check formatting without modifying files
2. **Do NOT format files** - Plan mode restricts file modifications
3. **When formatting is needed**, call `ExitPlanMode` tool
4. Wait for user to exit plan mode before applying formatting changes

## Overview

Format GDScript files using the fast Rust-based gdscript-formatter tool. Supports formatting, style checking, and code reordering according to the official GDScript style guide.

## Prerequisites

The `gdscript-formatter` binary must be installed and available in PATH. Download from: https://www.gdquest.com/library/gdscript_formatter/

## Quick Reference

### Format a single file
```bash
gdscript-formatter path/to/script.gd
```

### Format multiple files
```bash
gdscript-formatter file1.gd file2.gd file3.gd
```

### Check formatting without modifying (CI/validation)
```bash
gdscript-formatter --check path/to/script.gd
```
Exit code 1 means formatting is needed.

### Safe mode (prevents semantic changes)
```bash
gdscript-formatter --safe path/to/script.gd
```

### Reorder code to match style guide (experimental)
```bash
gdscript-formatter --reorder-code path/to/script.gd
```

## Batch Operations

Format all GDScript files in a directory:
```bash
find . -name "*.gd" -exec gdscript-formatter {} \;
```

Check all files (useful for CI):
```bash
find . -name "*.gd" -exec gdscript-formatter --check {} \;
```

Use the helper script for common operations:
```bash
# Format all .gd files in current directory
./scripts/format_all.sh

# Check only (no modifications)
./scripts/format_all.sh --check

# Format specific directory
./scripts/format_all.sh path/to/directory
```

## Formatting Behavior

- Single-line code stays single-line with corrected spacing
- Multi-line code is reformatted appropriately
- Does not auto-wrap at character limits
- Uses your code layout as guidance

## Code Reordering (--reorder-code)

When enabled, organizes code in this order:
1. Signals and variables at top
2. Built-in Godot methods (_ready, _process, etc.)
3. Public methods
4. Private methods (prefixed with _)

## Related Skills

- godot-character-body-2d - GDScript patterns for 2D movement
- godot-character-body-3d - GDScript patterns for 3D movement
