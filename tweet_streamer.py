from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

import twitter_credential
import numpy as np
import pandas as pd


### TWITTER CLIENT ###
class TwitterClient():

	def __init__(self, twitter_user=None):

		self.auth = TwitterAuthenticator().authenticate_twitter_app()
		self.twitter_client = API(self.auth, wait_on_rate_limit=True)

		self.twitter_user = twitter_user

	def get_twitter_client_api(self):

		return self.twitter_client

	def get_user_timeline_tweets(self, num_tweets):
		tweets =[]

		for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
			tweets.append(tweet)
		return tweets

	def get_home_timeline_tweets(self, num_tweets):
		home_timeline_tweets = []

		for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
			home_timeline_tweets.append(tweet)

		return home_timeline_tweets


### TWITTER AUTHENTICATOR###
class TwitterAuthenticator():

	def authenticate_twitter_app(self):
		auth = OAuthHandler(twitter_credential.CONSUMER_KEY, twitter_credential.CONSUMER_SECRET)
		auth.set_access_token(twitter_credential.ACCESS_TOKEN, twitter_credential.ACCESS_TOKEN_SECRET)
		return auth
### TWITTER STREAMTER ###
class TwitterStreamer():

	def __init__(self):
		self.twitter_authenticator = TwitterAuthenticator()

	def stream_tweets(self, fetched_filename, hash_tag_list):
		listener = TwitterListener(fetched_filename)
		auth = self.twitter_authenticator.authenticate_twitter_app()
		stream = Stream(auth, listener)

		# To filter twitter stream using keywords
		stream.filter(track=hash_tag_list)


class TwitterListener(StreamListener):

	def __init__(self, fetched_filename):
		self.fetched_filename = fetched_filename

	def on_data(self, data):

		try:
			print(data)
			with open(self.fetched_filename, 'a') as tf:
				tf.write(data)
			return True

		except BaseException as e:
			print("Error on data: %s" % str(e))

	def on_error(self, status):
		if status == 420:
			# Returning False on_data menthod in case rate limit occurs.
			return False
		print(status)

class TweetAnalyzer():
	"""
	Functionality for analyzing and categorizing from tweets
	"""

	def tweets_to_data_frame(self,tweets):

		df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])
		df['date'] = np.array([tweet.created_at for tweet in tweets])
		
		
		
		return df

if __name__ == "__main__":

	# hash_tag_list=['#KMJS']
	# fetched_filename = "tweets.json"

	# twitter_client = TwitterClient('mariachigamez')
	# print(twitter_client.get_home_timeline_tweets(1))

	# twitter_stream = TwitterStreamer()
	# twitter_stream.stream_tweets(fetched_filename,hash_tag_list)
	username = input("Enter username: ")

	twitter_client = TwitterClient()
	tweet_analyzer = TweetAnalyzer()
	api = twitter_client.get_twitter_client_api()

	tweets = api.home_timeline(screen_name=username, count=20)

	df = tweet_analyzer.tweets_to_data_frame(tweets)

	print(df)
	