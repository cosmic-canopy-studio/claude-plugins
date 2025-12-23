# Transcript Processor - Detailed Patterns

## Output Template

```markdown
# Meeting Summary: [Meeting Title/Topic]

**Date:** YYYY-MM-DD
**Duration:** [X minutes]
**Participants:** [Names if known]
**Source:** [Transcript file]

---

## Executive Summary

[2-3 sentences: main purpose, key outcome, critical action]

---

## Topics Discussed

### Topic 1: [Topic Name]

**Summary:** [Brief summary of discussion]

**Key Points:**
- [Point 1]
- [Point 2]

**Outcome:** [Decision or next step]

---

## Decisions Made

| Decision | Context | Owner | Date |
|----------|---------|-------|------|
| [Decision 1] | [Why/context] | [Who] | [When] |
| [Decision 2] | [Why/context] | [Who] | [When] |

---

## Action Items

| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| [Action 1] | [Name] | [Date] | High/Med/Low |
| [Action 2] | [Name] | [Date] | High/Med/Low |

---

## Key Insights

1. **[Insight 1]**
   - Context: [What led to this insight]
   - Implication: [What it means]

---

## Concerns Raised

| Concern | Raised By | Status |
|---------|-----------|--------|
| [Concern 1] | [Name] | Open/Addressed |

---

## Open Questions

1. [Question 1] - Owner: [Who will answer]
2. [Question 2] - Owner: [Who will answer]

---

## Follow-up Required

- [ ] [Follow-up 1]
- [ ] [Follow-up 2]

---

## Raw Quotes (Notable)

> "[Important quote]" - [Speaker]

---

## Processing Notes

**Confidence:** High | Medium | Low
**Ambiguities:** [Items that were unclear]
**Missing context:** [What wasn't captured]
```

## Extraction Patterns

### Decision Detection
Look for:
- "We decided to..."
- "Let's go with..."
- "The decision is..."
- "We're going to..."
- "Agreed that..."

### Action Item Detection
Look for:
- "[Name] will..."
- "Action item:"
- "TODO:"
- "Next step is..."
- "Can you..."
- "Please..."

### Concern Detection
Look for:
- "I'm worried about..."
- "Risk is..."
- "The problem is..."
- "Concern:"
- "What if..."

## Processing Flow

1. **Topic Detection**
   - Identify main topics discussed
   - Classify by theme/area
   - Note topic transitions

2. **Information Extraction**
   - **Decisions:** Clear choices made
   - **Action Items:** Tasks assigned
   - **Insights:** Key observations
   - **Concerns:** Risks or issues raised
   - **Open Questions:** Unresolved items

3. **Attribution**
   - Who said what (if identifiable)
   - When decisions were made
   - Who owns action items

4. **Summary Generation**
   - Executive summary
   - Topic-by-topic breakdown
   - Prioritized action items

## Quality Rules

- Mark unclear attributions as "[Unknown]"
- Note confidence level for extracted items
- Flag ambiguous decisions for clarification
- Don't fabricate missing information

---

**Template:** `templates/transcript-summary-template.md`
**Output:** `meetings/YYYY-MM-DD-{topic}.md`
