# Tracing Patterns

## Technique 1: Decision Archaeology

Search for when/why current approach was chosen:

1. **Check decision records** (`docs/decisions/`, `docs/adr/`, `.decisions/`)
2. **Git archaeology** (`git log --all --full-history -- path/to/file`)
3. **Search conversations**
4. **Ask the author** (if available)

**Document:**
```markdown
## Lineage: [Current Approach]

**When adopted:** [Date/commit]
**Why adopted:** [Original problem it solved]
**What it replaced:** [Previous approach]
**Why replaced:** [What was wrong with old approach]
**Context that drove change:** [External factors, new requirements]
```

---

## Technique 2: Failed Attempt Analysis

When someone says "we tried X and it didn't work":

**Don't assume:** X is fundamentally flawed
**Instead trace:**
1. What was the context? (constraints that no longer apply)
2. What specifically failed? (whole approach or one aspect?)
3. Why did it fail then? (technology limits, team constraints)
4. Has context changed? (new tools, different requirements)

**Document:**
```markdown
## Failed Attempt: [Approach]

**When attempted:** [Timeframe]
**What failed:** [Specific failure mode]
**Why it failed:** [Root cause, not symptoms]
**Context at time:** [Constraints that existed then]
**Context now:** [What's different today]
**Worth reconsidering?:** [Yes/No + reasoning]
```

---

## Technique 3: Revival Detection

When evaluating "new" approaches:

1. **Search for historical precedents** (tried before under different name?)
2. **Identify what's genuinely new** (vs. rebranded)
3. **Understand why it died** (if it's a revival)
4. **Check resurrection conditions** (has context changed enough?)

**Common revival patterns:**
- Microservices ← SOA ← Distributed Objects
- GraphQL ← SOAP ← RPC
- Serverless ← CGI scripts
- NoSQL ← Flat files ← Document stores

**Ask:** "What did we learn from the previous incarnation?"

---

## Technique 4: Paradigm Shift Mapping

**Map the transition:**
```markdown
## Paradigm Shift: From [Old] to [New]

**Pre-shift thinking:** [How we thought about problem]
**Catalyst:** [What triggered the shift]
**Post-shift thinking:** [How we think now]
**What was gained:** [New capabilities]
**What was lost:** [Old capabilities sacrificed]
**Lessons preserved:** [What we kept from old paradigm]
**Lessons forgotten:** [What we might need to relearn]
```
