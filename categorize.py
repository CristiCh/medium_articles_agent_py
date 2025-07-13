from openai import OpenAI

def categorize_article(summary, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.1", #"gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant that categorizes Medium articles."},
            {"role": "user", "content": f"Categorize the following summary into a concise topic without prefixing it with 'Topic:' or any label: {summary}"}
        ],
        temperature=0.5,
        max_tokens=100
    )
    return response.choices[0].message.content.strip()