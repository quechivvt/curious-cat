"""
Data models used across the project.
"""

from dataclasses import dataclass


@dataclass(slots=True)
class Article:
    """Represents a Help Center article."""

    id: int
    title: str
    body: str
    html_url: str
    updated_at: str