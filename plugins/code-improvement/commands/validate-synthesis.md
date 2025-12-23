---
name: validate-synthesis
description: Validate synthesis guides for attribution accuracy, source agreement, and coverage completeness
model: opus
---

# Validate Synthesis

You are validating synthesis guides in `guides/use-cases/*/index.md` for accuracy against their source analyses.

## Process

### Step 1: Inventory Guides and Sources

**Find all guides:**
```
guides/use-cases/*/index.md
```

**Find all source analyses:**
```
references/analysis_*.md
```

Create mapping of which sources should inform which guides (based on use case tags).

### Step 2: Define Validation Criteria

**Structural Requirements:**
- Quick Answer (1 sentence)
- The Problem + Signs you need this (3+ symptoms)
- The Solution + supporting quote
- Key Principles (2+ with source attribution)
- Step-by-Step Guide (3+ steps)
- Patterns & Templates (1+ template)
- Common Mistakes (2+ documented)
- Sources table

**Attribution Accuracy:**
- Every pattern/principle cites source
- Claims accurately represent sources
- Quotes are not out of context

**Agreement Verification:**
- High confidence claims have 3+ supporting sources
- Claimed agreements are real (sources actually agree)
- Single-source patterns marked appropriately

**Coverage Completeness:**
Expected topics by guide (from plan):
- context-management: dumb zone, compaction, progressive disclosure, subagent isolation
- debugging-verification: evidence-first, root cause, quality gates, hypothesis testing
- complex-codebases: RPI/EPCC workflow, research phase, planning, mental alignment
- reusable-tooling: skills structure, progressive disclosure, trigger words, token budgets
- team-setup: CLAUDE.md patterns, settings.json, permissions, enterprise config
- parallel-agents: delegation patterns, model selection, context isolation, coordination

### Step 3: Validate Each Guide

For each guide, perform deep validation:

**3a. Structure Check**
- Read guide completely
- Check all required sections present
- Verify section content meets minimums

**3b. Source Verification**
- Read Sources table
- Verify each cited source file exists
- For broken sources, note correct filename if obvious

**3c. Attribution Accuracy (Sample)**
Select 5 major claims from the guide:
1. Find the cited source
2. Read the relevant section
3. Verify claim accurately represents source
4. Flag any misrepresentations

**3d. Agreement Verification**
For each pattern claiming "best practice" or "agreed":
1. Count actual supporting sources
2. Verify sources explicitly agree (not just mention similar topic)
3. Flag false agreements

**3e. Coverage Assessment**
Compare guide content against expected topics for this use case:
- Mark covered topics
- Note missing topics
- Identify novel additions (good thing)

**3f. Cross-Reference Check**
- Find all links to other guides
- Verify each link path is valid

### Step 4: Generate Report

```markdown
# Synthesis Validation Report

**Generated**: [Date]
**Guides Validated**: [N]
**Average Score**: [X]/100

## Summary

| Guide | Structure | Attribution | Agreement | Coverage | Score | Tier |
|-------|-----------|-------------|-----------|----------|-------|------|
| context-management | 9/9 | 95% | High | 100% | 92 | Production |
| debugging-verification | 8/9 | 87% | Medium | 75% | 78 | Review |
| ... | ... | ... | ... | ... | ... | ... |

---

## Detailed Results

### context-management (Score: 92)

**Status**: PASS - Production Quality

#### Structure: 9/9 sections ✓

#### Attribution Accuracy: 95%
- Claims checked: 20
- Accurate: 19
- Issue: Line 45 overstates source agreement

**Issue Detail:**
> Guide claims: "All sources agree on the 40% threshold"
> Reality: Only Dex Horthy provides specific percentage
> Fix: Revise to "Dex Horthy recommends 40% as the threshold"

#### Agreement Verification: High ✓
| Pattern | Claimed | Actual | Status |
|---------|---------|--------|--------|
| Dumb zone concept | High | 3 sources | ✓ |
| Compaction strategy | High | 4 sources | ✓ |
| Progressive disclosure | Medium | 2 sources | ✓ |

#### Coverage: 4/4 topics (100%)
- ✓ Dumb zone
- ✓ Compaction
- ✓ Progressive disclosure
- ✓ Subagent isolation

#### Cross-References: 3 links, all valid ✓

---

### debugging-verification (Score: 78)

**Status**: FAIL - Needs Review

#### Structure: 8/9 sections
- ✗ Missing: Conflicting Advice section

#### Attribution Accuracy: 87%
**Issues Found:**

1. **Misrepresentation at Line 67**
   - Claim: "AI should never fix bugs directly"
   - Source says: "Don't let AI fix right away"
   - Issue: Different meaning - source allows AI fixes after investigation
   - Fix: Revise to match source intent

2. **Broken Source Reference**
   - Cited: `analysis_romanticize_code.md`
   - Actual: `analysis_transcript_RivViRdBlII.md`
   - Fix: Update reference path

#### Agreement Verification: Medium
| Pattern | Claimed | Actual | Status |
|---------|---------|--------|--------|
| Evidence-first | High | 3 sources | ✓ |
| Root cause analysis | High | 2 sources | ⚠ Overstated |
| Hypothesis testing | Medium | 1 source | ✗ Should be Low |

#### Coverage: 3/4 topics (75%)
- ✓ Evidence-first
- ✓ Root cause
- ✓ Quality gates
- ✗ Missing: Hypothesis testing

#### Cross-References: 2 links
- ✗ `./complex-codebases` - broken (should be `../complex-codebases/`)

---

## False Agreements Detected

| Guide | Pattern | Claimed | Actual | Fix |
|-------|---------|---------|--------|-----|
| debugging | Root cause emphasis | High | 2 sources | Lower to Medium |
| parallel-agents | Always use Sonnet | High | 1 source | Mark as emerging |

## Coverage Gaps

| Guide | Missing Topics | Suggested Sources |
|-------|----------------|-------------------|
| debugging | Hypothesis testing | analysis_transcript_RivViRdBlII.md |
| team-setup | Enterprise OIDC | analysis_repo_bedrock.md |

## Broken References

| Guide | Type | Broken | Correct |
|-------|------|--------|---------|
| debugging | Source | analysis_romanticize_code.md | analysis_transcript_RivViRdBlII.md |
| debugging | Cross-ref | ./complex-codebases | ../complex-codebases/ |

---

## Remediation Priority

### Critical (Accuracy issues)
1. **debugging:L67** - Revise misrepresented claim about AI fixes
2. **debugging** - Add Conflicting Advice section

### High (Completeness issues)
1. **debugging** - Add Hypothesis testing topic
2. **team-setup** - Expand Enterprise OIDC section

### Medium (Polish)
1. **debugging** - Fix broken source reference
2. **debugging** - Fix cross-reference path
3. **parallel-agents** - Downgrade single-source pattern confidence

---

## Next Steps

1. Fix [N] critical accuracy issues immediately
2. Address [N] coverage gaps
3. Update [N] broken references
4. Re-run validation: `/validate-synthesis`
```

## Important Notes

- Use the `synthesis-validator` agent for deep validation of individual guides
- For attribution checking, sample 5-10 major claims (don't check every sentence)
- "Sources agree" means they explicitly recommend the same approach, not just mention similar topics
- Novel patterns (not from sources) are OK if clearly marked as such

## Output Format

```markdown
# Synthesis Validation Report

**Generated**: [Date]
**Guides Validated**: [N]
**Average Score**: [X]/100

## Summary

| Guide | Structure | Attribution | Agreement | Coverage | Score | Tier |
|-------|-----------|-------------|-----------|----------|-------|------|

## Detailed Results
[Per-guide breakdowns with issues]

## Remediation Priority
### Critical / High / Medium
[Prioritized fix list]
```

## Success Criteria

Validation is complete when:
- [ ] All 6 use-case guides validated
- [ ] Attribution accuracy checked for each
- [ ] Agreement levels verified against actual sources
- [ ] Coverage gaps identified
- [ ] Cross-references validated
- [ ] Prioritized remediation list produced
