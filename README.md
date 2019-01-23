## Tweet_Catcher
### Introduction: 
Language : Python 3
Description : Script to catch 3246 "full" length tweet and retweet from public account. 
Requirement :  Developer credentials from [here.](https://developer.twitter.com/en/apply-for-access.html)
Functions: 
* Input : User Name(screen name) of the public account. 
* Output : File of username.txt in same directory.
### Code Snippet:
```python
fp = open(username+'.txt',"w+")
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret) 
api = tweepy.API(auth) 
tweets = api.user_timeline(screen_name=username, tweet_mode='extended', count=200) 
# Important here the tweet_mode change the 'text' field to 'full_text' in response.
for tweet in tweets:
    if 'retweeted_status' in tweet._json:
        fp.write("RT "+tweet._json['retweeted_status']['user']['screen_name']+": "+tweet._json['retweeted_status']['full_text']+"\n")
     else:
         fp.write(tweet.author._json["screen_name"]+": "+tweet.full_text)
```
    
