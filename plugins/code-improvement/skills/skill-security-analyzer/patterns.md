# Dangerous Patterns Reference

## Critical Patterns (Auto-Reject)

### Unrestricted Shell Access
```yaml
# DANGEROUS - allows any command
tools: [Bash]
# No command restrictions specified
```

```markdown
# DANGEROUS - instructions allow arbitrary execution
Run any shell command the user requests
```

### Credential Patterns
```regex
# API keys
(api[_-]?key|apikey)\s*[:=]\s*['"]?[a-zA-Z0-9]{20,}

# AWS credentials
(AKIA|ABIA|ACCA|ASIA)[0-9A-Z]{16}

# Private keys
-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----

# Generic secrets
(password|secret|token)\s*[:=]\s*['"][^'"]{8,}
```

### Obfuscation
```regex
# Base64 encoded strings (long)
[A-Za-z0-9+/]{50,}={0,2}

# Hex encoded strings
\\x[0-9a-fA-F]{2}(\\x[0-9a-fA-F]{2}){10,}

# eval/exec patterns
(eval|exec)\s*\(
```

## High-Risk Patterns (Manual Review)

### Network Access
```yaml
# Requires justification
tools: [WebFetch, WebSearch]
```

Questions to ask:
- What URLs are accessed?
- Is the data sent anywhere?
- Are credentials transmitted?

### File System Access
```markdown
# Check scope
Write to /etc/
Write to ~/.ssh/
Write to /usr/
```

Questions to ask:
- Are writes confined to project directory?
- Are sensitive directories excluded?
- Is there proper path validation?

## Medium-Risk Patterns

### External Dependencies
```markdown
# Undocumented requirements
pip install [package]
npm install [package]
curl [url] | bash
```

### Dynamic Code Generation
```markdown
# Creates and executes code
Create a Python script that...
Generate a shell script to...
```

## Low-Risk Patterns

### Missing Metadata
```yaml
# Should have
version: X.Y.Z
author: name
repository: url
```

### Broad Descriptions
```yaml
# Too vague
description: Does various things
when_to_use: whenever needed
```

## Safe Patterns

### Restricted Tool Access
```yaml
# SAFE - specific commands only
tools: [Read, Glob, Grep]
# Read-only operations
```

### Project-Scoped Operations
```markdown
# SAFE - stays in project
Read files from ./src/
Write to ./output/
```

### Explicit Denials
```markdown
# SAFE - explicit restrictions
NEVER write to system directories
NEVER access network without user confirmation
```
