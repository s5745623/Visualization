'''
Author: Steven Chang
Net ID: yc704
Title: HW7 
'''

import tweepy
from tweepy import OAuthHandler
import json
from tweepy import Stream
from tweepy.streaming import StreamListener
import sys
import json
from nltk.tokenize import word_tokenize
from nltk.tokenize import TweetTokenizer
import re
from os import path
from scipy.misc import imread
import matplotlib.pyplot as plt
##install wordcloud
from wordcloud import WordCloud, STOPWORDS
import re
import nltk
from nltk.corpus import stopwords
from pprint import pprint



class Listener(StreamListener):

	#print("In Listener...")
	tweet_number = 0

	def __init__(self, max_tweets):
		self.max_tweets = max_tweets
		print(self.max_tweets)
	
	def on_data(self, data):
		self.tweet_number += 1
		print('In on_data', self.tweet_number)
		try:
			print('In on_data in try')
			tweet = json.loads(data)
			with open('Twitter_RAW.json', 'a') as f:
				json.dump(tweet, f)
		except BaseException:
			print('NOPE')
			pass
		if self.tweet_number >= self.max_tweets:
			#sys.exit('Limit of ' + str(self.max_tweets) + 'tweet reached.')
			return False

	def on_error(self, status):
		print('ERROR')
		if status==420:		
			print('ERROR', status, 'rate limited')
			return False
 
def Parsejson():

	with open('Twitter_RAW.json', 'r') as f:
		data = f.read()
	

	pattern1 = re.compile('\"text\":\s\"(.+?)\"')
	text = re.findall(pattern1, data)

	for i in range(len(text)):
		text[i] = text[i].replace("\\n\\n",'')
		text[i] = re.sub(r"\\",'', text[i])
		text[i] = re.sub(r"\\.[\d]+",'', text[i])
		text[i] = re.sub(r"@|#",'', text[i])
		text[i] = re.sub(r"https://[^\s\'\"]+",'', text[i])
	
	
	tweet = []
	for text_cleaned in text:
		tweet_tokenized = [word for word in text_cleaned.split(' ') if word not in stopwords.words('english')]	
		#tweet.append(text_cleaned.lower())
		tweet_string = ' '.join(tweet_tokenized)
		tweet.append(tweet_string)
	#print(tweet)
		
		with open('tweet_cleaned.txt', 'w') as f:
			for line in tweet:
				f.write(line+'\n')
		f.close()
		
	return tweet

def Wordcloud(tweet):

	text_string = ' '.join(tweet)
	wordcloud = WordCloud().generate(text_string)
	plt.imshow(wordcloud, interpolation = 'bilinear')
	plt.axis("off")
	wordcloud = WordCloud().generate(text_string)
	plt.show()

def WordCount(tweet):

	tweet_len = len(tweet)
	freq = nltk.FreqDist(tweet)
	count = freq.most_common(tweet_len)
	print('\n\nWordCount:\n')
	for i in range(len(count)):
		print(count[i][0] + ', ' +str(count[i][1])) 

	with open('tweet_wordcount.txt', 'w') as f:
			for i in range(len(count)):
				f.write(count[i][0] + '\t' +str(count[i][1]) + '\n')
	f.close()


def main():

	hashtag = input('Enter a hashtag start with #: ')
	while (not hashtag.startswith('#')):
		print('\nPlease input start with #')
		hashtag = input('Enter a hashtag start with #: ')

	tweets = input('\nEnter how many tweets: ')
	while (int(tweets)>30):
		print('\nMaximum is 30 tweets, please re-enter')
		tweets = input('Enter how many tweets: ')



	consumer_key= 'fnNCz9EUaEbvJ6DR3uuHHVVId'
	consumer_secret= 'JvnTb3Xq5IjcZetBy5m2SVZNLjYsQMQzxWHnd7rrozjH6DcXhO'
	access_token= '455862038-8OGUeSSWD7FVdRj5lqDR4RUnlTy5TzFnRzdZ4aZI'
	access_secret= 'wnPiHLrI0i6EMuiTW8WuulZvGInMIanQ0VQCYa2q0L6aQ'

	auth= OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_secret)
	api= tweepy.API(auth)
	#print(api.home_timeline())


	twitter_stream= Stream(auth, Listener(int(tweets)))
	twitter_stream.filter(track=[hashtag])

	tweet = Parsejson()
	#pprint(tweet)
	WordCount(tweet)

	Wordcloud(tweet)
	

main()



