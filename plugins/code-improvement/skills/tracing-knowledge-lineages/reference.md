# Lineage Tracing Reference

## Search Strategies

**Where to look:**

1. **Decision records** (`docs/decisions/`, `docs/adr/`, `.adr/`)
2. **Git history** (`git log --grep="keyword"`, `git blame`)
3. **Issue/PR discussions** (GitHub/GitLab history)
4. **Documentation evolution** (`git log -- docs/`)
5. **Team knowledge** (ask: "Has anyone tried this before?")

**Bash patterns:**
```bash
# Find when approach was introduced
git log --all --grep="introduce.*caching"

# Find what file replaced
git log --diff-filter=D --summary | grep pattern

# Find discussion of abandoned approach
git log --all --grep="remove.*websocket"
```

---

## When to Override History

**You CAN ignore lineage when:**

1. **Context fundamentally changed**
   - Technology that didn't exist is now available
   - Constraints that forced decisions no longer apply

2. **We learned critical lessons**
   - Industry-wide understanding evolved
   - Better patterns emerged and were proven

3. **Original reasoning was flawed**
   - Based on assumptions later proven wrong
   - Cargo-culting without understanding

**But document WHY you're overriding:** Future you needs to know this was deliberate.

---

## Documentation Format

When proposing changes, include lineage:

```markdown
## Proposal: Switch from [Old] to [New]

### Current Approach Lineage
- **Adopted:** [When/why]
- **Replaced:** [What it replaced]
- **Worked because:** [Its strengths]
- **Struggling because:** [Current problems]

### Previous Attempts at [New]
- **Attempted:** [When, if ever]
- **Failed because:** [Why it didn't work then]
- **Context change:** [What's different now]

### Decision
[Proceed/Defer/Abandon] because [reasoning with historical context]
```

---

## Examples

### Good Lineage Tracing
"We used XML before JSON. XML died because verbosity hurt developer experience. But XML namespaces solved a real problem. If we hit namespace conflicts in JSON, we should study how XML solved it, not reinvent."

### Bad Lineage Ignorance
"REST is old, let's use GraphQL." (Ignores: Why did REST win over SOAP? What problems does it solve well?)

### Revival with Context
"We tried client-side routing in 2010, abandoned it due to poor browser support. Now that support is universal, worth reconsidering with lessons learned."

---

## Remember

- Current approaches exist for reasons (trace those reasons)
- Past failures might work now (context changes)
- "New" approaches might be revivals (check for precedents)
- Ignorance of history = doomed to repeat it
