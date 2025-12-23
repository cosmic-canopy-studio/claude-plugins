#!/usr/bin/env python3
"""
Suggest next step based on recent file activity in the PM Toolkit.

This hook runs at session end to suggest relevant follow-up actions
based on what files were created or modified during the session.
"""

import os
from pathlib import Path
from datetime import datetime


def get_recent_files(directory: Path, minutes: int = 30) -> list[tuple[Path, str]]:
    """Get files modified in the last N minutes with their type."""
    cutoff = datetime.now().timestamp() - (minutes * 60)
    recent = []

    type_dirs = {
        "research": "research",
        "prds": "prd",
        "requirements": "requirements",
        "plans": "plan",
        "meetings": "meeting",
    }

    for dir_name, file_type in type_dirs.items():
        dir_path = directory / dir_name
        if dir_path.exists():
            for f in dir_path.glob("*.md"):
                if f.stat().st_mtime > cutoff:
                    recent.append((f, file_type))

    return sorted(recent, key=lambda x: x[0].stat().st_mtime, reverse=True)


def suggest_next_step(file_type: str, file_path: Path) -> str:
    """Suggest next step based on file type."""
    suggestions = {
        "research": "Research complete. Consider:\n  - 'Create a PRD based on this research'\n  - 'Create a brief for stakeholders'",
        "prd": "PRD created. Consider:\n  - 'Break this down into implementation phases'\n  - 'Write detailed requirements'",
        "requirements": "Requirements documented. Consider:\n  - 'Create an implementation plan'\n  - 'Estimate complexity'",
        "plan": "Implementation plan ready. Consider:\n  - 'Create a status update'\n  - Start implementation",
        "meeting": "Meeting processed. Consider:\n  - 'Document the decisions formally'\n  - 'Create tasks from action items'",
    }
    return suggestions.get(file_type, "")


def main():
    project_dir = Path(os.environ.get("CLAUDE_PROJECT_DIR", Path.cwd()))

    recent = get_recent_files(project_dir)

    if recent:
        most_recent, file_type = recent[0]
        suggestion = suggest_next_step(file_type, most_recent)
        if suggestion:
            print(f"\n{suggestion}")


if __name__ == "__main__":
    main()
