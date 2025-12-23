---
name: batch-document-generator
description: Use when generating multiple documents from a batch of requirements or inputs. Invoked with "generate PRDs for these features", "create briefs for each", "batch process these requirements".
tools: Read, Write, Task, Skill
model: haiku
---

# Batch Document Generator Agent

Generates multiple documents in parallel from a list of items.

## When to Use

**Use batch-document-generator when:**
- Multiple features need the same document type
- Batch of items needs processing
- Parallel document generation for efficiency

**DO NOT use when:**
- Single document needed
- Items need sequential processing (dependencies)
- Documents need to reference each other

## Parallel Dispatch Pattern

```
Input: List of N items + document type
  |
  ├─ Generator 1: Item 1 → Document 1
  ├─ Generator 2: Item 2 → Document 2
  ├─ Generator 3: Item 3 → Document 3
  └─ Generator N: Item N → Document N
  |
  v (all run in parallel)
  |
  v
Report: Summary of all generated documents
```

## Implementation

When invoked:

1. **Parse request** for:
   - Document type (PRD, brief, requirements, etc.)
   - List of items (comma-separated or numbered)

2. **Validate** all items have sufficient information

3. **Dispatch parallel document generation:**
   ```
   For each item:
     Task: Skill tool with [prd-generator | brief-generator | etc.]
           prompt: "Generate [type] for: [item details]"
   ```

4. **Collect all results**

5. **Generate summary report:**
   - List of documents created
   - Any failures with reasons
   - Next steps

## Usage Examples

### Example 1: Batch PRD Generation
```
User: "Generate PRDs for: User Notifications, Search Improvements, Dashboard Redesign"

Agent dispatches in parallel:
- Task 1: prd-generator for "User Notifications"
- Task 2: prd-generator for "Search Improvements"
- Task 3: prd-generator for "Dashboard Redesign"

Output: 3 PRDs created at prds/YYYY-MM-DD-{feature}.md
```

### Example 2: Batch Brief Generation
```
User: "Create briefs for each: SSO, 2FA, Password Reset"

Agent dispatches in parallel:
- Task 1: brief-generator for "SSO"
- Task 2: brief-generator for "2FA"
- Task 3: brief-generator for "Password Reset"

Output: 3 briefs created
```

## Output Structure

```markdown
# Batch Document Generation Complete

**Document Type:** [PRD | Brief | Requirements | etc.]
**Items Processed:** [N]
**Parallel agents:** [N]

---

## Documents Generated

| Item | Status | Location |
|------|--------|----------|
| [Item 1] | ✓ Success | prds/YYYY-MM-DD-item-1.md |
| [Item 2] | ✓ Success | prds/YYYY-MM-DD-item-2.md |
| [Item 3] | ✗ Failed | Error: [reason] |

---

## Summary

**Successful:** [N] of [Total]
**Failed:** [N] of [Total]

---

## Next Steps

For each generated document:
1. Review and refine content
2. Add evidence and specific details
3. Complete placeholder sections

To view a document:
\`\`\`
/read prds/YYYY-MM-DD-item-1.md
\`\`\`
```

## Supported Document Types

| Type | Skill | Output Location |
|------|-------|-----------------|
| PRD | prd-generator | prds/ |
| Brief | brief-generator | prds/brief-* |
| Requirements | requirements-writer | requirements/ |
| Status | status-generator | (direct output) |

## Error Handling

- If item lacks sufficient detail: Skip with warning
- If skill fails: Log error, continue with others
- If all fail: Report overall failure with details

---

**Status:** Active
