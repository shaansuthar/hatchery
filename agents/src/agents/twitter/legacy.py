# Load environment variables
from dotenv import load_dotenv
import os
import requests
import shutil
from tweepy import Client, OAuth1UserHandler, API
import re

# Load the .env file
load_dotenv()

# Twitter API Configuration

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_SECRET = os.getenv("ACCESS_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

twitter_client = Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_SECRET
)

# Utility function to download files
def download(uri, filename):
    response = requests.get(uri, stream=True)
    if response.status_code == 200:
        with open(filename, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        print(f"Downloaded {filename} from {uri}")
    else:
        print(f"Failed to download {uri}. Status code: {response.status_code}")

def upload_media(filename):
    tweepy_auth = OAuth1UserHandler(
        API_KEY, API_SECRET, access_token=ACCESS_TOKEN, access_token_secret=ACCESS_SECRET
    )
    tweepy_api = API(tweepy_auth)

    post = tweepy_api.simple_upload(filename)
    text = str(post)
    media_id = re.search("media_id=(.+?),", text).group(1)
    return media_id


# Main tweet function
def tweet():
    uri = "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg"
    filename = "image.png"
    try:
        download(uri, filename)
        # Upload the image to Twitter
        media_id = upload_media(filename)

        # Post the tweet
        twitter_client.create_tweet(text="omg squid game1",  media_ids=[media_id], user_auth=True)
        
    except Exception as e:
        print(f"Error: {e}")

# Execute the function
tweet()