# Perform code review on Godot/GDScript files

Reviews code for clean practices, documentation standards, and idiomatic patterns.

## Usage

/code-review [--paths "file1.gd file2.gd"] [--pr PR_URL] [--branch BRANCH] [--strict]

## Options

- `--paths`: Specific files/directories to review (default: all staged changes)
- `--pr`: PR URL to review (uses GitHub API)
- `--branch`: Branch name to compare against main
- `--strict`: Enable strict mode (fails on warnings)
- `--fix`: Auto-fix common issues (formatting, unused imports)

## What it checks

### Code Quality
- GDScript style compliance (gdlint)
- Type annotations presence
- Unused variables/imports
- Magic numbers and hardcoded values

### Documentation
- Class and function docstrings
- File headers with purpose
- Inline comments (should be doc strings instead)

### Best Practices
- Godot idiomatic patterns
- Resource management
- Signal usage patterns
- Performance considerations

## Reports

- Summary table with file scores
- Detailed issues list
- Recommendations for fixes

---

cd /home/sam/code/lb_advisor && python tools/code_review.py $*