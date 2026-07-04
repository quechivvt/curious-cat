"""
Manage metadata for incremental article updates.
"""

import hashlib
import json
from pathlib import Path

from src.config import METADATA_FILE

import json

def load_metadata() -> dict:
    """Load metadata from disk."""
    if not METADATA_FILE.exists():
        return {}
    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    except json.JSONDecodeError:
        return {}

def save_metadata(metadata: dict) -> None:
    """Save metadata to disk."""

    METADATA_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(METADATA_FILE,"w",encoding="utf-8",) as file:
        json.dump(
            metadata,
            file,
            indent=2,
        )