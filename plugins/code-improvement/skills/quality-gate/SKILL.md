---
name: quality-gate
description: Use when completing analysis documents, finishing synthesis guides, or claiming pipeline work is done - enforces validation before proceeding to next phase (project) - when about to mark analysis complete, synthesis finished, batch processing done, or pipeline ready for use
when_to_use: when about to mark analysis complete, synthesis finished, batch processing done, or pipeline ready for use
---

# Quality Gate

Enforce validation at workflow boundaries. Auto-triggers when claiming work is complete.

## Quick Reference

| Trigger | Validation | Pass Criteria |
|---------|------------|---------------|
| "Analysis complete" | Run analysis-validator | Sections + evidence thresholds |
| "Domains extracted" | Run validate-domains | Patterns + provenance + cross-refs |
| "Synthesis finished" | Run synthesis-validator | Attribution + agreement + coverage |
| "Pipeline ready" | Run audit-pipeline | All scores ≥70% |

## Activation Triggers

Feel this skill activate when about to:
- Say "the analysis is done"
- Mark source as "Analyzed" in INTAKE.md
- Claim domain extraction is "complete"
- Claim guide is "ready for use"
- Suggest archiving completed work

## Gate Protocol

### Analysis Completion
1. **Self-Check**: All required sections present?
2. **Evidence**: Quotes ≥5, Use case tags ≥3
3. Pass → proceed; Fail → extract more from source

### Domain Extraction Completion
1. **Pattern Count**: Each domain has ≥5 patterns
2. **Provenance**: Every pattern has source mapping
3. **Cross-refs**: Domain links resolve correctly
4. Pass → proceed to synthesis; Fail → run domain-extractor

### Synthesis Completion
1. **Structure**: 8 required sections present
2. **Attribution**: Sample 5 claims, verify accuracy
3. **Agreement**: 3+ sources for "High" confidence claims
4. Pass → report score; Fail → fix issues

### Pipeline Completion
1. Run `/audit-pipeline`
2. All scores ≥70%
3. Pass → ready for use; Fail → address issues

See [patterns.md](patterns.md) for detailed validation checklists.
See [reference.md](reference.md) for report formats and common mistakes.

## Rationalization Prevention

**⚠️ Common excuses for skipping validation - DON'T ACCEPT THEM.**

| Excuse | Reality | Correct Action |
|--------|---------|----------------|
| "It's just a small analysis" | Small analyses still need 5 quotes minimum | Run full validation |
| "I'll validate later" | Validation after submission defeats the purpose | Validate NOW |
| "The source doesn't have enough content" | Document the limitation explicitly | Mark incomplete, don't skip |
| "The validation is too strict" | Standards exist for downstream quality | Meet them or document failure |
| "I'm confident it's good" | Confidence without evidence is rationalization | Show the evidence |
| "It's obvious this passes" | Obvious claims still need checkmarks | Complete the checklist |
| "Time pressure / moving fast" | Speed without quality creates rework | Slow down, validate |

**If you catch yourself making excuses, that's the signal to be MORE rigorous, not less.**

### Rationalization Self-Check

Before bypassing ANY validation step:
1. Write down the exact reason you want to skip
2. Ask: "Would I accept this excuse from someone else?"
3. If the answer is no → Don't skip
4. If still tempted → Ask user for explicit permission

## Integration

- `verification-before-completion` - Code/implementation work
- `systematic-debugging` - Bug investigation
- `knowledge-pipeline` - Workflow orchestration
