"""
Query the Gemini File Search Store using the OptiBot assistant.

Responsibilities:
- Ask questions using Gemini
- Search uploaded knowledge base
- Return answers with citations
"""
from typing import Any
import re
from google import genai

from src.config import (
    GEMINI_API_KEY,
    GEMINI_MODEL,
)

client = genai.Client(
    api_key=GEMINI_API_KEY,
)

SYSTEM_PROMPT = """
You are OptiBot, the customer-support bot for OptiSigns.com.
- Tone: helpful, factual, concise.
- Only answer using the uploaded docs.
- Max 5 bullet points; else link to the doc.
- Cite up to 3 "Article URL:" lines per reply.
"""

GENERATION_CONFIG = {
    'temperature': 0.2,
    'max_output_tokens': 65536,
    'top_p': 0.1,
    #'thinking_level': 'high',
}

URL_PATTERN = re.compile(r"Source:\s*(https?://\S+)")

def ask(question: str, store_name: str) -> str:
    """Ask the OptiBot assistant a question."""
    print(f"Question: {question}")
    interaction = _create_interaction(question, store_name)
    answer = []
    seen = set()
    article_urls = []
    has_citation = False

    for step in interaction.steps:
        if step.type != "model_output":
            continue
        for content in step.content:
            if content.type != "text":
                continue
            answer.append(content.text)
            if "Article URL:" in content.text:
                has_citation = True
            if content.annotations:
               _extract_article_urls(content.annotations, seen, article_urls)

    response = "\n".join(answer)
    if not has_citation and article_urls:
        response += "\n"
        response += "\n".join(
            f"Article URL: {url}"
            for url in article_urls
        )
    return response


def _create_interaction(question: str,store_name: str) -> Any:
    """Create a Gemini interaction using File Search."""
    tools = [
        {
            "type": "file_search",
            "file_search_store_names": [store_name],
        }
    ]
    try:
        interaction = client.interactions.create(
            model=GEMINI_MODEL,
            input=question,
            system_instruction=SYSTEM_PROMPT,
            tools=tools,
            generation_config=GENERATION_CONFIG,
        )
        return interaction
    except Exception as e:
        print(f"Error creating interaction: {e}")
        raise 

def _extract_article_urls(annotations,seen: set[str],article_urls: list[str]) -> None:
    """Extract up to three unique article URLs."""
    for annotation in annotations:
        if len(article_urls) == 3:
            return
        if annotation.type != "file_citation":
            continue
        match = URL_PATTERN.search(annotation.source or "")
        if not match:
            continue
        url = match.group(1)
        if url in seen:
            continue
        seen.add(url)
        article_urls.append(url)