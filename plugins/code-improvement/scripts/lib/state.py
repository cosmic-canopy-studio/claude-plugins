#!/usr/bin/env python3
"""
Shared state management for hooks.
"""

import json
import os
from pathlib import Path
from datetime import datetime
from typing import Any, Dict

# State file locations
CLAUDE_DIR = Path(os.environ.get("CLAUDE_PROJECT_DIR", ".")) / ".claude"
DATA_DIR = CLAUDE_DIR / "data"
STATE_FILE = DATA_DIR / "session_state.json"
LEARNING_LOG = DATA_DIR / "learning_log.jsonl"


def ensure_data_dir():
    """Ensure data directory exists."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)


def load_state() -> Dict[str, Any]:
    """Load current session state."""
    ensure_data_dir()
    if STATE_FILE.exists():
        try:
            with open(STATE_FILE, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return get_default_state()
    return get_default_state()


def save_state(state: Dict[str, Any]):
    """Save session state."""
    ensure_data_dir()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, default=str)


def get_default_state() -> Dict[str, Any]:
    """Return default session state."""
    return {
        "session_start": datetime.now().isoformat(),
        "tool_count": 0,
        "estimated_tokens": 3000,  # Base system prompt
        "consecutive_failures": 0,
        "last_tool": None,
        "warnings_issued": [],
        "patterns_detected": [],
    }


def update_state(updates: Dict[str, Any]):
    """Update specific fields in state."""
    state = load_state()
    state.update(updates)
    save_state(state)


def increment_counter(key: str, amount: int = 1) -> int:
    """Increment a counter in state and return new value."""
    state = load_state()
    current = state.get(key, 0)
    new_value = current + amount
    state[key] = new_value
    save_state(state)
    return new_value


def append_to_list(key: str, value: Any):
    """Append value to a list in state."""
    state = load_state()
    if key not in state:
        state[key] = []
    state[key].append(value)
    save_state(state)


def log_learning(entry: Dict[str, Any]):
    """Append entry to learning log (persistent across sessions)."""
    ensure_data_dir()
    entry["timestamp"] = datetime.now().isoformat()
    with open(LEARNING_LOG, "a") as f:
        f.write(json.dumps(entry) + "\n")


def read_learning_log(limit: int = 100) -> list:
    """Read recent entries from learning log."""
    ensure_data_dir()
    if not LEARNING_LOG.exists():
        return []

    entries = []
    with open(LEARNING_LOG, "r") as f:
        for line in f:
            try:
                entries.append(json.loads(line.strip()))
            except json.JSONDecodeError:
                continue

    return entries[-limit:]


def reset_state():
    """Reset session state to defaults."""
    save_state(get_default_state())
