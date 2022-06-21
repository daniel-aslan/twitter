#! /usr/bin/env python3

'''
This is the s3 endpoint
http://dannys-weekly-tweets.s3-website-us-east-1.amazonaws.com/
'''

import tweepy
import os
from datetime import datetime
import boto3

'''
Global Variables:
'''
#Removing the timestamp feature but just commenting it out in case I want it again later
#file_timestamp = datetime.now().strftime('%Y%m%d')
tweet_file = 'index.html'
bearer = 'bearer-token-encypt'
bucket = 'dannys-weekly-tweets'

'''
 Beginning of Functions
'''

#Get the twitter bearer token as a secret from aws parameter store 
def parameter_store():
    ssm = boto3.client('ssm')
    response = ssm.get_parameter(Name=bearer, WithDecryption=True)
    bearer_token = response['Parameter']['Value']
    return bearer_token

#Search twitter from the last 7 days and create a file that will be sent to s3 to be a static web page
def search_tweets(tag):
    client = tweepy.Client(parameter_store())
    query = "#{} -is:retweet".format(tag)
    #This will be the html headers
    with open(tweet_file, 'a+') as filehandler:
        filehandler.write(f'<!DOCTYPE html> \n <html> \n <body> \n\n <h1>My Weekly {tag} Tweet Digest</h1> \n\n ')
    #This will be the actual tweet.  I may revisit this and try to use another method to just insert the body into a template.  But need to work on that later.    
    with open(tweet_file, 'a+') as filehandler:
        for tweet in tweepy.Paginator(client.search_recent_tweets, query=query).flatten():
            filehandler.write('<p> %s \n </p>' % tweet.text)
    #This is to close off the headers at the end of the page
    with open(tweet_file, 'a+') as filehandler:
        filehandler.write('</body>\n </html>\n ')

# This sends the file to Amazon S3, make sure that the bucket is already set up to be a static web page.  
# Also use the Extra args to make sure that the content type is right otherwise it won't serve right
def send_to_s3(bucket):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(tweet_file, bucket, 'index.html', ExtraArgs={'ContentType': 'text/html'})

def main():
    search_tweets('HeatNation')
    search_tweets('python3')
    search_tweets('LabEveryday')
    send_to_s3(bucket)

if __name__ == '__main__':
    main()
