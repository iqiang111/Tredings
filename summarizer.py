from openai import OpenAI, APIError

from config import LLM_BASE_URL, LLM_API_KEY, LLM_MODEL

SYSTEM_PROMPT = """\
You are a concise tech newsletter writer. You will receive a list of trending \
GitHub repositories. Write an engaging daily summary in HTML format.

Rules:
- Write a 1-2 sentence intro about today's trends.
- For each repo, write a short paragraph (2-3 sentences) explaining what it does \
and why it is interesting. Include the repo name as a clickable link.
- Group repos by theme/category if natural groupings exist (e.g., AI/ML, DevTools, \
Web, etc.). Use <h3> tags for category headings.
- Use only these HTML tags: <h2>, <h3>, <p>, <a>, <strong>, <em>, <ul>, <li>.
- Do NOT include <html>, <head>, <body>, or <style> tags. Return only the inner \
content fragment.
- Keep the total summary under 1500 words.\
"""

client = OpenAI(base_url=LLM_BASE_URL, api_key=LLM_API_KEY, timeout=120)


def summarize(repos: list[dict]) -> str:
    lines = ["Here are today's trending GitHub repositories:\n"]
    for i, r in enumerate(repos, 1):
        lines.append(
            f"{i}. {r['name']} - ⭐ {r['stars']} - {r['language']}\n"
            f"   Description: {r['description']}\n"
            f"   Trending: {r['stars_delta']}\n"
            f"   URL: {r['url']}\n"
        )
    user_msg = "\n".join(lines)

    try:
        response = client.chat.completions.create(
            model=LLM_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_msg},
            ],
            temperature=0.7,
        )
    except APIError as e:
        raise RuntimeError(
            f"LLM API call failed [{e.status_code}]: {e.message}\n"
            f"  base_url: {LLM_BASE_URL}\n"
            f"  model:    {LLM_MODEL}\n"
            f"  Please check your LLM_BASE_URL, LLM_API_KEY, and LLM_MODEL in .env"
        ) from e
    return response.choices[0].message.content
