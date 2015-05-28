from TwitterAPI import TwitterAPI
import Settings

#Create an empty message container
messages = []

#Retrieve tweets
def get_tweets():

    #Create a TwitterAPI object
    api = TwitterAPI(Settings.consumer_key, Settings.consumer_secret, Settings.access_token_key, Settings.access_token_secret, auth_type='oAuth1',)

    #The retrieved tweets
    tweets = api.request('search/tweets', {'q': 'to:abnamro', 'count': '100', 'since': '2015-05-28'})

    #Create a message object of every tweet
    for tweet in tweets:
        if 'text' in tweet:

            messages.append(tweet['text'])

        else:
            tweet

    #Return the collection of messages
    return messages


#Convert tweet to a message object.
class message:

    #Convert JSON to a message object
    def __init__(self, item):

        self.text = item['text']
        self.storing = storing(self.text)
        self.toeslagen = toeslagen(self.text)


#Test tweet for occurrence of a certain string
def storing(item):
    if "storing" in item:
        return True


def toeslagen(item):
    if "toeslagen" in item:
        return True