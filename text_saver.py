import json

def save_sent_message(message, filename: str = "sent_messages.txt"):
    """Append the sent message details to a text file."""
    with open(filename, "a", encoding="utf-8") as f:
        for article in message:
            f.write(json.dumps(article, ensure_ascii=False) + "\n")
        f.write("-" * 40 + "\n")