---
name: godot-pattern-researcher
description: Researches and synthesizes game development patterns from multiple sources with conflict resolution. Use when you need to validate patterns across official docs, community examples, and existing skills; resolve contradictory implementations; or create comprehensive pattern documentation with static typing.
allowed-tools: Read, Grep, Glob, Bash
---

# Pattern Researcher

Research patterns across multiple sources and synthesize findings into comprehensive documentation with working, static-typed code examples.

## Quick Start

```gdscript
extends Node

# Research any game development pattern with conflict resolution
func _ready() -> void:
    var researcher := PatternResearcher.new()

    # Research pattern with multiple sources and automatic conflict resolution
    var findings: PatternFindings = researcher.research_pattern(
        "Singleton",
        ["official", "community", "godot-autoloads"]
    )

    # Get resolved implementation with Godot best practices
    var godot_implementation: String = findings.get_resolved_implementation()
    print("Godot-optimized implementation:\n", godot_implementation)

    # Generate comprehensive documentation
    var docs: String = findings.generate_documentation()
    save_pattern_documentation(docs)
```

## Multi-Source Research

### Basic Pattern Research
```gdscript
# Research pattern with default sources
extends Node

func research_pattern_basic(pattern_name: String) -> void:
    var researcher := PatternResearcher.new()
    var findings: PatternFindings = researcher.research_pattern(pattern_name)

    # Auto-resolves conflicts using priority: official > examples > community
    if findings.has_conflicts():
        print("Resolved conflicts for pattern: ", pattern_name)

    # Get Godot-specific implementation
    var code := findings.generate_code_example("godot-optimized")
    create_pattern_file(pattern_name.to_lower() + ".gd", code)
```

### Advanced Research with Custom Rules
```gdscript
# Custom research with specific conflict resolution rules
extends Node

func research_with_rules(pattern_name: String) -> void:
    var researcher := PatternResearcher.new()

    # Set custom source priority
    researcher.set_priority_order([
        "official",
        "godot-skills",
        "community-examples",
        "tutorials"
    ])

    # Add validation rules for Godot patterns
    researcher.add_validation_rule(func(impl: String) -> bool:
        return impl.contains("static var") or impl.contains("signal")
    )

    var findings: PatternFindings = researcher.research_pattern(
        pattern_name,
        ["official", "godot-skills", "community"]
    )

    # Generate implementation with Godot-specific optimizations
    var optimized_code := findings.apply_godot_optimizations()
    print("Optimized Godot implementation:\n", optimized_code)
```

## Conflict Resolution

### Automatic Conflict Resolution
```gdscript
# Let the researcher resolve conflicts automatically
extends Node

func auto_resolve_conflicts(pattern_name: String) -> void:
    var researcher := PatternResearcher.new()
    var findings: PatternFindings = researcher.research_pattern(pattern_name)

    # Check what conflicts were found and resolved
    var resolution_log: Array[String] = findings.get_resolution_log()
    for log_entry in resolution_log:
        print("Conflict resolved: ", log_entry)

    # Get the final resolved implementation
    var final_code := findings.get_resolved_code()
    print("Final implementation:\n", final_code)
```

### Manual Conflict Resolution
```gdscript
# Manually review and resolve conflicts
extends Node

func manual_conflict_resolution(pattern_name: String) -> void:
    var researcher := PatternResearcher.new()
    var findings: PatternFindings = researcher.research_pattern(pattern_name)

    if findings.has_conflicts():
        var conflicts := findings.get_conflicts()

        for conflict in conflicts:
            print("\nConflict detected:")
            print("Source A: ", conflict.source_a, " - ", conflict.impl_a)
            print("Source B: ", conflict.source_b, " - ", conflict.impl_b)

            # Choose preferred implementation
            var choice: int = await prompt_user_choice(conflict)
            findings.resolve_conflict(conflict.id, choice)

    # Generate code with manual resolutions applied
    var resolved_code := findings.generate_code_example()
    save_implementation(pattern_name, resolved_code)
```

## Pattern Integration

### Link to Existing Skills
```gdscript
# Cross-reference pattern with existing godot-* skills
extends Node

func integrate_with_skills(pattern_name: String) -> void:
    var researcher := PatternResearcher.new()
    var findings: PatternFindings = researcher.research_pattern(pattern_name)

    # Find related godot-* skills
    var related_skills := findings.find_related_skills()
    print("Related existing skills:")

    for skill in related_skills:
        print("- ", skill.name, ": ", skill.description)
        print("  Pattern overlap: ", skill.overlap_percentage, "%")

    # Generate documentation with skill cross-references
    var docs := findings.generate_cross_referenced_docs(related_skills)
    save_skill_integration_docs(pattern_name, docs)
```

### Pattern Validation
```gdscript
# Validate pattern implementation against Godot best practices
extends Node

func validate_pattern_implementation(pattern_name: String, implementation: String) -> void:
    var researcher := PatternResearcher.new()
    var validator := researcher.get_validator()

    # Check for static typing compliance
    var typing_score: float = validator.check_static_typing(implementation)
    print("Static typing score: ", typing_score)

    # Validate Godot-specific optimizations
    var optimizations := validator.validate_godot_optimizations(implementation)
    for opt in optimizations:
        print("Optimization: ", opt.type, " - ", opt.recommendation)

    # Check for integration with existing skills
    var integration_score := validator.check_skill_integration(pattern_name, implementation)
    print("Skill integration score: ", integration_score)
```

## Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `default_sources` | `Array[String]` | `["official", "godot-skills", "community"]` | Default research sources |
| `conflict_resolution` | `String` | `"auto"` | Conflict resolution: "auto", "manual", "priority" |
| `source_priority` | `Array[String]` | `["official", "godot-skills", "examples", "community"]` | Priority order for conflicts |
| `require_static_typing` | `bool` | `true` | Enforce static typing in all generated code |
| `godot_version` | `String` | `"4.3"` | Target Godot version for compatibility checks |
| `include_performance_notes` | `bool` | `true` | Add performance considerations to documentation |

## Related Skills

- **godot-autoloads** - Singleton pattern implementations and global managers
- **godot-event-bus** - Observer pattern for decoupled communication
- **godot-custom-resources** - Factory pattern for resource management
- **godot-enums** - Strategy pattern for type-safe state machines
- **godot-dictionaries** - Memento pattern for save systems

## See Also

- [patterns.md](patterns.md) - Complete pattern research workflows
- [reference.md](reference.md) - API reference for research classes
- [examples/](examples/) - Working research examples