# Skill Integration Example
# Demonstrates how pattern research integrates with existing godot-* skills
extends Node

class_name SkillIntegrationExample

func _ready() -> void:
	# Example 1: Find overlapping patterns
	await demonstrate_pattern_overlap()

	# Example 2: Generate integrated documentation
	await demonstrate_integration_docs()

	# Example 3: Create skill cross-references
	await demonstrate_cross_references()


# Find patterns that overlap with existing skills
func demonstrate_pattern_overlap() -> void:
	print("\n=== Pattern Overlap Analysis ===")

	var researcher := MultiSourcePatternResearcher.new()

	# Research Observer pattern and check for overlap with godot-event-bus
	print("Researching Observer pattern...")
	var findings: PatternFindings = await researcher.research_pattern("Observer")

	# Find related skills
	var related_skills := findings.find_related_skills()
	print("\nRelated existing skills:")

	for skill in related_skills:
		print("- ", skill.name)
		print("  Description: ", skill.description)
		print("  Overlap: ", skill.overlap_percentage, "%")
		print("  Shared patterns: ", skill.shared_patterns)

		if skill.overlap_percentage > 50:
			print("  → HIGH OVERLAP - Consider using existing skill")
		elif skill.overlap_percentage > 20:
			print("  → Partial overlap - Can be complementary")
		print()

	# Show integration recommendations
	var recommendations := findings.get_integration_recommendations()
	print("Integration Recommendations:")
	for rec in recommendations:
		print("- ", rec)


# Generate documentation that references existing skills
func demonstrate_integration_docs() -> void:
	print("\n=== Integrated Documentation Generation ===")

	var researcher := MultiSourcePatternResearcher.new()

	# Research Singleton pattern
	print("Researching Singleton pattern...")
	var findings: PatternFindings = await researcher.research_pattern("Singleton")

	# Find related skills (should find godot-autoloads)
	var related_skills := findings.find_related_skills()

	# Create cross-referenced documentation
	var synthesizer := PatternSynthesizer.new()
	var docs := synthesizer.generate_cross_referenced_documentation(findings, related_skills)

	print("Generated documentation with skill references:")
	print(docs.substr(0, 1000), "...")

	# Save the documentation
	save_integration_documentation("singleton_pattern_with_skills.md", docs)


# Create automatic cross-references between patterns and skills
func demonstrate_cross_references() -> void:
	print("\n=== Automatic Cross-Reference Creation ===")

	var researcher := MultiSourcePatternResearcher.new()
	var patterns := ["Observer", "Singleton", "Factory", "Command"]
	var cross_refs := { }

	# Research multiple patterns and build cross-reference map
	for pattern in patterns:
		print("Researching ", pattern, "...")
		var findings: PatternFindings = await researcher.research_pattern(pattern)
		var related_skills := findings.find_related_skills()

		cross_refs[pattern] = {
			"skills": related_skills,
			"findings": findings,
		}

	# Generate cross-reference matrix
	print("\nPattern-Skill Cross-Reference Matrix:")
	print("Pattern".ljust(15), "| Related Skills")
	print("-".repeat(50))

	for pattern in cross_refs:
		var skill_names := []
		for skill in cross_refs[pattern].skills:
			skill_names.append(skill.name)

		print(pattern.ljust(15), "| ", ", ".join(skill_names))

	# Find skill combinations for common architectures
	print("\nRecommended Skill Combinations:")
	var combinations := find_skill_combinations(cross_refs)
	for combo in combinations:
		print("- ", combo.architecture, ": ", ", ".join(combo.skills))


# Find which skills work well together for common architectures
func find_skill_combinations(cross_refs: Dictionary) -> Array[Dictionary]:
	var combinations := []

	# Observer + Command = Event-driven architecture
	if cross_refs.has("Observer") and cross_refs.has("Command"):
		var observer_skills := _extract_skill_names(cross_refs["Observer"].skills)
		var command_skills := _extract_skill_names(cross_refs["Command"].skills)

		combinations.append(
			{
				"architecture": "Event-driven",
				"skills": _merge_arrays(observer_skills, command_skills),
			},
		)

	# Singleton + Factory = Service locator pattern
	if cross_refs.has("Singleton") and cross_refs.has("Factory"):
		var singleton_skills := _extract_skill_names(cross_refs["Singleton"].skills)
		var factory_skills := _extract_skill_names(cross_refs["Factory"].skills)

		combinations.append(
			{
				"architecture": "Service Locator",
				"skills": _merge_arrays(singleton_skills, factory_skills),
			},
		)

	return combinations


# Helper functions
func _extract_skill_names(skills: Array) -> Array[String]:
	var names: Array[String] = []
	for skill in skills:
		names.append(skill.name)
	return names


func _merge_arrays(a: Array[String], b: Array[String]) -> Array[String]:
	var merged := a.duplicate()
	for item in b:
		if not merged.has(item):
			merged.append(item)
	return merged


func save_integration_documentation(filename: String, content: String) -> void:
	# In a real implementation, this would save to disk
	print("\nDocumentation saved to: ", filename)
	print("Content length: ", content.length(), " characters")


# Advanced integration: Create a unified pattern-skill index
func create_unified_index() -> void:
	print("\n=== Creating Unified Pattern-Skill Index ===")

	var researcher := MultiSourcePatternResearcher.new()
	var index := UnifiedPatternIndex.new()

	# Index all existing skills
	await index.index_all_skills()

	# Research and categorize patterns
	var patterns := ["Observer", "Singleton", "Factory", "Strategy", "Command"]
	for pattern in patterns:
		var findings := await researcher.research_pattern(pattern)
		index.add_pattern_research(pattern, findings)

	# Generate the unified index
	var unified_docs := index.generate_unified_documentation()
	print("Generated unified pattern-skill index")
	print(unified_docs.substr(0, 500), "...")

# Helper class for unified indexing
class_name UnifiedPatternIndex
extends RefCounted

var skill_index: Dictionary = { }
var pattern_research: Dictionary = { }


func index_all_skills() -> void:
	# In a real implementation, this would scan all godot-* skills
	print("Indexing existing skills...")

	# Simulate indexing
	skill_index = {
		"godot-event-bus": {
			"patterns": ["Observer", "Publisher-Subscriber"],
			"category": "Communication",
		},
		"godot-autoloads": {
			"patterns": ["Singleton", "Service Locator"],
			"category": "Architecture",
		},
		"godot-custom-resources": {
			"patterns": ["Factory", "Prototype"],
			"category": "Creation",
		},
	}


func add_pattern_research(pattern_name: String, findings: PatternFindings) -> void:
	pattern_research[pattern_name] = {
		"findings": findings,
		"related_skills": findings.find_related_skills(),
		"category": categorize_pattern(pattern_name),
	}


func categorize_pattern(pattern_name: String) -> String:
	match pattern_name.to_lower():
		"observer", "publisher-subscriber":
			return "Communication"
		"singleton", "service locator":
			return "Architecture"
		"factory", "prototype", "builder":
			return "Creation"
		"strategy", "command", "state":
			return "Behavioral"
		_:
			return "General"


func generate_unified_documentation() -> String:
	var docs := "# Unified Pattern-Skill Index\n\n"

	docs += "## Patterns by Category\n\n"

	var categories := { }
	for pattern in pattern_research:
		var category := pattern_research[pattern].category
		if not categories.has(category):
			categories[category] = []
		categories[category].append(pattern)

	for category in categories:
		docs += "### " + category + "\n\n"
		for pattern in categories[category]:
			docs += "- **" + pattern + "**: "
			var skills := pattern_research[pattern].related_skills
			var skill_names := []
			for skill in skills:
				skill_names.append(skill.name)
			docs += "See " + ", ".join(skill_names) + "\n"
		docs += "\n"

	docs += "## Skills by Pattern\n\n"
	for skill_name in skill_index:
		docs += "### " + skill_name + "\n"
		docs += "Implements: " + ", ".join(skill_index[skill_name].patterns) + "\n"
		docs += "Category: " + skill_index[skill_name].category + "\n\n"

	return docs
