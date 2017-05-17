import re
import tweepy
from tweepy import OAuthHandler
from textblob import TextBlob
import numpy as np
import matplotlib.pyplot as plt

class TwitterClient(object):
    def __init__(self):
        consumer_key = "4RV0pP34PCNZOYYBzKSY1woq1"
        consumer_secret = "0CLxxt72g9BrczIa8fK3HY7WzwvBY4zvZvHw5pJldYi43jYQhs"
        access_token = "286003503-gJg6tUXlhwDdK5nVk8n9mCN8HJG0QN3VwEc3U4jw"
        access_token_secret = "ZkqDI7lV15laCCQbogNzqzxxAQDUC4lH60H7MF3g2e57w"
        # attempt authentication
        try:
            # create OAuthHandler object
            self.auth = OAuthHandler(consumer_key, consumer_secret)
            # set access token and secret
            self.auth.set_access_token(access_token, access_token_secret)
            # create tweepy API object to fetch tweets
            self.api = tweepy.API(self.auth)
        except:
            print("Error: Authentication Failed")

    def clean_tweet(self, tweet):
        return (' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split()))

    def get_tweet_sentiment(self, tweet):
        # create TextBlob object of passed tweet text
        analysis = TextBlob(self.clean_tweet(tweet))
        # set sentiment
        if analysis.sentiment.polarity > 0:
            return 'positive'
        elif analysis.sentiment.polarity == 0:
            return 'neutral'
        else:
            return 'negative'

    def get_tweets(self, query, count = 10):
        # empty list to store parsed tweets
        tweets = []

        try:
            # call twitter api to fetch tweets
            fetched_tweets = self.api.search(q = query, count = count)

            # parsing tweets one by one
            for tweet in fetched_tweets:
                # empty dictionary to store required params of a tweet
                parsed_tweet = {}

                # saving text of tweet
                parsed_tweet['text'] = tweet.text
                # saving sentiment of tweet
                parsed_tweet['sentiment'] = self.get_tweet_sentiment(tweet.text)

                # appending parsed tweet to tweets list
                if tweet.retweet_count > 0:
                    # if tweet has retweets, ensure that it is appended only once
                    if parsed_tweet not in tweets:
                        tweets.append(parsed_tweet)
                else:
                    tweets.append(parsed_tweet)

            # return parsed tweets
            return tweets

        except tweepy.TweepError as e:
            # print error (if any)
            print("Error : " + str(e))

def main():
    # creating object of TwitterClient Class
    api = TwitterClient()

    keyword=input("Enter political party")
    tweets = api.get_tweets(query = keyword, count = 1000)
    ptweets = [tweet for tweet in tweets if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100*len(ptweets)/len(tweets)))
    party1pos=100*len(ptweets)/len(tweets)
    ntweets = [tweet for tweet in tweets if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100*len(ntweets)/len(tweets)))
    party1neg=100*len(ntweets)/len(tweets)
    print("Neutral tweets percentage: {} % ".format(100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)))
    party1neut=100*(len(tweets) - len(ntweets) - len(ptweets))/len(tweets)
    print("\n\nPositive tweets:")
    for tweet in ptweets[:10]:
        print(tweet['text'])
    print("\n\nNegative tweets:")
    for tweet in ntweets[:10]:
        print(tweet['text'])

    keyword1=input("Enter political party")
    tweets1 = api.get_tweets(query = keyword1, count = 1000)
    ptweets1 = [tweet for tweet in tweets1 if tweet['sentiment'] == 'positive']
    print("Positive tweets percentage: {} %".format(100*len(ptweets1)/len(tweets1)))
    party2pos=100*len(ptweets1)/len(tweets1)
    ntweets1 = [tweet for tweet in tweets1 if tweet['sentiment'] == 'negative']
    print("Negative tweets percentage: {} %".format(100*len(ntweets1)/len(tweets1)))
    party2neg=100*len(ntweets1)/len(tweets1)
    print("Neutral tweets percentage: {} % ".format(100*(len(tweets1) - len(ntweets1) - len(ptweets1))/len(tweets1)))
    party2neut=100*(len(tweets1) - len(ntweets1) - len(ptweets1))/len(tweets1)
    print("\n\nPositive tweets:")
    for tweet in ptweets1[:10]:
        print(tweet['text'])
    print("\n\nNegative tweets:")
    for tweet in ntweets1[:10]:
        print(tweet['text'])
    #for graph
    n_groups = 2
    val=20
    means_pos = (party1pos,party2pos)
    means_neg = (party1neg,party2neg)
    means_neut = (party1neut,party2neut)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.20
    opacity = 0.4
    error_config = {'ecolor': '0.3'}
    rects1 = plt.bar(index, means_pos, bar_width,
                 alpha=opacity,
                 color='b',
                 yerr=0,
                 error_kw=error_config,
                 label='Positive')
    rects2 = plt.bar(index + bar_width, means_neg, bar_width,
                 alpha=opacity,
                 color='r',
                 yerr=0,
                 error_kw=error_config,
                 label='Negative')
    rects3 = plt.bar(index + bar_width+bar_width, means_neut, bar_width,
                 alpha=opacity,
                 color='g',
                 yerr=0,
                 error_kw=error_config,
                 label='Neutral')
    plt.xlabel('Sentiment')
    plt.ylabel('Percentage')
    plt.title('Sentiment Analysis')
    plt.xticks(index + bar_width / 1,(keyword,keyword1))
    plt.legend()
    plt.tight_layout()
    plt.show()
    if(party2neg>party1neg):
        print(keyword," has more chances to win!!!")
    else:
        print(keyword1," has more chances to win!!!")

if __name__ == "__main__":

    main()