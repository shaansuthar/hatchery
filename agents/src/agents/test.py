import json
from callbacks import post_tweet
from dotenv import load_dotenv
load_dotenv()

post = {
  "caption": "Happy Monday! 🌸 Start your week with fresh blooms. Discover the beauty of nature in our new collection. #NatureLovers #FreshStart #MondayMotivation",
  "image_url": "https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg"
}

post_tweet(json.dumps(post, indent=4))