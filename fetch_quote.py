import time
import random
from openai import OpenAI

def get_inspirational_quote(api_key, history_path="quotes_history.txt"):
    client = OpenAI(api_key=api_key)

    previous_quotes = load_previous_quotes(history_path)

    quote_styles = [
        "Give me a quote to spark motivation today.",
        "Share a short, powerful quote to start the day inspired.",
        "What's a motivational quote that uplifts and empowers?",
        "Send me a famous or unknown quote that inspires positive action.",
        "Give me a deep, thoughtful quote to reflect on today."
    ]

    for _ in range(5):  # Try up to 5 times to get a unique quote
        prompt = random.choice(quote_styles)

        try:
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "system", "content": "You are a motivational assistant that gives original or famous quotes in a positive, uplifting tone. Do not repeat previous ones."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.95,
                max_tokens=80
            )

            quote = response.choices[0].message.content.strip()

            if quote not in previous_quotes:
                save_quote(quote, history_path)
                print(f"[INFO] Unique Quote: {quote}")
                return quote
            else:
                print(f"[WARN] Duplicate quote detected, retrying...")

        except Exception as e:
            print(f"[ERROR] Failed to fetch quote: {e}")
            return "“Stay positive, work hard, and make it happen.” — Unknown"

    return "“You're doing amazing. Keep pushing forward.” — Unknown"
    
def load_previous_quotes(filepath="quotes_history.txt"):
    try:
        with open(filepath, "r") as f:
            return set(line.strip() for line in f if line.strip())
    except FileNotFoundError:
        return set()

def save_quote(quote, filepath="quotes_history.txt"):
    with open(filepath, "a") as f:
        f.write(quote + "\n")