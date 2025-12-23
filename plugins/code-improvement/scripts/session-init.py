#!/usr/bin/env python3
"""
Session initialization hook.
Runs on SessionStart to initialize state.
"""

import sys
import os

# Add lib to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "lib"))

from state import save_state, get_default_state


def main():
    """Initialize session state."""
    state = get_default_state()
    save_state(state)

    # Output confirmation (will be shown to user via hook mechanism)
    print("Session initialized", file=sys.stderr)
    sys.exit(0)


if __name__ == "__main__":
    main()
