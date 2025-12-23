---
name: transcript-processor
description: Use when processing meeting content - extracts decisions, action items, insights, and concerns from transcripts
when_to_use: process meeting, extract action items, summarize discussion, meeting notes, what was decided, transcript summary
plan_mode: write
---

# Transcript Processor

## Quick Start

| You Say | Result |
|---------|--------|
| "Process this meeting transcript" | Summary at `meetings/YYYY-MM-DD-{topic}.md` |
| "What action items came from this?" | Extracted actions with owners and priorities |
| "What was decided in this meeting?" | Decisions with context and follow-ups |

## Announcement
"I'm using the transcript-processor to analyze [meeting/discussion]..."

## Process
1. Read transcript or meeting content
2. Detect topics discussed
3. Extract decisions, action items, insights, concerns
4. Attribute to speakers where identifiable
5. Generate executive summary
6. Save to `meetings/YYYY-MM-DD-{topic}.md`

## Output
Meeting summary with:
- Executive summary (purpose, outcome, critical action)
- Topics discussed with key points
- Decisions made (table with context, owner, date)
- Action items (table with owner, due, priority)
- Key insights with implications
- Concerns raised with status
- Open questions with owners

## Extraction Patterns
- **Decisions**: "We decided...", "Let's go with...", "Agreed that..."
- **Actions**: "[Name] will...", "TODO:", "Next step is..."
- **Concerns**: "I'm worried about...", "Risk is...", "The problem is..."

## Quality Rules
- Mark unclear attributions as "[Unknown]"
- Note confidence level for extracted items
- Don't fabricate missing information

## Transitions
- **Before**: User provides meeting transcript or notes
- **After**: decision-documenter (formal decision record) or task-breakdown (action planning)

See [patterns.md](patterns.md) for extraction patterns and template.
