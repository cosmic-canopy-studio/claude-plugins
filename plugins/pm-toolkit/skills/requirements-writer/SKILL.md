---
name: requirements-writer
description: Use when detailing feature specifications - generates functional requirements with acceptance criteria from PRD or feature description
when_to_use: detailed requirements, acceptance criteria, functional spec, expand the requirements, what should it do exactly
plan_mode: write
---

# Requirements Writer

## Quick Start

| You Say | Result |
|---------|--------|
| "Detail the requirements for this PRD" | Requirements doc with acceptance criteria |
| "Write acceptance criteria for X" | Testable criteria in Given/When/Then format |
| "Expand these user stories" | Full functional requirements with edge cases |

## Announcement
"I'm using the requirements-writer to generate detailed requirements for [feature]..."

## Process
1. Read PRD if provided, extract user stories
2. Expand requirements into detailed specifications
3. Add non-functional requirements with targets
4. Create user scenarios for key workflows
5. Validate completeness and testability
6. Save to `requirements/YYYY-MM-DD-{feature-slug}.md`

## Output
Requirements document with:
- Functional requirements (FR-001, FR-002...)
- Acceptance criteria (Given/When/Then)
- Edge cases with expected behavior
- Non-functional requirements (performance, security)
- User scenarios with steps
- Constraints and dependencies

## Quality Criteria
- Every requirement is testable
- Every requirement has acceptance criteria
- No implementation details (WHAT, not HOW)
- Clear traceability to user stories

## Transitions
- **Before**: prd-generator (PRD exists) or brief-generator (scope defined)
- **After**: task-breakdown (implementation planning)

See [patterns.md](patterns.md) for requirement template and patterns.
