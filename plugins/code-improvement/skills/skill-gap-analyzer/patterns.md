# Gap Detection Patterns

## Detection Heuristics

### Repeated Explanations

**Signal**: Claude explains the same concept multiple times.

**Detection markers:**
- "As I mentioned earlier..."
- "To reiterate..."
- "Remember that..."
- Similar paragraphs appearing in different responses

**Threshold**: 3+ occurrences → HIGH confidence gap

**Example:**
```
Turn 5: "In this project, we use Vitest, not Jest..."
Turn 12: "Remember, use Vitest for testing..."
Turn 23: "We use Vitest here, not Jest..."

→ Gap: Testing conventions not documented
→ Action: Add to CLAUDE.md or create skill
```

### Repeated Corrections

**Signal**: User corrects Claude on the same issue.

**Detection markers:**
- User: "No, actually..."
- User: "That's not right..."
- User: "We don't do it that way..."
- Same correction pattern appearing multiple times

**Threshold**: 2+ occurrences → HIGH confidence gap (corrections are costly)

**Example:**
```
Turn 7: User: "No, run tests before committing"
Turn 15: User: "You need to run tests first"

→ Gap: Pre-commit testing discipline
→ Action: Create skill with Iron Law
```

### Similar Workflows

**Signal**: Same sequence of actions repeated.

**Detection markers:**
- Same tool calls in same order
- Similar file patterns accessed
- Repeated multi-step processes

**Threshold**: 3+ occurrences → MEDIUM confidence gap

**Example:**
```
Session 1: grep → read file → edit → run test
Session 2: grep → read file → edit → run test
Session 3: grep → read file → edit → run test

→ Gap: Common editing workflow
→ Action: Create command
```

### Same Questions Asked

**Signal**: User asks the same or similar questions.

**Detection markers:**
- "How do I..."
- "What's the..."
- "Where is..."
- Question patterns recurring

**Threshold**: 2+ occurrences → MEDIUM confidence gap

**Example:**
```
Session 1: "Where are the test files?"
Session 3: "Which directory has tests?"

→ Gap: Project structure documentation
→ Action: Add to CLAUDE.md
```

## Gap Categories and Responses

### Behavioral Gaps

**Characteristic**: Claude should always/never do something.

**Indicators:**
- User corrections about behavior
- "Remember to..."
- "Don't forget to..."
- "Always..." / "Never..."

**Response**: Create skill with Iron Law section

**Template:**
```markdown
## Iron Law

```
ALWAYS [do thing]
NEVER [avoid thing]
No exceptions.
```
```

### Informational Gaps

**Characteristic**: Claude lacks project-specific knowledge.

**Indicators:**
- Repeated explanations of same concept
- "In this project..."
- "Our convention is..."
- Technical decisions explained multiple times

**Response**: Create reference skill or CLAUDE.md entry

### Procedural Gaps

**Characteristic**: Multi-step process repeated frequently.

**Indicators:**
- Same sequence of actions
- Workflow patterns
- "First... then... finally..."
- Recipe-like instructions

**Response**: Create command

### Contextual Gaps

**Characteristic**: Missing project-specific context.

**Indicators:**
- "We use X, not Y"
- Technology stack clarifications
- Naming convention corrections
- Architecture explanations

**Response**: Add to CLAUDE.md

## Confidence Scoring

| Factor | Points |
|--------|--------|
| User correction | +3 |
| Repeated explanation | +2 |
| Similar workflow | +1 |
| Same question | +1 |
| Spans multiple sessions | +2 |
| Recent occurrence | +1 |

**Confidence levels:**
- HIGH (7+ points): Create skill immediately
- MEDIUM (4-6 points): Verify with more data
- LOW (1-3 points): Monitor for recurrence

## False Positive Filters

**Not a gap if:**
- Pattern is task-specific, not generalizable
- User explicitly asked for repetition
- Pattern only appears once
- Pattern is already covered by existing skill
- Pattern is about external system (not our codebase)

## Gap Documentation Template

```markdown
## Gap: [Name]

### Evidence
| Session | Turn | Pattern | Type |
|---------|------|---------|------|
| 2025-01-15 | 12 | "Use Vitest" | Correction |
| 2025-01-16 | 5 | "Vitest not Jest" | Explanation |
| 2025-01-17 | 23 | "We use Vitest" | Explanation |

### Classification
- **Category**: Informational
- **Frequency**: 3x in 3 sessions
- **Confidence**: HIGH (7 points)
- **Impact**: Medium (testing workflow)

### Recommended Action
Create CLAUDE.md entry:
```markdown
## Testing
- Use Vitest (NOT Jest) for all tests
- Test directory: `tests/`
```

### Verification
- [ ] Check if pattern continues after fix
- [ ] Measure reduction in corrections
```

## Integration with Learning Capture

The gap analyzer feeds into the continuous learning system:

```
Session Telemetry → Pattern Detection → Gap Analysis → Skill Suggestion
                                              ↓
                                    Human Approval → Skill Creation
```

This creates a feedback loop where repeated patterns automatically surface as skill candidates.
