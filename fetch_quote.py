from openai import OpenAI
import config

def get_inspirational_quote(api_key):
    client = OpenAI(api_key=api_key)
    prompt = (
        "Provide an inspirational and motivational quote of the day. "
        "Keep it short, powerful, and uplifting."
        "If quoting someone, mention the name. "
        "Avoid hashtags, just plain text and emojis."
    )

    try:
        response = client.chat.completions.create(
            model="gpt-4.1", #"gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a motivational assistant."},
            {"role": "user", "content": prompt}
        ],
            temperature=0.7,
            max_tokens=80
        )

        quote = response.choices[0].message.content.strip()
        print(f"[INFO] Quote of the Day: {quote}")
        return quote
    except Exception as e:
        print(f"[ERROR] Failed to fetch quote: {e}")
        return "“Stay positive, work hard, and make it happen.” — Unknown"


if __name__ == "__main__":
    get_inspirational_quote(config.OPENAI_API_KEY)