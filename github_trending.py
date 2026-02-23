import requests
from bs4 import BeautifulSoup

from config import TRENDING_SINCE, TRENDING_COUNT


def fetch_trending() -> list[dict]:
    url = f"https://github.com/trending?since={TRENDING_SINCE}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    articles = soup.find_all("article", class_="Box-row")

    repos = []
    for article in articles[:TRENDING_COUNT]:
        # Repo name and URL
        h2 = article.find("h2")
        if not h2:
            continue
        a_tag = h2.find("a")
        if not a_tag:
            continue
        repo_path = a_tag["href"].strip("/")
        repo_url = f"https://github.com/{repo_path}"

        # Description
        p_tag = article.find("p")
        description = p_tag.get_text(strip=True) if p_tag else "No description"

        # Language
        lang_span = article.find("span", itemprop="programmingLanguage")
        language = lang_span.get_text(strip=True) if lang_span else "Unknown"

        # Stars and forks
        links = article.find_all("a", class_="Link--muted")
        stars = ""
        forks = ""
        for link in links:
            href = link.get("href", "")
            text = link.get_text(strip=True).replace(",", "")
            if "/stargazers" in href:
                stars = text
            elif "/forks" in href:
                forks = text

        # Stars today/this week/this month
        stars_delta = ""
        delta_span = article.find("span", class_="d-inline-block float-sm-right")
        if delta_span:
            stars_delta = delta_span.get_text(strip=True)

        repos.append(
            {
                "name": repo_path,
                "url": repo_url,
                "description": description,
                "stars": stars,
                "forks": forks,
                "language": language,
                "stars_delta": stars_delta,
            }
        )
    return repos
