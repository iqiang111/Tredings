import sys
from datetime import datetime


def main():
    print(f"[{datetime.now():%Y-%m-%d %H:%M}] Starting GitHub Trends Daily Summary...")

    # Step 1: Fetch trending repos
    print("Fetching trending repositories from GitHub...")
    from github_trending import fetch_trending

    repos = fetch_trending()
    if not repos:
        print("No trending repos found. Exiting.")
        sys.exit(0)
    print(f"Found {len(repos)} trending repos.")

    # Step 2: Summarize with LLM
    print("Generating summary with LLM...")
    from summarizer import summarize

    summary_html = summarize(repos)
    print("Summary generated.")

    # Step 3: Send email
    print("Sending email via Resend...")
    from emailer import send_email

    result = send_email(summary_html)
    print(f"Email sent successfully. ID: {result.get('id', 'unknown')}")


if __name__ == "__main__":
    main()
