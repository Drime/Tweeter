from TwitterAPI import TwitterAPI
import Settings

#Messages container for stroring global tweet-data
class Messages:

    #Sets the attributes.
    def __init__(self):
        self.tweets = []
        self.storingtweets = []
        self.storingen = 0
        self.toeslagentweets = []
        self.toeslagen = 0
        self.total = 0

#Convert tweet to a message object.
class Message:

    #Convert JSON to a message object
    def __init__(self, item):

        self.text = item['text']
        self.storing = storing(self.text)
        self.toeslagen = toeslagen(self.text)


#Test tweet for occurrence of a certain string
def storing(item):
    if "storing" in item:
        return True
    else:
        return False


def toeslagen(item):
    if "toeslagen" in item:
        return True
    else:
        return False

#Create an empty message container
tweet_container = Messages

#Retrieve tweets
def get_tweets():

    #Create a TwitterAPI object
    api = TwitterAPI(Settings.consumer_key, Settings.consumer_secret, Settings.access_token_key, Settings.access_token_secret, auth_type='oAuth1',)

    #Retrieve the last 100 tweets
    tweets = api.request('search/tweets', {'q': 'to:abnamro', 'count': '100', 'since': '2015-05-29'})

    #Create a message object of every tweet
    for tweet in tweets:

        #Validate returned JSON object
        if 'text' in tweet:

            #Create a message container
            tweet_message = Message(tweet)

            #Wrap the tweets into a container.
            if tweet_message.storing:

                tweet_container.storingtweets.append(tweet_message.text)

                tweet_container.storingen += 1
                tweet_container.total += 1

            elif tweet_message.toeslagen:

                tweet_container.toeslagentweets.append(tweet_message.text)

                tweet_container.toeslagen += 1
                tweet_container.total += 1

            else:

                tweet_container.tweets.append(tweet_message.text)
                tweet_container.total += 1

        else:
            tweet

    #Return the message container
    return Messages