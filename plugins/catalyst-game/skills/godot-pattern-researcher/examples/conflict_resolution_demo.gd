# Conflict Resolution Demonstration
# Shows how to handle conflicts between different pattern implementations
extends Node

class_name ConflictResolutionDemo

func _ready() -> void:
	# Demonstrate different conflict resolution strategies
	await demonstrate_automatic_resolution()
	await demonstrate_manual_resolution()
	await demonstrate_hybrid_resolution()


# Automatic conflict resolution using priority rules
func demonstrate_automatic_resolution() -> void:
	print("\n=== Automatic Conflict Resolution ===")

	var researcher := MultiSourcePatternResearcher.new()
	researcher.conflict_resolution_strategy = "auto"

	# Research State Machine pattern (likely to have conflicts)
	print("Researching State Machine pattern...")
	var findings: PatternFindings = await researcher.research_pattern(
		"State Machine",
		[SourceType.OFFICIAL, SourceType.COMMUNITY, SourceType.SKILL_EXAMPLES],
	)

	# Show conflict resolution log
	print("\nConflict Resolution Summary:")
	var resolution_log := findings.get_resolution_log()
	for entry in resolution_log:
		print("- ", entry.description)
		print("  Resolution: ", entry.resolution)
		print("  Rationale: ", entry.rationale)
		print()

	# Get the final resolved implementation
	var resolved_code := findings.get_resolved_implementation()
	print("Resolved implementation:")
	print(resolved_code)


# Manual conflict resolution with user input
func demonstrate_manual_resolution() -> void:
	print("\n=== Manual Conflict Resolution ===")

	var researcher := MultiSourcePatternResearcher.new()
	researcher.conflict_resolution_strategy = "manual"

	# Research Command pattern with manual conflict resolution
	print("Researching Command pattern...")
	var findings: PatternFindings = await researcher.research_pattern(
		"Command",
		[SourceType.OFFICIAL, SourceType.COMMUNITY],
	)

	if findings.has_conflicts():
		print("\nConflicts require manual resolution:")
		var conflicts := findings.get_conflicts()

		for conflict in conflicts:
			print("\nConflict ID: ", conflict.conflict_id)
			print("Type: ", conflict.conflict_type)
			print("Source A (", conflict.source_a, "):")
			print("  ", conflict.implementation_a.strip_edges().substr(0, 100), "...")
			print("Source B (", conflict.source_b, "):")
			print("  ", conflict.implementation_b.strip_edges().substr(0, 100), "...")

			# Simulate user choice (in real implementation, this would be UI)
			var choice := await simulate_user_choice(conflict)
			print("User chose: ", choice)

			# Apply manual resolution
			match choice:
				"a":
					findings.resolve_conflict_with_source(conflict.conflict_id, conflict.source_a)
				"b":
					findings.resolve_conflict_with_source(conflict.conflict_id, conflict.source_b)
				"hybrid":
					var hybrid := create_hybrid_implementation(conflict)
					findings.resolve_conflict_with_hybrid(conflict.conflict_id, hybrid)

	# Get the manually resolved implementation
	var final_code := findings.get_resolved_implementation()
	print("\nManually resolved implementation:")
	print(final_code)


# Hybrid resolution combining the best of multiple sources
func demonstrate_hybrid_resolution() -> void:
	print("\n=== Hybrid Conflict Resolution ===")

	var researcher := MultiSourcePatternResearcher.new()

	# Set up custom resolution rules for hybrid approach
	var resolver := researcher.get_conflict_resolver()
	resolver.add_resolution_rule(
		ConflictType.IMPLEMENTATION_DIFFERENCE,
		_create_hybrid_resolver,
	)

	# Research Strategy pattern
	print("Researching Strategy pattern with hybrid resolution...")
	var findings: PatternFindings = await researcher.research_pattern("Strategy")

	# Show how hybrid solutions were created
	print("\nHybrid Solutions Created:")
	var hybrid_log := findings.get_hybrid_creation_log()
	for entry in hybrid_log:
		print("- ", entry.conflict_id)
		print("  Combined features from: ", entry.sources_combined)
		print("  Added optimizations: ", entry.optimizations)

	# Get the hybrid implementation
	var hybrid_code := findings.get_resolved_implementation()
	print("\nHybrid implementation:")
	print(hybrid_code)


# Custom hybrid resolver that combines implementations
func _create_hybrid_resolver(conflict: PatternConflict) -> ResolutionResult:
	var result := ResolutionResult.new()
	result.resolution_type = ResolutionType.HYBRID

	# Extract best practices from both implementations
	var best_a := extract_best_practices(conflict.implementation_a)
	var best_b := extract_best_practices(conflict.implementation_b)

	# Create hybrid combining both
	var hybrid := create_hybrid_from_practices(best_a, best_b)
	result.hybrid_code = hybrid
	result.rationale = "Combined static typing from A with signal optimization from B"

	return result


# Simulate user choice for manual resolution
func simulate_user_choice(conflict: PatternConflict) -> String:
	# In a real implementation, this would show UI to the user
	# For demo purposes, we'll make choices based on conflict type

	match conflict.conflict_type:
		ConflictType.BEST_PRACTICE_VIOLATION:
			# Always choose the one following best practices
			return "b" # Assuming B is the correct one
		ConflictType.PERFORMANCE_CONCERN:
			# Choose the one with better performance
			return "a" # Assuming A has better performance
		_:
			# For other conflicts, create a hybrid
			return "hybrid"


# Extract best practices from an implementation
func extract_best_practices(implementation: String) -> Array[String]:
	var practices := []

	if implementation.contains("static var"):
		practices.append("static_variable")

	if implementation.contains("signal"):
		practices.append("godot_signals")

	if implementation.contains(":") and implementation.contains("->"):
		practices.append("static_typing")

	if implementation.contains("@onready"):
		practices.append("onready_optimization")

	return practices


# Create hybrid implementation from best practices
func create_hybrid_from_practices(practices_a: Array[String], practices_b: Array[String]) -> String:
	var all_practices := practices_a + practices_b
	var hybrid := "# Hybrid implementation combining best practices\n\n"

	hybrid += "extends Node\nclass_name HybridPattern\n\n"

	# Add static variables if any practice uses them
	if all_practices.has("static_variable"):
		hybrid += "static var instance: HybridPattern\n\n"

	# Add signals if any practice uses them
	if all_practices.has("godot_signals"):
		hybrid += "signal pattern_changed\nsignal state_updated\n\n"

	# Add methods with static typing
	if all_practices.has("static_typing"):
		hybrid += "func initialize() -> void:\n"
		hybrid += "\tpass\n\n"
		hybrid += "func execute_action(data: Dictionary) -> void:\n"
		hybrid += "\tpass\n"

	# Add Godot optimizations
	if all_practices.has("onready_optimization"):
		hybrid += "\n@onready var ui_container := $UIContainer\n"

	return hybrid


# Create a hybrid implementation for a specific conflict
func create_hybrid_implementation(conflict: PatternConflict) -> String:
	var hybrid := "# Hybrid implementation for " + conflict.pattern_name + "\n"
	hybrid += "# Combining approaches from " + str(conflict.source_a) + " and " + str(conflict.source_b) + "\n\n"

	# Simple example: take structure from A, optimizations from B
	hybrid += "# Structure from Source A:\n"
	var lines_a := conflict.implementation_a.split("\n")
	for i in range(min(10, lines_a.size())):
		if not lines_a[i].strip_edges().is_empty():
			hybrid += lines_a[i] + "\n"

	hybrid += "\n# Optimizations from Source B:\n"
	var lines_b := conflict.implementation_b.split("\n")
	for i in range(min(10, lines_b.size())):
		if lines_b[i].contains("signal") or lines_b[i].contains("static"):
			hybrid += "# " + lines_b[i] + "\n"

	return hybrid
