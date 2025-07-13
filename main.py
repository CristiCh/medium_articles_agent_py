from fetch_articles import fetch_articles_by_tags
from summarize_articles import summarize_article, extract_key_idea
from categorize import categorize_article
from email_sender import send_email
import config

def main():
    tags = ["ai", "ios development", "swift", "swift ai"]
    raw_articles = fetch_articles_by_tags(tags, max_articles_per_tag=3)
    processed_articles = []

    for article in raw_articles[:3]:
        summary_data = summarize_article(article['summary'], config.OPENAI_API_KEY)
        key_idea = extract_key_idea(article['summary'], config.OPENAI_API_KEY)
        category = categorize_article(article['summary'], config.OPENAI_API_KEY)

        processed_articles.append({
            "title": article["title"],
            "link": article["link"],
            "summary": summary_data,
            "key_idea": key_idea.strip(),
            "category": category,
            "published": article.get("published", "Unknown"),
            "tags": article.get("tags", []) 
        })

    send_email(config.RECIPIENT_EMAIL, processed_articles, config.SENDER_EMAIL, config.SENDER_PASSWORD)

if __name__ == "__main__":
    main()
