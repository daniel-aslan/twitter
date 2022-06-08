#! /usr/bin/env python3
'''
Using this tutorial
https://www.youtube.com/watch?v=0EekpQBEP_8
'''

import tweepy
import os
from datetime import datetime

# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")

client = tweepy.Client(bearer_token)
#I can create a regex with vim or sed to replace this variable just once and rerun it.
tag = "heatnation"

def search_tweets(tag):
    query = "#{} -is:retweet".format(tag)
    file_name ='tweets.txt'
    file_timestamp = datetime.now().strftime('%Y%m%d')
    tweet_file = file_timestamp + file_name
    with open(tweet_file, 'a+') as filehandler:
        for tweet in tweepy.Paginator(client.search_recent_tweets, query=query).flatten():
            #print(tweet.text + '\n')
            filehandler.write('%s\n' % tweet.text)
        

def main():
    search_tweets(tag)

if __name__ == '__main__':
    main()