from TwitterAPI import TwitterAPI
import Settings

#Messages container for stroring global tweet-data
class Messages:

    #Sets the attributes.
    def __init__(self):
        self.normaltweets = [0]
        self.storingtweets = [0]
        self.storingen = 0
        self.toeslagentweets = [0]
        self.toeslagen = 0
        self.total = 0
        self.lid = ''

#Convert tweet to a message object.
class Message:

    #Convert JSON to a message object
    def __init__(self, item):

        self.text = item['text']
        self.storing = storing(self.text)
        self.toeslagen = toeslagen(self.text)
        self.idn = item["id"]


#Test tweet for occurrence of a certain string
def storing(item):
    if "storing" in item:
        return True
    elif "storing?" in item:
        return True
    else:
        return False


def toeslagen(item):
    if "toeslagen" in item:
        return True
    else:
        return False



#Retrieve tweets
def get_tweets():

    #Create an empty message container
    tweet_container = Messages()

    #Create a TwitterAPI object
    api = TwitterAPI(Settings.consumer_key, Settings.consumer_secret, Settings.access_token_key, Settings.access_token_secret, auth_type='oAuth1',)

    #Retrieve the last 100 tweets
    tweets = api.request('search/tweets', {'q': 'to:abnamro', 'count': '100', 'since': '2015-05-29'})

    tweet_container= tweet_creator(tweets, tweet_container)

    ext_tweets = tweet_container.total
    i = 0

    while ext_tweets == (100) :

        max_id = tweet_container.lid
        tweets = api.request('search/tweets', {'q': 'to:abnamro', 'count': '100', 'since': '2015-05-29', 'max_id': +max_id })

        #add new data to tweet_container
        tweet_container= tweet_creator(tweets, tweet_container)

        #tweet container always adds a blank tweet.
        tweet_container.total -= 1

        #Extract the iterations
        i += 1
        ext_tweets = (tweet_container.total - (100 * i))


    #Return the message container
    return tweet_container

def remove_aab(tweet):

    return tweet.replace('@ABNAMRO', '')

def tweet_creator(tweets, tweet_container):
        #Create a message object of every tweet
    for tweet in tweets:

        #Validate returned JSON object
        if 'text' in tweet:

            #Create a message container
            tweet_message = Message(tweet)

            #Wrap the tweets into a container.
            if tweet_message.storing:

                tweet_container.storingtweets.append(remove_aab(tweet_message.text))

                tweet_container.storingen += 1
                tweet_container.total += 1

            elif tweet_message.toeslagen:

                tweet_container.toeslagentweets.append(remove_aab(tweet_message.text))

                tweet_container.toeslagen += 1
                tweet_container.total += 1

            else:

                tweet_container.normaltweets.append(remove_aab(tweet_message.text))
                tweet_container.total += 1

            tweet_container.lid = tweet_message.idn

        else:
            tweet

    return tweet_container