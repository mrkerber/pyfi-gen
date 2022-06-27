import tweepy
from dotenv import load_dotenv
import os

load_dotenv()

auth = tweepy.OAuthHandler(
    os.getenv('CONSUMER_KEY'), os.getenv('CONSUMER_SECRET')
)
auth.set_access_token(
     os.getenv('ACCESS_TOKEN'), os.getenv('ACCESS_TOKEN_SECRET')
)
api = tweepy.API(auth)

def postTweet(phrase, id):
    imgfile = './img/' + str(id) + '.png'
    media = api.media_upload(imgfile)
    try:
        if api.update_status(status=phrase, media_ids=[media.media_id]):
            print("Tweet success")
            os.remove(imgfile)
    except tweepy.error.TweepError as e:
        print(e)