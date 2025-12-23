# Basic Pattern Research Example
# Demonstrates how to research a pattern with automatic conflict resolution
extends Node

class_name BasicPatternResearchExample

func _ready() -> void:
	# Example 1: Basic research with default settings
	await demonstrate_basic_research()

	# Example 2: Research with custom sources
	await demonstrate_custom_sources()

	# Example 3: Research with validation
	await demonstrate_validated_research()


# Basic pattern research using default settings
func demonstrate_basic_research() -> void:
	print("\n=== Basic Pattern Research ===")

	# Create a researcher with default settings
	var researcher := MultiSourcePatternResearcher.new()

	# Connect to signals for progress tracking
	researcher.research_progress_updated.connect(_on_research_progress)
	researcher.conflict_detected.connect(_on_conflict_detected)
	researcher.research_completed.connect(_on_research_completed)

	# Research the Singleton pattern
	print("Researching Singleton pattern...")
	var findings: PatternFindings = await researcher.research_pattern("Singleton")

	# Get the resolved implementation
	var implementation: String = findings.get_resolved_implementation()
	print("\nResolved Implementation:")
	print(implementation)

	# Check if any conflicts were found and resolved
	if findings.has_conflicts():
		print("\nConflicts were detected and resolved")
		var resolution_log := findings.get_resolution_log()
		for entry in resolution_log:
			print("- ", entry)


# Research pattern with custom source configuration
func demonstrate_custom_sources() -> void:
	print("\n=== Custom Source Research ===")

	var researcher := MultiSourcePatternResearcher.new()

	# Set custom source priority (skills before official docs)
	researcher.set_priority_order(
		[
			SourceType.SKILL_EXAMPLES,
			SourceType.OFFICIAL,
			SourceType.COMMUNITY,
		],
	)

	# Add a validation rule for our specific needs
	researcher.add_validation_rule(
		func(code: String) -> bool:
			# Ensure singleton implementation has proper cleanup
			return code.contains("queue_free") or code.contains("_notification")
	)

	print("Researching Observer pattern with custom sources...")
	var findings: PatternFindings = await researcher.research_pattern(
		"Observer",
		[SourceType.SKILL_EXAMPLES, SourceType.OFFICIAL],
	)

	# Apply Godot-specific optimizations
	var optimized_code := findings.apply_godot_optimizations()
	print("\nGodot-optimized Observer implementation:")
	print(optimized_code)


# Research with comprehensive validation
func demonstrate_validated_research() -> void:
	print("\n=== Validated Pattern Research ===")

	var researcher := MultiSourcePatternResearcher.new()
	researcher.validation_enabled = true
	researcher.require_static_typing = true

	# Research the Factory pattern
	print("Researching Factory pattern with validation...")
	var findings: PatternFindings = await researcher.research_pattern("Factory")

	# Check validation results
	if findings.validation_issues.size() > 0:
		print("\nValidation issues found:")
		for issue in findings.validation_issues:
			print("  - ", issue)

		# Apply automatic fixes if available
		findings.apply_validation_fixes()
		print("\nApplied automatic fixes")
	else:
		print("\nNo validation issues - implementation is clean")

	# Get the final validated implementation
	var final_impl := findings.get_resolved_implementation()
	print("\nFinal validated implementation:")
	print(final_impl)


# Signal handlers for research progress
func _on_research_progress(stage: String, progress: float) -> void:
	print("Research progress: ", stage, " - ", int(progress * 100), "%")


func _on_conflict_detected(conflict: PatternConflict) -> void:
	print("Conflict detected between ", conflict.source_a, " and ", conflict.source_b)
	print("  Type: ", conflict.conflict_type)
	print("  Severity: ", conflict.severity)


func _on_research_completed(findings: PatternFindings) -> void:
	print("Research completed for pattern: ", findings.pattern_name)
	print("Sources researched: ", findings.source_findings.keys())
	if findings.has_conflicts():
		print("Conflicts resolved: ", findings.conflicts.size())
