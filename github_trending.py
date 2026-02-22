import requests
from datetime import datetime, timedelta, timezone

from config import GITHUB_TOKEN, TRENDING_DAYS, TRENDING_COUNT


def fetch_trending() -> list[dict]:
    since = (datetime.now(timezone.utc) - timedelta(days=TRENDING_DAYS)).strftime(
        "%Y-%m-%d"
    )
    params = {
        "q": f"created:>{since} stars:>50",
        "sort": "stars",
        "order": "desc",
        "per_page": TRENDING_COUNT,
    }
    headers = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"Bearer {GITHUB_TOKEN}"

    resp = requests.get(
        "https://api.github.com/search/repositories",
        params=params,
        headers=headers,
        timeout=30,
    )
    resp.raise_for_status()
    data = resp.json()

    repos = []
    for item in data.get("items", []):
        repos.append(
            {
                "name": item["full_name"],
                "url": item["html_url"],
                "description": item.get("description") or "No description",
                "stars": item["stargazers_count"],
                "language": item.get("language") or "Unknown",
                "topics": item.get("topics", []),
                "created_at": item["created_at"],
            }
        )
    return repos
