import datetime
from googleapiclient.discovery import build
from openai import OpenAI
import config

def get_monday_recipes(query, openai_api_key, youtube_api_key):
    # Check if today is Monday (0 = Monday)
    if datetime.datetime.today().weekday() != 0:
        return None
    
    raw_recipes = search_youtube_recipes(youtube_api_key, query)
    client = OpenAI(api_key = openai_api_key)
    prompt = f"""
        Please choose three {query} from these {raw_recipes} For each recipe, include:
        - Title
        - YouTube video link (use the exact original video URL provided; DO NOT change, shorten, or modify it in any way)
        - Photo link (use the exact original photo URL provided; DO NOT change, shorten, or modify it in any way)
        - List of ingredients
        - Short step-by-step cooking instructions

        Format the response exactly like this example (keep URLs exactly as given, without adding or removing anything):

        1. Recipe Title
        Video: https://www.youtube.com/watch?v=original_video_id
        Photo: https://img.youtube.com/vi/original_video_id/hqdefault.jpg
        Ingredients:
        - ingredient 1
        - ingredient 2
        Steps:
        • Step 1
        • Step 2

        Make sure the recipes are healthy, tasty, and use only one pot.

        IMPORTANT: The video and photo URLs must remain exactly as originally provided, with no changes, no shortening, no reformatting, and no additions.
        """
    
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant that provides recipes."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.7,
        max_tokens=700,
        n=1,
    )

    return response.choices[0].message.content.strip()

def search_youtube_recipes(youtube_api_key, query, max_results=9):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    request = youtube.search().list(
        q=query,
        part="snippet",
        maxResults=max_results,
        type="video",
        publishedAfter=(datetime.datetime.utcnow() - datetime.timedelta(days=365)).isoformat("T") + "Z"
    )
    response = request.execute()
    
    videos = []
    for item in response['items']:
        video_id = item['id']['videoId']
        title = item['snippet']['title']
        thumbnail = item['snippet']['thumbnails']['high']['url']
        
        videos.append({
            'title': title,
            'video_link': f"https://www.youtube.com/watch?v={video_id}",
            'photo_link': thumbnail
        })
    return videos

if __name__ == "__main__":
    recipes = get_monday_recipes("healthy tasty one pot recipes", config.OPENAI_API_KEY, config.YOUTUBE_API_KEY)
    if recipes:
        print("Here are your Monday recipes:\n")
        print(recipes)
    else:
        print("Today is not Monday, no recipes to send.")
        