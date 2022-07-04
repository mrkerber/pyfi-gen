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
    post_img = './img/' + str(id) + '.jpeg'
    prior_img = './img/' + str(id - 1) + '.jpeg'
    tweet_text = f'Prompt #{id + 1}: ' + phrase
    try:
        media = api.media_upload(post_img)
    except:
        print('Unable to load media')
    try:
        if api.update_status(status=tweet_text, media_ids=[media.media_id]):
            print("Tweet success")
            try:
                os.remove(prior_img)
            except:
                print('!ERROR: Unable to delete image')
    except tweepy.error.TweepError as e:
        print(e)