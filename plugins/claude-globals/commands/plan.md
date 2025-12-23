---
allowed-tools: Task, TodoWrite, Read, Write, Glob, Grep, Bash
argument-hint: [project description] | quick [task] | parallel [project1, project2, ...] | technical [technical project]
description: Comprehensive project planning using specialized planning subagents with research-first approach
---

# Project Planning System

Ultrathink about the planning requirements for: **$ARGUMENTS**

## Planning Context

- Current project state: !`find . -name "*.md" -o -name "package.json" -o -name "*.py" -o -name "*.js" | head -20`
- Existing documentation: @README.md @CLAUDE.md
- Current working directory structure: !`ls -la`

## Planning Modes

Determine the appropriate planning approach based on the arguments:

### Comprehensive Planning (default)
For complex projects requiring full analysis:
1. **Information Gathering** - Use info-gatherer subagent to research all necessary context and requirements
2. **Project Analysis** - Use project-planner subagent to understand scope and architecture
3. **Task Breakdown** - Use task-analyzer subagent to decompose into actionable items for Claude agents
4. **Dependency Mapping** - Use dependency-mapper subagent to identify task sequencing and relationships
5. **Risk Assessment** - Use risk-assessor subagent to identify technical risks and blockers

### Quick Planning (if "quick" in arguments)
For simple tasks requiring rapid breakdown:
1. Use info-gatherer subagent for essential context only
2. Use task-analyzer subagent for immediate task breakdown

### Parallel Planning (if "parallel" in arguments) 
For multiple projects simultaneously:
1. Spawn info-gatherer subagents in parallel for each project
2. Consolidate research and identify cross-project dependencies
3. Create unified execution plan

### Technical Planning (if "technical" in arguments)
For technical projects requiring architecture focus:
1. Enhanced info-gatherer analysis focusing on technical requirements and constraints
2. Architecture-focused project analysis
3. Technical task breakdown with implementation details
4. Technical risk assessment including scalability, maintainability, and integration challenges

## Planning Workflow

1. **Research Phase** (Critical First Step)
   - Create TodoWrite list for planning tasks
   - Set up planning_results/ directory structure
   - Use info-gatherer subagent to collect all necessary information
   - Research existing codebase patterns, dependencies, and constraints

2. **Analysis Phase**
   - Use findings from research to inform project analysis
   - Spawn appropriate planning subagents based on planning mode
   - Each subagent saves results to planning_results/

3. **Synthesis Phase**
   - Combine all subagent findings into actionable plan for Claude agents
   - Focus on task sequencing and execution readiness
   - Save final plan as planning_results/PROJECT_PLAN.md

## Output Structure

The planning system generates:
```
planning_results/
├── research_findings_[timestamp].md    # Information gathering results
├── project_analysis_[timestamp].md     # Project scope and architecture
├── task_breakdown_[timestamp].md       # Detailed tasks for Claude agents
├── dependencies_[timestamp].md         # Task sequencing and relationships
├── risk_assessment_[timestamp].md      # Technical risks and mitigation
└── PROJECT_PLAN.md                     # Final execution-ready plan
```

Begin with comprehensive research and information gathering, then proceed with the planning process adapted to the specific planning mode required by the arguments.