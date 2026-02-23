import os
from dotenv import load_dotenv

load_dotenv()


def _require(key: str) -> str:
    val = os.getenv(key)
    if not val:
        raise RuntimeError(f"Missing required environment variable: {key}")
    return val


# GitHub
GITHUB_TOKEN: str | None = os.getenv("GITHUB_TOKEN") or None

# LLM
LLM_BASE_URL: str = _require("LLM_BASE_URL")
LLM_API_KEY: str = _require("LLM_API_KEY")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")

# Resend
RESEND_API_KEY: str = _require("RESEND_API_KEY")

# Email
EMAIL_FROM: str = _require("EMAIL_FROM")
EMAIL_TO: str = _require("EMAIL_TO")

# Trending
TRENDING_SINCE: str = os.getenv("TRENDING_SINCE", "daily")  # daily, weekly, monthly
TRENDING_COUNT: int = int(os.getenv("TRENDING_COUNT", "15"))
