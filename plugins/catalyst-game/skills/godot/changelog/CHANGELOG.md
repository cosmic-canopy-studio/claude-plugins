# Godot Skills Changelog

All notable changes to the Godot skill system are documented here.

Format: [YYYY.MM.DD] - Date

## [2025.12.19] - 2025-12-19

### Added
- Initial progressive disclosure architecture
- Entry point SKILL.md with lookup instructions
- Searchable index.yaml with `when_to_use` triggers
- 5 dispatcher files for routing by use case:
  - `dispatchers/2d-gameplay.md` - 2D game development patterns
  - `dispatchers/3d-gameplay.md` - 3D game development patterns
  - `dispatchers/ui-systems.md` - User interface patterns
  - `dispatchers/audio-systems.md` - Audio and music patterns
  - `dispatchers/game-patterns.md` - Architecture and best practices
- Reference directory structure for consolidated content
- Changelog system with date-based versioning

### Changed
- Migrated from 120+ individual skills to unified lookup system
- Reorganized content by topic cluster instead of Godot node type

### Migration Notes
Individual `godot-*` skill directories are deprecated. Use dispatchers to find patterns.

**Old path:** `.claude/skills/godot/godot-character-body-2d/SKILL.md`
**New path:** `.claude/skills/godot/reference/movement/2d-character.md`

---

## Archive

Monthly archives in `YYYY-MM/` subdirectories contain detailed change logs.
