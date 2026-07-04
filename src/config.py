"""
Application configuration.
"""

import os
from dotenv import load_dotenv
from pathlib import Path
from google import genai

load_dotenv()


ARTICLES_API_URL = "https://support.optisigns.com/api/v2/help_center/en-us/articles.json"
MARKDOWN_OUTPUT_DIR = Path("data/markdown")

DEFAULT_PAGE_SIZE = 10
REQUEST_TIMEOUT = 30
POLL_INTERVAL = 5


# 0 = crawl all available pages
MAX_PAGES = int(os.getenv("MAX_PAGES", "0"))
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "models/gemini-embedding-2")
FILE_SEARCH_STORE_NAME = os.getenv("FILE_SEARCH_STORE_NAME", "OptiSigns Knowledge Base")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set.")