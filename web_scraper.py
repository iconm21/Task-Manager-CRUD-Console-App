# web_scraper.py
# Interactive web scraper for quotes.toscrape.com
# Menu: view a page, search by author, search by tag, export CSV

import csv
import sys
from typing import List, Dict, Tuple
import requests
from bs4 import BeautifulSoup

BASE_URL = "http://quotes.toscrape.com"


def fetch_page(page: int) -> Tuple[List[Dict], bool]:
    """
    Returns (quotes, has_next_page)
    quotes: list of {text, author, tags}
    """
    url = f"{BASE_URL}/page/{page}/"
    try:
        r = requests.get(url, timeout=10)
        if r.status_code == 404:
            return [], False
        r.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ Network error: {e}")
        return [], False

    soup = BeautifulSoup(r.text, "html.parser")
    q_divs = soup.select("div.quote")
    quotes = []
    for q in q_divs:
        text = q.select_one("span.text").get_text(strip=True)
        author = q.select_one("small.author").get_text(strip=True)
        tags = [t.get_text(strip=True) for t in q.select("div.tags a.tag")]
        quotes.append({"text": text, "author": author, "tags": tags})

    has_next = soup.select_one("li.next a") is not None
    return quotes, has_next


def print_quotes(quotes: List[Dict]):
    if not quotes:
        print("⚠️ No quotes found.")
        return
    for i, q in enumerate(quotes, 1):
        tags = ", ".join(q["tags"]) if q["tags"] else "-"
        print(f"\n{i}. {q['text']}\n   — {q['author']}  |  Tags: {tags}")


def search_across_pages(predicate, max_pages: int = 10) -> List[Dict]:
    results: List[Dict] = []
    page = 1
    while page <= max_pages:
        quotes, has_next = fetch_page(page)
        for q in quotes:
            if predicate(q):
                results.append(q)
        if not has_next:
            break
        page += 1
    return results


def export_csv(quotes: List[Dict], filename: str = "quotes.csv"):
    if not quotes:
        print("⚠️ Nothing to export.")
        return
    with open(filename, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["Text", "Author", "Tags"])
        for q in quotes:
            w.writerow([q["text"], q["author"], ", ".join(q["tags"])])
    print(f"✅ Exported {len(quotes)} quotes to {filename}")


def main():
    last_results: List[Dict] = []  # what you last viewed/searched (for export)
    while True:
        print("\n=== Interactive Web Scraper ===")
        print("1) View quotes from a page")
        print("2) Search quotes by author (across pages)")
        print("3) Search quotes by tag (across pages)")
        print("4) Export last results to CSV")
        print("5) Exit")
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            try:
                page = int(input("Enter page number (1..): ").strip())
            except ValueError:
                print("⚠️ Enter a valid number.")
                continue
            quotes, _ = fetch_page(page)
            last_results = quotes
            print_quotes(quotes)

        elif choice == "2":
            name = input("Author name (e.g., Albert Einstein): ").strip().lower()
            try:
                max_pages = int(input("Max pages to search (default 10): ") or "10")
            except ValueError:
                max_pages = 10
            results = search_across_pages(
                lambda q: name in q["author"].lower(),
                max_pages=max_pages,
            )
            last_results = results
            print_quotes(results)
            print(f"\n🔎 Found {len(results)} quotes by '{name.title()}'.")

        elif choice == "3":
            tag = input("Tag (e.g., life, love, truth): ").strip().lower()
            try:
                max_pages = int(input("Max pages to search (default 10): ") or "10")
            except ValueError:
                max_pages = 10
            results = search_across_pages(
                lambda q: any(tag == t.lower() for t in q["tags"]),
                max_pages=max_pages,
            )
            last_results = results
            print_quotes(results)
            print(f"\n🏷️ Found {len(results)} quotes with tag '{tag}'.")

        elif choice == "4":
            export_csv(last_results)

        elif choice == "5":
            print("👋 Bye!")
            sys.exit(0)

        else:
            print("⚠️ Invalid choice. Try again.")


if __name__ == "__main__":
    main()
