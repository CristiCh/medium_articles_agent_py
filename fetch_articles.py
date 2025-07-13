import feedparser
import json
import os
from bs4 import BeautifulSoup
import requests
import hashlib

def fetch_articles_by_tags(tags, max_articles_per_tag=None, sent_messages_file="sent_messages.txt"):
    articles = []
    seen_links = set()
    sent_links = load_sent_links(sent_messages_file)

    for tag in tags:
        tag_url = tag.replace(" ", "-")  # Medium feeds use hyphens in tag URLs
        feed_url = f"https://medium.com/feed/tag/{tag_url}"
        feed = feedparser.parse(feed_url)

        entries = feed.entries if max_articles_per_tag is None else feed.entries[:max_articles_per_tag]

        for entry in entries:
            if entry.link in seen_links or entry.link in sent_links:
                continue  # Avoid duplicates and previously sent
            
            image_path = download_article_image(entry.summary, entry.link)
            seen_links.add(entry.link)
            tag_terms = [t['term'] for t in entry.get('tags', [])]

            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary,
                "published": entry.published,
                "tags": tag_terms,
                "image": image_path
            })

    return articles

def load_sent_links(filename="sent_messages.txt"):
    sent_links = set()
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("-" * 5):
                    continue
                try:
                    article = json.loads(line)
                    if "link" in article:
                        sent_links.add(article["link"])
                except json.JSONDecodeError:
                    # skip lines that are not JSON (e.g., separator lines)
                    continue
    return sent_links


def download_article_image(html_summary: str, article_url: str) -> str:
    """Extract the first image from the HTML and download it. Returns local filename."""
    soup = BeautifulSoup(html_summary, 'html.parser')
    img_tag = soup.find('img')
    if not img_tag or not img_tag.get('src'):
        return None

    img_url = img_tag['src']
    ext = os.path.splitext(img_url)[-1].split("?")[0] or ".jpg"
    filename = f"images/{hashlib.md5(article_url.encode()).hexdigest()}{ext}"

    os.makedirs("images", exist_ok=True)
    try:
        response = requests.get(img_url, timeout=10)
        with open(filename, "wb") as f:
            f.write(response.content)
        return filename
    except Exception as e:
        print(f"Failed to download image: {img_url} - {e}")
        return None
