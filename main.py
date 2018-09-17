import tweepy 

# Fill the Developer's credentials obtained by tweeter  
'''
consumer_key = "XXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXX"
access_key = "XXXXXXXXXXXXX"
access_secret = "XXXXXXXXXXXXXXX"
'''

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

