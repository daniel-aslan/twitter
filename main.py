#! /usr/bin/env python3
'''
Using this tutorial
https://www.youtube.com/watch?v=0EekpQBEP_8
key alias daniel-aslan-june-2022
'''
import tweepy
import os
from datetime import datetime
import boto3

'''
I can create a regex with vim or sed to replace this variable just once and rerun it.

Global Variables:
'''
tag = "heatnation"
file_name ='tweets.txt'
file_timestamp = datetime.now().strftime('%Y%m%d')
tweet_file = file_timestamp + file_name
bearer = 'bearer-token-encypt'
bucket = 'weekly-tweets-digest'

# Beginning of Functions

#Get the twitter bearer token as a secret from aws parameter store 
def parameter_store():
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(Name=bearer, WithDecryption=True)
    bearer_token = response['Parameter']['Value']
    return bearer_token

#Search twitter from the last 7 days and create a file that will be sent to s3
def search_tweets(tag):
    client = tweepy.Client(parameter_store())
    query = "#{} -is:retweet".format(tag)
    with open(tweet_file, 'a+') as filehandler:
        for tweet in tweepy.Paginator(client.search_recent_tweets, query=query).flatten():
            filehandler.write('%s\n------------------------------\n' % tweet.text)

# send the file to Amazon S3
def send_to_s3(bucket):
    s3 = boto3.client('s3')
    with open(tweet_file, "rb") as f:
        s3.upload_fileobj(f, bucket, tweet_file)

def main():
    search_tweets('HeatNation')
    search_tweets('python3')
    search_tweets('LabEveryday')
    send_to_s3(bucket)

if __name__ == '__main__':
    main()