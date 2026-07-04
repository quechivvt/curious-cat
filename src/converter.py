"""
Convert Zendesk HTML articles into Markdown files.

Responsibilities:
- Convert HTML to Markdown
- Save Markdown files to disk
"""

from src.models import Article
from src.config import MARKDOWN_OUTPUT_DIR
from pathlib import Path
from markdownify import markdownify


def convert_to_markdown(article: Article) -> str:
    """Convert an Article's HTML body to Markdown."""
    markdown_body = markdownify(article.body, heading_style="ATX")

    markdown_content = (f"# {article.title}\n\n"
        f"Source: {article.html_url}\n\n"
        f"Last Updated: {article.updated_at}\n\n"
        f"---\n\n"
        f"{markdown_body}")
    
    return markdown_content

def save_markdown(article: Article, markdown_content: str, output_dir: str |None = None) -> Path:
    """Save the Markdown content to a file."""
    if output_dir is None:
        output_dir = MARKDOWN_OUTPUT_DIR

    Path(output_dir).mkdir(parents=True, exist_ok=True)

    filename = f"{article.id}.md"
    filepath = output_dir / filename

    filepath.write_text(
        markdown_content,
        encoding="utf-8",
    )
    return filepath