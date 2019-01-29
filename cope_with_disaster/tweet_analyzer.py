import nltk
from nltk.corpus import wordnet
from tweepy import API
from tweepy import Cursor
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from cope_with_disaster import twitter_credentials
from itertools import product
import numpy as np
import pandas as pd
from nltk.tokenize import TweetTokenizer
import paralleldots
import re


#nltk.download('wordnet')
need_keywords = ['need', 'require', 'want', 'lack']
send_keywords = ['send', 'give', 'donate', 'transfer', 'distribute', 'aid', 'help', 'procure']
common_resource = ['food', 'water', 'medicine', 'tent', 'clothes', 'communication', 'transport', 'infrastructure',
                   'shelter', 'internet', 'sanitation', 'hospital', 'donations']

mobile_no = "([+]?[0]?[1-9][0-9\s]*[-]?[0-9\s]+)"
email = "([a-zA-Z0-9]?[a-zA-Z0-9_.]+[@][a-zA-Z]*[.](com|net|edu|in|org|en))"
quant_no = "([0-9]*[,.]?[0-9]+[k]?)"

spam_keywords = ['[/url]', 'thx', 'sex', 'byob', 'nude', 'loan', 'debt', 'poze', 'bdsm', 'soma', 'visa', 'hotel',
                 'paxil', 'anime', 'naked', 'poker', 'coolhu', 'cialis', 'incest', 'casino', 'dating', 'payday',
                 'rental',
                 'ambien',
                 'holdem',
                 'adipex',
                 'booker',
                 'youtube',
                 'myspace',
                 'advicer',
                 'flowers',
                 'finance',
                 'freenet',
                 '=-online',
                 'shemale',
                 'meridia',
                 'cumshot',
                 'trading',
                 'adderall',

                 'gambling',
                 'roulette',
                 'top-site',
                 'mortgage',
                 'pharmacy',
                 'dutyfree',
                 'ownsthis',
                 'duty-free',
                 'insurance', 'ringtones', 'blackjack', 'hair-loss', 'bllogspot', 'baccarrat', 'thorcarlson',
                 'jrcreations', 'credit card', 'macinstruct', 'hydrocodone', 'leading-site', 'slot-machine',
                 'carisoprodol', 'ottawavalleyag', 'cyclobenzaprine', 'discreetordering', 'aceteminophen',
                 'phentermine', 'doxycycline', 'citalopram', 'cephalaxin', 'vicoprofen', 'lorazepam', 'oxycontin',
                 'oxycodone', 'percocet', 'propecia', 'tramadol', 'cymbalta', 'lunestra', 'fioricet', 'lesbian',
                 'lexapro', 'valtrex', 'titties', 'xenical', 'levitra', 'vicodin', 'ephedra', 'lipitor', 'breast',
                 'cyclen', 'viagra', 'valium', 'hqtube', 'ultram', 'clomid', 'vioxx', 'zolus', 'pussy', 'porno',
                 'xanax', 'bitch', 'penis', 'pills', 'porn', 'dick', 'cock', 'tits', 'ass', 'gdf', 'gds', 'baccarat',
                 'car-rentals-e-site', 'casinos', 'coolcoolhu', 'credit-card-debt', 'credit-report', 'cwas',
                 'dating-e-site', 'day-trading', 'debt-consolidation', 'debt-consolidation', 'consultant',
                 'equityloans', 'facial', 'femdom', 'fetish', 'flowers-leading-site', 'freenet-shopping', 'fucking',
                 'gambling', 'insurancedeals', 'holdempoker', 'holdemsoftware', 'holdemtexasturbow', 'ilson',
                 'homeequityloans', 'homefinance', 'hotel-dealse-site', 'hotele-site', 'hotelse-site', 'insurance',
                 'quotesdeals-4u', 'insurancedeals-4u', 'mortgage-4-u', 'mortgagequotes', 'online-gambling',
                 'onlinegambling-4u', 'palm-texas', 'holdem-game', 'poker-chip', 'rental-car-e-site', 'ringtone',
                 'roulette', 'shoes', 'texas holdem', 'texas-holdem', 'top-e-site', 'trim-spa', 'valeofglamorganco',
                 'nservatives']


flood_related_words = ['flood', 'disaster', 'dam', 'river bank', 'rescue', 'distruction', 'fatal', 'lost', 'damage']



class TwitterClient():
    def __init__(self, twitter_user=None):
        self.auth = TwitterAuthenticator().authenticate_twitter_app()
        self.twitter_client = API(self.auth)

        self.twitter_user = twitter_user

    def get_twitter_client_api(self):
        return self.twitter_client

    def get_user_timeline_tweets(self, num_tweets):
        tweets = []
        for tweet in Cursor(self.twitter_client.user_timeline, id=self.twitter_user).items(num_tweets):
            tweets.append(tweet)
        return tweets

    def get_friend_list(self, num_friends):
        friend_list = []
        for friend in Cursor(self.twitter_client.friends, id=self.twitter_user).items(num_friends):
            friend_list.append(friend)
        return friend_list

    def get_home_timeline_tweets(self, num_tweets):
        home_timeline_tweets = []
        for tweet in Cursor(self.twitter_client.home_timeline, id=self.twitter_user).items(num_tweets):
            home_timeline_tweets.append(tweet)
        return home_timeline_tweets


# # # # TWITTER AUTHENTICATER # # # #
class TwitterAuthenticator:
    def authenticate_twitter_app(self):
        auth = OAuthHandler(twitter_credentials.CONSUMER_KEY, twitter_credentials.CONSUMER_SECRET)
        auth.set_access_token(twitter_credentials.ACCESS_TOKEN, twitter_credentials.ACCESS_TOKEN_SECRET)
        return auth


# # # # TWITTER STREAMER # # # #
class TwitterStreamer:
    """
    Class for streaming and processing live tweets.
    """

    def __init__(self):
        self.twitter_autenticator = TwitterAuthenticator()

    def stream_tweets(self, fetched_tweets_filename, hash_tag_list):
        # This handles Twitter authetification and the connection to Twitter Streaming API
        listener = TwitterListener(fetched_tweets_filename)
        auth = self.twitter_autenticator.authenticate_twitter_app()
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords: 
        stream.filter(track=hash_tag_list)


# # # # TWITTER STREAM LISTENER # # # #
class TwitterListener(StreamListener):
    """
    This is a basic listener that just prints received tweets to stdout.
    """

    def __init__(self, fetched_tweets_filename):
        self.fetched_tweets_filename = fetched_tweets_filename

    def on_data(self, data):
        try:
            print(data)
            with open(self.fetched_tweets_filename, 'a') as tf:
                tf.write(data)
            return True
        except BaseException as e:
            print("Error on_data %s" % str(e))
        return True

    def on_error(self, status):
        if status == 420:
            # Returning False on_data method in case rate limit occurs.
            return False
        print(status)


class TweetAnalyzer:
    """
    Functionality for analyzing and categorizing content from tweets.
    """

    def tweets_to_data_frame(self, tweets):
        df = pd.DataFrame(data=[tweet.text for tweet in tweets], columns=['Tweets'])

        df['id'] = np.array([tweet.id for tweet in tweets])
        df['len'] = np.array([len(tweet.text) for tweet in tweets])
        df['date'] = np.array([tweet.created_at for tweet in tweets])
        df['source'] = np.array([tweet.source for tweet in tweets])
        df['likes'] = np.array([tweet.favorite_count for tweet in tweets])
        df['retweets'] = np.array([tweet.retweet_count for tweet in tweets])
        df['coordinates'] = np.array([tweet.geo for tweet in tweets])
        df['coordinates'] = np.array([tweet.coordinates for tweet in tweets])
        df['text'] = np.array([tweet.text for tweet in tweets])
        return df






def tweet_update():
    paralleldots.set_api_key("CobzARUsfZwPDTX5fxQ6QPkZxe0AwSicZPatZGvHAjY" )
    ans = ['0, 0','0','0']
    try :
        ans = extract_info()
    except Exception as e:
        print(e)
    lat = ans[0].split(',')[0].strip()
    lng = ans[0].split(',')[1].strip()
    num = ans[1].strip()
    info = ans[2]
    return lat,lng,num,info


# loc = str(tweets[0].coordinates['coordinates'][1])+', '+str(tweets[0].coordinates['coordinates'][0])



def get_contact(text, s):
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    num = '0'
    phone = False
    # mail = False
    numbers = re.findall(mobile_no, text)
    print(numbers)
    print("Contact Information")
    for i in numbers:
        i = i.strip(' ')
        if len(i) == 10:
            num = i
            phone = True
            print(num)
            break
    print(phone)
    if not phone:
        sn = s.user.screen_name
        m = "@%s Hello! please provide your mobile number for contact" % (sn)
        s = api.update_status(m, s.id)
    return num


# Filter abusive content from a text corpus
def extract_info():
    twitter_client = TwitterClient()
    tweet_analyzer = TweetAnalyzer()
    api = twitter_client.get_twitter_client_api()
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True)
    tweets = api.user_timeline(count=10, lang='en')
    df = tweet_analyzer.tweets_to_data_frame(tweets)
    for i in range(1):
        text = df['text'][i]  # "need food for 6 people at mesra contact no. 9932356934 email = aniketkumarj@gmail.com"
        temp=''
        print(paralleldots.abuse(text))
        response1 = paralleldots.abuse(text)
        print(response1)

        # Find intent of the user input
        response2 = paralleldots.intent(text)
        print(response2)

        if response1['sentence_type'] == 'Abusive' or response2['probabilities']['spam/junk'] > 0.5:
            flag = False
            ans = ['0, 0', '0', '0']
            return ans

        else:
            flag = True
            # print(flag)

        if flag:
            flag1 = False
            allsyns1 = set(ss for word in flood_related_words for ss in wordnet.synsets(word))
            allsyns2 = set(ss for word in tknzr.tokenize(text) for ss in wordnet.synsets(word))
            best = max((wordnet.wup_similarity(s1,s2) or 0,s1,s2)for s1,s2 in product(allsyns1,allsyns2))
            print(best)
            if best[0] > 0.6:
                flag1 = True
            if flag1:
                response = paralleldots.ner(text)
                print(response)
                for j in range(len(response['entities'])):
                    if (response['entities'][j]['category'] == 'place' and response['entities'][j][
                        'confidence_score'] > 0.6):
                        print(response['entities'][j]['name'])
                        # get_location(response['entities'][i]['name'])

                category = {"need": ['need', 'require', 'want', 'lack'],
                            "offer": ['send', 'have', 'give', 'donate', 'transfer', 'distribute', 'aid', 'help',
                                      'procure']}
                response = paralleldots.custom_classifier(text, category)
                print(response)
                if response['taxonomy'][0]['confidence_score'] > response['taxonomy'][1]['confidence_score']:
                    temp = "need"
                else:
                    temp = "offer"
            num = get_contact(text, tweets[0])
            if temp == "need":
                category = {"food": [], "water": [], "shelter": [], "first-aid": [], "help": []}
                response = paralleldots.custom_classifier(text, category)
                print(response)
                x = 0
                for j in range(5):

                    if response['taxonomy'][i]['confidence_score'] > x:
                        cat = response['taxonomy'][i]['tag']

            else:
                category = {"food": [], "water": [], "shelter": [], "first-aid": []}
                response = paralleldots.custom_classifier(text, category)
                print(response)
                x = 0
                for j in range(4):
                    if response['taxonomy'][i]['confidence_score'] > x:
                        cat = response['taxonomy'][i]['tag']



            quantity = re.findall(quant_no, text)
            qnt = []
            for j in quantity:
                if len(j) < 10:
                    qnt.append(j)

            print(qnt)
            s = tweets[0]
            loc1 =False
            if s.coordinates is None:
                sn = s.user.screen_name
                m = "@%s Hello! please share your location while tweeting" % (sn)
                s = api.update_status(m, s.id)
            else:
                loc1 = True

            ans = []

            if loc1:
                ans.append(
                    str(tweets[0].coordinates['coordinates'][1]) + ', ' + str(tweets[0].coordinates['coordinates'][0]))

            else:
                ans.append('0, 0')

            ans.append(num)
            print(len(qnt))
            if len(qnt) > 0:
                ans.append(qnt[0])
            else:
                ans.append('0')
            print(ans)

            return ans
