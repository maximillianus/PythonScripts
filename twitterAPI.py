"""
TestScript
to get the data based on last modified time
"""
import sys
sys.path.append("C:\\NotBackedUp\\datascience_projects\\env_ds\\Lib\\site-packages")
print(sys.path)
import time
import tweepy
from tweepy import OAuthHandler
#import urllib3.contrib.pyopenssl
import requests

proxies = {
  'http': 'http://10.62.36.14:80',
  'https': 'http://10.62.36.14:80',
}

api_key = 'VyawrF9rwgNIwmzpdysAKJVXg'
api_secret = 'OSRyPLxPspQ2QLxWh3DhyCa9vFbHUxrbQCNTH1l3YBvXAXJAMk'
token = '47151243-iLQ930rd04pdWbMHGs41XauahJnySHdzGxm91NlJ7'
token_secret = 'XMSdUcNUeXOEwqSjnuFfAUiLx8izMi9iFGzLNJx64Xn8k'

auth = OAuthHandler(api_key, api_secret)
auth.set_access_token(token, token_secret)
auth.secure=True

api = tweepy.API(auth, proxy='https://10.62.36.14:80', timeout=300)
#public_tweets = api.home_timeline()
api_limit = api.rate_limit_status()

home_timeline_reset = api_limit['resources']['statuses']['/statuses/home_timeline']['reset']

print(api_limit['resources']['statuses']['/statuses/home_timeline']['reset'])
