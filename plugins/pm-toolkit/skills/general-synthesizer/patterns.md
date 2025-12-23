# General Synthesizer - Detailed Patterns

## Research Workflow

### Step 1: Analyze the Research Question

Before exploring:
- Clarify what the user wants to know
- Identify the scope (project structure? specific feature? patterns?)
- Determine what "good enough" looks like for this research

**Questions to ask yourself:**
- What components/areas are relevant?
- What level of detail is needed?
- What decisions will this research inform?

### Step 2: Read Mentioned Files First

**CRITICAL**: If user mentions specific files, read them FULLY before spawning agents.

```markdown
User says: "Look at the planning docs in plans/ROADMAP.md"
You do: Read plans/ROADMAP.md completely first
Then: Use Explore agent for broader context
```

### Step 3: Use Explore Agent for Discovery

Leverage native Explore agent via Task tool with `subagent_type='Explore'`:

```markdown
Use Task tool with:
- subagent_type: 'Explore'
- prompt: "Find [specific thing] in [area]. Look for [patterns/files/concepts]."
- description: Short description of exploration goal
```

**Thoroughness levels:**
- "quick" - Basic search, first-pass discovery
- "medium" - Moderate exploration across likely locations
- "very thorough" - Comprehensive analysis, multiple naming conventions

### Step 4: Wait for ALL Agents to Complete

**CRITICAL**: Do not synthesize until all exploration is complete.

```markdown
✅ Task 1 completes → Wait
   Task 2 completes → Wait
   Task 3 completes → NOW synthesize all findings together
```

### Step 5: Synthesize Findings

Connect discoveries across different explorations:
- What patterns emerged?
- How do components relate?
- What's relevant to the research question?
- What file references support each finding?

### Step 6: Create Research Document

Write findings to `research/recon-YYYY-MM-DD-{topic}.md` using:
1. **Metadata** - Date, researcher, scope, status
2. **Executive Summary** - 2-3 sentence key takeaway
3. **Context** - Research questions, scope boundaries
4. **Findings** - Evidence-based discoveries with file:line refs
5. **Key Files** - Prioritized list (High/Medium/Reference)
6. **Patterns** - Architectural/organizational observations
7. **Gaps & Unknowns** - What's unclear or missing
8. **Recommendations** - Actionable next steps

**File reference format:**
```markdown
`path/to/file.ext:123` - Description of what's at this location
```

---

## Parallel Task Pattern

```markdown
# Parallel (fast) ✅
1. Launch structure + patterns + docs exploration simultaneously
2. Wait for ALL to complete
3. Synthesize
```

**When to use parallel:**
- Different areas of codebase (frontend + backend)
- Different types of search (files + patterns + docs)
- Independent research questions

**When to use sequential:**
- Second exploration depends on first results
- Need to refine search based on initial findings

---

## Common Mistakes

### ❌ Starting Without Reading Mentioned Files
### ✅ Read First, Then Explore

### ❌ Synthesizing Before All Tasks Complete
### ✅ Wait Then Synthesize

### ❌ Missing File References
```markdown
"The authentication system uses JWT tokens."
```

### ✅ Evidence-Based Findings
```markdown
"The authentication system uses JWT tokens (`src/auth/jwt.ts:45`)."
```

---

## Research Anti-Patterns

**Don't:**
- Suggest improvements unless explicitly asked
- Critique implementation choices
- Propose refactoring or optimization
- Make recommendations beyond research scope

**Do:**
- Document what exists and where
- Explain how components work
- Identify patterns and conventions
- Provide evidence with file references

---

## Quality Checklist

Before presenting research:
- [ ] All mentioned files read completely
- [ ] All exploration tasks completed
- [ ] Findings synthesized across all sources
- [ ] Every finding has file:line reference
- [ ] Key files prioritized (High/Medium/Reference)
- [ ] Patterns identified and documented
- [ ] Gaps and unknowns noted
- [ ] Research document created and saved
