# Godot Pattern Researcher Reference

## Core Classes

### MultiSourcePatternResearcher

The main class for researching patterns across multiple sources with automatic conflict resolution.

```gdscript
class_name MultiSourcePatternResearcher
extends Node

# Signals
signal research_progress_updated(stage: String, progress: float)
signal conflict_detected(conflict: PatternConflict)
signal research_completed(findings: PatternFindings)

# Properties
@export var default_sources: Array[SourceType] = [SourceType.OFFICIAL, SourceType.SKILL_EXAMPLES, SourceType.COMMUNITY]
@export var conflict_resolution_strategy: String = "auto"  # "auto", "manual", "priority"
@export var require_static_typing: bool = true
@export var godot_version: String = "4.3"
@export var validation_enabled: bool = true

# Main Methods
func research_pattern(pattern_name: String, sources: Array[SourceType] = default_sources) -> PatternFindings
func add_custom_source(source_type: SourceType, handler: Callable) -> void
func set_priority_order(priorities: Array[SourceType]) -> void
func add_validation_rule(rule: Callable) -> void
func get_research_history() -> Array[Dictionary]
```

### PatternFindings

Container for all research findings with conflict resolution capabilities.

```gdscript
class_name PatternFindings
extends RefCounted

# Properties
var pattern_name: String = ""
var source_findings: Dictionary = {}  # SourceType -> Dictionary
var conflicts: Array[PatternConflict] = []
var resolved_implementation: String = ""
var documentation: String = ""
var validation_issues: Array[String] = []
var related_skills: Array[Dictionary] = []

# Methods
func add_source_findings(source: SourceType, findings: Dictionary) -> void
func detect_conflicts() -> Array[PatternConflict]
func resolve_conflicts(priority_order: Array[SourceType]) -> void
func get_resolved_implementation() -> String
func has_conflicts() -> bool
func get_resolution_log() -> Array[Dictionary]
func validate_implementation() -> ValidationResult
func apply_godot_optimizations() -> String
```

### PatternConflict

Represents a conflict between different pattern implementations.

```gdscript
class_name PatternConflict
extends RefCounted

# Properties
var conflict_id: String
var pattern_name: String
var source_a: SourceType
var source_b: SourceType
var implementation_a: String
var implementation_b: String
var conflict_type: ConflictType
var severity: ConflictSeverity
var resolution: ResolutionType
var rationale: String

# Methods
static func create_implementation_difference(a: SourceType, b: SourceType, impl_a: String, impl_b: String) -> PatternConflict
static func create_best_practice_violation(violating: SourceType, correct: SourceType, reason: String) -> PatternConflict
func set_resolution(res_type: ResolutionType, reason: String) -> void
```

### PatternConflictResolver

Handles conflict resolution using rule-based logic and Godot best practices.

```gdscript
class_name PatternConflictResolver
extends RefCounted

# Methods
func resolve_conflict(conflict: PatternConflict) -> ResolutionResult
func resolve_all_conflicts(conflicts: Array[PatternConflict]) -> Array[ResolutionResult]
func add_resolution_rule(conflict_type: ConflictType, handler: Callable) -> void
func validate_resolution(resolution: ResolutionResult) -> bool
```

### PatternSynthesizer

Generates comprehensive documentation from research findings.

```gdscript
class_name PatternSynthesizer
extends RefCounted

# Methods
func generate_comprehensive_documentation(findings: PatternFindings) -> PatternDocumentation
func generate_quick_reference(findings: PatternFindings) -> String
func generate_tutorial(findings: PatternFindings) -> String
func generate_api_reference(findings: PatternFindings) -> String
```

## Enumerations

### SourceType

```gdscript
enum SourceType {
    OFFICIAL,        # Godot official documentation
    SKILL_EXAMPLES,  # Existing godot-* skills
    COMMUNITY,       # Community tutorials and examples
    TUTORIALS,       # Video tutorials and blog posts
    FORUMS,          # Forum discussions
    GITHUB,          # GitHub repositories
    CUSTOM          # User-defined sources
}
```

### ConflictType

```gdscript
enum ConflictType {
    IMPLEMENTATION_DIFFERENCE,  # Different code approaches
    NAMING_CONVENTION,         # Different naming styles
    ARCHITECTURAL_VARIATION,   # Different architectural approaches
    BEST_PRACTICE_VIOLATION,   # One violates best practices
    VERSION_SPECIFIC,          # Version-specific differences
    PERFORMANCE_CONCERN,       # Different performance characteristics
    MISSING_FEATURE,           # One lacks features present in another
}
```

### ConflictSeverity

```gdscript
enum ConflictSeverity {
    CRITICAL,    # Must be resolved (security, crashes)
    MAJOR,       # Should be resolved (performance, maintainability)
    MINOR,       # Can be documented (style, preference)
    INFO         # Informational only
}
```

### ResolutionType

```gdscript
enum ResolutionType {
    USE_SOURCE_A,        # Prefer implementation from source A
    USE_SOURCE_B,        # Prefer implementation from source B
    USE_HIGHEST_PRIORITY, # Use source with highest priority
    HYBRID,              # Combine best of both
    GODOT_OPTIMIZED,     # Use Godot-specific optimization
    DOCUMENT_BOTH,       # Document both approaches
    MANUAL_REVIEW        # Requires manual decision
}
```

## Configuration

### Research Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `max_sources` | `int` | `10` | Maximum number of sources to research |
| `research_depth` | `int` | `3` | How deep to follow linked references |
| `cache_enabled` | `bool` | `true` | Cache research results |
| `cache_duration` | `int` | `3600` | Cache duration in seconds |
| `parallel_research` | `bool` | `true` | Research multiple sources in parallel |

### Validation Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `require_static_typing` | `bool` | `true` | Enforce static typing in implementations |
| `check_godot_version` | `bool` | `true` | Validate against specific Godot version |
| `performance_validation` | `bool` | `true` | Check for performance issues |
| `security_validation` | `bool` | `true` | Check for security vulnerabilities |

### Documentation Configuration

| Property | Type | Default | Description |
|----------|------|---------|-------------|
| `include_examples` | `bool` | `true` | Include working code examples |
| `include_alternatives` | `bool` | `true` | Include alternative implementations |
| `include_performance_notes` | `bool` | `true` | Include performance considerations |
| `documentation_style` | `String` | `"comprehensive"` | "comprehensive", "quick", "tutorial" |

## Research Sources

### Official Documentation

**Type:** `SourceType.OFFICIAL`

**Coverage:**
- Pattern definitions and concepts
- Official code examples
- Best practices and guidelines
- Performance considerations
- Version-specific notes

**Access Methods:**
- `_search_official_docs(pattern_name)`
- `_parse_official_examples(pattern_name)`
- `_extract_best_practices(pattern_name)`

### Skill Examples

**Type:** `SourceType.SKILL_EXAMPLES`

**Coverage:**
- Working implementations in existing godot-* skills
- Real-world usage patterns
- Integration examples
- Edge case handling
- Performance optimizations

**Access Methods:**
- `_search_skill_examples(pattern_name)`
- `_analyze_skill_implementations(pattern_name)`
- `_extract_integration_patterns(pattern_name)`

### Community Examples

**Type:** `SourceType.COMMUNITY`

**Coverage:**
- Community tutorials and guides
- Forum discussions and Q&A
- GitHub repositories
- Blog posts and articles

**Access Methods:**
- `_search_community_tutorials(pattern_name)`
- `_analyze_forum_discussions(pattern_name)`
- `_scan_github_examples(pattern_name)`

## Quick Reference

### Common Research Tasks

#### Basic Pattern Research
```gdscript
# Quick pattern research with defaults
var researcher := MultiSourcePatternResearcher.new()
var findings := researcher.research_pattern("Singleton")
print(findings.get_resolved_implementation())
```

#### Custom Source Priority
```gdscript
# Set custom source priority
researcher.set_priority_order([
    SourceType.SKILL_EXAMPLES,
    SourceType.OFFICIAL,
    SourceType.COMMUNITY
])
```

#### Add Validation Rule
```gdscript
# Add custom validation rule
researcher.add_validation_rule(func(code: String) -> bool:
    return not code.contains("get_node().get_node()")  # Prevent chaining
)
```

#### Manual Conflict Resolution
```gdscript
# Review and manually resolve conflicts
var conflicts := findings.get_conflicts()
for conflict in conflicts:
    print("Conflict:", conflict.conflict_type)
    print("Choose A or B or type 'hybrid'")
    var choice := await get_user_input()
    findings.set_manual_resolution(conflict.conflict_id, choice)
```

### Pattern Validation

#### Static Typing Check
```gdscript
func validate_static_typing(code: String) -> bool:
    var lines := code.split("\n")
    for line in lines:
        if line.begins_with("var ") and not line.contains(":"):
            return false  # Found variable without type
        if line.begins_with("func ") and not line.contains("->") and not line.strip_edges().ends_with(":"):
            return false  # Found function without return type
    return true
```

#### Godot Best Practices Check
```gdscript
func validate_godot_practices(code: String, pattern_name: String) -> Array[String]:
    var issues := []

    # Check for signal usage in Observer pattern
    if pattern_name.to_lower() == "observer" and not code.contains("signal"):
        issues.append("Observer pattern should use Godot signals")

    # Check for proper node lifecycle
    if code.contains("get_node") and not code.contains("@onready"):
        issues.append("Use @onready for node references")

    # Check for queue_free usage
    if code.contains("free()") and not code.contains("queue_free()"):
        issues.append("Use queue_free() instead of free() for nodes")

    return issues
```

## Integration Examples

### Research and Validate Pattern
```gdscript
extends Node

func _ready() -> void:
    # Create researcher with validation
    var researcher := MultiSourcePatternResearcher.new()
    researcher.validation_enabled = true
    researcher.require_static_typing = true

    # Research the Observer pattern
    var findings := researcher.research_pattern(
        "Observer",
        [SourceType.OFFICIAL, SourceType.SKILL_EXAMPLES, SourceType.COMMUNITY]
    )

    # Check for validation issues
    if findings.validation_issues.size() > 0:
        print("Validation issues found:")
        for issue in findings.validation_issues:
            print("- ", issue)

    # Get the final resolved implementation
    var implementation := findings.apply_godot_optimizations()
    save_pattern_file("observer_pattern.gd", implementation)

    # Generate documentation
    var synthesizer := PatternSynthesizer.new()
    var docs := synthesizer.generate_comprehensive_documentation(findings)
    save_documentation("observer_pattern.md", docs)
```

### Custom Conflict Resolution
```gdscript
extends Node

func custom_conflict_resolution() -> void:
    var researcher := MultiSourcePatternResearcher.new()

    # Add custom resolution rule for performance
    var resolver := researcher.get_conflict_resolver()
    resolver.add_resolution_rule(ConflictType.PERFORMANCE_CONCERN, _resolve_performance_conflict)

    var findings := researcher.research_pattern("Factory")

func _resolve_performance_conflict(conflict: PatternConflict) -> ResolutionResult:
    var result := ResolutionResult.new()

    # Analyze both implementations for performance
    var perf_a := analyze_performance(conflict.implementation_a)
    var perf_b := analyze_performance(conflict.implementation_b)

    if perf_a.score > perf_b.score:
        result.resolution_type = ResolutionType.USE_SOURCE_A
        result.rationale = "Better performance characteristics"
    else:
        result.resolution_type = ResolutionType.USE_SOURCE_B
        result.rationale = "Better performance characteristics"

    return result
```

### Batch Pattern Research
```gdscript
extends Node

func research_multiple_patterns() -> void:
    var patterns := ["Singleton", "Observer", "Factory", "Strategy"]
    var researcher := MultiSourcePatternResearcher.new()
    var all_findings := {}

    for pattern in patterns:
        print("Researching pattern: ", pattern)
        var findings := researcher.research_pattern(pattern)
        all_findings[pattern] = findings

        # Save implementation
        var impl := findings.get_resolved_implementation()
        save_pattern_file(pattern.to_lower() + ".gd", impl)

    # Generate comparison documentation
    generate_comparison_docs(all_findings)
```