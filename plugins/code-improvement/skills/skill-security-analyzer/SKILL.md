---
name: skill-security-analyzer
description: Validate third-party skills for security risks before installation (project) - when installing third-party skills, reviewing external skill code, auditing skill security, checking skill safety before use, validating untrusted .skill files
when_to_use: when installing third-party skills, reviewing external skill code, auditing skill security, checking skill safety before use, validating untrusted .skill files
version: 1.0.0
---

# Skill Security Analyzer

## Overview

Scan skill files for security vulnerabilities before installation. Treats `.skill` files as executable code, not configuration.

## Quick Start

```
1. Provide path to skill file or directory
2. I scan for dangerous patterns
3. I report risk level and specific concerns
4. You decide whether to proceed
```

## Security Checks

| Risk | Pattern | Action |
|------|---------|--------|
| **CRITICAL** | Unrestricted Bash tool access | REJECT |
| **CRITICAL** | Embedded credentials/secrets | REJECT |
| **CRITICAL** | Obfuscated/encoded payloads | REJECT |
| **HIGH** | Network access (WebFetch/WebSearch) without justification | REVIEW |
| **HIGH** | File writes outside project scope | REVIEW |
| **MEDIUM** | Undocumented external dependencies | NOTE |
| **LOW** | Missing version or author info | NOTE |

## Iron Law

```
NEVER approve skills with:
- Unrestricted Bash tool access without specific command patterns
- Network access without clear, documented justification
- File writes outside the project directory
- Embedded credentials, API keys, or secrets
- Obfuscated code or base64-encoded payloads
```

## Analysis Process

1. **Parse YAML frontmatter** - Check for suspicious metadata
2. **Scan for tool declarations** - Identify Bash, network, file access
3. **Pattern match content** - Look for credential patterns, encoded strings
4. **Check file references** - Verify paths stay within project
5. **Generate risk report** - Summarize findings with severity

## Output Format

```markdown
## Security Analysis: [skill-name]

**Risk Level**: CRITICAL / HIGH / MEDIUM / LOW / SAFE

### Findings

| Severity | Issue | Location | Recommendation |
|----------|-------|----------|----------------|
| CRITICAL | Unrestricted Bash | line 45 | REJECT - too broad |
| HIGH | WebFetch call | line 78 | Review purpose |

### Verdict

[SAFE TO INSTALL / REVIEW REQUIRED / DO NOT INSTALL]
```

## Red Flags

| If You're Thinking... | The Reality Is... |
|-----------------------|-------------------|
| "It's from a popular repo" | Popular repos get compromised |
| "I'll review it later" | You won't, and it runs immediately |
| "It's just markdown" | Skills can execute arbitrary code |
| "The author is trustworthy" | Trust but verify |

## Integration

- Run before `/skill-validate` for comprehensive checks
- Pair with skill-testing-framework for behavioral validation
- Use in team approval workflows for new skill additions
