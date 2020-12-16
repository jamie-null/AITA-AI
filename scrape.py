from datetime import datetime
import praw
from psaw import PushshiftAPI
import pickle

r = praw.Reddit('AITA-AI', user_agent='AITA-AI scraper v 0.1')
api = PushshiftAPI(r)

posts = api.search_submissions(before="1d",subreddit="amitheasshole")

with open('posts.pkl','ab') as f:
    for post in posts:
        print(datetime.fromtimestamp(post.created_utc))
        pickle.dump(post,f)
