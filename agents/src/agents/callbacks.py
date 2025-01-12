from src.agents.twitter.twitter import TwitterBot
import os
import json

def trim_braces_content(input_string):
    start = input_string.find('{')
    end = input_string.rfind('}')
    if start != -1 and end != -1 and start < end:
        # Both `{` and `}` are found, and `{` comes before `}`
        return input_string[start:end+1]
    elif start != -1:
        # Only `{` is found
        return input_string[start:]
    elif end != -1:
        # Only `}` is found
        return input_string[:end+1]
    else:
        # Neither `{` nor `}` is found
        return input_string


def post_tweet(task_output):
    API_KEY = os.getenv("API_KEY")
    API_SECRET = os.getenv("API_SECRET")
    ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
    ACCESS_SECRET = os.getenv("ACCESS_SECRET")
    BEARER_TOKEN = os.getenv("BEARER_TOKEN")

    try:
        # Attempt to parse the JSON
        parsed_data = json.loads(trim_braces_content(task_output.raw))
        caption = parsed_data.get("caption", "No caption provided")
        image_url = parsed_data.get("image_url", "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg")
        image_url = "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg" # overwriting
        bot = TwitterBot(
            api_key=API_KEY,
            api_secret=API_SECRET,
            access_token=ACCESS_TOKEN,
            access_secret=ACCESS_SECRET,
            bearer_token=BEARER_TOKEN
        )
        bot.tweet(
            text=caption,
            media_uri=image_url
    )
    except Exception as e:
        # Catch JSON parsing errors
        print("Failed to parse JSON. Original task_output:")
        print(task_output)
        print("Error details:", str(e))

