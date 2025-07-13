import feedparser

def fetch_articles_by_tags(tags, max_articles_per_tag=None):
    articles = []
    seen_links = set()

    for tag in tags:
        tag_url = tag.replace(" ", "-")  # Medium feeds use hyphens in tag URLs
        feed_url = f"https://medium.com/feed/tag/{tag_url}"
        feed = feedparser.parse(feed_url)

        entries = feed.entries if max_articles_per_tag is None else feed.entries[:max_articles_per_tag]

        for entry in entries:
            if entry.link in seen_links:
                continue  # Avoid duplicates

            seen_links.add(entry.link)

            # Extract tag terms
            tag_terms = [t['term'] for t in entry.get('tags', [])]

            articles.append({
                "title": entry.title,
                "link": entry.link,
                "summary": entry.summary,
                "published": entry.published,
                "tags": tag_terms
            })

    return articles
