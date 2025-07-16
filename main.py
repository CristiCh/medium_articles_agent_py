from fetch_articles import fetch_articles_by_tags
from summarize_articles import summarize_article, extract_key_idea
from categorize import categorize_article
from email_sender import send_email
from text_saver import save_sent_message
from fetch_weather import fetch_weather
from fetch_quote import get_inspirational_quote
from article_chooser import choose_top_ios_articles
from fetch_algorithm import generate_swift_algorithm_exercise
import config

def main():
    tags = ["ai", "ios development", "swift", "swift ai"]
    raw_articles = fetch_articles_by_tags(tags, max_articles_per_tag=5)
    processed_articles = []
    selected_articles = choose_top_ios_articles(raw_articles, config.OPENAI_API_KEY)

    for article in selected_articles:
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
            "tags": article.get("tags", []),
            "image": article["image"]
        })

    weather = fetch_weather(config.ACCUWEATHER_API_KEY)
    quote = get_inspirational_quote(config.OPENAI_API_KEY)
    exercise = generate_swift_algorithm_exercise(config.OPENAI_API_KEY)

    send_email(config.RECIPIENT_EMAIL, 
               processed_articles, 
               config.SENDER_EMAIL, 
               config.SENDER_PASSWORD, 
               weather,
               quote,
               exercise)
    save_sent_message(message=processed_articles)

if __name__ == "__main__":
    main()
