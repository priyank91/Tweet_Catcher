import tweepy 
import json
from bson import json_util # to install bson install pymongo [https://stackoverflow.com/questions/35254975/import-error-no-module-named-bson]
import logging as log

log.basicConfig(
       filename="collection.log",
       level=log.INFO,
       format="%(asctime)s:%(levelname)s:%(message)s"
       )


# Fill the Developer's credentials obtained by tweeter  
'''
consumer_key = "XXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXX"
access_key = "XXXXXXXXXXXXX"
access_secret = "XXXXXXXXXXXXXXX"
'''
def stream_tweet_catcher():
	class StreamListener(tweepy.StreamListener):
	    def on_connect(self):
		log.info("Connected to the streaming API")

	    def on_error(self, status_code):
		log.info("An error occured, error code is below:\n{}".format(repr(status_code)))

	    def on_status(self,status):
		try:
		    with open('streamlistener.json', 'a') as f:
			obj = json.dumps(status._json, ensure_ascii=False)
			obj = json.loads(obj)
			if obj['lang']=='en':
			    f.write(json_util.dumps(obj)+'\n')
		except:
		    pass
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	listener = StreamListener(api=tweepy.API(wait_on_rate_limit=True, wait_on_rate_limit_notify=True))
	streamer = tweepy.Stream(auth=auth, listener=listener,tweet_mode='extended')
	log.info('Twitter SAMPLE API')
	streamer.sample()

# Function to extract FULL Length of tweets and retweets
def get_tweets_by_username(username):
        # Authorization to consumer key and consumer secret
        try:
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
        except tweepy.TweepError:
            print("Error ! Failed to get Request Token")
            return
		
        # Access to developer's access key and access secret 
        auth.set_access_token(access_key, access_secret) 
  
        # Calling api 
        api = tweepy.API(auth) 
  
        # 200 tweets to be extracted, tweet_mode = 'extended' is important here.
		# Tweets are trucated to 140 characters if tweet_mode is not set to extended.  
        try:
            tweets = api.user_timeline(screen_name=username, tweet_mode='extended', count=200)
        except tweepy.TweepError as e:
            print("Error !! Failed to Read the tweets REASON %s"%(e))
            return
        # Open the file to save the tweets
        fp = open(username+'.txt',"w+")
        # Empty Array to hold all tweets
        tmp=[]  
        tweets_collected=0
        for tweet in tweets:
            if 'retweeted_status' in tweet._json:
                fp.write("RT "+tweet._json['retweeted_status']['user']['screen_name']+": "+tweet._json['retweeted_status']['full_text']+"\n")
            else:
                fp.write(tweet.author._json["screen_name"]+": "+tweet.full_text)
        if len(tweets) == 0:
            print("User did not have any tweets.")
            return
        last_id = tweets[-1].id - 1
        tweets_collected+=len(tweets)
        print(tweets_collected, "Tweets Collected...")
        
		# Getting around 3.2K tweets.
        while True:
            try:
                tweets = api.user_timeline(screen_name=username, tweet_mode='extended', count=200, max_id = last_id)
            except tweepy.TweepError as e:
                print("Failed !! not able to read tweets REASON %s"%(e))
                return
            if len(tweets) == 0:
                break
            # Repeating the tweet segregation( NOTICE the use of full_text in place of text)
            for tweet in tweets:
                if 'retweeted_status' in tweet._json:
                    fp.write("RT "+tweet._json['retweeted_status']['user']['screen_name']+": "+tweet._json['retweeted_status']['full_text']+"\n")
                else:
                    fp.write(tweet.author._json["screen_name"]+": "+tweet.full_text+"\n")
            last_id = tweets[-1].id-1
            tweets_collected+=len(tweets)
            print(tweets_collected, "Tweets Collected...")
        # We have saved the tweets and we can exit now.         
        fp.close()
        return
if __name__ == '__main__': 
  
    # Put screen_name of the user... arora_priyank
    get_tweets_by_username("arora_priyank")
    stream_tweet_catcher()

