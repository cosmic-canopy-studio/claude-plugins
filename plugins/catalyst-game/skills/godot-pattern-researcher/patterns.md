# Godot Pattern Researcher Patterns

## Multi-Source Research Workflow

**Problem:** You need to research a game development pattern but don't know which sources to trust or how to resolve contradictory information between them.

**Solution:** Use a systematic research workflow that prioritizes sources, validates implementations, and resolves conflicts according to Godot best practices.

```gdscript
# Complete multi-source pattern research workflow
extends Node
class_name MultiSourcePatternResearcher

signal research_progress_updated(stage: String, progress: float)
signal conflict_detected(conflict: PatternConflict)
signal research_completed(findings: PatternFindings)

enum SourceType {
    OFFICIAL,       # Godot documentation and official examples
    SKILL_EXAMPLES, # Existing godot-* skills (tested and validated)
    COMMUNITY,      # Community tutorials and examples
    TUTORIALS,      # Video tutorials and blog posts
    FORUMS          # Forum discussions and Q&A
}

# Priority order for conflict resolution
const SOURCE_PRIORITY: Array[SourceType] = [
    SourceType.OFFICIAL,
    SourceType.SKILL_EXAMPLES,
    SourceType.COMMUNITY,
    SourceType.TUTORIALS,
    SourceType.FORUMS
]

func research_pattern(pattern_name: String, sources: Array[SourceType] = SOURCE_PRIORITY) -> PatternFindings:
    """Research pattern across multiple sources with conflict resolution."""
    var findings := PatternFindings.new()
    findings.pattern_name = pattern_name

    # Stage 1: Gather data from all sources
    research_progress_updated.emit("gathering", 0.0)
    for i in range(sources.size()):
        var source_type: SourceType = sources[i]
        var source_findings := _gather_from_source(source_type, pattern_name)
        findings.add_source_findings(source_type, source_findings)

        var progress: float = float(i + 1) / float(sources.size())
        research_progress_updated.emit("gathering", progress)

    # Stage 2: Detect and analyze conflicts
    research_progress_updated.emit("analyzing", 0.0)
    var conflicts := findings.detect_conflicts()
    for conflict in conflicts:
        conflict_detected.emit(conflict)

    # Stage 3: Resolve conflicts using priority rules
    research_progress_updated.emit("resolving", 0.0)
    findings.resolve_conflicts(SOURCE_PRIORITY)

    # Stage 4: Synthesize final implementation
    research_progress_updated.emit("synthesizing", 0.5)
    findings.synthesize_implementation()

    # Stage 5: Validate against Godot best practices
    research_progress_updated.emit("validating", 0.75)
    findings.validate_implementation()

    research_progress_updated.emit("complete", 1.0)
    research_completed.emit(findings)

    return findings

func _gather_from_source(source_type: SourceType, pattern_name: String) -> Dictionary:
    """Gather pattern information from a specific source type."""
    var source_data := {}

    match source_type:
        SourceType.OFFICIAL:
            source_data = _search_official_documentation(pattern_name)
        SourceType.SKILL_EXAMPLES:
            source_data = _search_existing_skills(pattern_name)
        SourceType.COMMUNITY:
            source_data = _search_community_examples(pattern_name)
        SourceType.TUTORIALS:
            source_data = _search_tutorials(pattern_name)
        SourceType.FORUMS:
            source_data = _search_forum_discussions(pattern_name)

    return source_data
```

**Variations:**
- **Quick Research**: Only uses OFFICIAL and SKILL_EXAMPLES sources
- **Deep Research**: Includes all sources with additional validation
- **Custom Priority**: User-defined source priority order

**Tips:**
- Always start with official documentation for the foundation
- Skill examples are pre-validated and often include edge cases
- Community sources provide real-world usage patterns
- Cross-reference multiple sources before resolving conflicts

---

## Conflict Resolution System

**Problem:** Different sources provide conflicting implementations of the same pattern, making it unclear which approach to use.

**Solution:** Use a rule-based conflict resolution system that prioritizes sources based on reliability, validates implementations against Godot best practices, and creates hybrid solutions when appropriate.

```gdscript
# Conflict resolution system for pattern research
extends Node
class_name PatternConflictResolver

class PatternConflict:
    var conflict_id: String
    var pattern_name: String
    var source_a: SourceType
    var source_b: SourceType
    var implementation_a: String
    var implementation_b: String
    var conflict_type: ConflictType
    var severity: ConflictSeverity
    var recommended_resolution: ResolutionType

enum ConflictType {
    IMPLEMENTATION_DIFFERENCE,  # Different code approaches
    NAMING_CONVENTION,         # Different naming styles
    ARCHITECTURAL_VARIATION,   # Different architectural approaches
    BEST_PRACTICE_VIOLATION,   # One violates best practices
    VERSION_SPECIFIC           # Version-specific differences
}

enum ConflictSeverity {
    CRITICAL,    # Must be resolved (e.g., security issues)
    MAJOR,       # Should be resolved (e.g., performance impact)
    MINOR,       # Can be documented (e.g., style differences)
    INFO         # Informational only
}

enum ResolutionType {
    USE_SOURCE_A,      # Prefer implementation from source A
    USE_SOURCE_B,      # Prefer implementation from source B
    HYBRID,           # Combine best of both
    GODOT_OPTIMIZED,  # Use Godot-specific optimization
    DOCUMENT_BOTH      # Document both approaches
}

func resolve_conflict(conflict: PatternConflict) -> ResolutionResult:
    """Resolve a pattern conflict using rule-based logic."""
    var result := ResolutionResult.new()

    # Rule 1: Best practice violations always lose
    if conflict.conflict_type == ConflictType.BEST_PRACTICE_VIOLATION:
        result.resolution_type = _resolve_best_practice_violation(conflict)
        result.confidence = 0.95
        return result

    # Rule 2: Official documentation wins for architectural decisions
    if conflict.conflict_type == ConflictType.ARCHITECTURAL_VARIATION:
        if conflict.source_a == SourceType.OFFICIAL or conflict.source_b == SourceType.OFFICIAL:
            result.resolution_type = ResolutionType.USE_OFFICIAL
            result.confidence = 0.90
            return result

    # Rule 3: Skill examples preferred for working implementations
    if conflict.conflict_type == ConflictType.IMPLEMENTATION_DIFFERENCE:
        if conflict.source_a == SourceType.SKILL_EXAMPLES or conflict.source_b == SourceType.SKILL_EXAMPLES:
            result.resolution_type = ResolutionType.USE_SKILL_EXAMPLE
            result.confidence = 0.85
            return result

    # Rule 4: Check for Godot-specific optimizations
    var godot_optimized := _find_godot_optimization(conflict)
    if godot_optimized.is_valid:
        result.resolution_type = ResolutionType.GODOT_OPTIMIZED
        result.optimized_code = godot_optimized.code
        result.confidence = 0.88
        return result

    # Rule 5: Create hybrid solution for minor differences
    if conflict.severity == ConflictSeverity.MINOR:
        result.resolution_type = ResolutionType.HYBRID
        result.hybrid_code = _create_hybrid_implementation(conflict)
        result.confidence = 0.75
        return result

    # Default: Use source priority
    result.resolution_type = ResolutionType.USE_PRIORITY
    result.selected_source = _get_higher_priority_source(conflict.source_a, conflict.source_b)
    result.confidence = 0.60
    return result

func _find_godot_optimization(conflict: PatternConflict) -> GodotOptimization:
    """Find Godot-specific optimizations that resolve the conflict."""
    var optimization := GodotOptimization.new()

    # Check if one implementation uses Godot signals vs manual callbacks
    if conflict.pattern_name.to_lower() == "observer":
        if conflict.implementation_a.contains("signal") and not conflict.implementation_b.contains("signal"):
            optimization.code = conflict.implementation_a
            optimization.reason = "Godot signals are native and more efficient"
            optimization.is_valid = true
            return optimization

    # Check for static typing in one implementation but not the other
    var has_static_typing_a := _has_static_typing(conflict.implementation_a)
    var has_static_typing_b := _has_static_typing(conflict.implementation_b)

    if has_static_typing_a and not has_static_typing_b:
        optimization.code = conflict.implementation_a
        optimization.reason = "Static typing improves performance and catch errors"
        optimization.is_valid = true
        return optimization
    elif has_static_typing_b and not has_static_typing_a:
        optimization.code = conflict.implementation_b
        optimization.reason = "Static typing improves performance and catch errors"
        optimization.is_valid = true
        return optimization

    # Check for Godot node lifecycle usage
    if _uses_godot_lifecycle(conflict.implementation_a) and not _uses_godot_lifecycle(conflict.implementation_b):
        optimization.code = conflict.implementation_a
        optimization.reason = "Proper integration with Godot node lifecycle"
        optimization.is_valid = true
        return optimization

    optimization.is_valid = false
    return optimization

func _create_hybrid_implementation(conflict: PatternConflict) -> String:
    """Create a hybrid implementation combining the best of both approaches."""
    var hybrid := ""

    # Extract best practices from both implementations
    var best_a := _extract_best_practices(conflict.implementation_a)
    var best_b := _extract_best_practices(conflict.implementation_b)

    # Combine with Godot-specific optimizations
    hybrid += "# Hybrid implementation combining multiple sources\n"
    hybrid += "# Source A: " + str(conflict.source_a) + "\n"
    hybrid += "# Source B: " + str(conflict.source_b) + "\n\n"

    # Add shared structure from the better-architected implementation
    var better_arch := _select_better_architecture(conflict.implementation_a, conflict.implementation_b)
    hybrid += better_arch + "\n\n"

    # Add optimizations from both
    hybrid += "# Optimizations from Source A:\n"
    for practice in best_a:
        hybrid += "#  - " + practice + "\n"

    hybrid += "\n# Optimizations from Source B:\n"
    for practice in best_b:
        hybrid += "#  - " + practice + "\n"

    return hybrid
```

**Variations:**
- **Strict Resolution**: Only uses highest priority source for any conflict
- **Consensus-Based**: Requires multiple sources to agree
- **Performance-First**: Always chooses implementation with better performance characteristics

**Tips:**
- Document all conflict resolutions for transparency
- Consider your project's specific constraints when applying resolutions
- Test resolved implementations thoroughly before use
- Some conflicts may be intentional variations rather than errors

---

## Pattern Synthesis and Documentation Generation

**Problem:** After research and conflict resolution, you need to generate comprehensive documentation that explains the pattern, its variations, and provides working code examples.

**Solution:** Use the pattern synthesis system to create structured documentation that combines research findings, resolved conflicts, and practical examples.

```gdscript
# Pattern synthesis and documentation generation
extends Node
class_name PatternSynthesizer

func generate_comprehensive_documentation(findings: PatternFindings) -> PatternDocumentation:
    """Generate complete pattern documentation from research findings."""
    var docs := PatternDocumentation.new()
    docs.pattern_name = findings.pattern_name

    # Section 1: Pattern Overview
    docs.overview = _generate_overview(findings)

    # Section 2: Implementation Approaches
    docs.implementations = _generate_implementations(findings)

    # Section 3: Conflict Resolutions
    docs.conflict_resolutions = _document_conflict_resolutions(findings)

    # Section 4: Godot-Specific Optimizations
    docs.godot_optimizations = _extract_godot_optimizations(findings)

    # Section 5: Integration Examples
    docs.integration_examples = _create_integration_examples(findings)

    # Section 6: Related Skills
    docs.related_skills = _find_related_skills(findings)

    return docs

func _generate_overview(findings: PatternFindings) -> String:
    """Generate pattern overview section."""
    var overview := ""

    # Start with a clear definition
    overview += "## Overview\n\n"
    overview += findings.get_consensus_description() + "\n\n"

    # Add purpose and use cases
    overview += "### Purpose\n\n"
    overview += findings.get_primary_purpose() + "\n\n"

    overview += "### Common Use Cases\n\n"
    var use_cases := findings.get_all_use_cases()
    for use_case in use_cases:
        overview += "- " + use_case + "\n"
    overview += "\n"

    # Add benefits and trade-offs
    overview += "### Benefits\n\n"
    var benefits := findings.get_consensus_benefits()
    for benefit in benefits:
        overview += "- " + benefit + "\n"
    overview += "\n"

    overview += "### Trade-offs\n\n"
    var tradeoffs := findings.get_documented_tradeoffs()
    for tradeoff in tradeoffs:
        overview += "- " + tradeoff + "\n"

    return overview

func _generate_implementations(findings: PatternFindings) -> Array[PatternImplementation]:
    """Generate implementation examples from resolved findings."""
    var implementations := []

    # Primary implementation (resolved conflicts)
    var primary := PatternImplementation.new()
    primary.title = "Recommended Godot Implementation"
    primary.description = "The recommended implementation with conflicts resolved using Godot best practices"
    primary.code = findings.get_resolved_implementation()
    primary.features = findings.get_resolved_features()
    implementations.append(primary)

    # Alternative implementations for different use cases
    var alternatives := findings.get_alternative_implementations()
    for alt in alternatives:
        var implementation := PatternImplementation.new()
        implementation.title = alt.title
        implementation.description = alt.description
        implementation.code = alt.code
        implementation.features = alt.features
        implementations.append(implementation)

    return implementations

func _extract_godot_optimizations(findings: PatternFindings) -> Array[GodotOptimization]:
    """Extract and document Godot-specific optimizations."""
    var optimizations := []

    # Check for signal optimizations
    var signal_opt := _analyze_signal_usage(findings)
    if signal_opt.is_applicable:
        optimizations.append(signal_opt)

    # Check for node lifecycle optimizations
    var lifecycle_opt := _analyze_lifecycle_usage(findings)
    if lifecycle_opt.is_applicable:
        optimizations.append(lifecycle_opt)

    # Check for static typing benefits
    var typing_opt := _analyze_static_typing(findings)
    if typing_opt.is_applicable:
        optimizations.append(typing_opt)

    # Check for memory management
    var memory_opt := _analyze_memory_management(findings)
    if memory_opt.is_applicable:
        optimizations.append(memory_opt)

    return optimizations

func _create_integration_examples(findings: PatternFindings) -> Array[IntegrationExample]:
    """Create examples showing integration with existing Godot systems."""
    var examples := []

    # Example 1: Integration with scene tree
    var scene_example := IntegrationExample.new()
    scene_example.title = "Scene Tree Integration"
    scene_example.description = "How to integrate the pattern with Godot's scene tree"
    scene_example.code = _generate_scene_integration_code(findings)
    examples.append(scene_example)

    # Example 2: Integration with signals
    var signal_example := IntegrationExample.new()
    signal_example.title = "Signal Integration"
    signal_example.description = "Using Godot signals with the pattern"
    signal_example.code = _generate_signal_integration_code(findings)
    examples.append(signal_example)

    # Example 3: Integration with resources
    var resource_example := IntegrationExample.new()
    resource_example.title = "Resource Integration"
    resource_example.description = "Working with Godot's resource system"
    resource_example.code = _generate_resource_integration_code(findings)
    examples.append(resource_example)

    return examples
```

**Variations:**
- **Quick Reference**: Generates condensed documentation for fast lookup
- **Tutorial Style**: Creates step-by-step tutorial format
- **API Reference**: Focuses on technical specifications

**Tips:**
- Always include working code examples with static typing
- Document the rationale behind conflict resolutions
- Include performance benchmarks when available
- Add troubleshooting sections for common issues

---

## Anti-Patterns

### Don't: Ignore Source Reliability

```gdscript
# BAD - Treating all sources as equally reliable
func bad_pattern_research(pattern_name: String) -> String:
    var sources = ["official", "forum_post", "tutorial", "skill_example"]
    var implementations := []

    # Just concatenate all implementations without validation
    for source in sources:
        var impl := get_implementation(source, pattern_name)
        implementations.append(impl)

    # Return the first one without checking quality
    return implementations[0]
```

```gdscript
# GOOD - Using weighted source reliability and validation
func good_pattern_research(pattern_name: String) -> PatternFindings:
    var researcher := MultiSourcePatternResearcher.new()

    # Research with automatic source prioritization
    var findings := researcher.research_pattern(
        pattern_name,
        [SourceType.OFFICIAL, SourceType.SKILL_EXAMPLES, SourceType.COMMUNITY]
    )

    # Validate the resolved implementation
    var validator := PatternValidator.new()
    var validation_result := validator.validate(findings.get_resolved_implementation())

    if not validation_result.passed:
        # Apply fixes and re-validate
        findings.apply_validation_fixes(validation_result.issues)

    return findings
```

### Don't: Generate Code Without Static Typing

```gdscript
# BAD - Generated code without static typing
func generate_bad_implementation() -> String:
    return """
extends Node

var instance  # No type annotation
var items = []  # Array without type specification

func get_instance():
    return instance

func process_item(item):
    return item.process()
"""
```

```gdscript
# GOOD - Always generate statically-typed code
func generate_good_implementation() -> String:
    return """
extends Node
class_name SingletonPattern

static var instance: SingletonPattern
var items: Array[Node] = []

func get_instance() -> SingletonPattern:
    if not instance:
        instance = SingletonPattern.new()
    return instance

func process_item(item: Node) -> void:
    if item.has_method("process"):
        item.process()
    else:
        push_warning("Item does not have process method: ", item)
"""
```

### Don't: Skip Conflict Resolution Documentation

```gdscript
# BAD - Resolving conflicts without documentation
func bad_conflict_resolution() -> void:
    var findings := research_pattern("Observer")

    # Silently choose one implementation
    var code := findings.get_source_implementation("official")
    apply_implementation(code)

    # No record of why this choice was made or what alternatives exist
```

```gdscript
# GOOD - Document all conflict resolutions
func good_conflict_resolution() -> void:
    var researcher := MultiSourcePatternResearcher.new()
    var findings := researcher.research_pattern("Observer")

    # Generate documentation with conflict explanations
    var docs := researcher.generate_resolution_documentation(findings)
    save_documentation("observer_pattern.md", docs)

    # Log resolution decisions for team transparency
    var resolution_log := findings.get_resolution_log()
    for entry in resolution_log:
        print("Conflict: ", entry.description)
        print("Resolution: ", entry.resolution)
        print("Rationale: ", entry.rationale)
        print("---")
```