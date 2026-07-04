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
)


client = genai.Client(
    api_key=GEMINI_API_KEY,
)

def upload_markdown_files(markdown_files: list[Path]) -> str:
    """Upload all Markdown files to a File Search Store."""
    store_name = _get_or_create_store()
    if not markdown_files:
        print("No new or updated Markdown files.")
        return store_name

    operations = []
    print("Uploading Markdown files...")
    for markdown_file in markdown_files:
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

def _get_existing_store() -> str | None:
    """Return an existing File Search Store name if one already exists."""
    for store in client.file_search_stores.list():
        if store.display_name == FILE_SEARCH_STORE_NAME:
            return store.name
    return None

def _create_file_search_store() -> str:
    """Create a Gemini File Search Store."""
    file_search_store = client.file_search_stores.create(
    config={
        'display_name': FILE_SEARCH_STORE_NAME,
        'embedding_model': EMBEDDING_MODEL
    })
    return file_search_store.name

def _get_or_create_store() -> str:
    """Return the File Search Store name and whether it was newly created."""
    store_name = _get_existing_store()
    if store_name:
        print(f"Using existing File Search Store: {store_name}")
        return store_name

    print("Creating new File Search Store...")
    return _create_file_search_store()


def _upload_file(file_search_store_name: str,markdown_file: Path) -> Any:
    """Upload a Markdown file to the File Search Store."""
    print(f"Uploading {markdown_file} to File Search Store...")
    operation = client.file_search_stores.upload_to_file_search_store(
        file=markdown_file,
        file_search_store_name=file_search_store_name,
        config={
            "display_name": markdown_file.stem,
        }
    )
    return operation


def _wait_for_operation(operation) -> None:
    """Wait until the upload operation completes."""
    while not operation.done:
        operation = client.operations.get(operation)
        time.sleep(POLL_INTERVAL)