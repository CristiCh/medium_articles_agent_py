from openai import OpenAI

def summarize_article(text, api_key):
    client = OpenAI(api_key=api_key)
    response = client.chat.completions.create(
        model="gpt-4.1", #"gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that summarizes Medium articles."},
            {"role": "user", "content": f"Summarize this article  without prefixing it with  **Summary:** and remove 'The article'intro, Get straight to it: {text}"}
        ],
        temperature=0.5,
        max_tokens=300
    )
    return response.choices[0].message.content.strip()

def extract_key_idea(summary, api_key):
    client = OpenAI(api_key=api_key)
    
    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {
                "role": "system",
                "content": "You are an assistant that summarizes the key idea of Medium articles."
            },
            {
                "role": "user",
                "content": f"Extract the key idea of this article summary in one clear sentence, removing prefix 'This article explains': {summary}"
            }
        ],
        temperature=0.5,
        max_tokens=100
    )
    
    return response.choices[0].message.content.strip()
