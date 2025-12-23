---
name: docs-reference
description: Create technical reference documentation
---

# Create Reference Documentation

Creates comprehensive technical specifications for accurate information lookup.

## Usage

/docs-reference --component=STRING [--format=markdown|html] [--scope=public|internal]

## Options

- `--component`: Component to document (required)
- `--format`: Output format (default: markdown)
- `--scope`: Documentation scope (default: public)

## Output Format

Reference docs follow this structure:
```markdown
# Reference: [Component]

## Overview
- Brief description
- Use cases

## API Reference
### Functions/Methods
- Function signatures
- Parameters with types
- Return values
- Error conditions

### Classes
- Class definitions
- Properties
- Methods
- Inheritance

## Configuration
- Available options
- Default values
- Valid ranges

## Examples
- Usage examples
- Common patterns
```

## Best Practices

- Be comprehensive and accurate
- Include type information
- Document all parameters
- Provide concrete examples
- Maintain factual, objective tone
- Organize for easy browsing

---

cd /home/sam/code/code_improvement && python tools/create_docs.py reference "$*"