"""
Entry point for the OptiBot mini-clone.
"""

from src.scraper import fetch_articles
from src.converter import convert_to_markdown, save_markdown
from src.uploader import upload_markdown_files
from src.assistant import ask
from src.metadata import load_metadata,save_metadata
from src.config import MARKDOWN_OUTPUT_DIR
from datetime import datetime
from zoneinfo import ZoneInfo

def main() -> None:
    """Run the article scraper."""
    print("=" * 50)
    print("OptiBot Daily Sync")
    now = datetime.now(ZoneInfo("Asia/Ho_Chi_Minh"))
    print(f"Run at: {now.strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)
    print()
    added = 0
    updated = 0
    skipped = 0
    changed_files = []

    articles = fetch_articles()
    metadata = load_metadata()
    print(f"Fetched {len(articles)} articles.\n")

    for article in articles:
        markdown_content = convert_to_markdown(article)
        article_id = str(article.id)
        old = metadata.get(article_id)
        if old is None:
            filepath = save_markdown(article, markdown_content)
            print(f"Saved article {article_id} to {filepath}")
            metadata[article_id] = {
                "updated_at": article.updated_at,
                "url": article.html_url
            }
            added += 1
            changed_files.append(filepath)
        elif old["updated_at"] != article.updated_at:
            print(f"Article {article_id} has been updated. Saving new version.")
            filepath = save_markdown(article, markdown_content)
            metadata[article_id] = {
                "updated_at": article.updated_at,
                "url": article.html_url
            }
            updated += 1
            changed_files.append(filepath)
        else:
            skipped += 1
    store_name = upload_markdown_files(changed_files)
    save_metadata(metadata)
    print()
    print("=" * 50)
    print("Summary")
    print(f"Added   : {added}")
    print(f"Updated : {updated}")
    print(f"Skipped : {skipped}")
    print(f"Uploaded files: {len(changed_files)}")
    print(f"Embedded chunks  : N/A (managed by Gemini File Search)")
    print("=" * 50)
    #answer = ask("How do I add a YouTube video?", store_name)
    #print("\nOptiBot Answer:\n")
    #print(answer)

if __name__ == "__main__":
    main()