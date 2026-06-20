"""Web fetch tool.

Unlike the Claude Agent SDK (which ships a built-in WebFetch), Pydantic AI has
no built-in web tool, so this is the custom equivalent: fetch a URL with httpx,
strip it to readable text with BeautifulSoup, and return a truncated result.

(For web *search*, add `pydantic_ai.common_tools.duckduckgo.duckduckgo_search_tool`
or the Tavily tool to the agent — those are first-class Pydantic AI tools.)
"""

from __future__ import annotations

MAX_CHARS = 8000
TIMEOUT_S = 15.0


def fetch_url(url: str) -> str:
    """Fetch a web page and return its readable text content.

    Args:
        url: The absolute http(s) URL to fetch.
    """
    import httpx

    if not url.startswith(("http://", "https://")):
        return "Rejected: url must start with http:// or https://."

    try:
        resp = httpx.get(
            url,
            timeout=TIMEOUT_S,
            follow_redirects=True,
            headers={"User-Agent": "pydantic-ai-sandbox/0.1"},
        )
        resp.raise_for_status()
    except httpx.HTTPError as e:
        return f"Fetch error: {e}"

    content_type = resp.headers.get("content-type", "")
    if "html" not in content_type:
        return f"[{content_type}]\n{resp.text[:MAX_CHARS]}"

    from bs4 import BeautifulSoup

    soup = BeautifulSoup(resp.text, "html.parser")
    for tag in soup(["script", "style", "noscript"]):
        tag.decompose()
    title = soup.title.string.strip() if soup.title and soup.title.string else url
    text = " ".join(soup.get_text(separator=" ").split())
    body = text[:MAX_CHARS]
    if len(text) > MAX_CHARS:
        body += " …(truncated)"
    return f"# {title}\n{url}\n\n{body}"


WEB_TOOLS = [fetch_url]
