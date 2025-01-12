import os
import re
import requests
import shutil
from tweepy import Client, OAuth1UserHandler, API

class TwitterBot:
    def __init__(self, api_key, api_secret, access_token, access_secret, bearer_token):
        # Twitter API Configuration
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token
        self.access_secret = access_secret
        self.bearer_token = bearer_token

        # Initialize Twitter client
        self.client = Client(
            bearer_token=self.bearer_token,
            consumer_key=self.api_key,
            consumer_secret=self.api_secret,
            access_token=self.access_token,
            access_token_secret=self.access_secret
        )

    @staticmethod
    def download_file(uri, filename):
        """Download a file from a URI and save it locally."""
        response = requests.get(uri, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as out_file:
                shutil.copyfileobj(response.raw, out_file)
            print(f"Downloaded {filename} from {uri}")
        else:
            raise Exception(f"Failed to download {uri}. Status code: {response.status_code}")

    def upload_media(self, filename):
        """Upload media to Twitter and return the media ID."""
        auth = OAuth1UserHandler(
            self.api_key, self.api_secret, access_token=self.access_token, access_token_secret=self.access_secret
        )
        api = API(auth)
        post = api.simple_upload(filename)
        media_id = re.search("media_id=(.+?),", str(post)).group(1)
        return media_id

    def tweet(self, text, media_uri):
        """Post a tweet with optional media."""
        filename = "temp_media.png"
        try:
            # Download the media file
            self.download_file(media_uri, filename)

            # Upload the media to Twitter
            media_id = self.upload_media(filename)

            # Post the tweet
            self.client.create_tweet(text=text, media_ids=[media_id], user_auth=True)
            print("Tweet posted successfully.")
        except Exception as e:
            print(f"Error while tweeting: {e}")
        finally:
            # Clean up downloaded file
            if os.path.exists(filename):
                os.remove(filename)