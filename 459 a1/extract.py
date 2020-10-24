# The code is provided by TA
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
import re

ACCESS_TOKEN = '750712360319406081-YMh0VKpNqEiVo4SYtkMZFu0i8swuNW7'
ACCESS_TOKEN_SECRET = 'teO7koe0CPKd1LWXQS7J1kPc5Nc7U9viKEeaMQfopqlhb'
CONSUMER_KEY = 'ZpN2pKCRjtex1oTokbpnkZaIQ'
CONSUMER_SECRET = '1elflKrKCZ0Gnoy2NWMv5cwzeJAiDAAZ2WEq2yWAkYDrU95bGd'

tracklist = ['COVID-19']
tweet_count = 0
n_tweets = 1000
# D1
# f = open('D1.txt','w')
# D2
f = open('D2.txt', 'w')
f.close()


class StdOutListener(StreamListener):
    def on_data(self, data):
        global tweet_count
        global n_tweets
        global stream

        if tweet_count < n_tweets:
            try:
                print(tweet_count, '\n')
                tweet_data = json.loads(data)
                pattern1 = re.compile(r'\n')
                tweet_txt = pattern1.sub(r'', tweet_data['text'])
                pattern2 = re.compile(r'RT')
                tweet = pattern2.sub(r'', tweet_txt)
                # D1
                # f = open('D1.txt', 'a+')
                # D2
                f = open('D2.txt', 'a+')
                f.write(str(tweet_data['id'])+'\t'+tweet+'\n')
                tweet_count += 1
            except BaseException:
                print('Error:', tweet_count)
            return True
        else:
            stream.disconnect()

    def on_error(self, status):
        print(status)


l = StdOutListener()
auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
stream = Stream(auth, l)
# D1
# stream.sample(is_async=True, languages=['en'])
# D2
stream.filter(track=tracklist, languages=['en'])
