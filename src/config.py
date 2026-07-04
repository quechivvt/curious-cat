"""
Application configuration.
"""

import os
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()

ARTICLES_API_URL = "https://support.optisigns.com/api/v2/help_center/en-us/articles.json"
MARKDOWN_OUTPUT_DIR = Path("data/markdown")

DEFAULT_PAGE_SIZE = 30
REQUEST_TIMEOUT = 30

# 0 = crawl all available pages
MAX_PAGES = int(os.getenv("MAX_PAGES", "0"))