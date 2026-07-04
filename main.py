"""
Entry point for the OptiBot mini-clone.
"""

from src.scraper import fetch_articles


def main() -> None:
    """Run the article scraper."""
    articles = fetch_articles()

    print(f"Fetched {len(articles)} articles.\n")

    if articles:
        first = articles[0]

        print("First article:")
        print(f"ID         : {first.id}")
        print(f"Title      : {first.title}")
        print(f"URL        : {first.html_url}")
        print(f"Updated At : {first.updated_at}")
        print(f"Body Preview:\n{first.body[:200]}...")


if __name__ == "__main__":
    main()