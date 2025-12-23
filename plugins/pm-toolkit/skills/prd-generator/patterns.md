# PRD Generator - Detailed Patterns

## Generation Scope

**GENERATE (60-70% content):**
- Executive Summary
- Problem Statement (current situation, affected users)
- 3-5 Core User Stories with acceptance criteria
- 3-5 Functional Requirements linked to stories

**HYBRID (structure only):**
- User Needs (primary need generated, secondary placeholders)
- Non-Functional Requirements (category structure with example targets)
- Success Metrics (framework, user defines specific KPIs)

**PLACEHOLDER (user completes):**
- Evidence in Problem Statement
- Supporting User Stories
- Design & UX
- Technical Considerations
- Launch Plan

## Content Patterns

### User Stories (3-5):

```markdown
**Story N: [Title]**

**As a** [user type]
**I want** [goal]
**So that** [benefit]

**Acceptance Criteria:**
- [ ] [Specific, testable criterion 1]
- [ ] [Specific, testable criterion 2]
- [ ] [Specific, testable criterion 3]

**Priority:** High | Medium | Low
```

### Functional Requirements (3-5):

```markdown
**Requirement N: [Title]**

**Description:** [System behavior]
**Rationale:** [Why, linked to user story]
**User Story:** Links to Story N

**Acceptance Criteria:**
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Edge Cases:**
- [Case 1] - [Expected behavior]

**Priority:** Must Have | Should Have | Nice to Have
```

## Validation Checklist

**Completeness:**
- [ ] All required sections present
- [ ] Executive Summary >= 100 words
- [ ] At least 3 user stories
- [ ] Each story has 3+ acceptance criteria
- [ ] At least 3 functional requirements

**Format:**
- [ ] Valid markdown syntax
- [ ] Correct header hierarchy
- [ ] As-a/I-want/So-that format
- [ ] Checkbox format for criteria

**Quality:**
- [ ] Testable acceptance criteria (no vague terms)
- [ ] User stories represent user value
- [ ] Executive Summary is concise

## Success Report

```
PRD created successfully!

Location: prds/{YYYY-MM-DD-{feature-slug}}.md
Feature: {feature_name}

Generated Content:
✓ Executive Summary
✓ Problem Statement with affected users
✓ {N} Core User Stories with acceptance criteria
✓ {N} Functional Requirements

Placeholders for Manual Completion (~25-30% remaining):
- [ ] Evidence in Problem Statement
- [ ] Non-functional requirements specific values
- [ ] Success metrics specific KPIs
- [ ] Design & UX section
- [ ] Launch Plan section
```

## Common Mistakes

**❌ Fabricating Evidence**
Leave Evidence section as placeholder - user adds real data

**❌ Including Implementation Details**
PRD = WHAT to build. No API designs, database schemas, tech choices.

**❌ Vague Acceptance Criteria**
"Fast" is not testable. "< 2 seconds P95" is testable.

**❌ Overgenerating Content**
Follow GENERATE/HYBRID/PLACEHOLDER scope. Don't fill placeholder sections.

## Quality Target

Generated PRDs require ~25-30% manual editing to be production-ready.

---

**Template:** `templates/prd-template.md`
**Output:** `prds/YYYY-MM-DD-{feature-slug}.md`
