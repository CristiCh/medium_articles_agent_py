from langdetect import detect
from openai import OpenAI

def is_english(text):
    try:
        return detect(text) == "en"
    except:
        return False

def choose_top_ios_articles(articles, api_key):
    client = OpenAI(api_key=api_key)
    
    # Filter English articles based on summary or title (fallback to summary)
    english_articles = [a for a in articles if is_english(a.get("summary", "") or a.get("title", ""))]

    if not english_articles:
        print("No English articles detected.")
        return []

    articles_text = ""
    for i, art in enumerate(english_articles, start=1):
        articles_text += (
            f"{i}. Title: {art['title']}\n"
            f"   Summary: {art['summary']}\n"
            f"   URL: {art['link']}\n\n"
        )
    
    prompt = (
        "You are an expert business professional with strong IT knowledge.\n"
        "From the list below, select the top 3 articles that would deliver the most valuable insights for an iOS developer interested in AI and monetization.\n"
        "Return only the numbers of the top 3 articles in order, separated by commas.\n\n"
        f"Articles:\n{articles_text}\n"
        "Answer with only the numbers separated by commas, e.g. 2,5,1"
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=50,
        )
        answer = response.choices[0].message.content.strip()
        indexes = [int(x.strip()) - 1 for x in answer.split(",") if x.strip().isdigit()]
        top_articles = [english_articles[i] for i in indexes if 0 <= i < len(english_articles)]
        return top_articles[:3]

    except Exception as e:
        print(f"OpenAI API error: {e}")
        return []
