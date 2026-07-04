"""
Upload Markdown documents to the Gemini File Search Store.

Responsibilities:
- Create a File Search Store
- Upload Markdown documents
- Wait for indexing to complete
- Log upload results
"""

from google import genai
from typing import Any
from pathlib import Path
import time
from src.config import (
    GEMINI_API_KEY,
    EMBEDDING_MODEL,
    FILE_SEARCH_STORE_NAME,
    POLL_INTERVAL,
    MARKDOWN_OUTPUT_DIR,
)


client = genai.Client(
    api_key=GEMINI_API_KEY,
)

def upload_markdown_files() -> str:
    """Upload all Markdown files to a File Search Store."""
    store_name = _create_file_search_store()

    operations = []
    for markdown_file in MARKDOWN_OUTPUT_DIR.glob("*.md"):
        operation = _upload_file(
            store_name,
            markdown_file,
        )
        operations.append(operation)

    total = len(operations)

    for index, operation in enumerate(operations, start=1):
        _wait_for_operation(operation)
        print(f"Indexed {index}/{total}")

    print(f"Uploaded {total} Markdown files.")
    print(f"File Search Store: {store_name}")
    print("File Search Store indexing completed.")
    return store_name


def _create_file_search_store() -> str:
    """Create a Gemini File Search Store."""
    file_search_store = client.file_search_stores.create(
    config={
        'display_name': FILE_SEARCH_STORE_NAME,
        'embedding_model': EMBEDDING_MODEL
    })
    return file_search_store.name


def _upload_file(file_search_store_name: str,markdown_file: Path) -> Any:
    """Upload a Markdown file to the File Search Store."""

    operation = client.file_search_stores.upload_to_file_search_store(
        file=markdown_file,
        file_search_store_name=file_search_store_name,
        config={
            "display_name": markdown_file.stem,
        }
    )
    print(f"Uploading {markdown_file.name} to {file_search_store_name}")
    return operation


def _wait_for_operation(operation) -> None:
    """Wait until the upload operation completes."""
    while not operation.done:
        operation = client.operations.get(operation)
        time.sleep(POLL_INTERVAL)