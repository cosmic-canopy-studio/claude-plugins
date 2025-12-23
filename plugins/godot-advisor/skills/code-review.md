---
name: code-review
description: Review GDScript code for best practices, style compliance, and potential issues
allowed-tools: Read, Grep, Glob, Bash
---

# Code Review

Quickly review GDScript code for best practices, style compliance, and potential issues.

## Examples

- "Review this file for code quality: path/to/script.gd"
- "Check the play_editor.gd file for Godot best practices"
- "Analyze the networking code for performance issues"
- "Review all files in the scene/ directory for documentation"
- "Check if this code follows GDScript naming conventions"

## Features

- **Style Compliance**: Checks adherence to GDScript style guide
- **Best Practices**: Validates Godot-specific patterns and conventions
- **Documentation**: Ensures appropriate docstrings and comments
- **Performance**: Identifies potential performance issues
- **Naming**: Verifies proper naming conventions
- **Resource Management**: Checks for proper resource handling

## Usage Patterns

1. **File Review**: Analyze specific files for quality issues
2. **PR Review**: Review all changes in a pull request
3. **Directory Scan**: Review all files in a directory
4. **Staged Changes**: Review only git-staged changes (default)
5. **Strict Mode**: Treat warnings as errors

## Integration

The skill integrates with:
- `/code-review` command for comprehensive analysis
- gdlint for official GDScript linting
- Git workflows for PR automation
- IDE plugins for real-time feedback