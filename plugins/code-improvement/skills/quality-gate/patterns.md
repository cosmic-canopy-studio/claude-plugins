# Quality Gate Patterns

## Analysis Document Validation

### Required Sections (Transcripts)
- [ ] Overview
- [ ] Key Insights (3+)
- [ ] Novel Patterns
- [ ] Conflicts/Disagreements
- [ ] Takeaways (3+)
- [ ] Cross-References

### Required Sections (Repos)
- [ ] Structure
- [ ] Commands
- [ ] Agents
- [ ] Skills
- [ ] CLAUDE.md Analysis
- [ ] Novel Patterns
- [ ] Takeaways

### Evidence Thresholds
- Quotes: ≥5 with attribution
- Use case tags: ≥3 distinct
- File refs (repos): ≥10

---

## Synthesis Guide Validation

### 8 Required Sections
1. **Quick Answer** - 1 sentence
2. **The Problem** - Signs you need this (3+ symptoms)
3. **The Solution** - With supporting quote
4. **Key Principles** - 2+ with source attribution
5. **Step-by-Step Guide** - 3+ steps
6. **Patterns & Templates** - 1+ template
7. **Common Mistakes** - 2+ documented
8. **Sources** - Attribution table

### Attribution Check
Sample 5 claims:
1. Find claimed source in `references/analysis_*.md`
2. Verify claim accurately represents source
3. Flag misrepresentations (reversed meaning, out of context)

### Agreement Check
For "best practice" or "agreed" claims:
- Count actual supporting sources
- "High" confidence requires 3+ explicit agreements
- Verify sources agree explicitly (not just similar topic)

### Coverage Check by Guide Type

**context-management:**
- dumb zone, compaction, progressive disclosure, subagent isolation

**debugging-verification:**
- evidence-first, root cause, quality gates, hypothesis testing

**complex-codebases:**
- RPI/EPCC workflow, research phase, planning, mental alignment

**reusable-tooling:**
- skills structure, progressive disclosure, trigger words, token budgets

**team-setup:**
- CLAUDE.md patterns, settings.json, permissions, enterprise config

**parallel-agents:**
- delegation patterns, model selection, context isolation, coordination

---

## Pipeline Audit

### Score Thresholds
| Metric | Minimum |
|--------|---------|
| Analysis Quality | ≥70% |
| Synthesis Quality | ≥70% |
| Pipeline Health | ≥70% |

### Audit Command
```bash
/audit-pipeline
```
