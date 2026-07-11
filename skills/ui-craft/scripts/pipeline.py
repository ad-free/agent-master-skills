#!/usr/bin/env python3
"""
Pipeline orchestrator for ui-craft.
Manages state, phase transitions, and cross-session persistence.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


STATE_FILE = "state.json"
PLAN_FILE = "plan.md"
CONTEXT_FILE = "context.md"
DECISIONS_DIR = "decisions"
SESSIONS_DIR = "sessions"
DESIGN_SYSTEM_DIR = "design-system"
PREVIEW_DIR = "preview"
TOKENS_DIR = "tokens"

PHASES = [
    "LOAD",
    "AUDIT",
    "ALIGN",
    "DESIGN",
    "SOURCE",
    "BUILD",
    "REVIEW",
    "HARDEN",
    "SHIP",
]


class PipelineState:
    """Manages pipeline state persistence."""

    def __init__(self, project_dir: str):
        self.project_dir = Path(project_dir)
        self.craft_dir = self.project_dir / ".ui-craft"
        self.state_file = self.craft_dir / "state.json"

    def load(self) -> dict:
        """Load pipeline state from .ui-craft/state.json."""
        if not self.state_file.exists():
            return self._detect_initial_state()
        try:
            with open(self.state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return self._detect_initial_state()

    def _detect_initial_state(self) -> dict:
        """Detect initial state based on project contents."""
        has_source = self._has_source_code()
        return {
            "currentPhase": 1 if has_source else 2,
            "completed": [],
            "stack": {},
            "slices": [],
            "findings": [],
            "status": "in_progress",
        }

    def _has_source_code(self) -> bool:
        """Check if project has existing source code."""
        source_dirs = ["src", "app", "components", "lib", "pages"]
        for d in source_dirs:
            if (self.project_dir / d).exists():
                return True
        return False

    def save(self, state: dict):
        """Save pipeline state."""
        self.craft_dir.mkdir(parents=True, exist_ok=True)
        with open(self.state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, indent=2)

    def get_current_phase(self, state: dict) -> int:
        """Get the current phase number."""
        return state.get("currentPhase", 0)

    def mark_phase_complete(self, state: dict, phase: int):
        """Mark a phase as complete and advance to next."""
        if phase not in state.get("completed", []):
            state.setdefault("completed", []).append(phase)
        state["currentPhase"] = phase + 1
        self.save(state)

    def is_complete(self, state: dict) -> bool:
        """Check if all phases are complete."""
        return state.get("status") == "complete"

    def mark_complete(self, state: dict):
        """Mark the entire pipeline as complete."""
        state["status"] = "complete"
        state["lastRun"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.save(state)

    def save_handoff(self, state: dict, message: str):
        """Save a handoff document for cross-session context."""
        sessions_dir = self.craft_dir / SESSIONS_DIR
        sessions_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        session_file = sessions_dir / f"session-{timestamp}.md"
        session_file.write_text(
            f"# Session Handoff\n\n"
            f"**Time:** {datetime.now().isoformat()}\n\n"
            f"**Phase:** {PHASES[state.get('currentPhase', 0)]}\n\n"
            f"**Message:** {message}\n\n"
            f"**State:**\n```json\n{json.dumps(state, indent=2)}\n```\n",
            encoding="utf-8",
        )
        return str(session_file)
